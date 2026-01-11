"""
添加下载对话框模块
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
import os

from ..utils.config import ConfigManager
from ..utils.helpers import is_valid_url, get_filename_from_url


class AddDownloadDialog(QDialog):
    """添加下载对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager()
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        self.setWindowTitle("添加下载")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # URL输入
        url_layout = QVBoxLayout()
        url_label = QLabel("下载链接:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("请输入下载链接...")
        self.url_input.textChanged.connect(self._on_url_changed)
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        # 文件名输入
        filename_layout = QVBoxLayout()
        filename_label = QLabel("文件名:")
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("自动从URL提取...")
        filename_layout.addWidget(filename_label)
        filename_layout.addWidget(self.filename_input)
        layout.addLayout(filename_layout)
        
        # 保存路径
        path_layout = QVBoxLayout()
        path_label = QLabel("保存位置:")
        
        path_input_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        default_dir = self.config.get('general.download_directory', os.path.expanduser('~/Downloads'))
        self.path_input.setText(default_dir)
        
        self.browse_button = QPushButton("浏览...")
        self.browse_button.clicked.connect(self._on_browse)
        
        path_input_layout.addWidget(self.path_input)
        path_input_layout.addWidget(self.browse_button)
        
        path_layout.addWidget(path_label)
        path_layout.addLayout(path_input_layout)
        layout.addLayout(path_layout)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.ok_button = QPushButton("确定")
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self._on_ok)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
    
    def _on_url_changed(self, text: str):
        """URL输入变化事件"""
        # 验证URL
        is_valid = is_valid_url(text)
        self.ok_button.setEnabled(is_valid)
        
        # 自动提取文件名
        if is_valid and not self.filename_input.text():
            filename = get_filename_from_url(text)
            if filename:
                self.filename_input.setText(filename)
    
    def _on_browse(self):
        """浏览文件夹"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择保存位置",
            self.path_input.text()
        )
        if directory:
            self.path_input.setText(directory)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        url = self.url_input.text().strip()
        save_dir = self.path_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "警告", "请输入下载链接")
            return
        
        if not is_valid_url(url):
            QMessageBox.warning(self, "警告", "下载链接格式不正确")
            return
        
        if not save_dir:
            QMessageBox.warning(self, "警告", "请选择保存位置")
            return
        
        if not os.path.exists(save_dir):
            reply = QMessageBox.question(
                self,
                "确认",
                f"目录 {save_dir} 不存在，是否创建？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                try:
                    os.makedirs(save_dir, exist_ok=True)
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"创建目录失败: {e}")
                    return
            else:
                return
        
        self.accept()
    
    def get_url(self) -> str:
        """获取URL"""
        return self.url_input.text().strip()
    
    def get_filename(self) -> str:
        """获取文件名"""
        return self.filename_input.text().strip()
    
    def get_save_path(self) -> str:
        """获取保存路径"""
        save_dir = self.path_input.text().strip()
        filename = self.get_filename()
        
        if not filename:
            filename = get_filename_from_url(self.get_url())
        
        if filename:
            return os.path.join(save_dir, filename)
        return save_dir
