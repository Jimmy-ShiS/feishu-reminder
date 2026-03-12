#!/usr/bin/env python3
"""
飞书定时提醒删除脚本

功能：删除指定的定时任务
核心机制：调用 openclaw cron remove 命令
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
    parser = argparse.ArgumentParser(description='飞书定时提醒删除脚本')
    parser.add_argument('--name', required=True, help='提醒任务名称')
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
    
    # 调用 openclaw cron remove
    cmd = ["openclaw", "cron", "remove", "--name", args.name, "--token", args.token]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            print(f"✅ 已删除提醒：{args.name}")
        else:
            if "not found" in result.stderr.lower() or "不存在" in result.stderr:
                print(f"❌ 未找到提醒：{args.name}")
            else:
                print(f"❌ 删除失败：{result.stderr}")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 执行命令失败：{e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ 未找到 openclaw 命令，请确保已安装 OpenClaw")
        sys.exit(1)


if __name__ == "__main__":
    main()
