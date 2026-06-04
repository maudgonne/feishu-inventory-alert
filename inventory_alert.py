#!/usr/bin/env python3
"""每日低库存预警：读取本地 CSV，通过飞书自定义机器人 Webhook 推送报告。"""

from __future__ import annotations

import csv
import sys
from datetime import datetime
from pathlib import Path

import requests

try:
    from config import WEBHOOK_URL
except ImportError:
    WEBHOOK_URL = "你的实际地址"

CSV_PATH = Path(__file__).resolve().parent / "inventory.csv"


def load_inventory(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def parse_row(row: dict) -> dict:
    return {
        "sku": row["SKU"].strip(),
        "current_qty": int(row["current_qty"]),
        "safe_threshold": int(row["safe_threshold"]),
    }


def risk_level(current_qty: int, safe_threshold: int) -> str:
    if safe_threshold <= 0:
        return "中"
    gap_ratio = (safe_threshold - current_qty) / safe_threshold
    return "高" if gap_ratio >= 0.5 else "中"


def find_low_stock(items: list[dict]) -> list[dict]:
    low = [item for item in items if item["current_qty"] < item["safe_threshold"]]
    for item in low:
        item["risk"] = risk_level(item["current_qty"], item["safe_threshold"])
    return low


def build_report(low_stock: list[dict]) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    if not low_stock:
        return "今日无低库存预警，所有SKU库存正常"

    lines = [f"📦 每日库存预警报告 – {today}"]
    for i, item in enumerate(low_stock, start=1):
        lines.append(
            f"{i}. SKU: {item['sku']} | 当前库存: {item['current_qty']} | "
            f"安全阈值: {item['safe_threshold']} | 缺货风险: {item['risk']}"
        )
    lines.append(f"   共 {len(low_stock)} 个SKU低于安全阈值，请关注。")
    return "\n".join(lines)


def send_feishu_message(webhook_url: str, text: str) -> None:
    if not webhook_url or webhook_url == "你的实际地址":
        raise ValueError(
            "请配置 Webhook：复制 config.example.py 为 config.py 并填入真实地址"
        )
    payload = {"msg_type": "text", "content": {"text": text}}
    resp = requests.post(webhook_url, json=payload, timeout=15)
    resp.raise_for_status()
    body = resp.json()
    if body.get("code") not in (0, None):
        raise RuntimeError(f"飞书返回错误: {body}")


def main() -> int:
    if not CSV_PATH.exists():
        print(f"找不到库存文件: {CSV_PATH}", file=sys.stderr)
        return 1

    items = [parse_row(row) for row in load_inventory(CSV_PATH)]
    report = build_report(find_low_stock(items))
    print(report)
    print("---")
    send_feishu_message(WEBHOOK_URL, report)
    print("已发送到飞书群。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
