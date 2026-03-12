# 飞书主动推送提醒 Skill

> 通过 OpenClaw Gateway 将消息主动推送到飞书，支持定时任务、周期提醒等场景。

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/Jimmy-ShiS/feishu-reminder.git
cd feishu-reminder
```

### 基本用法

**设置一次性提醒**：
```bash
python3 scripts/feishu_reminder_cron.py \
  --name "吃药提醒" \
  --at "30m" \
  --message "主人，该吃药啦！💊" \
  --user-id "ou_xxxxx"
```

**设置每天提醒**：
```bash
python3 scripts/feishu_reminder_cron.py \
  --name "打卡提醒" \
  --at "09:00" \
  --repeat "daily" \
  --message "主人，该打卡啦！☀️" \
  --user-id "ou_xxxxx"
```

**查询已设置的提醒**：
```bash
python3 scripts/feishu_reminder_list.py \
  --user-id "ou_xxxxx"
```

**删除提醒**：
```bash
python3 scripts/feishu_reminder_delete.py \
  --name "吃药提醒" \
  --user-id "ou_xxxxx"
```

## 📖 功能特性

- ✅ 一次性定时提醒（如：30 分钟后）
- ✅ 周期性提醒（每天/每周/每月）
- ✅ 固定时间提醒（如：每天 9:00）
- ✅ 飞书消息主动推送
- ✅ 隔离会话，不影响主会话历史

## 🛠️ 脚本说明

### feishu_reminder_cron.py - 设置提醒

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--name` | ✅ | 提醒任务名称 | `"晨会提醒"` |
| `--at` | ✅ | 触发时间 | `30m`, `1h`, `09:00`, `2026-03-12T15:00:00+08:00` |
| `--message` | ✅ | 推送的消息内容 | `"主人，该开会啦！"` |
| `--user-id` | ✅ | 目标用户 ID | `ou_adf0d189f4676cb9f7176af21cc1aa0a` |
| `--repeat` | ❌ | 重复规则 | `once`（默认）, `daily`, `weekly`, `monthly` |

### feishu_reminder_list.py - 查询提醒

| 参数 | 必填 | 说明 |
|------|------|------|
| `--user-id` | ✅ | 目标用户 ID |

### feishu_reminder_delete.py - 删除提醒

| 参数 | 必填 | 说明 |
|------|------|------|
| `--name` | ✅ | 提醒任务名称 |
| `--user-id` | ✅ | 目标用户 ID |

## 📋 使用场景

| 场景 | 示例命令 |
|------|----------|
| 30 分钟后提醒 | `--at "30m"` |
| 每天早上 9 点 | `--at "09:00" --repeat "daily"` |
| 每周一 10 点 | `--at "10:00" --repeat "weekly"` |
| 每月 1 号 | `--at "09:00" --repeat "monthly"` |
| 具体时间 | `--at "2026-03-12T15:00:00+08:00"` |

## 🔑 配置

Gateway Token 自动从 `~/.openclaw/openclaw.json` 读取，无需手动配置。

如需手动指定：
```bash
python3 scripts/feishu_reminder_cron.py \
  --name "测试" \
  --at "10m" \
  --message "测试消息" \
  --user-id "ou_xxxxx" \
  --token "your-gateway-token"
```

## 💡 与 FlashMemo 的区别

| 特性 | feishu-reminder | FlashMemo |
|------|-----------------|-----------|
| 推送方式 | 主动推送 | 到时间推送一次 |
| 适用场景 | 周期性、固定时间提醒 | 待办事项管理 |
| 存储位置 | OpenClaw cron | ImportantMemo.md |
| 查询方式 | `feishu_reminder_list.py` | `flashmemo_query.py` |

**配合使用示例**：
```bash
# 每周一 10 点推送提醒
python3 feishu_reminder_cron.py --at "10:00" --repeat "weekly" ...

# 同时在 FlashMemo 记待办
python3 flashmemo_store.py --category "memo" --text "写周报" ...
```

## 📁 文件结构

```
feishu-reminder/
├── README.md
├── SKILL.md
├── scripts/
│   ├── feishu_reminder_cron.py      # 设置定时任务
│   ├── feishu_reminder_list.py      # 查询任务列表
│   └── feishu_reminder_delete.py    # 删除任务
└── references/
```

## ⚠️ 注意事项

1. **Gateway Token 安全**：不要硬编码或泄露
2. **用户 ID 隔离**：每个用户的提醒独立存储
3. **时区处理**：所有时间使用 Asia/Shanghai 时区
4. **任务命名**：同名提醒会覆盖之前的

## 🎯 快速决策卡片

| 用户说... | 第一反应 |
|----------|---------|
| "X 分钟后提醒我 XXX" | ✅ feishu_reminder_cron.py |
| "每天 X 点提醒我 XXX" | ✅ feishu_reminder_cron.py + --repeat daily |
| "每周一提醒我 XXX" | ✅ feishu_reminder_cron.py + --repeat weekly |
| "我有哪些提醒" | ✅ feishu_reminder_list.py |
| "删除 XXX 提醒" | ✅ feishu_reminder_delete.py |

## 📄 许可证

MIT

---

**版本**: v1.0  
**日期**: 2026-03-12  
**作者**: Jimmy-ShiS  
**仓库**: https://github.com/Jimmy-ShiS/feishu-reminder
