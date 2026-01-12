"""
主窗口模块
实现应用程序的主界面
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QStatusBar, QMenuBar, QMenu, QMessageBox,
    QScrollArea, QLabel, QPushButton, QFileDialog
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QAction, QIcon, QKeySequence
from typing import List, Optional
import os

from ..core.download_task import DownloadTask
from ..core.download_manager import DownloadManager
from ..utils.config import ConfigManager
from ..utils.logger import Logger
from ..utils.helpers import format_size, format_speed
from ..utils.icon_manager import IconManager
from .add_download_dialog import AddDownloadDialog
from .settings_dialog import SettingsDialog
from .download_item import DownloadItem


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
        self.logger = Logger()
        self.download_manager = DownloadManager()
        self.download_items = {}  # 存储下载项UI组件
        
        self._init_ui()
        self._create_actions()
        self._create_menus()
        self._create_toolbar()
        self._create_statusbar()
        self._connect_signals()
        self._load_settings()
        
        # 定时更新状态栏
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_statusbar)
        self.status_timer.start(1000)  # 每秒更新一次
        
        self.logger.info("主窗口初始化完成")
    
    def _init_ui(self):
        """初始化UI"""
        self.setWindowTitle("下载管理器")
        self.setMinimumSize(900, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建滚动区域用于显示下载列表
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # 下载列表容器
        self.download_list_widget = QWidget()
        self.download_list_layout = QVBoxLayout(self.download_list_widget)
        self.download_list_layout.setContentsMargins(5, 5, 5, 5)
        self.download_list_layout.setSpacing(5)
        self.download_list_layout.addStretch()
        
        scroll_area.setWidget(self.download_list_widget)
        main_layout.addWidget(scroll_area)
        
        # 如果没有下载任务，显示提示
        self.empty_label = QLabel("暂无下载任务\n点击「添加下载」开始")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("""
            QLabel {
                color: #999;
                font-size: 16px;
                padding: 50px;
            }
        """)
        self.download_list_layout.insertWidget(0, self.empty_label)
    
    def _create_actions(self):
        """创建动作"""
        # 文件菜单动作
        self.add_action = QAction(IconManager.get_icon("add"), "添加下载", self)
        self.add_action.setShortcut(QKeySequence("Ctrl+N"))
        self.add_action.setToolTip("添加新的下载任务")
        self.add_action.triggered.connect(self._on_add_download)
        
        self.add_batch_action = QAction(IconManager.get_icon("list"), "批量添加", self)
        self.add_batch_action.setShortcut(QKeySequence("Ctrl+B"))
        self.add_batch_action.triggered.connect(self._on_add_batch)
        
        self.exit_action = QAction(IconManager.get_icon("exit"), "退出", self)
        self.exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        self.exit_action.triggered.connect(self.close)
        
        # 编辑菜单动作
        self.start_all_action = QAction(IconManager.get_icon("start"), "全部开始", self)
        self.start_all_action.triggered.connect(self._on_start_all)
        
        self.pause_all_action = QAction(IconManager.get_icon("pause"), "全部暂停", self)
        self.pause_all_action.triggered.connect(self._on_pause_all)
        
        self.clear_completed_action = QAction(IconManager.get_icon("clear"), "清除已完成", self)
        self.clear_completed_action.triggered.connect(self._on_clear_completed)
        
        self.settings_action = QAction(IconManager.get_icon("settings"), "设置", self)
        self.settings_action.setShortcut(QKeySequence("Ctrl+,"))
        self.settings_action.triggered.connect(self._on_settings)
        
        # 查看菜单动作
        self.show_downloading_action = QAction(IconManager.get_status_icon("downloading"), "正在下载", self)
        self.show_downloading_action.setCheckable(True)
        self.show_downloading_action.setChecked(True)
        
        self.show_completed_action = QAction(IconManager.get_status_icon("completed"), "已完成", self)
        self.show_completed_action.setCheckable(True)
        self.show_completed_action.setChecked(True)
        
        self.show_failed_action = QAction(IconManager.get_status_icon("failed"), "失败", self)
        self.show_failed_action.setCheckable(True)
        self.show_failed_action.setChecked(True)
        
        # 帮助菜单动作
        self.about_action = QAction(IconManager.get_icon("help"), "关于", self)
        self.about_action.triggered.connect(self._on_about)
    
    def _create_menus(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        file_menu.addAction(self.add_action)
        file_menu.addAction(self.add_batch_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")
        edit_menu.addAction(self.start_all_action)
        edit_menu.addAction(self.pause_all_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.clear_completed_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.settings_action)
        
        # 查看菜单
        view_menu = menubar.addMenu("查看")
        view_menu.addAction(self.show_downloading_action)
        view_menu.addAction(self.show_completed_action)
        view_menu.addAction(self.show_failed_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        help_menu.addAction(self.about_action)
    
    def _create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)
        
        toolbar.addAction(self.add_action)
        toolbar.addSeparator()
        toolbar.addAction(self.start_all_action)
        toolbar.addAction(self.pause_all_action)
        toolbar.addSeparator()
        toolbar.addAction(self.settings_action)
    
    def _create_statusbar(self):
        """创建状态栏"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        self.statusbar.addWidget(self.status_label)
        
        # 速度标签
        self.speed_label = QLabel("速度: 0 B/s")
        self.statusbar.addPermanentWidget(self.speed_label)
        
        # 任务统计标签
        self.task_count_label = QLabel("任务: 0")
        self.statusbar.addPermanentWidget(self.task_count_label)
    
    def _connect_signals(self):
        """连接信号"""
        # 连接下载管理器信号
        self.download_manager.task_added.connect(self._on_task_added)
        self.download_manager.task_removed.connect(self._on_task_removed)
        self.download_manager.task_updated.connect(self._on_task_updated)
    
    def _load_settings(self):
        """加载设置"""
        # 加载窗口位置和大小
        try:
            geometry = self.config.get('ui.window_geometry')
            if geometry:
                self.restoreGeometry(geometry)
        except:
            pass
        
        # 加载下载目录
        download_dir = self.config.get('general.download_directory')
        if download_dir:
            os.makedirs(download_dir, exist_ok=True)
    
    def _update_statusbar(self):
        """更新状态栏"""
        # 获取所有任务
        tasks = self.download_manager.get_all_tasks()
        
        # 统计任务数量
        downloading = sum(1 for t in tasks if t.status == 'downloading')
        completed = sum(1 for t in tasks if t.status == 'completed')
        failed = sum(1 for t in tasks if t.status == 'failed')
        paused = sum(1 for t in tasks if t.status == 'paused')
        
        # 计算总速度
        total_speed = sum(t.speed for t in tasks if t.status == 'downloading')
        
        # 更新标签
        self.task_count_label.setText(f"任务: {len(tasks)} (下载:{downloading} 完成:{completed} 失败:{failed} 暂停:{paused})")
        self.speed_label.setText(f"速度: {format_speed(total_speed)}")
        
        if downloading > 0:
            self.status_label.setText(f"正在下载 {downloading} 个任务")
        else:
            self.status_label.setText("就绪")
    
    def _on_add_download(self):
        """添加下载"""
        dialog = AddDownloadDialog(self)
        if dialog.exec():
            url = dialog.get_url()
            save_path = dialog.get_save_path()
            if url and save_path:
                self.download_manager.add_task(url, save_path)
                self.logger.info(f"添加下载任务: {url}")
    
    def _on_add_batch(self):
        """批量添加下载"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择URL列表文件", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                
                save_dir = self.config.get('general.download_directory')
                for url in urls:
                    self.download_manager.add_task(url, save_dir)
                
                self.logger.info(f"批量添加 {len(urls)} 个下载任务")
                QMessageBox.information(self, "成功", f"已添加 {len(urls)} 个下载任务")
            except Exception as e:
                self.logger.error(f"批量添加失败: {e}")
                QMessageBox.critical(self, "错误", f"批量添加失败: {e}")
    
    def _on_start_all(self):
        """开始所有任务"""
        tasks = self.download_manager.get_all_tasks()
        for task in tasks:
            if task.status in ['paused', 'failed']:
                self.download_manager.start_task(task.task_id)
        self.logger.info("开始所有任务")
    
    def _on_pause_all(self):
        """暂停所有任务"""
        tasks = self.download_manager.get_all_tasks()
        for task in tasks:
            if task.status == 'downloading':
                self.download_manager.pause_task(task.task_id)
        self.logger.info("暂停所有任务")
    
    def _on_clear_completed(self):
        """清除已完成的任务"""
        tasks = self.download_manager.get_all_tasks()
        completed_tasks = [t for t in tasks if t.status == 'completed']
        
        if not completed_tasks:
            QMessageBox.information(self, "提示", "没有已完成的任务")
            return
        
        reply = QMessageBox.question(
            self, "确认", 
            f"确定要清除 {len(completed_tasks)} 个已完成的任务吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            for task in completed_tasks:
                self.download_manager.remove_task(task.task_id)
            self.logger.info(f"清除 {len(completed_tasks)} 个已完成任务")
    
    def _on_settings(self):
        """打开设置对话框"""
        dialog = SettingsDialog(self)
        dialog.exec()
    
    def _on_about(self):
        """关于对话框"""
        QMessageBox.about(
            self,
            "关于",
            "<h3>下载管理器</h3>"
            "<p>一个基于PySide6的开源下载工具</p>"
            "<p>版本: 0.1.0</p>"
            "<p>作者: Your Name</p>"
        )
    
    def _on_task_added(self, task: DownloadTask):
        """任务添加事件"""
        # 隐藏空提示
        if self.empty_label.isVisible():
            self.empty_label.hide()
        
        # 创建下载项UI
        download_item = DownloadItem(task)
        self.download_items[task.task_id] = download_item
        
        # 添加到列表
        count = self.download_list_layout.count()
        self.download_list_layout.insertWidget(count - 1, download_item)  # 插入到stretch之前
        
        self.logger.info(f"任务已添加到界面: {task.filename}")
    
    def _on_task_removed(self, task_id: str):
        """任务移除事件"""
        if task_id in self.download_items:
            item = self.download_items[task_id]
            self.download_list_layout.removeWidget(item)
            item.deleteLater()
            del self.download_items[task_id]
            
            # 如果没有任务了，显示空提示
            if not self.download_items:
                self.empty_label.show()
            
            self.logger.info(f"任务已从界面移除: {task_id}")
    
    def _on_task_updated(self, task: DownloadTask):
        """任务更新事件"""
        if task.task_id in self.download_items:
            self.download_items[task.task_id].update_task(task)
    
    def closeEvent(self, event):
        """关闭事件"""
        # 检查是否有正在下载的任务
        tasks = self.download_manager.get_all_tasks()
        downloading = [t for t in tasks if t.status == 'downloading']
        
        if downloading:
            reply = QMessageBox.question(
                self,
                "确认退出",
                f"还有 {len(downloading)} 个任务正在下载，确定要退出吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                event.ignore()
                return
        
        # 关闭下载管理器（会自动保存任务状态）
        self.download_manager.shutdown()
        
        # 保存窗口大小（但不保存geometry，因为QByteArray无法序列化）
        self.config.set('ui.window.width', self.width())
        self.config.set('ui.window.height', self.height())
        self.config.save_config()
        
        self.logger.info("应用程序关闭")
        event.accept()
