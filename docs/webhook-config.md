# Webhook 使用

## 配置

通过将 webhook 部分添加到您的配置文件并将 `webhook.enabled` 设置为 `true` 来启用 webhook。

示例配置（使用 IFTTT 测试）。

```json
  "webhook": {
        "enabled": true,
        "url": "https://maker.ifttt.com/trigger/<YOUREVENT>/with/key/<YOURKEY>/",
        "entry": {
            "value1": "Buying {pair}",
            "value2": "limit {limit:8f}",
            "value3": "{stake_amount:8f} {stake_currency}"
        },
        "entry_cancel": {
            "value1": "Cancelling Open Buy Order for {pair}",
            "value2": "limit {limit:8f}",
            "value3": "{stake_amount:8f} {stake_currency}"
        },
         "entry_fill": {
            "value1": "Buy Order for {pair} filled",
            "value2": "at {open_rate:8f}",
            "value3": ""
        },
        "exit": {
            "value1": "Exiting {pair}",
            "value2": "limit {limit:8f}",
            "value3": "profit: {profit_amount:8f} {stake_currency} ({profit_ratio})"
        },
        "exit_cancel": {
            "value1": "Cancelling Open Exit Order for {pair}",
            "value2": "limit {limit:8f}",
            "value3": "profit: {profit_amount:8f} {stake_currency} ({profit_ratio})"
        },
        "exit_fill": {
            "value1": "Exit Order for {pair} filled",
            "value2": "at {close_rate:8f}.",
            "value3": ""
        },
        "status": {
            "value1": "Status: {status}",
            "value2": "",
            "value3": ""
        }
    },
```

