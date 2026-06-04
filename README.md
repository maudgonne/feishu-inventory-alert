# 飞书每日低库存预警

本地脚本读取 CSV 库存数据，筛选低于安全阈值的 SKU，并通过飞书自定义机器人 Webhook 推送「今日低库存预警汇总」报告。

## 运行环境

- Python 3.8+
- 可访问互联网（调用飞书 Webhook）
- 依赖见 `requirements.txt`：`requests`、`schedule`（定时任务可选）

## 安装与配置

### 1. 克隆仓库并安装依赖

```bash
git clone https://github.com/maudgonne/feishu-inventory-alert.git
cd feishu-inventory-alert
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 创建飞书自定义机器人

1. 注册/登录 [飞书](https://www.feishu.cn/)，创建或加入一个测试群。
2. 群设置 → **群机器人** → **添加机器人** → **自定义机器人**。
3. 设置机器人名称（如「库存预警」），复制生成的 **Webhook 地址**。
4. 将 `config.example.py` 复制为 `config.py`，把地址填入：

```python
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/你的token"
```

> `config.py` 已加入 `.gitignore`，请勿将真实 Webhook 提交到仓库。

参考文档：[飞书自定义机器人](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot)

### 3. 库存数据

默认使用项目根目录 `inventory.csv`，字段：`SKU`、`current_qty`、`safe_threshold`。可按需修改行数据。

## 如何运行

### 方式 A：手动执行（基础要求）

```bash
python inventory_alert.py
```

**预期效果：**

- 终端打印报告正文；
- 飞书测试群收到一条文本消息；
- 若有低库存 SKU，消息格式示例：

```text
📦 每日库存预警报告 – 2026-06-04
1. SKU: ASIN-B07X123 | 当前库存: 12 | 安全阈值: 20 | 缺货风险: 高
2. SKU: ASIN-B09Y456 | 当前库存: 8 | 安全阈值: 10 | 缺货风险: 中
   共 2 个SKU低于安全阈值，请关注。
```

若无低库存，则发送：`今日无低库存预警，所有SKU库存正常`。

**缺货风险规则：** `(安全阈值 - 当前库存) / 安全阈值 ≥ 50%` 为「高」，否则为「中」。日期为脚本运行当天。

### 方式 B：每天 16:00 定时（加分）

```bash
python schedule_runner.py
```

进程需保持运行；也可使用系统 cron，例如：

```cron
0 16 * * * cd /path/to/feishu-inventory-alert && /path/to/.venv/bin/python inventory_alert.py
```

## 项目结构

| 文件 | 说明 |
|------|------|
| `inventory.csv` | 本地库存数据源 |
| `inventory_alert.py` | 主程序：读 CSV、生成报告、推送飞书 |
| `schedule_runner.py` | 定时任务入口（16:00） |
| `config.example.py` | Webhook 配置模板 |
| `screenshots/` | 飞书群消息截图（交付用） |

## 注意事项

1. **敏感信息**：提交前确认仓库中 Webhook 为占位符；真实地址仅放在本地 `config.py`。
2. **日期**：报告标题中的日期由运行时刻动态生成。
3. **现场演示**：评审前请在本机配置好 `config.py` 并再执行一次 `python inventory_alert.py` 验证。

## 作者

马尧 — 飞书测试题
