import hashlib
import base64
import hmac
from cryptography.fernet import Fernet


class Crypto:
    """加密工具类"""
    
    @staticmethod
    def md5_hash(text):
        """MD5加密"""
        if isinstance(text, str):
            text = text.encode('utf-8')
        return hashlib.md5(text).hexdigest()
    
    @staticmethod
    def sha256_hash(text):
        """SHA256加密"""
        if isinstance(text, str):
            text = text.encode('utf-8')
        return hashlib.sha256(text).hexdigest()
    
    @staticmethod
    def base64_encode(text):
        """Base64编码"""
        if isinstance(text, str):
            text = text.encode('utf-8')
        return base64.b64encode(text).decode('utf-8')
    
    @staticmethod
    def base64_decode(encoded_text):
        """Base64解码"""
        if isinstance(encoded_text, str):
            encoded_text = encoded_text.encode('utf-8')
        return base64.b64decode(encoded_text).decode('utf-8')
    
    @staticmethod
    def hmac_sign(message, secret):
        """HMAC签名"""
        if isinstance(message, str):
            message = message.encode('utf-8')
        if isinstance(secret, str):
            secret = secret.encode('utf-8')
        return hmac.new(secret, message, hashlib.sha256).hexdigest()
    
    class AESCipher:
        """AES加密解密类"""
        
        def __init__(self, key):
            """初始化密钥"""
            if len(key) < 32:
                key = key.ljust(32, '0')[:32]
            self.key = key.encode('utf-8')
            self.fernet = Fernet(base64.urlsafe_b64encode(self.key))
        
        def encrypt(self, text):
            """加密"""
            if isinstance(text, str):
                text = text.encode('utf-8')
            return self.fernet.encrypt(text).decode('utf-8')
        
        def decrypt(self, encrypted_text):
            """解密"""
            if isinstance(encrypted_text, str):
                encrypted_text = encrypted_text.encode('utf-8')
            return self.fernet.decrypt(encrypted_text).decode('utf-8')
    
    @staticmethod
    def generate_key():
        """生成加密密钥"""
        return Fernet.generate_key().decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """验证密码"""
        # 这里假设hashed_password是使用sha256加密的
        return Crypto.sha256_hash(plain_password) == hashed_password
    
    @staticmethod
    def hash_password(password):
        """密码加密"""
        return Crypto.sha256_hash(password)
