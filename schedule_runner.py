#!/usr/bin/env python3
"""方式 B：每天 16:00 自动发送库存预警（需保持进程运行）。"""

import schedule
import time

from inventory_alert import main as send_report


def job() -> None:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 定时任务触发")
    send_report()


def run_scheduler() -> None:
    schedule.every().day.at("16:00").do(job)
    print("定时任务已启动，每天 16:00 发送报告。按 Ctrl+C 退出。")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    run_scheduler()
