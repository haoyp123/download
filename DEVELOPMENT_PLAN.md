# PyDownloader 开发计划

## 项目概述

开发一个功能完善的多线程下载管理器，核心参考 NDM（Neat Download Manager）的设计理念，使用 PySide6 构建现代化的桌面应用。

---

## 当前进度总结

### 已完成里程碑
- ✅ **M1**: 完成基础UI和单线程下载
- ✅ **M2**: 实现多线程下载和断点续传

### 当前状态
- **测试日期**: 2026年1月11日
- **当前版本**: v0.1.0
- **开发阶段**: 阶段三已完成，准备进入阶段四
- **代码质量**: 优秀，核心功能测试通过率100%

### 已实现功能清单
1. ✅ 项目基础架构（配置、日志、工具模块）
2. ✅ 基础UI框架（主窗口、添加对话框、设置对话框）
3. ✅ 下载任务模型（DownloadTask数据类）
4. ✅ 单线程下载器（完整实现）
5. ✅ 多线程分块下载（4线程测试通过）
6. ✅ 断点续传机制（暂停/恢复功能验证通过）
7. ✅ 下载管理器（任务调度、信号机制）
8. ✅ 临时文件管理（.tmp文件机制）
9. ✅ 文件完整性验证
10. ✅ 进度跟踪与回调

### 测试验证情况
详见 [TEST_REPORT.md](TEST_REPORT.md)
- ✅ 依赖安装测试
- ✅ 应用启动/关闭测试
- ✅ 下载功能集成测试（3/3通过）
  - 单线程下载：15KB文件
  - 多线程下载：11MB文件，2.71秒
  - 暂停/恢复：功能正常

### 已修复的重要Bug
1. Bug #5: 文件路径拼接错误（严重）- `downloader.py`中4处修复
2. Bug #6: QCoreApplication单例冲突（中等）
3. Bug #7: 暂停/恢复测试触发优化（轻微）

---

## 下一步开发重点

### 🎯 当前优先级：UI集成与功能完善

虽然核心下载功能已经实现并测试通过，但目前还无法通过GUI使用这些功能。下一步应该：

#### 第一优先级：UI与下载功能集成
1. **连接UI和下载管理器**
   - 在main_window.py中集成DownloadManager实例
   - 实现"添加下载"按钮的实际功能
   - 连接AddDownloadDialog与DownloadManager
   - 实现任务添加后的UI更新

2. **下载列表UI实现**
   - 使用QListWidget或QTableWidget显示下载任务
   - 为每个任务创建DownloadItem组件实例
   - 实现任务的实时进度更新
   - 添加任务状态图标和颜色标识

3. **任务控制集成**
   - 实现工具栏按钮功能（暂停、恢复、删除）
   - 实现右键菜单功能
   - 添加任务选择和批量操作
   - 实现"打开文件夹"功能

4. **状态栏信息更新**
   - 显示当前下载速度
   - 显示活动任务数量
   - 显示总下载/上传统计

#### 第二优先级：设置功能实现
1. **完善SettingsDialog**
   - 实现默认下载路径设置
   - 实现最大并发下载数设置
   - 实现下载线程数默认值设置
   - 添加速度限制基础设置

2. **配置持久化**
   - 确保用户设置保存到config/settings.yaml
   - 应用启动时加载用户设置
   - 实现设置的实时应用

#### 第三优先级：基础数据持久化
在UI功能基本可用后，实现：
1. 下载任务列表的持久化存储
2. 应用重启后恢复任务列表
3. 下载历史记录基础功能

---

## 开发阶段详细规划

### 阶段一：项目基础搭建 ✅ 已完成

#### 1.1 环境准备
- [x] 创建项目目录结构
- [x] 配置虚拟环境
- [x] 安装基础依赖（使用清华源）
  - PySide6==6.6.1
  - requests==2.31.0
  - aiohttp==3.9.1
  - PyYAML==6.0.1
  - pytest==7.4.3
  - black==23.12.1

#### 1.2 项目框架
- [x] 创建主程序入口 `main.py`
- [x] 设计配置文件结构 `config/settings.yaml`
- [x] 实现配置管理模块 `src/utils/config.py`
- [x] 实现日志模块 `src/utils/logger.py`
- [x] 实现辅助函数 `src/utils/helpers.py`

