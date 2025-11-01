# 止损

`stoploss` 配置参数是应触发卖出的损失比率。
例如，值 `-0.10` 将在给定交易的利润低于 -10% 时立即卖出。此参数是可选的。
止损计算确实包括手续费，因此 -10% 的止损正好放在入场点下方 10% 处。

大多数策略文件已包含最佳 `stoploss` 值。

!!! Info "信息"
    本文件中提到的所有止损属性可以在策略中或在配置中设置。
    <ins>配置值将覆盖策略值。</ins>

## 交易所止损 / Freqtrade 止损

这些止损模式可以是*交易所上*或*交易所外*。

可以使用以下值配置这些模式：

``` python
    'emergency_exit': 'market',
    'stoploss_on_exchange': False
    'stoploss_on_exchange_interval': 60,
    'stoploss_on_exchange_limit_ratio': 0.99
```

交易所止损仅支持以下交易所，并非所有交易所都支持止损限价和止损市价。
如果只有一种模式可用，订单类型将被忽略。

??? info "Supported exchanges and stoploss types"
    
    --8<-- "includes/exchange-features.md"

!!! Note "紧密止损"
    <ins>使用交易所止损时，不要设置太低/太紧的止损值！</ins>
    如果设置得太低/太紧，您将面临订单无法成交的更大风险，止损将不起作用。

### stoploss_on_exchange 和 stoploss_on_exchange_limit_ratio

启用或禁用交易所止损。
如果止损在*交易所上*，这意味着在买入订单成交后立即在交易所放置止损限价订单。这将保护您免受市场突然崩盘的影响，因为订单执行完全在交易所内进行，没有潜在的网络开销。

如果 `stoploss_on_exchange` 使用限价订单，交易所需要 2 个价格，止损价格和限价。
`stoploss` 定义放置限价订单的止损价格 - 限价应略低于此价格。
如果交易所同时支持限价和市价止损订单，则 `stoploss` 的值将用于确定止损类型。

计算示例：我们以 100\$ 购买资产。
止损价格为 95\$，则限价将是 `95 * 0.99 = 94.05$` - 因此限价订单成交可能发生在 95$ 和 94.05$ 之间。

例如，假设止损在交易所上，并且启用了追踪止损，市场正在上涨，那么机器人会自动取消先前的止损订单并放置一个新的止损值高于先前止损订单的订单。

!!! Note "注意"
    如果启用了 `stoploss_on_exchange` 并且在交易所手动取消了止损，则机器人将创建新的止损订单。

### stoploss_on_exchange_interval

对于交易所止损，还有另一个参数称为 `stoploss_on_exchange_interval`。这配置了机器人检查止损并在必要时更新的间隔（以秒为单位）。
机器人不能每 5 秒（每次迭代）执行这些操作，否则它会被交易所封禁。
因此，此参数将告诉机器人应该多久更新一次止损订单。默认值为 60（1 分钟）。
如果您意外取消止损订单，此相同逻辑将在交易所上重新应用止损订单。

### stoploss_price_type

!!! Warning "仅适用于期货"
    `stoploss_price_type` 仅适用于期货市场（在支持的交易所上）。
    Freqtrade 将在启动时验证此设置，如果为您的交易所选择了无效设置，将无法启动。
    支持的价格类型因交易所而异。请与您的交易所确认它支持哪些价格类型。

期货市场上的交易所止损可以在不同的价格类型上触发。
交易所术语中这些价格的命名通常不同，但通常围绕"last"（或"contract price"）、"mark"和"index"。

