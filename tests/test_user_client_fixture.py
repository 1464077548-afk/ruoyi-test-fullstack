#!/usr/bin/env python3
"""测试user_client fixture是否正确设置了token"""
import pytest


def test_user_client_auth(user_client):
    """测试user_client是否正确设置了认证"""
    print(f"user_client: {user_client}")
    # 检查是否有Authorization头
    headers = user_client.session.headers
    print(f"user_client headers: {headers}")
    assert 'Authorization' in headers
    assert 'Bearer' in headers['Authorization']
    print("✅ user_client认证设置正确！")


def test_user_client_get_list(user_client):
    """测试user_client是否能正确获取用户列表"""
    print("测试获取用户列表...")
    response = user_client.get_user_list()
    print(f"获取用户列表响应: {response}")
    assert response.get("code") == 200
    print("✅ 用户列表获取成功！")