#### 1.3 基础UI框架
- [x] 创建主窗口类 `src/ui/main_window.py`
  - [x] 菜单栏（文件、编辑、视图、帮助）
  - [x] 工具栏（添加、暂停、恢复、删除）
  - [x] 状态栏（下载统计、速度显示）
  - [x] 主界面布局（下载列表区域）
- [x] 创建添加下载对话框 `src/ui/add_download_dialog.py`
  - [x] URL输入框
  - [x] 保存路径选择
  - [x] 文件名设置
  - [x] 线程数选择
- [x] 创建设置对话框 `src/ui/settings_dialog.py`
  - [x] 常规设置（默认下载路径、最大同时下载数）
  - [x] 网络设置（代理、超时时间）
  - [x] 外观设置（主题选择）

**阶段总结**: UI框架已搭建完成，但功能尚未与后端逻辑连接。

### 阶段二：核心下载功能 ✅ 已完成

#### 2.1 下载任务模型
- [x] 创建下载任务类 `src/core/download_task.py`
  - [x] 任务状态枚举（PENDING、DOWNLOADING、PAUSED、COMPLETED、FAILED、CANCELLED）
  - [x] 任务信息（task_id、url、filename、save_path、file_size、downloaded_size）
  - [x] 进度计算属性（progress、speed、eta）
  - [x] 使用@dataclass装饰器实现

#### 2.2 单线程下载器
- [x] 实现基础下载器 `src/core/downloader.py`
  - [x] HTTP请求处理（支持HEAD和GET请求）
  - [x] 响应头解析（Content-Length、Accept-Ranges检测）
  - [x] 文件写入（支持单线程和多线程模式）
  - [x] 进度回调（通过回调函数机制）
  - [x] 异常处理（网络错误、文件系统错误）
  - [x] **Bug修复**: 文件路径拼接错误已修复

#### 2.3 下载项UI组件
- [x] 创建下载项组件 `src/ui/download_item.py`
  - [x] 文件图标和名称显示
  - [x] 进度条（QProgressBar）
  - [x] 速度和剩余时间显示
  - [x] 操作按钮（暂停、恢复、删除、打开文件夹）
  - [x] 状态标签显示
  - [x] 右键菜单（重新下载、删除、属性）

**注意**: DownloadItem组件已创建，但尚未在主窗口中实际使用。

#### 2.4 下载管理器
- [x] 实现下载管理器逻辑 `src/core/download_manager.py`
  - [x] 下载队列管理（tasks字典）
  - [x] 最大并发控制（max_concurrent参数）
  - [x] 任务调度（_process_queue方法）
  - [x] 事件通知机制（Qt信号系统）
    - [x] task_started、task_progress、task_completed等信号
  - [x] 线程管理（使用threading.Thread）

**阶段总结**: 核心下载功能已完整实现并通过测试，但尚未与UI集成。

### 阶段三：多线程下载与断点续传 ✅ 已完成

#### 3.1 分块下载策略
- [x] 实现文件分块算法（在`downloader.py`中）
  - [x] 根据文件大小和线程数计算分块
  - [x] 每块大小计算（chunk_size = file_size // num_threads）
  - [x] 块索引管理（chunk_ranges列表）
  - [x] Range请求支持检测

#### 3.2 线程池管理
- [x] 使用ThreadPoolExecutor管理下载线程
  - [x] 工作线程管理（ThreadPoolExecutor内置）
  - [x] 任务分配（submit方法）
  - [x] 线程同步（Event和Lock）
  - [x] 资源清理（shutdown方法）

#### 3.3 断点续传
- [x] 实现断点续传机制
  - [x] 下载状态跟踪（通过DownloadTask）
  - [x] 已下载数据记录（downloaded_size）
  - [x] 恢复下载逻辑（pause/resume方法）
  - [x] 临时文件管理（.tmp后缀，下载完成后重命名）
  - [x] **测试验证**: 暂停/恢复功能测试通过

#### 3.4 文件合并
- [x] 实现文件合并逻辑（在`downloader.py`中）
  - [x] 分块文件合并（_download_with_chunks方法）
  - [x] 文件完整性校验（大小验证）
  - [x] 临时文件自动清理

**阶段总结**: 多线程下载和断点续传功能已完整实现，通过集成测试验证。
- ✅ 单线程下载测试通过（15KB文件）
- ✅ 多线程下载测试通过（11MB文件，4线程，2.71秒）
- ✅ 暂停/恢复测试通过

### 阶段四：数据持久化 🔄 待开发