`webhook.url` 中的 url 应指向您的 webhook 的正确 url。如果您使用 [IFTTT](https://ifttt.com)（如上面的示例所示），请将您的事件和密钥插入到 url 中。

您可以将 POST 正文格式设置为 Form-Encoded（默认）、JSON-Encoded 或原始数据。分别使用 `"format": "form"`、`"format": "json"` 或 `"format": "raw"`。用于 Mattermost Cloud 集成的示例配置：

```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURSUBDOMAIN>.cloud.mattermost.com/hooks/<YOURHOOK>",
        "format": "json",
        "status": {
            "text": "Status: {status}"
        }
    },
```

结果将是一个 POST 请求，例如 `{"text":"Status: running"}` 正文和 `Content-Type: application/json` 标头，这会在 Mattermost 频道中产生 `Status: running` 消息。

使用 Form-Encoded 或 JSON-Encoded 配置时，您可以配置任意数量的有效载荷值，键和值都会在 POST 请求中输出。但是，使用原始数据格式时，您只能配置一个值，并且它**必须**命名为 `"data"`。在这种情况下，数据键不会在 POST 请求中输出，只会输出值。例如：

```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURHOOKURL>",
        "format": "raw",
        "webhookstatus": {
            "data": "Status: {status}"
        }
    },
```

结果将是一个 POST 请求，例如 `Status: running` 正文和 `Content-Type: text/plain` 标头。

### 嵌套 Webhook 配置

某些 webhook 目标需要嵌套结构。
可以通过将内容设置为字典或列表而不是直接作为文本来完成。

这仅在 JSON 格式中受支持。

```json
"webhook": {
    "enabled": true,
    "url": "https://<yourhookurl>",
    "format": "json",
    "status": {
        "msgtype": "text",
        "text": {
            "content": "Status update: {status}"
        }
    }
}
```

结果将是一个 POST 请求，例如 `{"msgtype":"text","text":{"content":"Status update: running"}}` 正文和 `Content-Type: application/json` 标头。

## 附加配置

`webhook.retries` 参数可以设置为 webhook 请求在失败时（即 HTTP 响应状态不是 200）应尝试的最大重试次数。默认情况下，这设置为 `0`，表示已禁用。可以设置额外的 `webhook.retry_delay` 参数来指定重试尝试之间的时间（以秒为单位）。默认情况下，这设置为 `0.1`（即 100 毫秒）。请注意，如果 webhook 存在连接问题，增加重试次数或重试延迟可能会减慢交易者速度。
您还可以指定 `webhook.timeout` - 这定义了机器人在假设其他主机无响应之前将等待多长时间（默认为 10 秒）。

重试的示例配置：

```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURHOOKURL>",
        "timeout": 10,
        "retries": 3,
        "retry_delay": 0.2,
        "status": {
            "status": "Status: {status}"
        }
    },
```

可以通过策略内的 `self.dp.send_msg()` 函数将自定义消息发送到 Webhook 端点。要启用此功能，请将 `allow_custom_messages` 选项设置为 `true`：

```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURHOOKURL>",
        "allow_custom_messages": true,
        "strategy_msg": {
            "status": "StrategyMessage: {msg}"
        }
    },
```

可以为不同事件配置不同的有效载荷。并非所有字段都是必需的，但您应该至少配置其中一个字典，否则 webhook 永远不会被调用。

## Webhook 消息类型

### 入场 / 入场成交

当机器人下达多头/空头订单以增加头寸时，或在该订单成交时，`webhook.entry` 和 `webhook.entry_fill` 中的字段将被填充。参数使用 string.format 填充。
可能的参数是：

* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* ~~`limit` # Deprecated - should no longer be used.~~
* `open_rate`
* `amount`
* `open_date`
* `stake_amount`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `order_type`
* `current_rate`
* `enter_tag`

### 入场取消

当机器人取消多头/空头订单时，`webhook.entry_cancel` 中的字段将被填充。参数使用 string.format 填充。
可能的参数是：

* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* `limit`
* `amount`
* `open_date`
* `stake_amount`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `order_type`
* `current_rate`
* `enter_tag`

### 出场 / 出场成交

当机器人下达出场订单时，或在该出场订单成交时，`webhook.exit` 和 `webhook.exit_fill` 中的字段将被填充。参数使用 string.format 填充。
可能的参数是：

* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* `gain`
* `amount`
* `open_rate`
* `close_rate`
* `current_rate`
* `profit_amount`
* `profit_ratio`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `enter_tag`
* `exit_reason`
* `order_type`
* `open_date`
* `close_date`
* `sub_trade`
* `is_final_exit`


### 出场取消

当机器人取消出场订单时，`webhook.exit_cancel` 中的字段将被填充。参数使用 string.format 填充。
可能的参数是：

* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* `gain`
* `order_rate`
* `amount`
* `open_rate`
* `current_rate`
* `profit_amount`
* `profit_ratio`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `exit_reason`
* `order_type`
* `open_date`
* `close_date`

### 状态

`webhook.status` 中的字段用于常规状态消息（已启动 / 已停止 / ...）。参数使用 string.format 填充。

这里唯一可能的值是 `{status}`。

## Discord

为 Discord 提供了一种特殊形式的 webhook。
您可以按如下方式配置：

```json
"discord": {
    "enabled": true,
    "webhook_url": "https://discord.com/api/webhooks/<Your webhook URL ...>",
    "exit_fill": [
        {"Trade ID": "{trade_id}"},
        {"Exchange": "{exchange}"},
        {"Pair": "{pair}"},
        {"Direction": "{direction}"},
        {"Open rate": "{open_rate}"},
        {"Close rate": "{close_rate}"},
        {"Amount": "{amount}"},
        {"Open date": "{open_date:%Y-%m-%d %H:%M:%S}"},
        {"Close date": "{close_date:%Y-%m-%d %H:%M:%S}"},
        {"Profit": "{profit_amount} {stake_currency}"},
        {"Profitability": "{profit_ratio:.2%}"},
        {"Enter tag": "{enter_tag}"},
        {"Exit Reason": "{exit_reason}"},
        {"Strategy": "{strategy}"},
        {"Timeframe": "{timeframe}"},
    ],
    "entry_fill": [
        {"Trade ID": "{trade_id}"},
        {"Exchange": "{exchange}"},
        {"Pair": "{pair}"},
        {"Direction": "{direction}"},
        {"Open rate": "{open_rate}"},
        {"Amount": "{amount}"},
        {"Open date": "{open_date:%Y-%m-%d %H:%M:%S}"},
        {"Enter tag": "{enter_tag}"},
        {"Strategy": "{strategy} {timeframe}"},
    ]
}
```

上面表示默认值（`exit_fill` 和 `entry_fill` 是可选的，将默认为上述配置）- 显然可以进行修改。
要禁用两个默认值中的任何一个（`entry_fill` / `exit_fill`），您可以将它们分配为空数组（`exit_fill: []`）。

可用字段对应于 webhook 的字段，并在相应的 webhook 部分中记录。

默认情况下，通知将如下所示。

![discord-notification](assets/discord_notification.png)

可以通过 dataprovider.send_msg() 函数从策略向 Discord 端点发送自定义消息。要启用此功能，请将 `allow_custom_messages` 选项设置为 `true`：

```json
  "discord": {
        "enabled": true,
        "webhook_url": "https://discord.com/api/webhooks/<Your webhook URL ...>",
        "allow_custom_messages": true,
    },
```
