---
name: feishu-reminder
description: 飞书主动推送提醒工具。支持定时任务、一次性提醒、周期推送等场景，通过 OpenClaw Gateway 将消息主动推送到飞书。
---

# 飞书主动推送提醒 Skill

## 📖 技能说明

这是一个**主动推送消息到飞书**的工具，适用于：
- 定时提醒（如每天 9 点打卡提醒）
- 周期推送（如每周一周报提醒）
- 一次性提醒（如 30 分钟后开会）
- 主动通知（如任务完成通知）

**核心机制**：
- 使用 `openclaw cron` 命令设置定时任务
- 通过 Gateway 认证推送到飞书
- 使用隔离会话，不影响主会话历史

---

## 🔑 配置信息

### Gateway Token

从 `~/.openclaw/openclaw.json` 获取：
```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "973af4fcde07588ee560689fa9842fd189d3d8339265b559"
    }
  }
}
```

### 飞书用户 ID

格式：`ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

从消息上下文的 `SenderId` 获取，或通过 `feishu_search_user` 查询。

---

## 🛠️ 可用工具

### 1. 定时提醒脚本

**路径**: `scripts/feishu_reminder_cron.py`

**功能**: 设置定时推送任务

**调用方式**:
```bash
python3 scripts/feishu_reminder_cron.py \
  --name "提醒名称" \
  --at "10m" \
  --message "主人，该开会啦！" \
  --user-id "ou_xxxxx" \
  --channel "feishu"
```

**参数说明**:

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--name` | ✅ | 提醒任务名称 | "晨会提醒" |
| `--at` | ✅ | 触发时间 | 见下方时间格式 |
| `--message` | ✅ | 推送的消息内容 | "主人，该开会啦！" |
| `--user-id` | ✅ | 目标用户 ID | "ou_adf0d189f4676cb9f7176af21cc1aa0a" |
| `--channel` | ✅ | 渠道（固定为 feishu） | "feishu" |
| `--repeat` | ❌ | 重复规则 | "daily", "weekly", "monthly" |

**时间格式** (`--at`):

| 格式 | 说明 | 示例 |
|------|------|------|
| `10m` | 10 分钟后 | `--at "10m"` |
| `1h` | 1 小时后 | `--at "1h"` |
| `2026-03-12T15:00:00+08:00` | 具体时间（ISO 8601） | `--at "2026-03-12T15:00:00+08:00"` |
| `09:00` | 每天固定时间 | `--at "09:00"`（需配合 `--repeat daily`） |

**重复规则** (`--repeat`):

| 值 | 说明 | 示例 |
|------|------|------|
| `once` | 一次性（默认） | 30 分钟后提醒一次 |
| `daily` | 每天 | 每天 9 点提醒 |
| `weekly` | 每周 | 每周一 9 点提醒 |
| `monthly` | 每月 | 每月 1 号 9 点提醒 |

---

### 2. 查询定时任务

**路径**: `scripts/feishu_reminder_list.py`

**功能**: 查看已设置的定时任务

**调用方式**:
```bash
python3 scripts/feishu_reminder_list.py \
  --user-id "ou_xxxxx"
```

**输出**: 定时任务列表（名称、触发时间、状态）

---

### 3. 删除定时任务

**路径**: `scripts/feishu_reminder_delete.py`

**功能**: 删除指定的定时任务

**调用方式**:
```bash
python3 scripts/feishu_reminder_delete.py \
  --name "提醒名称" \
  --user-id "ou_xxxxx"
```

---

## 📋 使用场景

### 场景 1：一次性提醒

**用户**: "30 分钟后提醒我吃药"

**OpenClaw 调用**:
```bash
python3 scripts/feishu_reminder_cron.py \
  --name "吃药提醒" \
  --at "30m" \
  --message "主人，该吃药啦！💊" \
  --user-id "ou_adf0d189f4676cb9f7176af21cc1aa0a"
```

**回复**:
```
✅ 已设置提醒：吃药提醒
⏰ 触发时间：30 分钟后
```

---

### 场景 2：每天固定时间提醒

**用户**: "每天早上 9 点提醒我打卡"

**OpenClaw 调用**:
```bash
python3 scripts/feishu_reminder_cron.py \
  --name "打卡提醒" \
  --at "09:00" \
  --repeat "daily" \
  --message "主人，该打卡啦！☀️ 新的一天加油～" \
  --user-id "ou_adf0d189f4676cb9f7176af21cc1aa0a"
```

**回复**:
```
✅ 已设置每日提醒：打卡提醒
⏰ 触发时间：每天 09:00
🔁 重复：每天
```

---

### 场景 3：每周一提醒

**用户**: "每周一上午 10 点提醒我写周报"

**OpenClaw 调用**:
```bash
python3 scripts/feishu_reminder_cron.py \
  --name "周报提醒" \
  --at "10:00" \
  --repeat "weekly" \
  --message "主人，该写周报啦！📝 别忘了总结本周工作～" \
  --user-id "ou_adf0d189f4676cb9f7176af21cc1aa0a"
```