**前置条件**: 建议先完成UI集成，使功能可通过GUI使用后再实现数据持久化。

#### 4.1 数据库设计
- [ ] 设计数据表结构 `database/models.py`
  - downloads表（下载任务信息）
  - settings表（应用配置）
  - categories表（下载分类）

#### 4.2 数据库管理
- [ ] 实现数据库管理器 `database/db_manager.py`
  - 数据库初始化
  - CRUD操作封装
  - 查询优化
  - 数据迁移支持

#### 4.3 历史记录
- [ ] 实现下载历史功能
  - 历史记录查看
  - 搜索和筛选
  - 重新下载
  - 批量清理

### 阶段五：高级功能 (预计7-10天)

#### 5.1 速度控制
- [ ] 实现速度限制功能
  - 全局速度限制
  - 单任务速度限制
  - 时段限速（可选）
  - 令牌桶算法实现

#### 5.2 浏览器集成
- [ ] 浏览器扩展支持
  - 监听剪贴板（可选）
  - 浏览器扩展通信协议
  - 文件类型过滤

#### 5.3 批量下载
- [ ] 实现批量下载功能
  - 批量URL导入（文本文件）
  - 批量任务管理
  - 下载完成后操作（关机、休眠等）

#### 5.4 通知系统
- [ ] 实现通知功能
  - 下载完成通知
  - 错误提醒
  - 系统托盘图标
  - 托盘菜单

#### 5.5 主题与美化
- [ ] 实现主题系统
  - 亮色主题
  - 暗色主题
  - 自定义QSS样式表
  - 图标适配

### 阶段六：优化与测试 (预计5-7天)

#### 6.1 性能优化
- [ ] 内存使用优化
- [ ] 大文件下载优化
- [ ] UI响应优化（异步处理）
- [ ] 网络连接池优化

#### 6.2 异常处理
- [ ] 网络异常处理
- [ ] 文件系统异常处理
- [ ] 崩溃恢复机制
- [ ] 错误日志记录

#### 6.3 测试
- [ ] 单元测试编写
- [ ] 集成测试
- [ ] 压力测试（大文件、多任务）
- [ ] 跨平台测试（Windows、macOS、Linux）

#### 6.4 文档完善
- [ ] 用户手册
- [ ] API文档
- [ ] 开发文档
- [ ] 更新日志

## 技术实现指南

### 1. UI集成实现详解

#### 1.1 MainWindow与DownloadManager集成

**步骤一：在MainWindow中初始化DownloadManager**

```python
# src/ui/main_window.py
from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PySide6.QtCore import QThread, Slot
from ..core.download_manager import DownloadManager
from ..core.download_task import DownloadTask, DownloadStatus

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # 初始化下载管理器
        self.download_manager = DownloadManager(max_concurrent=3)
        
        # 连接信号到槽函数
        self._connect_signals()
        
    def _connect_signals(self):
        """连接下载管理器的所有信号"""
        self.download_manager.task_started.connect(self.on_task_started)
        self.download_manager.task_progress.connect(self.on_task_progress)
        self.download_manager.task_completed.connect(self.on_task_completed)
        self.download_manager.task_failed.connect(self.on_task_failed)
        self.download_manager.task_paused.connect(self.on_task_paused)
        self.download_manager.task_resumed.connect(self.on_task_resumed)
        
    @Slot(str)
    def on_task_started(self, task_id: str):
        """任务开始时更新UI"""
        task = self.download_manager.get_task(task_id)
        if task:
            self._add_task_to_list(task)
            self.statusBar().showMessage(f"开始下载: {task.filename}")
    
    @Slot(str, int, float)
    def on_task_progress(self, task_id: str, downloaded: int, speed: float):
        """更新任务进度"""
        self._update_task_progress(task_id, downloaded, speed)
    
    @Slot(str)
    def on_task_completed(self, task_id: str):
        """任务完成时更新UI"""
        task = self.download_manager.get_task(task_id)
        if task:
            self._update_task_status(task_id, DownloadStatus.COMPLETED)
            self.statusBar().showMessage(f"下载完成: {task.filename}")
    
    @Slot(str, str)
    def on_task_failed(self, task_id: str, error: str):
        """任务失败时更新UI"""
        self._update_task_status(task_id, DownloadStatus.FAILED)
        self.statusBar().showMessage(f"下载失败: {error}")
```

**步骤二：实现添加下载功能**

