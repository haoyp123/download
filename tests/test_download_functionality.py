#!/usr/bin/env python3
"""
下载功能集成测试脚本
测试多线程下载、断点续传、暂停/恢复等功能
"""

import sys
import os
import time
import tempfile
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtCore import QCoreApplication, QTimer
from src.core.download_manager import DownloadManager
from src.utils.logger import get_logger

logger = get_logger()


class SingleTestRunner:
    """单个测试运行器"""
    
    def __init__(self, test_name, test_dir, app):
        self.test_name = test_name
        self.test_dir = test_dir
        self.app = app
        self.manager = DownloadManager()
        self.current_task_id = None
        self.result = None
    
    def run_single_thread_test(self):
        """测试1：单线程下载"""
        print("\n" + "="*60)
        print("测试1：单线程下载小文件")
        print("="*60)
        
        url = "https://www.python.org/static/img/python-logo.png"
        filename = "python-logo.png"
        
        def on_task_updated(updated_task):
            if updated_task.task_id == self.current_task_id:
                percent = updated_task.progress
                speed = updated_task.speed / 1024
                print(f"进度: {percent:.1f}% - 速度: {speed:.2f} KB/s")
        
        def on_task_completed(task_id):
            if task_id == self.current_task_id:
                print("✅ 下载完成！")
                file_path = os.path.join(self.test_dir, filename)
                file_exists = os.path.exists(file_path)
                file_size = os.path.getsize(file_path) if file_exists else 0
                self.result = {
                    'test': '单线程下载',
                    'success': file_exists and file_size > 0,
                    'details': f"文件大小: {file_size} bytes"
                }
                self.app.quit()
        
        def on_task_failed(task_id, error_msg):
            if task_id == self.current_task_id:
                print(f"❌ 下载失败: {error_msg}")
                self.result = {
                    'test': '单线程下载',
                    'success': False,
                    'details': error_msg
                }
                self.app.quit()
        
        self.manager.task_updated.connect(on_task_updated)
        self.manager.task_completed.connect(on_task_completed)
        self.manager.task_failed.connect(on_task_failed)
        
        task = self.manager.add_task(url, self.test_dir, filename, connections=1)
        if task:
            self.current_task_id = task.task_id
        else:
            self.result = {
                'test': '单线程下载',
                'success': False,
                'details': '添加任务失败'
            }
            return self.result
        
        QTimer.singleShot(60000, lambda: self._timeout("单线程下载"))
        self.app.exec()
        return self.result
    
    def run_multi_thread_test(self):
        """测试2：多线程下载"""
        print("\n" + "="*60)
        print("测试2：多线程下载（4线程）")
        print("="*60)
        
        url = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip"
        filename = "python-embed.zip"
        start_time = time.time()
        
        def on_task_updated(updated_task):
            if updated_task.task_id == self.current_task_id:
                percent = updated_task.progress
                speed = updated_task.speed / 1024
                print(f"进度: {percent:.1f}% - 速度: {speed:.2f} KB/s")
        
        def on_task_completed(task_id):
            if task_id == self.current_task_id:
                elapsed = time.time() - start_time
                print(f"✅ 下载完成！用时: {elapsed:.2f}秒")
                file_path = os.path.join(self.test_dir, filename)
                file_exists = os.path.exists(file_path)
                file_size = os.path.getsize(file_path) if file_exists else 0
                self.result = {
                    'test': '多线程下载',
                    'success': file_exists and file_size > 1000000,
                    'details': f"文件大小: {file_size} bytes, 用时: {elapsed:.2f}秒"
                }
                self.app.quit()
        
        def on_task_failed(task_id, error_msg):
            if task_id == self.current_task_id:
                print(f"❌ 下载失败: {error_msg}")
                self.result = {
                    'test': '多线程下载',
                    'success': False,
                    'details': error_msg
                }
                self.app.quit()
        
        self.manager.task_updated.connect(on_task_updated)
        self.manager.task_completed.connect(on_task_completed)
        self.manager.task_failed.connect(on_task_failed)
        
        task = self.manager.add_task(url, self.test_dir, filename, connections=4)
        if task:
            self.current_task_id = task.task_id
        else:
            self.result = {
                'test': '多线程下载',
                'success': False,
                'details': '添加任务失败'
            }
            return self.result
        
        QTimer.singleShot(180000, lambda: self._timeout("多线程下载"))
        self.app.exec()
        return self.result
    
    def run_pause_resume_test(self):
        """测试3：暂停和恢复功能"""
        print("\n" + "="*60)
        print("测试3：暂停和恢复功能")
        print("="*60)
        
        url = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip"
        filename = "python-embed-pause-test.zip"
        
        pause_triggered = False
        resume_triggered = False
        
        def on_task_updated(updated_task):
            nonlocal pause_triggered, resume_triggered
            
            if updated_task.task_id == self.current_task_id:
                percent = updated_task.progress
                speed = updated_task.speed / 1024
                
                # 下载到10%时暂停（降低阈值以便更容易触发）
                if not pause_triggered and percent > 10 and percent < 95:
                    print(f"\n⏸️  暂停下载 (进度: {percent:.1f}%)")
                    self.manager.pause_task(self.current_task_id)
                    pause_triggered = True
                    
                    # 2秒后恢复
                    QTimer.singleShot(2000, lambda: resume_download())
                
                if not pause_triggered or resume_triggered:
                    print(f"进度: {percent:.1f}% - 速度: {speed:.2f} KB/s")
        
        def resume_download():
            nonlocal resume_triggered
            print("▶️  恢复下载")
            self.manager.resume_task(self.current_task_id)
            resume_triggered = True
        
        def on_task_completed(task_id):
            if task_id == self.current_task_id:
                print("✅ 下载完成！")
                success = pause_triggered and resume_triggered
                self.result = {
                    'test': '暂停/恢复功能',
                    'success': success,
                    'details': f"暂停: {pause_triggered}, 恢复: {resume_triggered}"
                }
                self.app.quit()
        
        def on_task_failed(task_id, error_msg):
            if task_id == self.current_task_id:
                print(f"❌ 下载失败: {error_msg}")
                self.result = {
                    'test': '暂停/恢复功能',
                    'success': False,
                    'details': error_msg
                }
                self.app.quit()
        
        self.manager.task_updated.connect(on_task_updated)
        self.manager.task_completed.connect(on_task_completed)
        self.manager.task_failed.connect(on_task_failed)
        
        # 使用单线程以降低下载速度，更容易测试暂停功能
        task = self.manager.add_task(url, self.test_dir, filename, connections=1)
        if task:
            self.current_task_id = task.task_id
        else:
            self.result = {
                'test': '暂停/恢复功能',
                'success': False,
                'details': '添加任务失败'
            }
            return self.result
        
        QTimer.singleShot(180000, lambda: self._timeout("暂停/恢复功能"))
        self.app.exec()
        return self.result
    
    def _timeout(self, test_name):
        """测试超时处理"""
        print(f"\n⏱️  测试超时: {test_name}")
        self.result = {
            'test': test_name,
            'success': False,
            'details': '测试超时'
        }
        self.app.quit()


