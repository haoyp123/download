"""
图标管理器模块
提供统一的图标访问接口
"""
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtWidgets import QStyle, QApplication
from PySide6.QtCore import Qt, QSize
import os
from typing import Optional


class IconManager:
    """图标管理器类"""
    
    # 图标缓存
    _icon_cache = {}
    
    # 图标根目录
    ICON_DIR = "resources/icons"
    
    @classmethod
    def get_icon(cls, name: str, color: Optional[str] = None) -> QIcon:
        """
        获取图标
        
        Args:
            name: 图标名称
            color: 图标颜色（十六进制，如 "#3B82FE"）
            
        Returns:
            QIcon对象
        """
        cache_key = f"{name}_{color}" if color else name
        
        # 检查缓存
        if cache_key in cls._icon_cache:
            return cls._icon_cache[cache_key]
        
        # 尝试从文件加载
        icon_path = os.path.join(cls.ICON_DIR, f"{name}.svg")
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            if color:
                icon = cls._colorize_icon(icon, color)
            cls._icon_cache[cache_key] = icon
            return icon
        
        # 使用Qt标准图标作为后备
        icon = cls._get_standard_icon(name)
        if color:
            icon = cls._colorize_icon(icon, color)
        
        cls._icon_cache[cache_key] = icon
        return icon
    
    @classmethod
    def _get_standard_icon(cls, name: str) -> QIcon:
        """
        获取Qt标准图标
        
        Args:
            name: 图标名称
            
        Returns:
            QIcon对象
        """
        style = QApplication.style()
        
        # 图标名称映射
        icon_map = {
            # 文件和文件夹
            'file': QStyle.SP_FileIcon,
            'folder': QStyle.SP_DirIcon,
            'open_folder': QStyle.SP_DirOpenIcon,
            
            # 控制按钮
            'add': QStyle.SP_FileDialogNewFolder,
            'delete': QStyle.SP_TrashIcon,
            'refresh': QStyle.SP_BrowserReload,
            
            # 对话框图标
            'info': QStyle.SP_MessageBoxInformation,
            'warning': QStyle.SP_MessageBoxWarning,
            'error': QStyle.SP_MessageBoxCritical,
            'question': QStyle.SP_MessageBoxQuestion,
            
            # 导航
            'up': QStyle.SP_ArrowUp,
            'down': QStyle.SP_ArrowDown,
            'left': QStyle.SP_ArrowLeft,
            'right': QStyle.SP_ArrowRight,
            
            # 媒体控制
            'play': QStyle.SP_MediaPlay,
            'pause': QStyle.SP_MediaPause,
            'stop': QStyle.SP_MediaStop,
            
            # 其他
            'settings': QStyle.SP_FileDialogDetailedView,
            'help': QStyle.SP_DialogHelpButton,
            'close': QStyle.SP_DialogCloseButton,
        }
        
        standard_pixmap = icon_map.get(name, QStyle.SP_FileIcon)
        return style.standardIcon(standard_pixmap)
    
    @classmethod
    def _colorize_icon(cls, icon: QIcon, color: str) -> QIcon:
        """
        为图标着色
        
        Args:
            icon: 原始图标
            color: 目标颜色
            
        Returns:
            着色后的图标
        """
        pixmap = icon.pixmap(QSize(64, 64))
        
        # 创建新的pixmap
        colored_pixmap = QPixmap(pixmap.size())
        colored_pixmap.fill(Qt.transparent)
        
        # 绘制着色后的图标
        painter = QPainter(colored_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(colored_pixmap.rect(), QColor(color))
        painter.end()
        
        return QIcon(colored_pixmap)
    
    @classmethod
    def create_simple_icon(cls, shape: str, color: str = "#000000", size: int = 64) -> QIcon:
        """
        创建简单的几何图标
        
        Args:
            shape: 形状类型 ('circle', 'square', 'triangle', 'download_arrow', 'check', 'cross')
            color: 颜色
            size: 尺寸
            
        Returns:
            QIcon对象
        """
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(color))
        
        if shape == 'circle':
            painter.drawEllipse(4, 4, size-8, size-8)
        elif shape == 'square':
            painter.drawRect(4, 4, size-8, size-8)
        elif shape == 'download_arrow':
            # 绘制下载箭头
            painter.setPen(QColor(color))
            painter.setPen(Qt.SolidLine)
            pen = painter.pen()
            pen.setWidth(3)
            painter.setPen(pen)
            
            # 箭头主体
            center_x = size // 2
            painter.drawLine(center_x, 10, center_x, size - 20)
            
            # 箭头头部
            arrow_size = 10
            painter.drawLine(center_x, size - 20, center_x - arrow_size, size - 20 - arrow_size)
            painter.drawLine(center_x, size - 20, center_x + arrow_size, size - 20 - arrow_size)
        elif shape == 'check':
            # 绘制勾选标记
            painter.setPen(QColor(color))
            pen = painter.pen()
            pen.setWidth(4)
            painter.setPen(pen)
            
            painter.drawLine(size//4, size//2, size//2, size*3//4)
            painter.drawLine(size//2, size*3//4, size*3//4, size//4)
        elif shape == 'cross':
            # 绘制叉号
            painter.setPen(QColor(color))
            pen = painter.pen()
            pen.setWidth(4)
            painter.setPen(pen)
            
            margin = size // 4
            painter.drawLine(margin, margin, size-margin, size-margin)
            painter.drawLine(size-margin, margin, margin, size-margin)
        elif shape == 'pause':
            # 绘制暂停标记（两个竖条）
            bar_width = size // 6
            margin = size // 4
            painter.drawRect(margin, margin, bar_width, size - 2*margin)
            painter.drawRect(size - margin - bar_width, margin, bar_width, size - 2*margin)
        
        painter.end()
        
        return QIcon(pixmap)
    
    @classmethod
    def get_file_type_icon(cls, filename: str) -> QIcon:
        """
        根据文件名获取文件类型图标
        
        Args:
            filename: 文件名
            
        Returns:
            QIcon对象
        """
        ext = os.path.splitext(filename)[1].lower()
        
        # 视频文件
        video_exts = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm', '.m4v']
        if ext in video_exts:
            return cls.create_simple_icon('square', '#EF4444')  # 红色
        
        # 音频文件
        audio_exts = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a']
        if ext in audio_exts:
            return cls.create_simple_icon('circle', '#8B5CF6')  # 紫色
        
        # 图片文件
        image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico']
        if ext in image_exts:
            return cls.create_simple_icon('square', '#10B981')  # 绿色
        
        # 压缩文件
        archive_exts = ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz']
        if ext in archive_exts:
            return cls.create_simple_icon('square', '#F59E0B')  # 橙色
        
        # 文档文件
        doc_exts = ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt']
        if ext in doc_exts:
            return cls.create_simple_icon('square', '#3B82F6')  # 蓝色
        
        # 默认文件图标
        return cls.get_icon('file')
    
    @classmethod
    def get_status_icon(cls, status: str) -> QIcon:
        """
        获取状态图标
        
        Args:
            status: 状态名称 ('downloading', 'completed', 'failed', 'paused', 'pending')
            
        Returns:
            QIcon对象
        """
        status_map = {
            'downloading': ('download_arrow', '#3B82FE'),  # 蓝色
            'completed': ('check', '#10B981'),              # 绿色
            'failed': ('cross', '#EF4444'),                 # 红色
            'paused': ('pause', '#F59E0B'),                 # 橙色
            'pending': ('circle', '#9CA3AF'),               # 灰色
            'cancelled': ('cross', '#6B7280'),              # 深灰色
        }
        
        if status in status_map:
            shape, color = status_map[status]
            return cls.create_simple_icon(shape, color, 32)
        
        return cls.get_icon('file')
    
    @classmethod
    def clear_cache(cls):
        """清除图标缓存"""
        cls._icon_cache.clear()


# 便捷函数
def get_icon(name: str, color: Optional[str] = None) -> QIcon:
    """获取图标的便捷函数"""
    return IconManager.get_icon(name, color)


def get_file_icon(filename: str) -> QIcon:
    """获取文件类型图标的便捷函数"""
    return IconManager.get_file_type_icon(filename)


def get_status_icon(status: str) -> QIcon:
    """获取状态图标的便捷函数"""
    return IconManager.get_status_icon(status)
