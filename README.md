# 飞书低库存预警脚本

## 运行环境要求

- Python 3.8+
- 依赖包：`requests`、`schedule`

## 安装依赖

```bash
pip install requests schedule
```

## 配置步骤

### 1. 创建飞书机器人

1. 打开飞书，创建或进入一个测试群
2. 点击群设置 → 机器人 → 添加机器人 → 自定义机器人
3. 填写机器人名称，点击添加
4. 复制生成的 **Webhook 地址**

### 2. 配置 Webhook

打开 `main.py`，将第 6 行替换为你的实际地址：

```python
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx"
```

## 如何运行

### 方式 A：立即手动执行一次

```bash
python main.py
```

### 方式 B：定时每天 16:00 自动发送

```bash
python main.py --schedule
```

## 注意事项

- **Webhook 地址属于敏感信息**，提交代码前请替换为占位符
- `inventory.csv` 与 `main.py` 需在同一目录下运行
- 确保网络可访问飞书 API（`open.feishu.cn`）
