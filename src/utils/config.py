"""
配置管理模块
负责加载、保存和管理应用程序配置
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认路径
        """
        if config_path is None:
            # 默认配置文件路径
            self.config_path = Path(__file__).parent.parent.parent / "config" / "settings.yaml"
        else:
            self.config_path = Path(config_path)
        
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """加载配置文件"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f) or {}
                print(f"配置文件加载成功: {self.config_path}")
            else:
                print(f"配置文件不存在: {self.config_path}，使用默认配置")
                self.config = self._get_default_config()
        except Exception as e:
            print(f"加载配置文件失败: {e}，使用默认配置")
            self.config = self._get_default_config()
    
    def save_config(self) -> bool:
        """
        保存配置到文件
        
        Returns:
            bool: 保存是否成功
        """
        try:
            # 确保目录存在
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(self.config, f, allow_unicode=True, default_flow_style=False)
            print(f"配置文件保存成功: {self.config_path}")
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key_path: 配置项路径，使用点号分隔，例如 "general.download_path"
            default: 默认值
        
        Returns:
            配置值或默认值
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """
        设置配置项
        
        Args:
            key_path: 配置项路径，使用点号分隔
            value: 配置值
        """
        keys = key_path.split('.')
        config = self.config
        
        # 遍历到倒数第二个键
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # 设置最后一个键的值
        config[keys[-1]] = value
    
    def get_download_path(self) -> str:
        """
        获取下载路径，并展开用户目录
        
        Returns:
            str: 展开后的下载路径
        """
        path = self.get('general.download_path', '~/Downloads')
        return os.path.expanduser(path)
    
    def get_database_path(self) -> str:
        """
        获取数据库路径，并展开用户目录
        
        Returns:
            str: 展开后的数据库路径
        """
        path = self.get('database.path', '~/.pydownloader/downloads.db')
        return os.path.expanduser(path)
    
    def get_log_file_path(self) -> str:
        """
        获取日志文件路径，并展开用户目录
        
        Returns:
            str: 展开后的日志文件路径
        """
        path = self.get('logging.file', '~/.pydownloader/logs/app.log')
        return os.path.expanduser(path)
    
    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """
        获取默认配置
        
        Returns:
            Dict: 默认配置字典
        """
        return {
            'general': {
                'download_path': '~/Downloads',
                'max_concurrent_downloads': 3,
                'default_thread_count': 8,
                'auto_start': True,
                'completion_action': 'none'
            },
            'network': {
                'timeout': 30,
                'retry_count': 3,
                'proxy': {
                    'enabled': False,
                    'http': '',
                    'https': ''
                },
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            'speed': {
                'global_limit': 0,
                'per_task_limit': 0
            },
            'ui': {
                'theme': 'light',
                'window': {
                    'width': 1000,
                    'height': 600
                },
                'show_tray_icon': True,
                'minimize_to_tray': False
            },
            'notifications': {
                'download_complete': True,
                'download_failed': True,
                'system_notification': True
            },
            'database': {
                'path': '~/.pydownloader/downloads.db',
                'auto_cleanup_days': 0
            },
            'logging': {
                'level': 'INFO',
                'file': '~/.pydownloader/logs/app.log',
                'max_size': 10,
                'backup_count': 5
            }
        }


# 全局配置实例
_config_instance: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """
    获取全局配置实例（单例模式）
    
    Returns:
        ConfigManager: 配置管理器实例
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance
