"""
下载项UI组件

显示单个下载任务的UI组件，包括文件信息、进度条、控制按钮等。
通过信号与主窗口和下载管理器通信。
"""

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
    QPushButton, QProgressBar, QFrame
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

from src.core.download_task import DownloadTask
from src.utils.helpers import format_size, format_speed, format_time


class DownloadItem(QWidget):
    """下载项组件类
    
    显示单个下载任务的详细信息和控制按钮。
    支持开始、暂停、恢复、删除等操作。
    """
    
    # 信号定义
    start_requested = Signal(str)  # 开始下载请求(task_id)
    pause_requested = Signal(str)  # 暂停下载请求(task_id)
    resume_requested = Signal(str)  # 恢复下载请求(task_id)
    remove_requested = Signal(str)  # 删除任务请求(task_id)
    open_file_requested = Signal(str)  # 打开文件请求(task_id)
    open_folder_requested = Signal(str)  # 打开文件夹请求(task_id)
    
    def __init__(self, task: DownloadTask, parent=None):
        """初始化下载项
        
        Args:
            task: 下载任务对象
            parent: 父组件
        """
        super().__init__(parent)
        
        self.task = task
        self.task_id = task.task_id
        
        # UI组件
        self.filename_label = None
        self.url_label = None
        self.progress_bar = None
        self.status_label = None
        self.size_label = None
        self.speed_label = None
        self.time_label = None
        self.start_pause_button = None
        self.remove_button = None
        self.open_button = None
        
        # 设置UI
        self._setup_ui()
        
        # 更新显示
        self._update_display()
    
    def _setup_ui(self):
        """设置UI布局"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # 顶部区域：文件名和控制按钮
        top_layout = QHBoxLayout()
        
        # 文件名标签
        self.filename_label = QLabel(self.task.filename)
        filename_font = QFont()
        filename_font.setPointSize(12)
        filename_font.setBold(True)
        self.filename_label.setFont(filename_font)
        self.filename_label.setWordWrap(False)
        top_layout.addWidget(self.filename_label, 1)
        
        # 控制按钮容器
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        
        # 开始/暂停按钮
        self.start_pause_button = QPushButton("开始")
        self.start_pause_button.setFixedWidth(60)
        self.start_pause_button.clicked.connect(self._on_start_pause_clicked)
        button_layout.addWidget(self.start_pause_button)
        
        # 打开文件按钮
        self.open_button = QPushButton("打开")
        self.open_button.setFixedWidth(60)
        self.open_button.clicked.connect(self._on_open_clicked)
        self.open_button.setEnabled(False)
        button_layout.addWidget(self.open_button)
        
        # 删除按钮
        self.remove_button = QPushButton("删除")
        self.remove_button.setFixedWidth(60)
        self.remove_button.clicked.connect(self._on_remove_clicked)
        button_layout.addWidget(self.remove_button)
        
        top_layout.addLayout(button_layout)
        main_layout.addLayout(top_layout)
        
        # URL标签
        self.url_label = QLabel(self.task.url)
        self.url_label.setStyleSheet("color: gray;")
        self.url_label.setWordWrap(False)
        url_font = QFont()
        url_font.setPointSize(9)
        self.url_label.setFont(url_font)
        main_layout.addWidget(self.url_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(20)
        main_layout.addWidget(self.progress_bar)
        
        # 底部信息区域
        bottom_layout = QHBoxLayout()
        
        # 状态标签
        self.status_label = QLabel("等待中")
        self.status_label.setStyleSheet("color: blue;")
        bottom_layout.addWidget(self.status_label)
        
        # 间隔
        bottom_layout.addStretch()
        
        # 大小标签
        self.size_label = QLabel("大小: 未知")
        bottom_layout.addWidget(self.size_label)
        
        # 速度标签
        self.speed_label = QLabel("速度: --")
        bottom_layout.addWidget(self.speed_label)
        
        # 剩余时间标签
        self.time_label = QLabel("剩余: --")
        bottom_layout.addWidget(self.time_label)
        
        main_layout.addLayout(bottom_layout)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # 设置固定高度
        self.setFixedHeight(130)
    
    def update_task(self, task: DownloadTask):
        """更新任务信息
        
        Args:
            task: 更新后的任务对象
        """
        self.task = task
        self._update_display()
    
    def _update_display(self):
        """更新显示内容"""
        # 更新进度条
        self.progress_bar.setValue(int(self.task.progress))
        self.progress_bar.setFormat(f"{self.task.progress:.1f}%")
        
        # 更新状态
        status_text, status_color = self._get_status_info()
        self.status_label.setText(status_text)
        self.status_label.setStyleSheet(f"color: {status_color};")
        
        # 更新按钮状态
        self._update_button_states()
        
        # 更新大小信息
        if self.task.total_size > 0:
            downloaded = int(self.task.total_size * self.task.progress / 100)
            size_text = f"大小: {format_size(downloaded)} / {format_size(self.task.total_size)}"
        else:
            size_text = "大小: 未知"
        self.size_label.setText(size_text)
        
        # 更新速度信息
        if self.task.status == "downloading" and self.task.speed > 0:
            speed_text = f"速度: {format_speed(self.task.speed)}"
        else:
            speed_text = "速度: --"
        self.speed_label.setText(speed_text)
        
        # 更新剩余时间
        if self.task.status == "downloading" and self.task.speed > 0 and self.task.total_size > 0:
            downloaded = int(self.task.total_size * self.task.progress / 100)
            remaining = self.task.total_size - downloaded
            remaining_time = remaining / self.task.speed if self.task.speed > 0 else 0
            time_text = f"剩余: {format_time(remaining_time)}"
        else:
            time_text = "剩余: --"
        self.time_label.setText(time_text)
    
    def _get_status_info(self) -> tuple:
        """获取状态信息
        
        Returns:
            (状态文本, 状态颜色)
        """
        status_map = {
            "waiting": ("等待中", "blue"),
            "downloading": ("下载中", "green"),
            "paused": ("已暂停", "orange"),
            "completed": ("已完成", "darkgreen"),
            "failed": ("失败", "red"),
            "stopped": ("已停止", "gray")
        }
        
        status_text, status_color = status_map.get(
            self.task.status, 
            ("未知", "black")
        )
        
        # 如果失败，添加错误信息
        if self.task.status == "failed" and self.task.error:
            status_text = f"{status_text}: {self.task.error}"
        
        return status_text, status_color
    
    def _update_button_states(self):
        """更新按钮状态"""
        status = self.task.status
        
        # 更新开始/暂停按钮
        if status in ["waiting", "paused", "stopped", "failed"]:
            self.start_pause_button.setText("开始")
            self.start_pause_button.setEnabled(True)
        elif status == "downloading":
            self.start_pause_button.setText("暂停")
            self.start_pause_button.setEnabled(True)
        elif status == "completed":
            self.start_pause_button.setText("完成")
            self.start_pause_button.setEnabled(False)
        
        # 更新打开按钮
        if status == "completed":
            self.open_button.setEnabled(True)
        else:
            self.open_button.setEnabled(False)
        
        # 删除按钮始终可用
        self.remove_button.setEnabled(True)
    
    def _on_start_pause_clicked(self):
        """处理开始/暂停按钮点击"""
        if self.task.status == "downloading":
            # 暂停
            self.pause_requested.emit(self.task_id)
        elif self.task.status == "paused":
            # 恢复
            self.resume_requested.emit(self.task_id)
        elif self.task.status in ["waiting", "stopped", "failed"]:
            # 开始
            self.start_requested.emit(self.task_id)
    
    def _on_remove_clicked(self):
        """处理删除按钮点击"""
        self.remove_requested.emit(self.task_id)
    
    def _on_open_clicked(self):
        """处理打开按钮点击"""
        if self.task.status == "completed":
            self.open_file_requested.emit(self.task_id)
