# Jzrm OpenClaw 自动化系统说明

> 给“容易忘”的未来自己：这份文档是当前系统的总览 + 实现方式 + 常用命令。
> 
> 本套系统默认采用并参考以下项目思路进行搭建：
> - SegmentFault Wiki（OpenClaw 相关文章）：https://segmentfault.com/a/1190000047594387

## 一、这套系统已经实现了什么

1. **OpenClaw 由 systemd 托管**（开机自启、异常自动重启）
2. **记忆体系三层化**
   - `memory/`：每日原始日志
   - `learnings/`：每日学习总结
   - `MEMORY.md`：长期沉淀
3. **定时任务自动化**
   - 每天 `00:00`：学习总结与长期记忆更新
   - 每天 `07:15`：天气 + 热点新闻推送（PushPlus）
4. **Heartbeat 心跳轮询**
   - 每 `30m` 执行一次心跳
   - 按 `HEARTBEAT.md` 的清单做同步与检查

---

## 二、目录结构（核心）

```text
~/.openclaw/workspace/
├── AGENTS.md       # 行为规则、记忆管理、维护策略
├── HEARTBEAT.md    # 心跳任务清单
├── MEMORY.md       # 长期记忆
├── memory/         # 每日原始日志（含 TEMPLATE.md）
├── learnings/      # 每日提炼总结
├── SOUL.md         # 助手人格
├── USER.md         # 用户信息与偏好
└── .git/           # 版本管理
```

---

## 三、关键实现方式（带中文注释）

### 1）systemd 服务

服务文件：`/etc/systemd/system/openclaw-gateway.service`

```ini
[Unit]
Description=OpenClaw Gateway 🤖
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw

# systemd 环境较“干净”，显式给 PATH，避免找不到命令
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Telegram Bot Token（注意：泄露后必须轮换）
Environment="TELEGRAM_BOT_TOKEN=你的Token"

# 代理配置（你的 OpenClash 混合端口）
Environment="HTTP_PROXY=http://192.168.5.3:7893"
Environment="HTTPS_PROXY=http://192.168.5.3:7893"
Environment="ALL_PROXY=http://192.168.5.3:7893"

# 当前版本使用 run，不带 --config
ExecStart=/usr/bin/openclaw gateway run

# 异常自动重启
Restart=always
RestartSec=5
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

> 注意：之前踩过坑，`openclaw gateway run --config ...` 在当前版本会报 `unknown option '--config'`。

---

### 2）Heartbeat 配置

当前使用新格式：

```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "30m" // 每30分钟一次心跳
      }
    }
  }
}
```

心跳执行内容写在 `HEARTBEAT.md`。

---

### 3）每日学习总结任务（Cron）

- 时间：每天 `00:00`（Asia/Shanghai）
- 动作：读取 `memory/YYYY-MM-DD.md` → 写 `learnings/YYYY-MM-DD.md` → 更新 `MEMORY.md` → Git 提交推送

---

### 4）每日晨报任务（Cron）

- 时间：每天 `07:15`（Asia/Shanghai）
- 内容：天气 + 热点新闻
- 推送：PushPlus（token + 群组编码 topic）

---

## 四、常用运维命令（最重要）

### 服务管理

```bash
# 启动/重启/停止
systemctl start openclaw-gateway
systemctl restart openclaw-gateway
systemctl stop openclaw-gateway

# 开机自启
systemctl enable openclaw-gateway

# 查看状态
systemctl status openclaw-gateway --no-pager -l

# 实时日志
journalctl -u openclaw-gateway -f
```

### OpenClaw 状态检查

```bash
openclaw status
openclaw gateway status
openclaw doctor --repair --non-interactive --yes
```

### Git 同步

```bash
# 查看变更
git -C /root/.openclaw/workspace status

# 提交
git -C /root/.openclaw/workspace add .
git -C /root/.openclaw/workspace commit -m "chore: update docs and configs"

# 推送到 main
git -C /root/.openclaw/workspace push origin master:main
```

---

## 五、排障速记

1. **服务反复重启**
   - 先看日志：`journalctl -u openclaw-gateway -f`
   - 常见错误：ExecStart 参数不兼容（例如 `--config`）

2. **Bot 没反应**
   - 看服务是否 `active (running)`
   - `openclaw status` 看 Telegram 通道是否 `OK`
   - 检查 token 是否正确、是否已过期

3. **Git 推送失败**
   - GitHub 不支持密码，必须用 PAT 或 SSH
   - 推荐长期改 SSH 免密

---

## 六、项目来源与参考

- 主参考项目（Wiki）：https://segmentfault.com/a/1190000047594387
- 说明：本套系统的目录规划、自动化思路、日常维护策略均以该项目为参考基线，再结合当前环境（systemd / Telegram / PushPlus / Git）做本地化调整。

## 七、记忆维护原则（给未来的自己）

- 做完重要事：写 `memory/YYYY-MM-DD.md`
- 每天结束：提炼 `learnings/YYYY-MM-DD.md`
- 每隔几天：把可复用知识沉淀到 `MEMORY.md`
- `MEMORY.md` 只留“长期有价值”的内容，避免臃肿

---

最后更新时间：2026-02-12
