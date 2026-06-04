import csv
import os


def read_inventory(cfg):
    filepath = os.path.join(os.path.dirname(__file__), "..", cfg["csv_file"])
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({
                "sku": row[cfg["sku_column"]],
                "current": int(row[cfg["current_qty_column"]]),
                "threshold": int(row[cfg["safe_threshold_column"]]),
            })
    return rows