def run_test_in_subprocess(test_func, test_name, test_dir):
    """在独立进程中运行单个测试"""
    runner = SingleTestRunner(test_name, test_dir)
    return test_func(runner)


def main():
    """主测试函数"""
    print("PyDownloader 下载功能集成测试")
    print("="*60)
    
    test_dir = tempfile.mkdtemp(prefix="pydownloader_test_")
    logger.info(f"测试目录: {test_dir}")
    
    # 创建共享的QCoreApplication实例
    app = QCoreApplication(sys.argv)
    
    results = []
    
    try:
        print("\n开始测试...")
        
        # 测试1：单线程下载
        runner1 = SingleTestRunner("单线程下载", test_dir, app)
        result1 = runner1.run_single_thread_test()
        results.append(result1)
        
        # 测试2：多线程下载
        runner2 = SingleTestRunner("多线程下载", test_dir, app)
        result2 = runner2.run_multi_thread_test()
        results.append(result2)
        
        # 测试3：暂停/恢复
        runner3 = SingleTestRunner("暂停/恢复", test_dir, app)
        result3 = runner3.run_pause_resume_test()
        results.append(result3)
        
        # 打印结果
        print("\n" + "="*60)
        print("测试结果汇总")
        print("="*60)
        
        passed = sum(1 for r in results if r and r['success'])
        total = len(results)
        
        for result in results:
            if result:
                status = "✅ 通过" if result['success'] else "❌ 失败"
                print(f"{result['test']}: {status}")
                print(f"  详情: {result['details']}")
        
        print(f"\n总计: {passed}/{total} 测试通过")
        print("="*60)
        
        return 0 if passed == total else 1
        
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        return 1
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}", exc_info=True)
        return 1
    finally:
        # 清理测试文件
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            logger.info(f"已清理测试目录: {test_dir}")


if __name__ == "__main__":
    sys.exit(main())
