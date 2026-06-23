#!/usr/bin/env python3
"""测试fixture是否正常工作"""
import pytest


def test_fixture_chain(get_login_token):
    """测试fixture链是否正常工作"""
    print(f"获取到的token: {get_login_token}")
    assert get_login_token is not None
    assert len(get_login_token) > 0
    print("✅ Fixture链正常工作！")


def test_authenticated_client(authenticated_client):
    """测试已认证的客户端"""
    print(f"已认证客户端: {authenticated_client}")
    # 检查是否有Authorization头
    headers = authenticated_client.session.headers
    print(f"客户端 headers: {headers}")
    assert 'Authorization' in headers
    assert 'Bearer' in headers['Authorization']
    print("✅ 已认证客户端正常！")

def test_config_client(config_client):
    """测试配置客户端"""
    print(f"配置客户端: {config_client}")
    # 检查是否有Authorization头
    headers = config_client.session.headers
    print(f"客户端 headers: {headers}")
    assert 'Authorization' in headers
    assert 'Bearer' in headers['Authorization']
    print("✅ 配置客户端正常！")