```python
# src/ui/main_window.py (继续)
from .add_download_dialog import AddDownloadDialog

class MainWindow(QMainWindow):
    # ... 前面的代码 ...
    
    def on_add_download(self):
        """处理添加下载按钮点击"""
        dialog = AddDownloadDialog(self)
        if dialog.exec():
            # 获取对话框数据
            url = dialog.url_edit.text().strip()
            save_path = dialog.path_edit.text().strip()
            filename = dialog.filename_edit.text().strip()
            num_threads = dialog.threads_spinbox.value()
            
            # 验证输入
            if not url or not save_path:
                self.statusBar().showMessage("请填写完整信息")
                return
            
            # 添加到下载管理器
            try:
                task_id = self.download_manager.add_task(
                    url=url,
                    save_path=save_path,
                    filename=filename,
                    num_threads=num_threads
                )
                self.statusBar().showMessage(f"已添加下载任务: {filename}")
            except Exception as e:
                self.statusBar().showMessage(f"添加任务失败: {str(e)}")
```

#### 1.2 下载列表UI实现

**推荐方案：使用QTableWidget**

```python
# src/ui/main_window.py
class MainWindow(QMainWindow):
    def setup_ui(self):
        # ... 其他UI代码 ...
        
        # 创建下载列表表格
        self.download_table = QTableWidget()
        self.download_table.setColumnCount(6)
        self.download_table.setHorizontalHeaderLabels([
            "文件名", "状态", "进度", "速度", "大小", "操作"
        ])
        
        # 设置列宽
        self.download_table.setColumnWidth(0, 250)  # 文件名
        self.download_table.setColumnWidth(1, 80)   # 状态
        self.download_table.setColumnWidth(2, 150)  # 进度
        self.download_table.setColumnWidth(3, 100)  # 速度
        self.download_table.setColumnWidth(4, 100)  # 大小
        self.download_table.setColumnWidth(5, 150)  # 操作
        
        # 设置表格属性
        self.download_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.download_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.setCentralWidget(self.download_table)
        
        # 任务ID到行号的映射
        self.task_row_map = {}
    
    def _add_task_to_list(self, task: DownloadTask):
        """添加任务到列表"""
        row = self.download_table.rowCount()
        self.download_table.insertRow(row)
        
        # 存储映射关系
        self.task_row_map[task.task_id] = row
        
        # 文件名
        self.download_table.setItem(row, 0, QTableWidgetItem(task.filename))
        
        # 状态
        status_item = QTableWidgetItem(self._get_status_text(task.status))
        self.download_table.setItem(row, 1, status_item)
        
        # 进度条
        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        self.download_table.setCellWidget(row, 2, progress_bar)
        
        # 速度
        self.download_table.setItem(row, 3, QTableWidgetItem("0 KB/s"))
        
        # 大小
        size_text = self._format_size(task.file_size) if task.file_size else "未知"
        self.download_table.setItem(row, 4, QTableWidgetItem(size_text))
        
        # 操作按钮
        self._create_action_buttons(row, task.task_id)
    
    def _update_task_progress(self, task_id: str, downloaded: int, speed: float):
        """更新任务进度"""
        if task_id not in self.task_row_map:
            return
        
        row = self.task_row_map[task_id]
        task = self.download_manager.get_task(task_id)
        if not task:
            return
        
        # 更新进度条
        progress_bar = self.download_table.cellWidget(row, 2)
        if isinstance(progress_bar, QProgressBar) and task.file_size:
            progress = int((downloaded / task.file_size) * 100)
            progress_bar.setValue(progress)
        
        # 更新速度
        speed_text = f"{self._format_speed(speed)}"
        self.download_table.item(row, 3).setText(speed_text)
    
    def _format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    def _format_speed(self, speed: float) -> str:
        """格式化下载速度"""
        return f"{self._format_size(speed)}/s"
    
    def _get_status_text(self, status: DownloadStatus) -> str:
        """获取状态文本"""
        status_map = {
            DownloadStatus.PENDING: "等待中",
            DownloadStatus.DOWNLOADING: "下载中",
            DownloadStatus.PAUSED: "已暂停",
            DownloadStatus.COMPLETED: "已完成",
            DownloadStatus.FAILED: "失败",
            DownloadStatus.CANCELLED: "已取消"
        }
        return status_map.get(status, "未知")
```

#### 1.3 任务控制功能实现

