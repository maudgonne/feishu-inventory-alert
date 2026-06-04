from datetime import date


def build(low_stock, cfg):
    today = date.today().strftime("%Y-%m-%d")
    sep = [{"tag": "text", "text": "─" * 40}]
    at_all = cfg.get("at_all_on_high_risk", False)
    notify_users = cfg.get("notify_users", [])

    if not low_stock:
        rows = [
            [{"tag": "text", "text": f"日期: {today}"}],
            sep,
            [{"tag": "text", "text": "今日无低库存预警，所有SKU库存正常。"}],
        ]
    else:
        rows = [[{"tag": "text", "text": f"日期: {today}"}], sep]
        for i, item in enumerate(low_stock, 1):
            row = [{"tag": "text", "text": (
                f"{i}.  SKU: {item['sku']}    "
                f"当前库存: {item['current']}  安全阈值: {item['threshold']}    "
                f"缺货风险: {item['risk']}"
            )}]
            if at_all and item["risk"] == "高":
                row.append({"tag": "at", "user_id": "all"})
            rows.append(row)

        summary = [{"tag": "text", "text": f"共 {len(low_stock)} 个SKU低于安全阈值，请 "}]
        if notify_users:
            names = "、".join(f"{u['name']}({u['phone']})" for u in notify_users)
            summary.append({"tag": "text", "text": names + " "})
        if at_all:
            summary.append({"tag": "at", "user_id": "all"})
            summary.append({"tag": "text", "text": " "})
        summary.append({"tag": "text", "text": "及时处理。"})
        rows += [sep, summary]

    return {
        "msg_type": "post",
        "content": {"post": {"zh_cn": {"title": "每日库存预警报告", "content": rows}}},
    }
