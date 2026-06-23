#!/usr/bin/env python3
"""
测试数据清理工具

提供命令行接口来清理测试数据
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from common.utils.db_helper import DBHelper
from common.logger import Logger

# 配置日志
logger = Logger(__name__)


def setup_logging(verbose: bool = False):
    """配置日志级别"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def print_cleanup_report(results: dict):
    """打印清理报告"""
    print("\n" + "=" * 60)
    print("测试数据清理报告")
    print("=" * 60)
    
    if results['dry_run']:
        print("⚠️  试运行模式 - 未实际删除数据")
    else:
        print("✅ 实际删除模式")
    
    print(f"\n总表数: {results['total_tables']}")
    print(f"已清理表数: {results['cleaned_tables']}")
    print(f"总记录数: {results['total_records']}")
    
    if results['details']:
        print("\n详细信息:")
        print("-" * 60)
        for detail in results['details']:
            if 'error' in detail:
                print(f"❌ {detail['table']} ({detail['description']}): 错误 - {detail['error']}")
            else:
                print(f"✅ {detail['table']} ({detail['description']}): {detail['count']} 条记录")
    else:
        print("\n✅ 没有需要清理的测试数据")
    
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='测试数据清理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查看有多少测试数据（试运行）
  python tools/data_cleanup.py --dry-run
  
  # 清理所有测试数据
  python tools/data_cleanup.py
  
  # 只清理指定表
  python tools/data_cleanup.py --tables sys_user,sys_role
  
  # 查看帮助
  python tools/data_cleanup.py --help
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='试运行，只统计不删除'
    )
    
    parser.add_argument(
        '--tables',
        type=str,
        help='指定要清理的表，多个表用逗号分隔（如：sys_user,sys_role）'
    )
    
    parser.add_argument(
        '--list-tables',
        action='store_true',
        help='列出所有可清理的表'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='显示详细日志'
    )
    
    parser.add_argument(
        '--confirm',
        '-y',
        action='store_true',
        help='跳过确认，直接执行'
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    
    # 列出可清理的表
    if args.list_tables:
        print("\n可清理的表:")
        print("-" * 40)
        for table, config in DBHelper.CLEANUP_CONFIG.items():
            print(f"  - {table}: {config['description']}")
        print()
        return 0
    
    # 解析表列表
    tables = None
    if args.tables:
        tables = [t.strip() for t in args.tables.split(',')]
    
    # 初始化数据库助手
    db = DBHelper()
    
    try:
        # 试运行模式，先看一下有多少数据
        if not args.dry_run:
            dry_results = db.cleanup_test_data(tables=tables, dry_run=True)
            
            if dry_results['total_records'] == 0:
                print("✅ 没有需要清理的测试数据")
                return 0
            
            # 确认
            if not args.confirm:
                print(f"\n⚠️  即将删除 {dry_results['total_records']} 条测试数据")
                response = input("确认继续吗？(y/N): ")
                if response.lower() not in ['y', 'yes']:
                    print("已取消")
                    return 0
        
        # 执行清理
        results = db.cleanup_test_data(tables=tables, dry_run=args.dry_run)
        
        # 打印报告
        print_cleanup_report(results)
        
        return 0
        
    except Exception as e:
        logger.error(f"清理失败: {e}")
        return 1
    finally:
        db.close()


if __name__ == '__main__':
    sys.exit(main())
