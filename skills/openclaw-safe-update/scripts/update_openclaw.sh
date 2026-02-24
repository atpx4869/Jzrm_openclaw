#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-check}"
PKG="@qingchencloud/openclaw-zh"
BIN_LINK="/usr/bin/openclaw"
BIN_TARGET="../lib/node_modules/@qingchencloud/openclaw-zh/openclaw.mjs"
BIN_FILE="/usr/lib/node_modules/@qingchencloud/openclaw-zh/openclaw.mjs"

current_version() {
  /usr/bin/openclaw --version 2>/dev/null || openclaw --version 2>/dev/null || echo "unknown"
}

latest_version() {
  npm view "$PKG" version 2>/dev/null || echo "unknown"
}

status_line() {
  local cur lat
  cur="$(current_version)"
  lat="$(latest_version)"
  echo "current=$cur latest=$lat"
}

repair_link() {
  ln -sf "$BIN_TARGET" "$BIN_LINK"
  chmod +x "$BIN_FILE" || true
}

restart_gateway() {
  if /usr/bin/openclaw gateway restart >/dev/null 2>&1; then
    return 0
  fi
  pkill -f openclaw-gateway >/dev/null 2>&1 || true
  sleep 1
  /usr/bin/openclaw gateway start >/dev/null 2>&1 || true
}

check() {
  echo "[check] $(status_line)"
  echo "[check] bin=$(command -v openclaw || echo missing)"
}

do_update() {
  local before after latest
  before="$(current_version)"
  latest="$(latest_version)"

  echo "[update] before=$before latest=$latest"

  if [[ "$before" == "$latest" && "$before" != "unknown" ]]; then
    echo "[update] already-latest"
    return 0
  fi

  if ! npm i -g "$PKG@latest"; then
    stale_dir="$(ls -d /usr/lib/node_modules/@qingchencloud/.openclaw-zh-* 2>/dev/null | head -n1 || true)"
    if [[ -n "${stale_dir:-}" ]]; then
      echo "[update] retry-after-clean-stale=$stale_dir"
      rm -rf "$stale_dir"
      npm i -g "$PKG@latest"
    else
      echo "[update] failed-no-stale-dir"
      return 1
    fi
  fi

  repair_link
  hash -r || true
  restart_gateway || true

  after="$(current_version)"
  latest="$(latest_version)"
  echo "[update] after=$after latest=$latest"
}

case "$MODE" in
  check) check ;;
  update) do_update ;;
  *)
    echo "usage: $0 [check|update]" >&2
    exit 2
    ;;
esac
