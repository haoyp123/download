# PyDownloader - 开源多线程下载工具

## 项目简介

基于 PySide6 开发的现代化下载管理器，参考 NDM（Neat Download Manager）设计理念，提供高效的多线程下载、断点续传等核心功能。

## 技术栈

- **UI框架**: PySide6 (Qt for Python)
- **网络请求**: aiohttp / requests
- **数据库**: SQLite3
- **配置管理**: PyYAML
- **日志**: logging

## 核心功能

### 第一阶段（MVP）
- [x] 项目结构搭建
- [ ] 基础UI界面（主窗口、下载列表、工具栏）
- [ ] 单线程下载功能
- [ ] 下载进度显示
- [ ] 基础配置管理

### 第二阶段
- [ ] 多线程下载（分块下载）
- [ ] 断点续传
- [ ] 下载队列管理
- [ ] 暂停/恢复/取消功能
- [ ] 速度限制

### 第三阶段
- [ ] 数据库存储（下载历史、配置）
- [ ] 文件分类管理
- [ ] 批量下载
- [ ] 浏览器扩展集成
- [ ] 系统托盘功能

### 第四阶段
- [ ] 高级设置（代理、UA等）
- [ ] 下载完成通知
- [ ] 主题切换（亮色/暗色）
- [ ] 国际化支持

## 项目结构

```
pydownloader/
├── main.py                 # 程序入口
├── requirements.txt        # 依赖列表
├── config/                 # 配置文件
│   └── settings.yaml
├── src/
│   ├── __init__.py
│   ├── ui/                 # UI界面
│   │   ├── __init__.py
│   │   ├── main_window.py  # 主窗口
│   │   ├── download_item.py # 下载项组件
│   │   ├── settings_dialog.py # 设置对话框
│   │   └── add_download_dialog.py # 添加下载对话框
│   ├── core/               # 核心功能
│   │   ├── __init__.py
│   │   ├── downloader.py   # 下载器核心
│   │   ├── download_task.py # 下载任务
│   │   ├── thread_pool.py  # 线程池管理
│   │   └── file_manager.py # 文件管理
│   ├── database/           # 数据库
│   │   ├── __init__.py
│   │   ├── db_manager.py   # 数据库管理
│   │   └── models.py       # 数据模型
│   └── utils/              # 工具类
│       ├── __init__.py
│       ├── config.py       # 配置管理
│       ├── logger.py       # 日志
│       └── helpers.py      # 辅助函数
├── resources/              # 资源文件
│   ├── icons/              # 图标
│   └── styles/             # 样式表
└── tests/                  # 测试
    └── __init__.py
```

## 安装依赖

使用清华源安装依赖：

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

## 开发进度

详见 [开发计划文档](DEVELOPMENT_PLAN.md)

## 许可证

MIT License
