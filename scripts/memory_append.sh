#!/usr/bin/env bash
set -euo pipefail

# 用法：scripts/memory_append.sh "要记录的事项"
ROOT="/root/.openclaw/workspace"
TODAY="$(date +%F)"
FILE="$ROOT/memory/$TODAY.md"
MSG="${1:-}"

if [[ -z "$MSG" ]]; then
  echo "用法: $0 \"要记录的事项\""
  exit 1
fi

mkdir -p "$ROOT/memory"

if [[ ! -f "$FILE" ]]; then
  cat > "$FILE" <<'EOF'
# __DATE__

## 今日事件

## 技术笔记

## 待办
EOF
  sed -i "s/__DATE__/$TODAY/" "$FILE"
fi

TS="$(date '+%H:%M')"
sed -i "/^## 今日事件$/a - [$TS] $MSG" "$FILE"

echo "已写入: $FILE"
