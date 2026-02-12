# HEARTBEAT.md

## 每次 heartbeat 检查以下内容：

### 1. 检查共享知识库更新
```bash
cd ~/.openclaw/shared-knowledge && git pull --rebase origin master
```
- 如果有新内容，阅读学习

### 2. 同步自己的记忆
```bash
cd ~/.openclaw/workspace && git push origin master:main
```
