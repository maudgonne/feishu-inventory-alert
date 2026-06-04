import sys
import schedule
import time

from src.config import load_config
from src.reader import read_inventory
from src.analyzer import analyze
from src.message import build
from src.notifier import send


def run():
    cfg = load_config()
    inventory = read_inventory(cfg)
    low_stock = analyze(inventory, cfg["high_risk_ratio"])
    payload = build(low_stock, cfg)
    result = send(cfg["webhook_url"], payload)
    print(f"发送成功: {result}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        cfg = load_config()
        schedule_time = cfg["schedule_time"]
        schedule.every().day.at(schedule_time).do(run)
        print(f"定时任务已启动，每天 {schedule_time} 发送报告...")
        while True:
            schedule.run_pending()
            time.sleep(30)
    else:
        run()
