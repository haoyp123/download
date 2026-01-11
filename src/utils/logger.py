"""
日志模块
提供统一的日志记录功能
"""

import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


class Logger:
    """日志管理器"""
    
    def __init__(self, name: str = "PyDownloader", log_file: Optional[str] = None,
                 level: str = "INFO", max_bytes: int = 10485760, backup_count: int = 5):
        """
        初始化日志管理器
        
        Args:
            name: 日志记录器名称
            log_file: 日志文件路径
            level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            max_bytes: 日志文件最大大小（字节）
            backup_count: 保留的日志文件数量
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self._get_log_level(level))
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self._get_log_level(level))
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
            # 文件处理器
            if log_file:
                try:
                    # 确保日志目录存在
                    log_path = Path(log_file)
                    log_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    file_handler = RotatingFileHandler(
                        log_file,
                        maxBytes=max_bytes,
                        backupCount=backup_count,
                        encoding='utf-8'
                    )
                    file_handler.setLevel(self._get_log_level(level))
                    file_formatter = logging.Formatter(
                        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                    )
                    file_handler.setFormatter(file_formatter)
                    self.logger.addHandler(file_handler)
                except Exception as e:
                    self.logger.warning(f"无法创建日志文件处理器: {e}")
    
    @staticmethod
    def _get_log_level(level: str) -> int:
        """
        将字符串日志级别转换为logging常量
        
        Args:
            level: 日志级别字符串
        
        Returns:
            int: logging级别常量
        """
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return level_map.get(level.upper(), logging.INFO)
    
    def debug(self, message: str) -> None:
        """记录DEBUG级别日志"""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """记录INFO级别日志"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """记录WARNING级别日志"""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False) -> None:
        """
        记录ERROR级别日志
        
        Args:
            message: 日志消息
            exc_info: 是否包含异常信息
        """
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False) -> None:
        """
        记录CRITICAL级别日志
        
        Args:
            message: 日志消息
            exc_info: 是否包含异常信息
        """
        self.logger.critical(message, exc_info=exc_info)
    
    def exception(self, message: str) -> None:
        """记录异常信息（自动包含堆栈跟踪）"""
        self.logger.exception(message)


# 全局日志实例
_logger_instance: Optional[Logger] = None


def get_logger(name: str = "PyDownloader") -> Logger:
    """
    获取全局日志实例（单例模式）
    
    Args:
        name: 日志记录器名称
    
    Returns:
        Logger: 日志管理器实例
    """
    global _logger_instance
    if _logger_instance is None:
        # 尝试从配置文件读取日志设置
        try:
            from .config import get_config
            config = get_config()
            log_file = config.get_log_file_path()
            level = config.get('logging.level', 'INFO')
            max_size = config.get('logging.max_size', 10) * 1024 * 1024  # MB转字节
            backup_count = config.get('logging.backup_count', 5)
            
            _logger_instance = Logger(
                name=name,
                log_file=log_file,
                level=level,
                max_bytes=max_size,
                backup_count=backup_count
            )
        except Exception as e:
            # 如果配置加载失败，使用默认设置
            print(f"加载日志配置失败: {e}，使用默认设置")
            _logger_instance = Logger(name=name)
    
    return _logger_instance


def setup_logger(log_file: Optional[str] = None, level: str = "INFO",
                max_bytes: int = 10485760, backup_count: int = 5) -> Logger:
    """
    手动设置日志配置
    
    Args:
        log_file: 日志文件路径
        level: 日志级别
        max_bytes: 日志文件最大大小（字节）
        backup_count: 保留的日志文件数量
    
    Returns:
        Logger: 配置后的日志实例
    """
    global _logger_instance
    _logger_instance = Logger(
        name="PyDownloader",
        log_file=log_file,
        level=level,
        max_bytes=max_bytes,
        backup_count=backup_count
    )
    return _logger_instance