```python
# src/ui/main_window.py
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget

class MainWindow(QMainWindow):
    def _create_action_buttons(self, row: int, task_id: str):
        """创建操作按钮"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # 暂停/恢复按钮
        pause_btn = QPushButton("暂停")
        pause_btn.clicked.connect(lambda: self._on_pause_resume(task_id))
        layout.addWidget(pause_btn)
        
        # 删除按钮
        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(lambda: self._on_delete_task(task_id))
        layout.addWidget(delete_btn)
        
        # 打开文件夹按钮
        open_btn = QPushButton("打开")
        open_btn.clicked.connect(lambda: self._on_open_folder(task_id))
        layout.addWidget(open_btn)
        
        self.download_table.setCellWidget(row, 5, widget)
    
    def _on_pause_resume(self, task_id: str):
        """暂停或恢复任务"""
        task = self.download_manager.get_task(task_id)
        if not task:
            return
        
        if task.status == DownloadStatus.DOWNLOADING:
            self.download_manager.pause_task(task_id)
        elif task.status == DownloadStatus.PAUSED:
            self.download_manager.resume_task(task_id)
    
    def _on_delete_task(self, task_id: str):
        """删除任务"""
        # 显示确认对话框
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, 
            "确认删除",
            "确定要删除此下载任务吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.download_manager.cancel_task(task_id)
            # 从列表中移除
            if task_id in self.task_row_map:
                row = self.task_row_map[task_id]
                self.download_table.removeRow(row)
                # 更新映射
                del self.task_row_map[task_id]
                self._rebuild_row_map()
    
    def _on_open_folder(self, task_id: str):
        """打开文件所在文件夹"""
        import os
        import subprocess
        import platform
        
        task = self.download_manager.get_task(task_id)
        if not task:
            return
        
        if task.status != DownloadStatus.COMPLETED:
            self.statusBar().showMessage("文件尚未下载完成")
            return
        
        file_path = os.path.join(task.save_path, task.filename)
        if not os.path.exists(file_path):
            self.statusBar().showMessage("文件不存在")
            return
        
        # 跨平台打开文件夹
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.run(['explorer', '/select,', file_path])
            elif system == "Darwin":  # macOS
                subprocess.run(['open', '-R', file_path])
            else:  # Linux
                subprocess.run(['xdg-open', task.save_path])
        except Exception as e:
            self.statusBar().showMessage(f"打开文件夹失败: {str(e)}")
    
    def _rebuild_row_map(self):
        """重建任务ID到行号的映射"""
        new_map = {}
        for task_id, old_row in self.task_row_map.items():
            # 查找任务ID对应的新行号
            for row in range(self.download_table.rowCount()):
                # 这里需要在表格中存储task_id，可以使用item的data
                pass
        self.task_row_map = new_map
```

#### 1.4 状态栏信息更新

```python
# src/ui/main_window.py
from PySide6.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        # ... 其他初始化代码 ...
        
        # 创建状态栏更新定时器
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_status_bar)
        self.status_timer.start(1000)  # 每秒更新一次
    
    def _update_status_bar(self):
        """更新状态栏统计信息"""
        stats = self.download_manager.get_statistics()
        
        # 活动任务数
        active_count = stats.get('active_tasks', 0)
        
        # 总下载速度
        total_speed = stats.get('total_speed', 0)
        speed_text = self._format_speed(total_speed)
        
        # 更新状态栏
        message = f"活动任务: {active_count} | 总速度: {speed_text}"
        self.statusBar().showMessage(message)
```

### 2. 设置功能实现

#### 2.1 SettingsDialog完善

