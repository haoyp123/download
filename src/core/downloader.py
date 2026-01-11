"""
下载器核心模块
实现多线程分块下载
"""
import os
import threading
import time
from typing import Optional, Callable
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..utils.config import ConfigManager
from ..utils.logger import Logger
from ..utils.helpers import calculate_chunks
from .download_task import DownloadTask


class Downloader:
    """下载器类"""
    
    def __init__(self, task: DownloadTask, progress_callback: Optional[Callable] = None):
        """
        初始化下载器
        
        Args:
            task: 下载任务
            progress_callback: 进度回调函数
        """
        self.task = task
        self.progress_callback = progress_callback
        self.config = ConfigManager()
        self.logger = Logger()
        
        self._stop_flag = threading.Event()
        self._pause_flag = threading.Event()
        self._lock = threading.Lock()
        
        # 下载统计
        self._downloaded_chunks = {}  # 记录每个分块已下载的字节数
        self._last_update_time = time.time()
        self._last_downloaded_size = 0
    
    def start(self):
        """开始下载"""
        try:
            self.logger.info(f"开始下载: {self.task.url}")
            self.task.mark_as_downloading()
            
            # 获取文件信息
            if not self._get_file_info():
                return
            
            # 检查是否支持分块下载
            if self.task.total_size > 0:
                self._download_with_chunks()
            else:
                self._download_single()
            
            # 检查是否完成
            if not self._stop_flag.is_set() and not self._pause_flag.is_set():
                if self._verify_download():
                    self.task.mark_as_completed()
                    self.logger.info(f"下载完成: {self.task.filename}")
                    self._notify_progress()
                else:
                    self.task.mark_as_failed("文件验证失败")
                    self.logger.error(f"文件验证失败: {self.task.filename}")
        
        except Exception as e:
            self.task.mark_as_failed(str(e))
            self.logger.error(f"下载失败: {e}")
    
    def pause(self):
        """暂停下载"""
        self._pause_flag.set()
        self.task.mark_as_paused()
        self.logger.info(f"暂停下载: {self.task.filename}")
    
    def stop(self):
        """停止下载"""
        self._stop_flag.set()
        self._pause_flag.set()
        self.logger.info(f"停止下载: {self.task.filename}")
    
    def _get_file_info(self) -> bool:
        """获取文件信息"""
        try:
            timeout = self.config.get('network.timeout', 30)
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            response = requests.head(self.task.url, headers=headers, timeout=timeout, allow_redirects=True)
            
            # 获取文件大小
            content_length = response.headers.get('Content-Length')
            if content_length:
                self.task.total_size = int(content_length)
            
            # 检查是否支持Range请求
            accept_ranges = response.headers.get('Accept-Ranges', 'none')
            if accept_ranges == 'bytes' and self.task.total_size > 0:
                # 支持分块下载
                connections = self.config.get('network.connections_per_file', 8)
                self.task.connections = connections
                self.task.chunks = calculate_chunks(self.task.total_size, connections)
            else:
                # 不支持分块下载
                self.task.connections = 1
                self.task.chunks = [{'start': 0, 'end': self.task.total_size - 1, 'downloaded': 0}]
            
            self.logger.info(f"文件大小: {self.task.total_size} 字节, 分块数: {self.task.connections}")
            return True
        
        except Exception as e:
            self.task.mark_as_failed(f"获取文件信息失败: {e}")
            self.logger.error(f"获取文件信息失败: {e}")
            return False
    
    def _download_with_chunks(self):
        """分块下载"""
        # 创建临时文件
        final_file_path = os.path.join(self.task.save_path, self.task.filename)
        temp_file = final_file_path + '.tmp'
        
        # 如果是恢复下载，读取已下载的进度
        if os.path.exists(temp_file):
            self._load_progress(temp_file)
        else:
            # 创建空文件
            with open(temp_file, 'wb') as f:
                f.seek(self.task.total_size - 1)
                f.write(b'\0')
        
        # 使用线程池下载各个分块
        with ThreadPoolExecutor(max_workers=self.task.connections) as executor:
            futures = []
            
            for i, chunk in enumerate(self.task.chunks):
                if chunk.get('downloaded', 0) >= (chunk['end'] - chunk['start'] + 1):
                    # 该分块已下载完成
                    continue
                
                future = executor.submit(self._download_chunk, i, chunk, temp_file)
                futures.append(future)
            
            # 等待所有分块下载完成
            for future in as_completed(futures):
                if self._stop_flag.is_set() or self._pause_flag.is_set():
                    # 取消所有未完成的任务
                    for f in futures:
                        f.cancel()
                    break
                
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"分块下载失败: {e}")
        
        # 如果下载完成，重命名临时文件
        if not self._stop_flag.is_set() and not self._pause_flag.is_set():
            if os.path.exists(temp_file):
                if os.path.exists(final_file_path):
                    os.remove(final_file_path)
                os.rename(temp_file, final_file_path)
    
    def _download_chunk(self, chunk_index: int, chunk: dict, temp_file: str):
        """下载单个分块"""
        start = chunk['start'] + chunk.get('downloaded', 0)
        end = chunk['end']
        
        if start > end:
            return
        
        try:
            timeout = self.config.get('network.timeout', 30)
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Range': f'bytes={start}-{end}'
            }
            
            response = requests.get(
                self.task.url,
                headers=headers,
                timeout=timeout,
                stream=True
            )
            response.raise_for_status()
            
            # 写入文件
            with open(temp_file, 'r+b') as f:
                f.seek(start)
                
                for data in response.iter_content(chunk_size=8192):
                    if self._stop_flag.is_set() or self._pause_flag.is_set():
                        break
                    
                    if data:
                        f.write(data)
                        chunk_size = len(data)
                        
                        # 更新进度
                        with self._lock:
                            chunk['downloaded'] = chunk.get('downloaded', 0) + chunk_size
                            self._downloaded_chunks[chunk_index] = chunk['downloaded']
                            self._update_progress()
        
        except Exception as e:
            self.logger.error(f"分块 {chunk_index} 下载失败: {e}")
            raise
    
    def _download_single(self):
        """单线程下载（不支持分块）"""
        try:
            timeout = self.config.get('network.timeout', 30)
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            response = requests.get(
                self.task.url,
                headers=headers,
                timeout=timeout,
                stream=True
            )
            response.raise_for_status()
            
            # 写入文件
            final_file_path = os.path.join(self.task.save_path, self.task.filename)
            with open(final_file_path, 'wb') as f:
                for data in response.iter_content(chunk_size=8192):
                    if self._stop_flag.is_set() or self._pause_flag.is_set():
                        break
                    
                    if data:
                        f.write(data)
                        chunk_size = len(data)
                        
                        # 更新进度
                        with self._lock:
                            self.task.downloaded_size += chunk_size
                            self._update_progress()
        
        except Exception as e:
            self.logger.error(f"下载失败: {e}")
            raise
    
    def _update_progress(self):
        """更新下载进度"""
        current_time = time.time()
        time_diff = current_time - self._last_update_time
        
        # 每秒更新一次
        if time_diff >= 1.0:
            # 计算总已下载大小
            total_downloaded = sum(self._downloaded_chunks.values())
            
            # 计算速度
            size_diff = total_downloaded - self._last_downloaded_size
            speed = size_diff / time_diff if time_diff > 0 else 0
            
            # 更新任务
            self.task.update_progress(total_downloaded, speed)
            
            # 通知回调
            self._notify_progress()
            
            # 更新统计信息
            self._last_update_time = current_time
            self._last_downloaded_size = total_downloaded
    
    def _notify_progress(self):
        """通知进度更新"""
        if self.progress_callback:
            try:
                self.progress_callback(self.task)
            except Exception as e:
                self.logger.error(f"进度回调失败: {e}")
    
    def _load_progress(self, temp_file: str):
        """加载下载进度"""
        try:
            file_size = os.path.getsize(temp_file)
            
            # 简单实现：假设从头开始
            # 实际应该保存分块的下载进度
            self.task.downloaded_size = 0
            
            for chunk in self.task.chunks:
                chunk['downloaded'] = 0
        
        except Exception as e:
            self.logger.error(f"加载进度失败: {e}")
    
    def _verify_download(self) -> bool:
        """验证下载是否完成"""
        try:
            final_file_path = os.path.join(self.task.save_path, self.task.filename)
            if not os.path.exists(final_file_path):
                return False
            
            file_size = os.path.getsize(final_file_path)
            
            # 如果知道文件大小，检查是否匹配
            if self.task.total_size > 0:
                return file_size == self.task.total_size
            
            # 如果不知道文件大小，只要文件存在就认为成功
            return file_size > 0
        
        except Exception as e:
            self.logger.error(f"验证下载失败: {e}")
            return False
