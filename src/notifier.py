import requests


def send(webhook_url, payload):
    resp = requests.post(webhook_url, json=payload, timeout=10)
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") != 0:
        raise RuntimeError(f"飞书接口返回错误: {result}")
    return result
