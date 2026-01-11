# PyDownloader 安装指南

## 系统要求

- Python 3.9 或更高版本
- pip 包管理器
- 支持的操作系统：Windows 10+, macOS 12+, Ubuntu 20.04+

## 安装步骤

### 1. 克隆或下载项目

```bash
cd /path/to/your/projects
# 如果使用git
git clone <repository-url>
cd pydownloader
```

### 2. 创建虚拟环境（推荐）

**使用 venv:**
```bash
python3 -m venv venv
```

**激活虚拟环境:**

- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

- Windows:
  ```bash
  venv\Scripts\activate
  ```

### 3. 配置清华源（国内用户推荐）

```bash
# 临时使用清华源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 或永久设置清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 验证安装

```bash
python main.py
```

如果应用成功启动并显示主窗口，说明安装成功！

## 常见问题

### Q1: 安装PySide6时出错

**解决方案:**
- 确保Python版本 >= 3.9
- 更新pip: `pip install --upgrade pip`
- 尝试使用清华源安装

### Q2: 找不到模块错误

**解决方案:**
- 确保在项目根目录运行 `python main.py`
- 检查虚拟环境是否已激活
- 重新安装依赖: `pip install -r requirements.txt`

### Q3: macOS上运行报错

**解决方案:**
- 安装Xcode命令行工具: `xcode-select --install`
- 使用Homebrew安装Python: `brew install python@3.11`

### Q4: Windows上DLL加载错误

**解决方案:**
- 安装Visual C++ Redistributable
- 更新Windows系统
- 使用管理员权限运行

## 开发环境设置

如果你想参与开发，还需要安装开发依赖：

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pytest pytest-qt black flake8
```

## 配置文件

首次运行后，配置文件位于：
- macOS/Linux: `~/.pydownloader/`
- Windows: `C:\Users\<用户名>\.pydownloader\`

你可以编辑 `config/settings.yaml` 来自定义默认设置。

## 卸载

```bash
# 停用虚拟环境
deactivate

# 删除项目目录
rm -rf pydownloader

# 删除配置文件（可选）
rm -rf ~/.pydownloader
```

## 技术支持

如遇问题，请查看：
- [开发计划](DEVELOPMENT_PLAN.md)
- [项目README](README.md)
- 提交Issue到项目仓库
