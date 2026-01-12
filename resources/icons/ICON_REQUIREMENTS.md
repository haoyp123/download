# 项目图标需求清单

## 概述
本文档列出了PyDownloader项目所需的所有图标及其用途。

## 图标需求列表

### 主要功能图标

#### 1. 下载相关图标
- **添加下载** (add_download.svg)
  - 用途：工具栏"添加下载"按钮
  - 建议：加号+下载箭头组合图标
  - Iconfont搜索关键词：添加下载、add download

- **下载中** (downloading.svg)
  - 用途：任务状态显示
  - 建议：带有动画效果的下载箭头
  - Iconfont搜索关键词：下载

- **下载完成** (completed.svg)
  - 用途：已完成任务状态图标
  - 建议：勾选标记或完成图标
  - Iconfont搜索关键词：完成、成功

- **下载失败** (failed.svg)
  - 用途：失败任务状态图标
  - 建议：叉号或警告图标
  - Iconfont搜索关键词：错误、失败

#### 2. 控制按钮图标
- **暂停** (pause.svg)
  - 用途：暂停下载按钮
  - 建议：双竖线暂停图标
  - Iconfont搜索关键词：暂停

- **恢复/继续** (resume.svg)
  - 用途：恢复下载按钮
  - 建议：播放/开始图标
  - Iconfont搜索关键词：播放、开始

- **停止/取消** (stop.svg)
  - 用途：取消下载按钮
  - 建议：方形停止图标或叉号
  - Iconfont搜索关键词：停止、取消

- **删除** (delete.svg)
  - 用途：删除任务按钮
  - 建议：垃圾桶图标
  - Iconfont搜索关键词：删除、垃圾桶

#### 3. 导航和工具图标
- **设置** (settings.svg)
  - 用途：设置按钮
  - 建议：齿轮图标
  - Iconfont搜索关键词：设置、齿轮

- **文件夹** (folder.svg)
  - 用途：打开文件夹按钮
  - 建议：文件夹图标
  - Iconfont搜索关键词：文件夹

- **刷新** (refresh.svg)
  - 用途：刷新列表按钮
  - 建议：循环箭头
  - Iconfont搜索关键词：刷新

#### 4. 文件类型图标
- **通用文件** (file.svg)
  - 用途：默认文件图标
  - Iconfont搜索关键词：文件

- **视频文件** (video.svg)
  - 用途：视频文件图标
  - Iconfont搜索关键词：视频

- **音频文件** (audio.svg)
  - 用途：音频文件图标
  - Iconfont搜索关键词：音频、音乐

- **图片文件** (image.svg)
  - 用途：图片文件图标
  - Iconfont搜索关键词：图片

- **压缩文件** (archive.svg)
  - 用途：压缩包图标
  - Iconfont搜索关键词：压缩、zip

- **文档文件** (document.svg)
  - 用途：文档文件图标
  - Iconfont搜索关键词：文档

#### 5. 状态和提示图标
- **信息** (info.svg)
  - 用途：信息提示
  - Iconfont搜索关键词：信息

- **警告** (warning.svg)
  - 用途：警告提示
  - Iconfont搜索关键词：警告

- **帮助** (help.svg)
  - 用途：帮助按钮
  - Iconfont搜索关键词：帮助、问号

#### 6. 应用程序图标
- **应用Logo** (app_icon.svg / app_icon.png)
  - 用途：应用程序图标
  - 尺寸要求：16x16, 32x32, 64x64, 128x128, 256x256
  - 建议：下载箭头+简洁设计

## 从Iconfont下载图标步骤

### 方法一：逐个下载（推荐用于精选图标）
1. 访问 https://www.iconfont.cn
2. 在搜索框输入对应的关键词（如"下载"）
3. 浏览图标，找到合适的设计
4. 点击图标，然后点击"下载"按钮
5. 选择SVG格式下载
6. 将下载的SVG文件重命名并放入 `resources/icons/` 目录

### 方法二：创建项目批量下载（推荐用于系统性管理）
1. 在Iconfont网站注册/登录账号
2. 创建新项目（项目名：PyDownloader）
3. 搜索并收藏所需图标到项目
4. 在项目页面点击"下载至本地"
5. 选择格式：SVG
6. 解压后将图标文件复制到 `resources/icons/` 目录

### 方法三：使用IconFont字体（适合大量图标）
1. 在Iconfont创建项目并添加图标
2. 选择"Font class"方式
3. 下载生成的CSS和字体文件
4. 在项目中引入IconFont

## 图标使用规范

### 文件命名规范
- 使用小写字母和下划线
- 示例：`add_download.svg`, `pause_button.svg`

### 图标尺寸
- 工具栏图标：24x24px
- 按钮图标：20x20px  
- 状态图标：16x16px
- 文件类型图标：32x32px

### 颜色规范
- 使用单色SVG（黑色）
- 在代码中通过QIcon的setColor动态设置颜色
- 主题色：#3B82FE（蓝色）
- 危险色：#EF4444（红色）
- 成功色：#10B981（绿色）
- 警告色：#F59E0B（橙色）

## 当前状态
- [ ] 下载所需图标
- [ ] 整理图标到icons目录
- [ ] 在代码中集成图标
- [ ] 测试图标显示效果

## 备选方案
如果不方便从Iconfont下载，可以考虑：
1. 使用Qt内置图标：QStyle.StandardPixmap
2. 使用开源图标库：Material Icons, Font Awesome
3. 手动绘制简单图标：使用QPainter
