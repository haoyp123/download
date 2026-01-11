"""
下载管理器模块

负责管理所有下载任务的生命周期，包括添加、删除、启动、暂停等操作。
通过Qt信号机制与UI层通信，实现任务状态的实时更新。
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path
from PySide6.QtCore import QObject, Signal, QTimer

from src.core.download_task import DownloadTask
from src.core.downloader import Downloader
from src.utils.config import ConfigManager
from src.utils.logger import Logger


class DownloadManager(QObject):
    """下载管理器类
    
    管理所有下载任务，提供统一的任务管理接口。
    使用Qt信号与UI层通信，实现松耦合设计。
    """
    
    # 信号定义
    task_added = Signal(DownloadTask)  # 任务添加信号
    task_removed = Signal(str)  # 任务删除信号(task_id)
    task_updated = Signal(DownloadTask)  # 任务更新信号
    task_completed = Signal(str)  # 任务完成信号(task_id)
    task_failed = Signal(str, str)  # 任务失败信号(task_id, error_message)
    all_tasks_completed = Signal()  # 所有任务完成信号
    
    def __init__(self, parent=None):
        """初始化下载管理器
        
        Args:
            parent: 父对象
        """
        super().__init__(parent)
        
        self.logger = Logger()
        self.config = ConfigManager()
        
        # 任务存储
        self.tasks: Dict[str, DownloadTask] = {}  # task_id -> DownloadTask
        self.downloaders: Dict[str, Downloader] = {}  # task_id -> Downloader
        
        # 队列管理
        self.max_concurrent = self.config.get('download.max_concurrent', 3)
        self.active_count = 0
        
        # 数据持久化路径
        self.data_dir = Path.home() / '.ndm_clone' / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.tasks_file = self.data_dir / 'tasks.json'
        
        # 定时保存任务状态
        self.save_timer = QTimer(self)
        self.save_timer.timeout.connect(self._save_tasks)
        self.save_timer.start(30000)  # 每30秒保存一次
        
        # 加载已保存的任务
        self._load_tasks()
        
        self.logger.info("下载管理器初始化完成")
    
    def add_task(self, url: str, save_path: str, filename: str,
                 connections: int = None) -> Optional[DownloadTask]:
        """添加下载任务
        
        Args:
            url: 下载URL
            save_path: 保存路径
            filename: 文件名
            connections: 连接数（为None时使用配置值）
        
        Returns:
            创建的下载任务，失败则返回None
        """
        try:
            # 创建任务
            if connections is None:
                connections = self.config.get('download.connections', 8)
            
            task = DownloadTask(
                url=url,
                save_path=save_path,
                filename=filename,
                connections=connections
            )
            
            # 检查文件是否已存在
            file_path = os.path.join(save_path, filename)
            if os.path.exists(file_path):
                self.logger.warning(f"文件已存在: {file_path}")
                return None
            
            # 添加到任务列表
            self.tasks[task.task_id] = task
            
            # 发送信号
            self.task_added.emit(task)
            
            self.logger.info(f"添加下载任务: {filename}")
            
            # 如果有空闲槽位，自动开始下载
            if self.active_count < self.max_concurrent:
                self.start_task(task.task_id)
            
            return task
            
        except Exception as e:
            self.logger.error(f"添加任务失败: {str(e)}")
            return None
    
    def remove_task(self, task_id: str) -> bool:
        """删除下载任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            是否成功删除
        """
        try:
            if task_id not in self.tasks:
                return False
            
            # 如果任务正在下载，先停止
            if task_id in self.downloaders:
                self.stop_task(task_id)
            
            # 删除任务
            task = self.tasks.pop(task_id)
            
            # 删除临时文件
            temp_file = os.path.join(task.save_path, f"{task.filename}.tmp")
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception as e:
                    self.logger.warning(f"删除临时文件失败: {str(e)}")
            
            # 发送信号
            self.task_removed.emit(task_id)
            
            self.logger.info(f"删除任务: {task.filename}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"删除任务失败: {str(e)}")
            return False
    
    def start_task(self, task_id: str) -> bool:
        """开始下载任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            是否成功开始
        """
        try:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            
            # 检查任务状态
            if task.status == "downloading":
                return True
            
            if task.status == "completed":
                self.logger.warning("任务已完成，无需重新下载")
                return False
            
            # 检查并发限制
            if self.active_count >= self.max_concurrent:
                self.logger.warning("达到最大并发数，任务将排队等待")
                task.status = "waiting"
                self.task_updated.emit(task)
                return False
            
            # 创建下载器，传入回调函数
            def progress_callback(updated_task):
                """进度更新回调"""
                # 更新任务对象
                self.tasks[task_id] = updated_task
                
                # 根据任务状态发送相应信号
                if updated_task.status == "completed":
                    self._on_download_completed(task_id)
                elif updated_task.status == "failed":
                    self._on_download_failed(task_id, updated_task.error or "未知错误")
                else:
                    self._on_progress_updated(task_id)
            
            downloader = Downloader(task, progress_callback=progress_callback)
            
            # 保存下载器引用
            self.downloaders[task_id] = downloader
            
            # 更新状态
            task.status = "downloading"
            self.active_count += 1
            
            # 在单独的线程中开始下载
            import threading
            download_thread = threading.Thread(target=downloader.start, daemon=True)
            download_thread.start()
            
            # 发送信号
            self.task_updated.emit(task)
            
            self.logger.info(f"开始下载: {task.filename}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"开始任务失败: {str(e)}")
            return False
    
    def pause_task(self, task_id: str) -> bool:
        """暂停下载任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            是否成功暂停
        """
        try:
            if task_id not in self.tasks or task_id not in self.downloaders:
                return False
            
            task = self.tasks[task_id]
            downloader = self.downloaders[task_id]
            
            # 暂停下载
            downloader.pause()
            
            # 更新状态
            task.status = "paused"
            self.active_count -= 1
            
            # 发送信号
            self.task_updated.emit(task)
            
            self.logger.info(f"暂停下载: {task.filename}")
            
            # 检查是否有等待的任务可以开始
            self._start_next_waiting_task()
            
            return True
            
        except Exception as e:
            self.logger.error(f"暂停任务失败: {str(e)}")
            return False
    
    def resume_task(self, task_id: str) -> bool:
        """恢复下载任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            是否成功恢复
        """
        try:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            
            if task.status != "paused":
                return False
            
            # 重新开始任务
            return self.start_task(task_id)
            
        except Exception as e:
            self.logger.error(f"恢复任务失败: {str(e)}")
            return False
    
    def stop_task(self, task_id: str) -> bool:
        """停止下载任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            是否成功停止
        """
        try:
            if task_id not in self.downloaders:
                return False
            
            downloader = self.downloaders[task_id]
            task = self.tasks[task_id]
            
            # 停止下载
            downloader.stop()
            
            # 清理下载器
            self.downloaders.pop(task_id)
            
            # 更新状态
            if task.status == "downloading":
                self.active_count -= 1
                task.status = "stopped"
            
            # 发送信号
            self.task_updated.emit(task)
            
            self.logger.info(f"停止下载: {task.filename}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"停止任务失败: {str(e)}")
            return False
    
    def get_task(self, task_id: str) -> Optional[DownloadTask]:
        """获取任务信息
        
        Args:
            task_id: 任务ID
        
        Returns:
            任务对象，不存在则返回None
        """
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[DownloadTask]:
        """获取所有任务
        
        Returns:
            任务列表
        """
        return list(self.tasks.values())
    
    def clear_completed_tasks(self) -> int:
        """清除已完成的任务
        
        Returns:
            清除的任务数量
        """
        completed_ids = [
            task_id for task_id, task in self.tasks.items()
            if task.status == "completed"
        ]
        
        for task_id in completed_ids:
            self.remove_task(task_id)
        
        self.logger.info(f"清除了 {len(completed_ids)} 个已完成任务")
        
        return len(completed_ids)
    
    def _on_progress_updated(self, task_id: str):
        """处理进度更新
        
        Args:
            task_id: 任务ID
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            self.task_updated.emit(task)
    
    def _on_download_completed(self, task_id: str):
        """处理下载完成
        
        Args:
            task_id: 任务ID
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = "completed"
            task.progress = 100.0
            
            # 清理下载器
            if task_id in self.downloaders:
                self.downloaders.pop(task_id)
                self.active_count -= 1
            
            # 发送信号
            self.task_updated.emit(task)
            self.task_completed.emit(task_id)
            
            self.logger.info(f"下载完成: {task.filename}")
            
            # 检查是否所有任务都完成
            if all(task.status == "completed" for task in self.tasks.values()):
                self.all_tasks_completed.emit()
            
            # 启动下一个等待的任务
            self._start_next_waiting_task()
    
    def _on_download_failed(self, task_id: str, error: str):
        """处理下载失败
        
        Args:
            task_id: 任务ID
            error: 错误信息
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = "failed"
            task.error = error
            
            # 清理下载器
            if task_id in self.downloaders:
                self.downloaders.pop(task_id)
                self.active_count -= 1
            
            # 发送信号
            self.task_updated.emit(task)
            self.task_failed.emit(task_id, error)
            
            self.logger.error(f"下载失败: {task.filename}, 错误: {error}")
            
            # 启动下一个等待的任务
            self._start_next_waiting_task()
    
    def _start_next_waiting_task(self):
        """启动下一个等待的任务"""
        if self.active_count >= self.max_concurrent:
            return
        
        # 查找等待中的任务
        for task_id, task in self.tasks.items():
            if task.status == "waiting":
                self.start_task(task_id)
                break
    
    def _save_tasks(self):
        """保存任务到文件"""
        try:
            tasks_data = []
            for task in self.tasks.values():
                tasks_data.append(task.to_dict())
            
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)
            
            self.logger.debug(f"保存了 {len(tasks_data)} 个任务")
            
        except Exception as e:
            self.logger.error(f"保存任务失败: {str(e)}")
    
    def _load_tasks(self):
        """从文件加载任务"""
        try:
            if not self.tasks_file.exists():
                return
            
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            for task_data in tasks_data:
                task = DownloadTask.from_dict(task_data)
                
                # 只加载未完成的任务
                if task.status not in ["completed"]:
                    # 重置状态为暂停
                    if task.status == "downloading":
                        task.status = "paused"
                    
                    self.tasks[task.task_id] = task
                    self.task_added.emit(task)
            
            self.logger.info(f"加载了 {len(self.tasks)} 个任务")
            
        except Exception as e:
            self.logger.error(f"加载任务失败: {str(e)}")
    
    def shutdown(self):
        """关闭下载管理器"""
        try:
            # 停止所有下载
            for task_id in list(self.downloaders.keys()):
                self.stop_task(task_id)
            
            # 保存任务状态
            self._save_tasks()
            
            # 停止定时器
            self.save_timer.stop()
            
            self.logger.info("下载管理器已关闭")
            
        except Exception as e:
            self.logger.error(f"关闭下载管理器失败: {str(e)}")
