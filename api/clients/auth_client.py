from typing import Dict, Any
from api.clients.base_client import BaseClient
from api.models.user import UserInfoResponse


class AuthClient(BaseClient):
    """认证API客户端"""
    
    def get_captcha(self) -> Dict[str, Any]:
        """获取验证码"""
        endpoint = "/captchaImage"
        response = self.get(endpoint)
        # self.logger.debug(f"验证码接口响应: {response}")
        return response
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """登录接口"""
        captcha_response = self.get_captcha()
        if captcha_response.get("code") != 200:
            raise Exception(f"获取验证码失败: {captcha_response.get('msg')}")
        
        captcha_enabled = captcha_response.get("captchaEnabled", True)
        
        endpoint = "/login"
        data = {
            "username": username,
            "password": password
        }
        
        if captcha_enabled:
            captcha = "1234"
            uuid = captcha_response.get("uuid")
            data["captcha"] = captcha
            data["uuid"] = uuid
        
        response = self.post(endpoint, data)
        # 确保响应格式一致，将token放入data字段
        if "token" in response and "data" not in response:
            response["data"] = {"token": response["token"]}
            token = response["token"]
        elif "data" in response and "token" in response["data"]:
            token = response["data"]["token"]
        else:
            # 响应格式错误，打印详细信息
            print(f"登录响应格式错误: {response}")
            return response
        
        # 登录成功后自动保存token到会话头
        self.set_token(token)
        return response
    
    def logout(self) -> Dict[str, Any]:
        """登出接口"""
        endpoint = "/logout"
        return self.post(endpoint)
    
    def get_user_info(self) -> Dict[str, Any]:
        """获取用户信息"""
        endpoint = "/getInfo"
        response = self.get(endpoint)
        print(f"获取用户信息接口响应: {response}")
        return self.validate_response(response, UserInfoResponse)
    
    def refresh_token(self) -> Dict[str, Any]:
        """刷新令牌"""
        endpoint = "/refresh"
        return self.post(endpoint)
    
    def send_verification_code(self, email: str) -> Dict[str, Any]:
        """发送验证码"""
        endpoint = "/sendCode"
        data = {
            "email": email
        }
        return self.post(endpoint, data)
    
    def reset_password(self, email: str, code: str, new_password: str) -> Dict[str, Any]:
        """重置密码"""
        endpoint = "/resetPassword"
        data = {
            "email": email,
            "code": code,
            "newPassword": new_password
        }
        return self.post(endpoint, data)
