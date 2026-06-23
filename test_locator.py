#!/usr/bin/env python3
"""
测试定位器配置是否正确加载
"""

import sys
sys.path.append('.')

from config.locator_map import LocatorMap

# 初始化定位器映射
locator_map = LocatorMap()

# 测试获取 home.user_info 定位器
print("测试获取 home.user_info 定位器...")
locator_info = locator_map.get_locator_info("home.user_info")
if locator_info:
    print(f"✅ 成功获取 home.user_info 定位器:")
    print(f"   策略: {locator_info['strategy']}")
    print(f"   值: {locator_info['value']}")
    print(f"   选项: {locator_info['options']}")
    print(f"   描述: {locator_info['description']}")
else:
    print("❌ 无法获取 home.user_info 定位器")

# 测试获取 home.logout_button 定位器
print("\n测试获取 home.logout_button 定位器...")
locator_info = locator_map.get_locator_info("home.logout_button")
if locator_info:
    print(f"✅ 成功获取 home.logout_button 定位器:")
    print(f"   策略: {locator_info['strategy']}")
    print(f"   值: {locator_info['value']}")
    print(f"   选项: {locator_info['options']}")
    print(f"   描述: {locator_info['description']}")
else:
    print("❌ 无法获取 home.logout_button 定位器")

# 测试获取 login.username_input 定位器
print("\n测试获取 login.username_input 定位器...")
locator_info = locator_map.get_locator_info("login.username_input")
if locator_info:
    print(f"✅ 成功获取 login.username_input 定位器:")
    print(f"   策略: {locator_info['strategy']}")
    print(f"   值: {locator_info['value']}")
    print(f"   选项: {locator_info['options']}")
    print(f"   描述: {locator_info['description']}")
else:
    print("❌ 无法获取 login.username_input 定位器")

# 打印所有定位器
print("\n所有定位器配置:")
all_locators = locator_map.get_all_locators()
print(f"顶层键: {list(all_locators.keys())}")

# 检查是否存在 home 模块
if 'home' in all_locators:
    print("\nhome 模块中的定位器:")
    print(f"home 模块中的键: {list(all_locators['home'].keys())}")
else:
    print("\n❌ 不存在 home 模块")
