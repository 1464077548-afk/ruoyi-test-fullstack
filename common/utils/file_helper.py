import os
import json
import yaml
import csv
import pickle
from typing import Any, Dict, List, Optional


class FileHelper:
    """文件处理工具类"""
    
    @staticmethod
    def read_file(file_path: str, encoding: str = 'utf-8') -> str:
        """读取文件内容"""
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    
    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> None:
        """写入文件内容"""
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
    
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """读取JSON文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def write_json(file_path: str, data: Any, indent: int = 2) -> None:
        """写入JSON文件"""
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
    
    @staticmethod
    def read_yaml(file_path: str) -> Dict[str, Any]:
        """读取YAML文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def write_yaml(file_path: str, data: Any) -> None:
        """写入YAML文件"""
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    
    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, str]]:
        """读取CSV文件"""
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    @staticmethod
    def write_csv(file_path: str, data: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None) -> None:
        """写入CSV文件"""
        if not data:
            return
        
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if fieldnames is None:
            fieldnames = list(data[0].keys())
        
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    @staticmethod
    def read_pickle(file_path: str) -> Any:
        """读取Pickle文件"""
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    
    @staticmethod
    def write_pickle(file_path: str, data: Any) -> None:
        """写入Pickle文件"""
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """检查文件是否存在"""
        return os.path.exists(file_path)
    
    @staticmethod
    def delete_file(file_path: str) -> None:
        """删除文件"""
        if os.path.exists(file_path):
            os.remove(file_path)
    
    @staticmethod
    def copy_file(src_path: str, dst_path: str) -> None:
        """复制文件"""
        # 确保目标目录存在
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        with open(src_path, 'rb') as src, open(dst_path, 'wb') as dst:
            dst.write(src.read())
    
    @staticmethod
    def move_file(src_path: str, dst_path: str) -> None:
        """移动文件"""
        # 确保目标目录存在
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        os.rename(src_path, dst_path)
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """获取文件大小（字节）"""
        return os.path.getsize(file_path)
    
    @staticmethod
    def get_file_modified_time(file_path: str) -> float:
        """获取文件修改时间"""
        return os.path.getmtime(file_path)
    
    @staticmethod
    def list_files(directory: str, pattern: Optional[str] = None) -> List[str]:
        """列出目录中的文件"""
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if pattern is None or pattern in filename:
                    files.append(os.path.join(root, filename))
        return files
    
    @staticmethod
    def create_directory(directory: str) -> None:
        """创建目录"""
        os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def delete_directory(directory: str) -> None:
        """删除目录"""
        if os.path.exists(directory):
            for root, _, filenames in os.walk(directory, topdown=False):
                for filename in filenames:
                    os.remove(os.path.join(root, filename))
                os.rmdir(root)
