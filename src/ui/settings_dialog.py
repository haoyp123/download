"""
设置对话框模块
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSpinBox, QCheckBox,
    QFileDialog, QTabWidget, QWidget, QGroupBox,
    QFormLayout, QComboBox
)
from PySide6.QtCore import Qt
import os

from ..utils.config import ConfigManager


class SettingsDialog(QDialog):
    """设置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager()
        self._init_ui()
        self._load_settings()
    
    def _init_ui(self):
        """初始化UI"""
        self.setWindowTitle("设置")
        self.setModal(True)
        self.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 常规设置标签页
        self.general_tab = self._create_general_tab()
        self.tab_widget.addTab(self.general_tab, "常规")
        
        # 网络设置标签页
        self.network_tab = self._create_network_tab()
        self.tab_widget.addTab(self.network_tab, "网络")
        
        # 速度设置标签页
        self.speed_tab = self._create_speed_tab()
        self.tab_widget.addTab(self.speed_tab, "速度")
        
        layout.addWidget(self.tab_widget)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self._on_ok)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        self.apply_button = QPushButton("应用")
        self.apply_button.clicked.connect(self._on_apply)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.apply_button)
        
        layout.addLayout(button_layout)
    
    def _create_general_tab(self) -> QWidget:
        """创建常规设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 下载目录设置
        download_group = QGroupBox("下载设置")
        download_layout = QFormLayout()
        
        # 下载目录
        dir_layout = QHBoxLayout()
        self.download_dir_input = QLineEdit()
        browse_button = QPushButton("浏览...")
        browse_button.clicked.connect(self._on_browse_download_dir)
        dir_layout.addWidget(self.download_dir_input)
        dir_layout.addWidget(browse_button)
        download_layout.addRow("下载目录:", dir_layout)
        
        # 最大同时下载数
        self.max_concurrent_input = QSpinBox()
        self.max_concurrent_input.setRange(1, 10)
        self.max_concurrent_input.setSuffix(" 个")
        download_layout.addRow("最大同时下载:", self.max_concurrent_input)
        
        # 自动开始下载
        self.auto_start_checkbox = QCheckBox("添加任务后自动开始下载")
        download_layout.addRow("", self.auto_start_checkbox)
        
        download_group.setLayout(download_layout)
        layout.addWidget(download_group)
        
        # 通知设置
        notification_group = QGroupBox("通知设置")
        notification_layout = QFormLayout()
        
        self.notify_complete_checkbox = QCheckBox("下载完成时显示通知")
        notification_layout.addRow("", self.notify_complete_checkbox)
        
        self.notify_error_checkbox = QCheckBox("下载失败时显示通知")
        notification_layout.addRow("", self.notify_error_checkbox)
        
        notification_group.setLayout(notification_layout)
        layout.addWidget(notification_group)
        
        layout.addStretch()
        return widget
    
    def _create_network_tab(self) -> QWidget:
        """创建网络设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 连接设置
        connection_group = QGroupBox("连接设置")
        connection_layout = QFormLayout()
        
        # 连接数
        self.connections_input = QSpinBox()
        self.connections_input.setRange(1, 32)
        self.connections_input.setSuffix(" 个")
        connection_layout.addRow("每个任务的连接数:", self.connections_input)
        
        # 超时设置
        self.timeout_input = QSpinBox()
        self.timeout_input.setRange(10, 300)
        self.timeout_input.setSuffix(" 秒")
        connection_layout.addRow("连接超时:", self.timeout_input)
        
        # 重试次数
        self.retry_input = QSpinBox()
        self.retry_input.setRange(0, 10)
        self.retry_input.setSuffix(" 次")
        connection_layout.addRow("失败重试次数:", self.retry_input)
        
        connection_group.setLayout(connection_layout)
        layout.addWidget(connection_group)
        
        # 代理设置
        proxy_group = QGroupBox("代理设置")
        proxy_layout = QFormLayout()
        
        self.use_proxy_checkbox = QCheckBox("使用代理服务器")
        self.use_proxy_checkbox.toggled.connect(self._on_proxy_toggled)
        proxy_layout.addRow("", self.use_proxy_checkbox)
        
        # 代理类型
        self.proxy_type_combo = QComboBox()
        self.proxy_type_combo.addItems(["HTTP", "HTTPS", "SOCKS5"])
        proxy_layout.addRow("代理类型:", self.proxy_type_combo)
        
        # 代理地址
        self.proxy_host_input = QLineEdit()
        self.proxy_host_input.setPlaceholderText("例如: 127.0.0.1")
        proxy_layout.addRow("代理地址:", self.proxy_host_input)
        
        # 代理端口
        self.proxy_port_input = QSpinBox()
        self.proxy_port_input.setRange(1, 65535)
        proxy_layout.addRow("代理端口:", self.proxy_port_input)
        
        # 代理用户名
        self.proxy_username_input = QLineEdit()
        self.proxy_username_input.setPlaceholderText("可选")
        proxy_layout.addRow("用户名:", self.proxy_username_input)
        
        # 代理密码
        self.proxy_password_input = QLineEdit()
        self.proxy_password_input.setEchoMode(QLineEdit.Password)
        self.proxy_password_input.setPlaceholderText("可选")
        proxy_layout.addRow("密码:", self.proxy_password_input)
        
        proxy_group.setLayout(proxy_layout)
        layout.addWidget(proxy_group)
        
        layout.addStretch()
        return widget
    
    def _create_speed_tab(self) -> QWidget:
        """创建速度设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 速度限制
        speed_group = QGroupBox("速度限制")
        speed_layout = QFormLayout()
        
        # 全局下载速度限制
        self.enable_global_limit_checkbox = QCheckBox("启用全局下载速度限制")
        self.enable_global_limit_checkbox.toggled.connect(self._on_global_limit_toggled)
        speed_layout.addRow("", self.enable_global_limit_checkbox)
        
        self.global_limit_input = QSpinBox()
        self.global_limit_input.setRange(0, 100000)
        self.global_limit_input.setSuffix(" KB/s")
        self.global_limit_input.setSpecialValueText("不限制")
        speed_layout.addRow("全局下载速度:", self.global_limit_input)
        
        # 单任务速度限制
        self.enable_task_limit_checkbox = QCheckBox("启用单任务速度限制")
        self.enable_task_limit_checkbox.toggled.connect(self._on_task_limit_toggled)
        speed_layout.addRow("", self.enable_task_limit_checkbox)
        
        self.task_limit_input = QSpinBox()
        self.task_limit_input.setRange(0, 100000)
        self.task_limit_input.setSuffix(" KB/s")
        self.task_limit_input.setSpecialValueText("不限制")
        speed_layout.addRow("单任务速度:", self.task_limit_input)
        
        speed_group.setLayout(speed_layout)
        layout.addWidget(speed_group)
        
        layout.addStretch()
        return widget
    
    def _load_settings(self):
        """加载设置"""
        # 常规设置
        self.download_dir_input.setText(
            self.config.get('general.download_directory', os.path.expanduser('~/Downloads'))
        )
        self.max_concurrent_input.setValue(
            self.config.get('general.max_concurrent_downloads', 3)
        )
        self.auto_start_checkbox.setChecked(
            self.config.get('general.auto_start', True)
        )
        
        # 通知设置
        self.notify_complete_checkbox.setChecked(
            self.config.get('notifications.on_complete', True)
        )
        self.notify_error_checkbox.setChecked(
            self.config.get('notifications.on_error', True)
        )
        
        # 网络设置
        self.connections_input.setValue(
            self.config.get('network.connections_per_file', 8)
        )
        self.timeout_input.setValue(
            self.config.get('network.timeout', 30)
        )
        self.retry_input.setValue(
            self.config.get('network.max_retries', 3)
        )
        
        # 代理设置
        use_proxy = self.config.get('network.proxy.enabled', False)
        self.use_proxy_checkbox.setChecked(use_proxy)
        self.proxy_host_input.setText(
            self.config.get('network.proxy.host', '')
        )
        self.proxy_port_input.setValue(
            self.config.get('network.proxy.port', 8080)
        )
        self.proxy_username_input.setText(
            self.config.get('network.proxy.username', '')
        )
        self.proxy_password_input.setText(
            self.config.get('network.proxy.password', '')
        )
        
        # 速度设置
        enable_global = self.config.get('speed.global_limit_enabled', False)
        self.enable_global_limit_checkbox.setChecked(enable_global)
        self.global_limit_input.setValue(
            self.config.get('speed.global_limit_kbps', 0)
        )
        self.global_limit_input.setEnabled(enable_global)
        
        enable_task = self.config.get('speed.per_task_limit_enabled', False)
        self.enable_task_limit_checkbox.setChecked(enable_task)
        self.task_limit_input.setValue(
            self.config.get('speed.per_task_limit_kbps', 0)
        )
        self.task_limit_input.setEnabled(enable_task)
    
    def _save_settings(self):
        """保存设置"""
        # 常规设置
        self.config.set('general.download_directory', self.download_dir_input.text())
        self.config.set('general.max_concurrent_downloads', self.max_concurrent_input.value())
        self.config.set('general.auto_start', self.auto_start_checkbox.isChecked())
        
        # 通知设置
        self.config.set('notifications.on_complete', self.notify_complete_checkbox.isChecked())
        self.config.set('notifications.on_error', self.notify_error_checkbox.isChecked())
        
        # 网络设置
        self.config.set('network.connections_per_file', self.connections_input.value())
        self.config.set('network.timeout', self.timeout_input.value())
        self.config.set('network.max_retries', self.retry_input.value())
        
        # 代理设置
        self.config.set('network.proxy.enabled', self.use_proxy_checkbox.isChecked())
        self.config.set('network.proxy.host', self.proxy_host_input.text())
        self.config.set('network.proxy.port', self.proxy_port_input.value())
        self.config.set('network.proxy.username', self.proxy_username_input.text())
        self.config.set('network.proxy.password', self.proxy_password_input.text())
        
        # 速度设置
        self.config.set('speed.global_limit_enabled', self.enable_global_limit_checkbox.isChecked())
        self.config.set('speed.global_limit_kbps', self.global_limit_input.value())
        self.config.set('speed.per_task_limit_enabled', self.enable_task_limit_checkbox.isChecked())
        self.config.set('speed.per_task_limit_kbps', self.task_limit_input.value())
        
        # 保存到文件
        self.config.save()
    
    def _on_browse_download_dir(self):
        """浏览下载目录"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择下载目录",
            self.download_dir_input.text()
        )
        if directory:
            self.download_dir_input.setText(directory)
    
    def _on_proxy_toggled(self, checked: bool):
        """代理复选框切换事件"""
        self.proxy_type_combo.setEnabled(checked)
        self.proxy_host_input.setEnabled(checked)
        self.proxy_port_input.setEnabled(checked)
        self.proxy_username_input.setEnabled(checked)
        self.proxy_password_input.setEnabled(checked)
    
    def _on_global_limit_toggled(self, checked: bool):
        """全局速度限制切换事件"""
        self.global_limit_input.setEnabled(checked)
    
    def _on_task_limit_toggled(self, checked: bool):
        """单任务速度限制切换事件"""
        self.task_limit_input.setEnabled(checked)
    
    def _on_ok(self):
        """确定按钮点击事件"""
        self._save_settings()
        self.accept()
    
    def _on_apply(self):
        """应用按钮点击事件"""
        self._save_settings()
