# 图标使用指南

## 概述

本项目使用 `IconManager` 类统一管理所有图标资源。该系统支持SVG图标和Qt标准图标的混合使用，提供了灵活的图标管理方案。

## IconManager 功能

### 1. 基础图标获取

```python
from src.utils.icon_manager import IconManager

# 获取标准图标
icon = IconManager.get_icon("add")        # 添加按钮图标
icon = IconManager.get_icon("settings")   # 设置图标
icon = IconManager.get_icon("folder")     # 文件夹图标
```

支持的图标名称：
- `add` - 添加/新建
- `remove`/`delete` - 删除
- `start` - 开始/播放
- `pause` - 暂停
- `stop` - 停止
- `settings` - 设置
- `folder` - 文件夹
- `file` - 文件
- `download` - 下载
- `clear` - 清除
- `list` - 列表
- `help` - 帮助
- `exit` - 退出

### 2. 状态图标

```python
# 获取不同状态的图标（带颜色）
downloading_icon = IconManager.get_status_icon("downloading")  # 蓝色
completed_icon = IconManager.get_status_icon("completed")      # 绿色
failed_icon = IconManager.get_status_icon("failed")           # 红色
paused_icon = IconManager.get_status_icon("paused")           # 橙色
pending_icon = IconManager.get_status_icon("pending")         # 灰色
```

### 3. 文件类型图标

```python
# 根据文件名自动获取对应的文件类型图标
video_icon = IconManager.get_file_type_icon("movie.mp4")      # 紫色视频图标
audio_icon = IconManager.get_file_type_icon("song.mp3")       # 橙色音频图标
image_icon = IconManager.get_file_type_icon("photo.jpg")      # 绿色图片图标
doc_icon = IconManager.get_file_type_icon("report.pdf")       # 红色文档图标
archive_icon = IconManager.get_file_type_icon("data.zip")     # 黄色压缩包图标
code_icon = IconManager.get_file_type_icon("script.py")       # 蓝色代码图标
```

### 4. 自定义颜色图标

```python
# 为图标指定自定义颜色
red_icon = IconManager.get_icon("circle", color="#FF0000")
blue_icon = IconManager.get_icon("square", color="#0000FF")
```

### 5. 简单几何图标

```python
# 创建程序绘制的简单图标
circle = IconManager.create_simple_icon("circle", "#3498db", 32)
square = IconManager.create_simple_icon("square", "#e74c3c", 32)
arrow = IconManager.create_simple_icon("download_arrow", "#2ecc71", 32)
check = IconManager.create_simple_icon("check", "#27ae60", 32)
cross = IconManager.create_simple_icon("cross", "#c0392b", 32)
pause = IconManager.create_simple_icon("pause", "#f39c12", 32)
```

## 在UI组件中使用

### 在QAction中使用

```python
from PySide6.QtGui import QAction
from src.utils.icon_manager import IconManager

# 创建带图标的动作
add_action = QAction(IconManager.get_icon("add"), "添加下载", self)
settings_action = QAction(IconManager.get_icon("settings"), "设置", self)
```

### 在QPushButton中使用

```python
from PySide6.QtWidgets import QPushButton
from src.utils.icon_manager import IconManager

# 创建带图标的按钮
start_button = QPushButton(IconManager.get_icon("start"), "开始")
pause_button = QPushButton(IconManager.get_icon("pause"), "暂停")
```

### 在QLabel中显示图标

```python
from PySide6.QtWidgets import QLabel
from src.utils.icon_manager import IconManager

# 在标签中显示图标
icon_label = QLabel()
icon = IconManager.get_status_icon("downloading")
icon_label.setPixmap(icon.pixmap(16, 16))  # 16x16像素
```

## 图标缓存

IconManager 内置了图标缓存机制，相同名称和颜色的图标只会创建一次，提升性能。

## 添加自定义SVG图标

1. 将SVG文件放入 `resources/icons/` 目录
2. 文件命名遵循规范（如：`icon_add.svg`, `icon_download.svg`）
3. 使用时直接通过名称引用（不带 `icon_` 前缀和 `.svg` 后缀）

```python
# 假设有文件 resources/icons/icon_custom.svg
icon = IconManager.get_icon("custom")
```

## 后备机制

如果指定的SVG图标文件不存在，IconManager会自动降级使用Qt标准图标，确保应用始终能正常显示图标。

## 从Iconfont下载图标

如需从Iconfont网站下载新图标：

1. 访问 [iconfont.cn](https://www.iconfont.cn/)
2. 搜索并选择所需图标
3. 下载SVG格式
4. 重命名为 `icon_[名称].svg` 格式
5. 放入 `resources/icons/` 目录
6. 在代码中使用 `IconManager.get_icon("[名称]")`

## 注意事项

- SVG文件应使用单色设计，以便支持动态着色
- 图标尺寸建议为24x24或32x32像素
- 使用缓存机制时，相同参数的图标会返回同一实例
- 状态图标的颜色是预定义的，符合UI设计规范
