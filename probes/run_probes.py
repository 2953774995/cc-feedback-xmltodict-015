#!/usr/bin/env python3
"""批量 XML 解析验收探针。

契约：
  from xmltodict.batch import parse_many
  res = parse_many(docs)            docs 为 XML 字符串列表
  res.items    与输入等长的列表，成功的项是 dict，失败位置为 None
  res.errors   列表，每项含 .index 与 .message
  res.ok       全部成功时为 True
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

FAILED = 0
PASSED = 0


def check(code, desc, fn):
    global FAILED, PASSED
    try:
        fn()
        print(f"[PASS] {code} {desc}")
        PASSED += 1
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] {code} {desc}")
        print(f"        {type(exc).__name__}: {exc}")
        FAILED += 1


def main():
    try:
        from xmltodict.batch import parse_many  # noqa: F401
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] P0 导入 xmltodict.batch 失败：{type(exc).__name__}: {exc}")
        print("-" * 60)
        print("探针汇总：0/5 通过")
        return 1

    def p1():
        res = parse_many(["<a><b>1</b></a>", "<a><b>2</b></a>"])
        assert [x["a"]["b"] for x in res.items] == ["1", "2"], res.items
        assert res.ok is True

    def p2():
        res = parse_many(["<a/>", "<a><b></a>"])
        assert len(res.items) == 2, res.items
        assert res.items[1] is None
        assert res.ok is False

    def p3():
        res = parse_many(["<a/>", "<broken", "<c/>"])
        assert [e.index for e in res.errors] == [1], [e.index for e in res.errors]
        assert res.items[0] == {"a": None} or isinstance(res.items[0], dict)

    def p4():
        res = parse_many([])
        assert res.items == [] and res.errors == [] and res.ok is True

    def p5():
        import xmltodict
        assert xmltodict.parse("<a><b>1</b></a>")["a"]["b"] == "1"

    check("P1", "多文档各自解析", p1)
    check("P2", "坏文档位置占位且 ok=False", p2)
    check("P3", "错误项带下标", p3)
    check("P4", "空输入", p4)
    check("P5", "既有 parse 不变", p5)

    print("-" * 60)
    print(f"探针汇总：{PASSED}/{PASSED + FAILED} 通过")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
