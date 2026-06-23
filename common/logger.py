import logging
import os
import sys
from config.settings import settings

# 标准输出流强制utf8
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


class Logger:
    """日志工具类"""
    
    def __init__(self, name=__name__):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        
        # 检查是否已经有处理器，避免重复添加
        if not self.logger.handlers:
            # 创建日志目录
            log_dir = os.path.join(settings.REPORT_DIR, 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            # 创建文件处理器
            log_file = os.path.join(log_dir, 'test.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            
            # 设置日志格式
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # 添加处理器
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def debug(self, message):
        """调试级别日志"""
        self.logger.debug(message)
    
    def info(self, message):
        """信息级别日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """警告级别日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """错误级别日志"""
        self.logger.error(message)
    
    def critical(self, message):
        """严重错误级别日志"""
        self.logger.critical(message)

# 全局日志实例
logger = Logger()

def get_logger(name=None):
    """获取全局日志实例"""
    return logger