```python
# src/ui/settings_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QPushButton, QSpinBox, QFileDialog, QDialogButtonBox
)
from ..utils.config import ConfigManager

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager()
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        self.setWindowTitle("设置")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        # 默认下载路径
        self.download_path_edit = QLineEdit()
        path_btn = QPushButton("浏览...")
        path_btn.clicked.connect(self.browse_download_path)
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.download_path_edit)
        path_layout.addWidget(path_btn)
        form.addRow("默认下载路径:", path_layout)
        
        # 最大并发下载数
        self.max_concurrent_spin = QSpinBox()
        self.max_concurrent_spin.setRange(1, 10)
        self.max_concurrent_spin.setValue(3)
        form.addRow("最大并发下载:", self.max_concurrent_spin)
        
        # 默认线程数
        self.default_threads_spin = QSpinBox()
        self.default_threads_spin.setRange(1, 16)
        self.default_threads_spin.setValue(4)
        form.addRow("默认下载线程数:", self.default_threads_spin)
        
        layout.addLayout(form)
        
        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.save_settings)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def load_settings(self):
        """加载当前设置"""
        download_path = self.config.get('download.default_path', '')
        max_concurrent = self.config.get('download.max_concurrent', 3)
        default_threads = self.config.get('download.default_threads', 4)
        
        self.download_path_edit.setText(download_path)
        self.max_concurrent_spin.setValue(max_concurrent)
        self.default_threads_spin.setValue(default_threads)
    
    def save_settings(self):
        """保存设置"""
        self.config.set('download.default_path', self.download_path_edit.text())
        self.config.set('download.max_concurrent', self.max_concurrent_spin.value())
        self.config.set('download.default_threads', self.default_threads_spin.value())
        self.config.save()
        self.accept()
    
    def browse_download_path(self):
        """浏览选择下载路径"""
        path = QFileDialog.getExistingDirectory(
            self, 
            "选择下载文件夹",
            self.download_path_edit.text()
        )
        if path:
            self.download_path_edit.setText(path)
```

### 3. 数据库设计建议

#### 3.1 数据表结构

```python
# src/database/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class DownloadRecord:
    """下载记录数据模型"""
    id: Optional[int] = None
    task_id: str = ""
    url: str = ""
    filename: str = ""
    save_path: str = ""
    file_size: int = 0
    downloaded_size: int = 0
    status: str = "PENDING"
    num_threads: int = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

# SQL表结构
CREATE_DOWNLOADS_TABLE = """
CREATE TABLE IF NOT EXISTS downloads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT UNIQUE NOT NULL,
    url TEXT NOT NULL,
    filename TEXT NOT NULL,
    save_path TEXT NOT NULL,
    file_size INTEGER DEFAULT 0,
    downloaded_size INTEGER DEFAULT 0,
    status TEXT DEFAULT 'PENDING',
    num_threads INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);
"""

CREATE_SETTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
```

#### 3.2 数据库管理器实现

```python
# src/database/db_manager.py
import sqlite3
from typing import List, Optional
from .models import DownloadRecord, CREATE_DOWNLOADS_TABLE, CREATE_SETTINGS_TABLE

class DatabaseManager:
    def __init__(self, db_path: str = "data/downloads.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(CREATE_DOWNLOADS_TABLE)
            conn.execute(CREATE_SETTINGS_TABLE)
            conn.commit()
    
    def save_download(self, record: DownloadRecord) -> int:
        """保存下载记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT OR REPLACE INTO downloads 
                (task_id, url, filename, save_path, file_size, downloaded_size, 
                 status, num_threads, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.task_id, record.url, record.filename, record.save_path,
                record.file_size, record.downloaded_size, record.status,
                record.num_threads, record.error_message
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_downloads(self) -> List[DownloadRecord]:
        """获取所有下载记录"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM downloads ORDER BY created_at DESC")
            return [self._row_to_record(row) for row in cursor.fetchall()]
    
    def _row_to_record(self, row: sqlite3.Row) -> DownloadRecord:
        """将数据库行转换为记录对象"""
        return DownloadRecord(
            id=row['id'],
            task_id=row['task_id'],
            url=row['url'],
            filename=row['filename'],
            save_path=row['save_path'],
            file_size=row['file_size'],
            downloaded_size=row['downloaded_size'],
            status=row['status'],
            num_threads=row['num_threads'],
            error_message=row['error_message']
        )
```

### 4. 性能优化建议

#### 4.1 内存优化

```python
# 分块读写，避免一次性加载大文件
CHUNK_SIZE = 8192  # 8KB

def download_chunk(url, start, end, output_file):
    """下载文件块（流式处理）"""
    headers = {'Range': f'bytes={start}-{end}'}
    with requests.get(url, headers=headers, stream=True) as response:
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
```

#### 4.2 UI响应优化

```python
# 使用QTimer延迟更新UI，避免频繁刷新
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._pending_updates = {}
        self._update_timer = QTimer()
        self._update_timer.timeout.connect(self._flush_updates)
        self._update_timer.start(100)  # 100ms更新一次
    
    def on_task_progress(self, task_id: str, downloaded: int, speed: float):
        """缓存进度更新"""
        self._pending_updates[task_id] = (downloaded, speed)
    
    def _flush_updates(self):
        """批量更新UI"""
        for task_id, (downloaded, speed) in self._pending_updates.items():
            self._update_task_progress(task_id, downloaded, speed)
        self._pending_updates.clear()
```

