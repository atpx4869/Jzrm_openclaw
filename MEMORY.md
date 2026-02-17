# MEMORY.md - 长期记忆

> 这是我的核心知识库，记录重要的知识、经验和洞察。
> 每日日志在 memory/ 目录，学习总结在 learnings/ 目录。

## 🧠 核心知识库

### 技术知识
（记录学到的重要技术点）

### 踩坑记录
（记录遇到的问题和解决方案）

### 经验教训
- 每日 00:00 的学习总结依赖 `memory/YYYY-MM-DD.md`；若当日未写日志，会导致总结内容为空，需在白天及时补记关键事项。
- 若要复盘“刚过去的一天”，应优先读取“昨日日志”（`memory/前一日日期.md`）；否则在 00:00 读取当天文件大概率为空。
- 2026-02-16 再次验证：午夜执行总结时若 `memory/当日.md` 缺失，只能产出空摘要；应通过白天持续记日志来保证总结质量。
- 2026-02-17 再次验证：`memory/2026-02-17.md` 在 00:00 不存在，学习总结无可提取内容；需坚持白天记日志，或单独设“昨日日志复盘”任务。
- 2026-02-18 再次验证：`memory/2026-02-18.md` 在 00:00 不存在，本次总结仅能记录流程性经验；建议将总结任务改为读取昨日日志，或把执行时间调整到当日有内容沉淀之后。

## 👤 关于用户
- **名字**：
- **位置**：
- **偏好**：
  - 希望我在自动化运维与文档整理中，主动做提醒（尤其定时任务、日志、推送链路）。
  - 偏好中文沟通。

## 📁 重要路径
- `~/.openclaw/workspace/`：主工作区（所有核心文档与记忆文件）
- `~/.openclaw/workspace/MEMORY.md`：长期记忆（精华沉淀）
- `~/.openclaw/workspace/memory/`：每日日志目录
- `~/.openclaw/workspace/learnings/`：学习总结目录
- `~/.openclaw/workspace/HEARTBEAT.md`：心跳检查清单
- `~/.openclaw/openclaw.json`：OpenClaw 主配置文件
- `/etc/systemd/system/openclaw-gateway.service`：网关 systemd 服务文件
- `~/.openclaw/openclaw.env`：运行时环境变量（API Key 等）
- `~/.openclaw/shared-knowledge/`：共享知识库目录
- `~/.openclaw/shared-knowledge/knowledge/`：共享知识条目目录
- `/vol2/1000/docker`：所有 Docker 配置文件目录

## 🧷 记录规范（重要）
- 后续新增路径、规则、流程时，**必须添加中文备注**，避免后期遗忘与误用。
- 我需要在关键节点主动提醒你（如：定时任务状态、推送异常、凭据轮换、日志维护）。

---
*最后更新：2026-02-18*
