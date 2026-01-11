"""
辅助函数模块
提供通用的工具函数
"""

import os
import re
from typing import Tuple
from urllib.parse import urlparse, unquote


def format_size(size_bytes: int) -> str:
    """
    格式化文件大小为可读格式
    
    Args:
        size_bytes: 文件大小（字节）
    
    Returns:
        str: 格式化后的文件大小字符串
    """
    if size_bytes < 0:
        return "未知"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.2f} {units[unit_index]}"


def format_speed(bytes_per_second: float) -> str:
    """
    格式化下载速度
    
    Args:
        bytes_per_second: 每秒字节数
    
    Returns:
        str: 格式化后的速度字符串
    """
    return f"{format_size(int(bytes_per_second))}/s"


def format_time(seconds: int) -> str:
    """
    格式化时间为可读格式
    
    Args:
        seconds: 秒数
    
    Returns:
        str: 格式化后的时间字符串
    """
    if seconds < 0:
        return "未知"
    
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}分{secs}秒"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}小时{minutes}分"


def get_filename_from_url(url: str) -> str:
    """
    从URL中提取文件名
    
    Args:
        url: 下载链接
    
    Returns:
        str: 文件名
    """
    try:
        parsed_url = urlparse(url)
        path = unquote(parsed_url.path)
        filename = os.path.basename(path)
        
        # 如果文件名为空或只有扩展名，使用默认名称
        if not filename or filename.startswith('.'):
            return "download"
        
        return filename
    except Exception:
        return "download"


def get_filename_from_headers(headers: dict) -> str:
    """
    从HTTP响应头中提取文件名
    
    Args:
        headers: HTTP响应头字典
    
    Returns:
        str: 文件名，如果未找到则返回空字符串
    """
    content_disposition = headers.get('Content-Disposition', '')
    if content_disposition:
        # 尝试匹配 filename*=UTF-8''filename 格式
        match = re.search(r"filename\*=UTF-8''(.+?)(?:;|$)", content_disposition)
        if match:
            return unquote(match.group(1))
        
        # 尝试匹配 filename="filename" 或 filename=filename 格式
        match = re.search(r'filename=["\']?([^"\';\n]+)', content_disposition)
        if match:
            return match.group(1).strip()
    
    return ""


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除不合法字符
    
    Args:
        filename: 原始文件名
    
    Returns:
        str: 清理后的文件名
    """
    # 移除或替换不合法字符
    illegal_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(illegal_chars, '_', filename)
    
    # 移除首尾空格和点
    sanitized = sanitized.strip('. ')
    
    # 如果文件名为空，使用默认名称
    if not sanitized:
        sanitized = "download"
    
    return sanitized


def get_unique_filename(directory: str, filename: str) -> str:
    """
    获取唯一的文件名（如果文件已存在，添加序号）
    
    Args:
        directory: 目录路径
        filename: 原始文件名
    
    Returns:
        str: 唯一的文件名
    """
    base_path = os.path.join(directory, filename)
    
    if not os.path.exists(base_path):
        return filename
    
    # 分离文件名和扩展名
    name, ext = os.path.splitext(filename)
    counter = 1
    
    while True:
        new_filename = f"{name} ({counter}){ext}"
        new_path = os.path.join(directory, new_filename)
        if not os.path.exists(new_path):
            return new_filename
        counter += 1


def calculate_chunks(file_size: int, chunk_count: int, min_chunk_size: int = 1048576) -> list:
    """
    计算文件分块信息
    
    Args:
        file_size: 文件总大小
        chunk_count: 期望的分块数量
        min_chunk_size: 最小分块大小（默认1MB）
    
    Returns:
        list: 分块信息列表，每项为(start, end)元组
    """
    if file_size <= 0:
        return []
    
    # 如果文件太小，只使用一个块
    if file_size < min_chunk_size:
        return [(0, file_size - 1)]
    
    # 计算实际分块大小
    chunk_size = file_size // chunk_count
    
    # 如果计算出的分块大小小于最小值，减少分块数量
    if chunk_size < min_chunk_size:
        chunk_count = max(1, file_size // min_chunk_size)
        chunk_size = file_size // chunk_count
    
    chunks = []
    for i in range(chunk_count):
        start = i * chunk_size
        # 最后一块包含所有剩余字节
        end = file_size - 1 if i == chunk_count - 1 else (i + 1) * chunk_size - 1
        chunks.append((start, end))
    
    return chunks


def is_valid_url(url: str) -> bool:
    """
    验证URL是否有效
    
    Args:
        url: URL字符串
    
    Returns:
        bool: URL是否有效
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https', 'ftp']
    except Exception:
        return False


def get_file_extension(filename: str) -> str:
    """
    获取文件扩展名
    
    Args:
        filename: 文件名
    
    Returns:
        str: 文件扩展名（包含点号），如果没有扩展名则返回空字符串
    """
    return os.path.splitext(filename)[1].lower()


def get_mime_type_category(content_type: str) -> str:
    """
    根据Content-Type获取文件类别
    
    Args:
        content_type: HTTP Content-Type头
    
    Returns:
        str: 文件类别（video, audio, image, document, compressed, other）
    """
    if not content_type:
        return "other"
    
    content_type = content_type.lower()
    
    if 'video' in content_type:
        return "video"
    elif 'audio' in content_type:
        return "audio"
    elif 'image' in content_type:
        return "image"
    elif any(x in content_type for x in ['pdf', 'document', 'word', 'excel', 'powerpoint', 'text']):
        return "document"
    elif any(x in content_type for x in ['zip', 'rar', '7z', 'tar', 'gz', 'compressed']):
        return "compressed"
    else:
        return "other"