此设置的可接受值是 `"last"`、`"mark"` 和 `"index"` - freqtrade 将自动将其转换为相应的 API 类型，并相应地放置[交易所止损](#stoploss_on_exchange-and-stoploss_on_exchange_limit_ratio)订单。

### force_exit

`force_exit` 是一个可选值，默认与 `exit` 相同，在从 Telegram 或 Rest API 发送 `/forceexit` 命令时使用。

### force_entry

`force_entry` 是一个可选值，默认与 `entry` 相同，在从 Telegram 或 Rest API 发送 `/forceentry` 命令时使用。

### emergency_exit

`emergency_exit` 是一个可选值，默认为 `market`，在创建交易所止损订单失败时使用。
以下是如果在策略或配置文件中未更改则使用的默认值。

策略文件示例：

``` python
order_types = {
    "entry": "limit",
    "exit": "limit",
    "emergency_exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": True,
    "stoploss_on_exchange_interval": 60,
    "stoploss_on_exchange_limit_ratio": 0.99
}
```

## 止损类型

目前机器人包含以下止损支持模式：

1. 静态止损。
2. 追踪止损。
3. 追踪止损，自定义正亏损。
4. 仅在交易达到某个偏移后追踪止损。
5. [自定义止损函数](strategy-callbacks.md#custom-stoploss)

### 静态止损

这非常简单，您定义止损为 x（作为价格的比率，即价格的 x * 100%）。一旦损失超过定义的损失，这将尝试卖出资产。

止损示例：

``` python
    stoploss = -0.10
```

例如，简化数学：

* 机器人以 100$ 的价格购买资产
* 止损定义为 -10%
* 一旦资产跌破 90$，止损将被触发

### 追踪止损

此的初始值是 `stoploss`，就像您定义静态止损一样。
要启用追踪止损：

``` python
    stoploss = -0.10
    trailing_stop = True
```

这将激活一个算法，每次资产价格上涨时自动向上移动止损。

例如，简化数学：

* 机器人以 100$ 的价格购买资产
* 止损定义为 -10%
* 一旦资产跌破 90$，止损将被触发
* 假设资产现在增加到 102$
* 止损现在将是 102$ 的 -10% = 91.8$
* 现在资产价值下降到 101\$，止损仍将是 91.8$，并将在 91.8$ 触发。

总结：止损将调整为始终是最观察价格的 -10%。

### 追踪止损，不同的正亏损

您也可以在买入处于亏损状态（买入 - 手续费）时设置默认止损，但一旦达到正收益（或您定义的偏移），系统将使用具有不同值的新止损。
例如，您的默认止损是 -10%，但一旦达到盈利（例如 0.1%），将使用不同的追踪止损。

!!! Note "注意"
    如果您希望止损仅在达到盈亏平衡或盈利时更改（大多数用户想要的），请参阅下一节，启用[偏移](#trailing-stop-loss-only-once-the-trade-has-reached-a-certain-offset)。

这两个值都需要将 `trailing_stop` 设置为 true，并且 `trailing_stop_positive` 具有值。

``` python
    stoploss = -0.10
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.0
    trailing_only_offset_is_reached = False  # 默认 - 此示例不需要
```

例如，简化数学：

* 机器人以 100$ 的价格购买资产
* 止损定义为 -10%
* 一旦资产跌破 90$，止损将被触发
* 假设资产现在增加到 102$
* 止损现在将是 102$ 的 -2% = 99.96$（99.96$ 止损将被锁定，并将跟随资产价格上涨，保持 -2%）
* 现在资产价值下降到 101\$，止损仍将是 99.96$，并将在 99.96$ 触发

0.02 将转换为 -2% 止损。
在此之前，`stoploss` 用于追踪止损。

!!! Tip "使用偏移来更改止损"
    使用 `trailing_stop_positive_offset` 通过将 `trailing_stop_positive_offset` 设置为高于 `trailing_stop_positive` 来确保您的新追踪止损将处于盈利状态。然后，您的第一个新止损值将已经锁定利润。

    简化数学示例：

    ``` python
        stoploss = -0.10
        trailing_stop = True
        trailing_stop_positive = 0.02
        trailing_stop_positive_offset = 0.03
    ```

    * 机器人以 100$ 的价格购买资产
    * 止损定义为 -10%，因此一旦资产跌破 90$，止损将被触发
    * 假设资产现在增加到 102$
    * 止损现在将在 91.8$ - 最高观察价格的 10% 以下
    * 假设资产现在增加到 103.5$（高于配置的偏移）
    * 止损现在将是 103.5$ 的 -2% = 101.43$
    * 现在资产价值下降到 102\$，止损仍将是 101.43$，一旦价格跌破 101.43$ 将触发

### 仅在交易达到某个偏移后追踪止损

您也可以保持静态止损直到达到偏移，然后在市场转向时追踪交易以获利。

如果 `trailing_only_offset_is_reached = True`，则仅在达到偏移后激活追踪止损。在此之前，止损保持在配置的 `stoploss` 处，不追踪。
将此值保留为 `trailing_only_offset_is_reached=False` 将允许追踪止损在资产价格超过初始入场价格时立即开始追踪。

此选项可以与或没有 `trailing_stop_positive` 一起使用，但使用 `trailing_stop_positive_offset` 作为偏移。

配置（偏移是买入价格 + 3%）：

``` python
    stoploss = -0.10
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True
```

例如，简化数学：

* 机器人以 100$ 的价格购买资产
* 止损定义为 -10%
* 一旦资产跌破 90$，止损将被触发
* 除非资产增加到配置的偏移或以上，止损将保持在 90$
* 假设资产现在增加到 103$（我们配置偏移的地方）
* 止损现在将是 103$ 的 -2% = 100.94$
* 现在资产价值下降到 101\$，止损仍将是 100.94$，并将在 100.94$ 触发

!!! Tip "提示"
    确保此值（`trailing_stop_positive_offset`）低于最小 ROI，否则最小 ROI 将首先应用并卖出交易。

## 止损和杠杆

止损应该被视为"此交易的风险" - 因此，100$ 交易上 10% 的止损意味着您愿意在此交易上损失 10$（10%） - 如果价格向下跌 10%，这将触发。

使用杠杆时，应用相同的原则 - 止损定义交易的风险（您愿意损失的金额）。

因此，10 倍交易上 10% 的止损将在价格移动 1% 时触发。
如果您的入金金额（自有资金）是 100$ - 此交易在 10 倍（杠杆后）将是 1000$。
如果价格移动 1% - 您已经损失了 10$ 的自有资金 - 因此在这种情况下止损将触发。

请务必了解这一点，并避免使用太紧的止损（在 10 倍杠杆下，10% 的风险可能太少，无法让交易"呼吸"一点）。

## 更改未平仓交易的止损

可以通过更改配置或策略中的值并使用 `/reload_config` 命令来更改未平仓交易的止损（或者，完全停止并重新启动机器人也可以）。

新的止损值将应用于未平仓交易（并将生成相应的日志消息）。

### Limitations

Stoploss values cannot be changed if `trailing_stop` is enabled and the stoploss has already been adjusted.
