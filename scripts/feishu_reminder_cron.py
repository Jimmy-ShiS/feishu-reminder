#!/usr/bin/env python3
"""
飞书定时提醒设置脚本 - 使用 sessions_spawn 异步任务

功能：设置定时推送任务到飞书
核心机制：使用 openclaw cron + 简化的 agent 指令
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
    parser = argparse.ArgumentParser(description='飞书定时提醒设置脚本')
    parser.add_argument('--name', required=True, help='提醒任务名称')
    parser.add_argument('--at', required=True, help='触发时间（10m/1h/09:00/ISO8601）')
    parser.add_argument('--message', required=True, help='推送的消息内容')
    parser.add_argument('--user-id', required=True, help='目标用户 ID')
    parser.add_argument('--channel', default='feishu', help='渠道（默认：feishu）')
    parser.add_argument('--token', default=None, help='Gateway Token（不传则从配置文件读取）')
    parser.add_argument('--repeat', choices=['once', 'daily', 'weekly', 'monthly'], 
                        default='once', help='重复规则（默认：once）')
    
    args = parser.parse_args()
    
    # 获取 Token（如果未提供）
    if not args.token:
        try:
            args.token = get_gateway_token()
        except Exception as e:
            print(f"❌ 获取 Gateway Token 失败：{e}")
            sys.exit(1)
    
    # 构建更明确的 agent 指令，强制调用 message 工具
    agent_instruction = f"""【任务】发送飞书消息

请**立即**调用 message 工具发送以下消息：
- action: send
- channel: {args.channel}
- target: user:{args.user_id}
- message: {args.message}

**重要**：
1. 不要回复其他内容
2. 直接调用 message 工具
3. 调用完成后输出"✅ 已发送"

现在开始执行！"""
    
    cmd = [
        "openclaw", "cron", "add",
        "--name", args.name,
        "--at", args.at,
        "--session", "isolated",
        "--announce",
        "--message", agent_instruction,
        "--channel", args.channel,
        "--to", f"user:{args.user_id}",
        "--token", args.token,
        "--thinking", "minimal",
        "--timeout", "10000"
    ]
    
    print(f"⏰ 正在设置提醒：{args.name}")
    print(f"📍 触发时间：{args.at}")
    if args.repeat != "once":
        print(f"🔁 重复规则：{args.repeat}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # 输出 JSON 结果
        try:
            job_info = json.loads(result.stdout)
            print(f"✅ 已设置提醒：{args.name}")
            print(f"📍 触发时间：{args.at}")
            if args.repeat != "once":
                print(f"🔁 重复：{args.repeat}")
        except json.JSONDecodeError:
            print(f"✅ 已设置提醒：{args.name}")
            print(f"📍 触发时间：{args.at}")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 执行命令失败：{e}")
        print(f"错误信息：{e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ 未找到 openclaw 命令，请确保已安装 OpenClaw")
        sys.exit(1)


if __name__ == "__main__":
    main()
