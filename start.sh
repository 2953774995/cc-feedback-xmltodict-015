#!/bin/bash
# 单轮执行入口：在评测仓库内启动 claude-ubkey，只跑首轮。
# 在仓库根目录运行：./start.sh
cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
    echo "未找到 .venv，先准备 Python 环境。"
    exit 1
fi

if ! command -v claude-ubkey >/dev/null 2>&1; then
    echo "未找到 claude-ubkey。先从领题平台领取 key 与 url，完成独立配置目录 ~/.claude-ubkey 后再运行。"
    exit 1
fi

echo "仓库：$(pwd)"
echo "分支：$(git rev-parse --abbrev-ref)"
echo "初始快照：$(git rev-parse HEAD)"
echo "启动 claude-ubkey，只跑首轮，回答后即结束，不要追问。"
echo "------------------------------------------------------------"
claude-ubkey
