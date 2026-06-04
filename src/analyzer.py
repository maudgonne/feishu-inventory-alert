def analyze(inventory, high_risk_ratio):
    low_stock = []
    for item in inventory:
        if item["current"] < item["threshold"]:
            gap = (item["threshold"] - item["current"]) / item["threshold"]
            low_stock.append({**item, "risk": "高" if gap >= high_risk_ratio else "中"})
    return low_stock
