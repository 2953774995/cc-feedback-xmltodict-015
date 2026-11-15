#!/bin/bash
cd "$(dirname "$0")"
PY=.venv/bin/python
[ -x "$PY" ] || PY=python3

echo "============================================================"
echo "第一部分：验收探针"
echo "============================================================"
$PY probes/run_probes.py
PROBE_RC=$?
echo

echo "============================================================"
echo "第二部分：既有测试（不得退化）"
echo "============================================================"
$PY -m pytest -q  2>&1 | tail -3
PYTEST_RC=${PIPESTATUS[0]}
echo

echo "############################################################"
echo "# 汇总"
echo "############################################################"
[ $PROBE_RC -eq 0 ] && echo "验收探针：PASS" || echo "验收探针：FAIL"
[ $PYTEST_RC -eq 0 ] && echo "既有测试：PASS" || echo "既有测试：FAIL"
if [ $PROBE_RC -eq 0 ] && [ $PYTEST_RC -eq 0 ]; then
    echo; echo "总体结果：全部通过"; exit 0
fi
echo; echo "总体结果：存在未通过项"; exit 1