**回复**:
```
✅ 已设置每周提醒：周报提醒
⏰ 触发时间：每周一 10:00
🔁 重复：每周
```

---

### 场景 4：查询已设置的提醒

**用户**: "我有哪些定时提醒"

**OpenClaw 调用**:
```bash
python3 scripts/feishu_reminder_list.py \
  --user-id "ou_adf0d189f4676cb9f7176af21cc1aa0a"
```

**回复**:
```
📋 你的定时提醒：

| 名称 | 触发时间 | 重复 | 状态 |
|------|----------|------|------|
| 打卡提醒 | 每天 09:00 | 每天 | ✅ 启用 |
| 周报提醒 | 每周一 10:00 | 每周 | ✅ 启用 |
| 吃药提醒 | 2026-03-12 15:42 | 一次 | ⏳ 等待中 |
```

---

### 场景 5：删除提醒

**用户**: "删除吃药提醒"

**OpenClaw 调用**:
```bash
python3 scripts/feishu_reminder_delete.py \
  --name "吃药提醒" \
  --user-id "ou_adf0d189f4676cb9f7176af21cc1aa0a"
```

**回复**:
```
✅ 已删除提醒：吃药提醒
```

---

## 📁 文件结构

```
feishu-reminder/
├── README.md                    # 快速开始指南
├── SKILL.md                     # 本文档
├── scripts/
│   ├── feishu_reminder_cron.py      # 设置定时任务
│   ├── feishu_reminder_list.py      # 查询任务列表
│   └── feishu_reminder_delete.py    # 删除任务
└── references/
```

---

## 💡 最佳实践

### 1. 提醒命名规范

- 简洁明了：`打卡提醒 `、` 吃药提醒`、`周报提醒`
- 包含时间（可选）：`9 点打卡提醒 `、` 周一周报提醒`
- 避免重复：同名提醒会覆盖之前的

### 2. 消息内容设计

- 友好亲昵：用"主人"称呼
- 适当 emoji：💊 ☀️ 📝 ⏰
- 简洁有力：一句话说明意图

**示例**:
```
✅ 好：
"主人，该吃药啦！💊"
"主人，该打卡啦！☀️ 新的一天加油～"

❌ 差：
"这是一个提醒通知"
"根据您之前的设置，现在应该执行以下操作..."
```

### 3. 时间选择建议

| 场景 | 推荐时间 |
|------|----------|
| 起床/打卡 | 08:00-09:00 |
| 午休/吃药 | 12:00-13:00 |
| 下午茶/休息 | 15:00-16:00 |
| 日报/总结 | 18:00-19:00 |
| 周报 | 周一 10:00 或周五 16:00 |

### 4. 重复规则选择

| 场景 | 重复规则 |
|------|----------|
| 吃药、喝水 | `daily`（每天） |
| 打卡、晨会 | `daily`（工作日） |
| 周报、周会 | `weekly`（每周） |
| 账单、还款 | `monthly`（每月） |
| 一次性事项 | `once`（默认） |

---

## ⚠️ 注意事项

1. **Gateway Token 安全**
   - 不要硬编码在代码中
   - 从 `~/.openclaw/openclaw.json` 读取
   - 不要泄露给他人

2. **用户 ID 隔离**
   - 每个用户的提醒独立存储
   - 查询/删除时务必传对 `--user-id`

3. **时区处理**
   - 所有时间使用 Asia/Shanghai 时区
   - ISO 8601 格式必须包含时区：`+08:00`

4. **任务命名唯一性**
   - 同名提醒会覆盖之前的
   - 建议命名包含时间或场景

---

## 🎯 快速决策卡片

**遇到以下情况，使用 feishu-reminder：**

| 用户说... | 第一反应 |
|----------|---------|
| "X 分钟后提醒我 XXX" | ✅ feishu_reminder_cron.py |
| "每天 X 点提醒我 XXX" | ✅ feishu_reminder_cron.py + --repeat daily |
| "每周一提醒我 XXX" | ✅ feishu_reminder_cron.py + --repeat weekly |
| "我有哪些提醒" | ✅ feishu_reminder_list.py |
| "删除 XXX 提醒" | ✅ feishu_reminder_delete.py |

**与 FlashMemo 的区别：**
- **FlashMemo**: 待办事项管理，需要用户主动查询或到时间推送一次
- **feishu-reminder**: 定时推送工具，适合周期性、固定时间的主动提醒

**可以配合使用：**
```
用户："每周一 10 点提醒我写周报"

方案 1（仅提醒）:
→ feishu-reminder：每周一 10 点推送消息

方案 2（提醒 + 待办）:
→ feishu-reminder：每周一 10 点推送消息
→ FlashMemo：记一条待办"写周报"（周一 10 点）
```

---

**版本**: v1.0  
**日期**: 2026-03-12  
**功能**: 飞书主动推送提醒，支持定时任务和周期推送
**仓库**: https://github.com/Jimmy-ShiS/feishu-reminder
