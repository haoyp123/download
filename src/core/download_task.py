"""
下载任务模型
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import uuid


@dataclass
class DownloadTask:
    """下载任务类"""
    
    # 基本信息
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    url: str = ""
    filename: str = ""
    save_path: str = ""
    
    # 文件信息
    total_size: int = 0  # 总大小（字节）
    downloaded_size: int = 0  # 已下载大小（字节）
    
    # 状态信息
    status: str = "waiting"  # waiting, downloading, paused, completed, failed
    progress: float = 0.0  # 进度百分比（0-100）
    speed: float = 0.0  # 下载速度（字节/秒）
    
    # 时间信息
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # 其他信息
    error_message: str = ""
    retry_count: int = 0
    connections: int = 8  # 分块数量
    
    # 分块信息
    chunks: List[dict] = field(default_factory=list)
    
    def __post_init__(self):
        """初始化后处理"""
        if not self.filename and self.url:
            from ..utils.helpers import get_filename_from_url
            self.filename = get_filename_from_url(self.url)
    
    @property
    def remaining_size(self) -> int:
        """剩余大小"""
        return max(0, self.total_size - self.downloaded_size)
    
    @property
    def eta(self) -> float:
        """预计剩余时间（秒）"""
        if self.speed > 0:
            return self.remaining_size / self.speed
        return 0
    
    @property
    def is_completed(self) -> bool:
        """是否完成"""
        return self.status == "completed"
    
    @property
    def is_downloading(self) -> bool:
        """是否正在下载"""
        return self.status == "downloading"
    
    @property
    def is_paused(self) -> bool:
        """是否暂停"""
        return self.status == "paused"
    
    @property
    def is_failed(self) -> bool:
        """是否失败"""
        return self.status == "failed"
    
    @property
    def can_start(self) -> bool:
        """是否可以开始"""
        return self.status in ["waiting", "paused", "failed"]
    
    @property
    def can_pause(self) -> bool:
        """是否可以暂停"""
        return self.status == "downloading"
    
    @property
    def can_resume(self) -> bool:
        """是否可以恢复"""
        return self.status == "paused"
    
    @property
    def can_retry(self) -> bool:
        """是否可以重试"""
        return self.status == "failed"
    
    def update_progress(self, downloaded_size: int, speed: float):
        """更新进度"""
        self.downloaded_size = downloaded_size
        self.speed = speed
        
        if self.total_size > 0:
            self.progress = (self.downloaded_size / self.total_size) * 100
        else:
            self.progress = 0
    
    def mark_as_downloading(self):
        """标记为正在下载"""
        self.status = "downloading"
        if not self.started_at:
            self.started_at = datetime.now()
    
    def mark_as_paused(self):
        """标记为暂停"""
        self.status = "paused"
    
    def mark_as_completed(self):
        """标记为完成"""
        self.status = "completed"
        self.progress = 100.0
        self.downloaded_size = self.total_size
        self.completed_at = datetime.now()
    
    def mark_as_failed(self, error_message: str):
        """标记为失败"""
        self.status = "failed"
        self.error_message = error_message
    
    def increment_retry(self):
        """增加重试次数"""
        self.retry_count += 1
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'task_id': self.task_id,
            'url': self.url,
            'filename': self.filename,
            'save_path': self.save_path,
            'total_size': self.total_size,
            'downloaded_size': self.downloaded_size,
            'status': self.status,
            'progress': self.progress,
            'speed': self.speed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'connections': self.connections,
            'chunks': self.chunks
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DownloadTask':
        """从字典创建"""
        # 转换时间字符串
        if data.get('created_at'):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if data.get('started_at'):
            data['started_at'] = datetime.fromisoformat(data['started_at'])
        if data.get('completed_at'):
            data['completed_at'] = datetime.fromisoformat(data['completed_at'])
        
        return cls(**data)