### 5. 核心技术选型理由

1. **PySide6**: 官方支持的Qt Python绑定，性能优异，跨平台支持好
2. **requests**: 简单易用的HTTP库，适合同步下载场景
3. **threading**: Python标准库，无需额外依赖，适合CPU密集型任务
4. **SQLite3**: 轻量级数据库，无需额外配置，适合桌面应用
5. **PyYAML**: 人类友好的配置文件格式

### 6. 关键技术实现

#### 多线程下载原理
```python
# 实现流程
1. 发送HEAD请求获取文件大小
2. 检查是否支持Range头
3. 计算分块：chunk_size = file_size // num_threads
4. 为每个线程分配Range: bytes=start-end
5. 并行下载各个块到临时文件
6. 下载完成后合并所有块
7. 校验文件完整性
8. 删除临时文件
```

#### 断点续传实现
```python
# 状态保存格式
{
    "task_id": "uuid",
    "url": "http://example.com/file.zip",
    "total_size": 104857600,
    "downloaded_size": 52428800,
    "status": "PAUSED",
    "temp_files": ["file.part1", "file.part2"]
}

# 恢复时读取状态，从downloaded_size处继续
```

#### 速度限制算法
```python
# 令牌桶算法实现
import time

class SpeedLimiter:
    def __init__(self, rate: int):  # rate: bytes/second
        self.rate = rate
        self.tokens = 0
        self.last_update = time.time()
    
    def consume(self, tokens: int) -> bool:
        """尝试消耗指定数量的令牌"""
        # 更新令牌
        now = time.time()
        elapsed = now - self.last_update
        self.tokens += elapsed * self.rate
        self.tokens = min(self.tokens, self.rate)  # 令牌上限
        self.last_update = now
        
        # 消耗令牌
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def wait_time(self, tokens: int) -> float:
        """计算需要等待的时间"""
        if self.tokens >= tokens:
            return 0
        return (tokens - self.tokens) / self.rate
```

## 依赖清单

### 核心依赖
- PySide6 >= 6.6.0 (UI框架)
- requests >= 2.31.0 (HTTP请求)
- aiohttp >= 3.9.0 (异步HTTP)
- aiofiles >= 23.2.0 (异步文件IO)
- PyYAML >= 6.0 (配置文件)

### 可选依赖
- psutil (系统资源监控)
- cryptography (文件加密)
- qasync (Qt异步集成)

## 里程碑

- **M1**: 完成基础UI和单线程下载 (第1-2周)
- **M2**: 实现多线程下载和断点续传 (第3-4周)
- **M3**: 完成数据持久化和历史记录 (第5周)
- **M4**: 实现高级功能（速度控制、通知等） (第6-7周)
- **M5**: 优化、测试和文档 (第8周)
- **M6**: 发布v1.0版本

## 风险与挑战

1. **网络异常处理**: 各种网络环境下的稳定性
2. **大文件处理**: 内存占用和性能优化
3. **跨平台兼容**: 不同操作系统的文件系统差异
4. **UI响应性**: 避免下载任务阻塞UI线程

## 后续扩展方向

1. 云存储集成（OneDrive、Google Drive等）
2. BT/磁力链接支持
3. 视频嗅探功能
4. FTP/SFTP支持
5. 远程下载（Web界面控制）
6. 插件系统

## 开发规范

### 代码风格
- 遵循PEP 8规范
- 使用类型注解
- 编写文档字符串
- 单元测试覆盖率 > 60%

### Git工作流
- main: 稳定版本分支
- develop: 开发分支
- feature/*: 功能分支
- bugfix/*: 修复分支

### 提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具链
```

## 资源需求

### 开发环境
- Python 3.9+
- PyCharm Professional / VS Code
- Git版本控制
- 虚拟环境管理（venv/conda）

### 测试环境
- Windows 10/11
- macOS 12+
- Ubuntu 20.04+

## 时间估算

总预计开发时间：**8-10周**

- 阶段一：2-3天
- 阶段二：5-7天
- 阶段三：5-7天
- 阶段四：3-4天
- 阶段五：7-10天
- 阶段六：5-7天

*注：以上为全职开发估算，兼职开发时间需相应调整*
