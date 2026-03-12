#!/usr/bin/env python3
"""
飞书定时提醒查询脚本

功能：查看已设置的定时任务
核心机制：调用 openclaw cron list 命令
"""

import argparse
import subprocess
import sys
import json
from pathlib import Path


def get_gateway_token() -> str:
    """从 openclaw.json 获取 Gateway Token"""
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在：{config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    try:
        token = config["gateway"]["auth"]["token"]
        return token
    except KeyError:
        raise ValueError("无法从配置文件中获取 Gateway Token")


def main():
    parser = argparse.ArgumentParser(description='飞书定时提醒查询脚本')
    parser.add_argument('--user-id', required=True, help='目标用户 ID')
    parser.add_argument('--channel', default='feishu', help='渠道（默认：feishu）')
    parser.add_argument('--token', default=None, help='Gateway Token（不传则从配置文件读取）')
    
    args = parser.parse_args()
    
    # 获取 Token（如果未提供）
    if not args.token:
        try:
            args.token = get_gateway_token()
        except Exception as e:
            print(f"❌ 获取 Gateway Token 失败：{e}")
            sys.exit(1)
    
    # 调用 openclaw cron list
    cmd = ["openclaw", "cron", "list", "--token", args.token]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if not output or "No cron jobs" in output:
                print("📋 你还没有设置任何定时提醒～")
                return
            
            # 输出表格
            print("📋 你的定时提醒：\n")
            print(output)
        else:
            print(f"❌ 查询失败：{result.stderr}")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 执行命令失败：{e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ 未找到 openclaw 命令，请确保已安装 OpenClaw")
        sys.exit(1)


if __name__ == "__main__":
    main()
