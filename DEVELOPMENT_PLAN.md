# PyDownloader 开发计划

## 项目概述

开发一个功能完善的多线程下载管理器，核心参考 NDM（Neat Download Manager）的设计理念，使用 PySide6 构建现代化的桌面应用。

## 开发阶段详细规划

### 阶段一：项目基础搭建 (预计2-3天)

#### 1.1 环境准备
- [x] 创建项目目录结构
- [ ] 配置虚拟环境
- [ ] 安装基础依赖（使用清华源）
  ```bash
  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
  pip install PySide6 requests PyYAML aiohttp aiofiles
  ```

#### 1.2 项目框架
- [ ] 创建主程序入口 `main.py`
- [ ] 设计配置文件结构 `config/settings.yaml`
- [ ] 实现配置管理模块 `utils/config.py`
- [ ] 实现日志模块 `utils/logger.py`
- [ ] 实现辅助函数 `utils/helpers.py`

#### 1.3 基础UI框架
- [ ] 创建主窗口类 `ui/main_window.py`
  - 菜单栏（文件、编辑、视图、帮助）
  - 工具栏（添加、暂停、恢复、删除）
  - 状态栏（下载统计、速度显示）
  - 主界面布局（下载列表区域）
- [ ] 创建添加下载对话框 `ui/add_download_dialog.py`
  - URL输入框
  - 保存路径选择
  - 文件名设置
  - 线程数选择
- [ ] 创建设置对话框 `ui/settings_dialog.py`
  - 常规设置（默认下载路径、最大同时下载数）
  - 网络设置（代理、超时时间）
  - 外观设置（主题选择）

### 阶段二：核心下载功能 (预计5-7天)

#### 2.1 下载任务模型
- [ ] 创建下载任务类 `core/download_task.py`
  - 任务状态枚举（等待、下载中、暂停、完成、失败）
  - 任务信息（URL、文件名、大小、进度、速度）
  - 任务控制方法（开始、暂停、恢复、取消）

#### 2.2 单线程下载器
- [ ] 实现基础下载器 `core/downloader.py`
  - HTTP请求处理
  - 响应头解析（Content-Length、Content-Type、支持断点续传检测）
  - 文件写入
  - 进度回调
  - 异常处理

#### 2.3 下载项UI组件
- [ ] 创建下载项组件 `ui/download_item.py`
  - 文件图标和名称显示
  - 进度条
  - 速度和剩余时间显示
  - 操作按钮（暂停、恢复、打开文件夹）
  - 右键菜单（重新下载、删除、属性）

#### 2.4 下载管理器
- [ ] 实现下载管理器逻辑
  - 下载队列管理
  - 最大并发控制
  - 任务调度
  - 事件通知机制

### 阶段三：多线程下载与断点续传 (预计5-7天)

#### 3.1 分块下载策略
- [ ] 实现文件分块算法
  - 根据文件大小计算分块数
  - 每块大小计算（考虑Range头支持）
  - 块索引管理

#### 3.2 线程池管理
- [ ] 创建线程池 `core/thread_pool.py`
  - 工作线程管理
  - 任务分配
  - 线程同步
  - 资源清理

#### 3.3 断点续传
- [ ] 实现断点续传机制
  - 下载状态持久化（JSON/SQLite）
  - 已下载块记录
  - 恢复下载逻辑
  - 临时文件管理（.tmp后缀）

#### 3.4 文件合并
- [ ] 实现文件合并逻辑 `core/file_manager.py`
  - 块文件合并
  - 文件完整性校验（MD5/SHA256可选）
  - 临时文件清理

### 阶段四：数据持久化 (预计3-4天)

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

## 技术要点

### 核心技术选型理由

1. **PySide6**: 官方支持的Qt Python绑定，性能优异，跨平台支持好
2. **aiohttp**: 高性能异步HTTP客户端，支持并发下载
3. **SQLite3**: 轻量级数据库，无需额外配置，适合桌面应用
4. **PyYAML**: 人类友好的配置文件格式

### 关键技术实现

#### 多线程下载原理
```python
# 伪代码示例
1. 发送HEAD请求获取文件大小
2. 检查是否支持Range头
3. 计算分块：chunk_size = file_size / thread_count
4. 为每个线程分配Range: bytes=start-end
5. 并行下载各个块到临时文件
6. 下载完成后合并所有块
7. 校验文件完整性
8. 删除临时文件
```

#### 断点续传实现
```python
# 保存下载状态
{
    "url": "http://example.com/file.zip",
    "total_size": 104857600,
    "downloaded_chunks": [
        {"index": 0, "start": 0, "end": 1048576, "completed": true},
        {"index": 1, "start": 1048576, "end": 2097152, "completed": false}
    ]
}

# 恢复时读取状态，跳过已完成的块
```

#### 速度限制算法
```python
# 令牌桶算法
class SpeedLimiter:
    def __init__(self, rate):  # rate: bytes/second
        self.rate = rate
        self.tokens = 0
        self.last_update = time.time()
    
    def consume(self, tokens):
        # 更新令牌
        now = time.time()
        self.tokens += (now - self.last_update) * self.rate
        self.tokens = min(self.tokens, self.rate)
        self.last_update = now
        
        # 消耗令牌
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
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
