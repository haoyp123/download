"""
PyDownloader - 开源多线程下载工具
主程序入口
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from src.utils.config import get_config
from src.utils.logger import get_logger
from src.ui.main_window import MainWindow


def main():
    """主函数"""
    # 初始化配置
    config = get_config()
    
    # 初始化日志
    logger = get_logger()
    logger.info("=" * 50)
    logger.info("PyDownloader 启动")
    logger.info("=" * 50)
    
    # 创建Qt应用
    app = QApplication(sys.argv)
    app.setApplicationName("PyDownloader")
    app.setOrganizationName("PyDownloader")
    
    # 设置高DPI支持
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    try:
        # 创建并显示主窗口
        window = MainWindow()
        window.show()
        
        logger.info("主窗口已创建并显示")
        
        # 运行应用
        exit_code = app.exec()
        
        logger.info(f"应用退出，退出码: {exit_code}")
        sys.exit(exit_code)
        
    except Exception as e:
        logger.exception(f"应用运行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
