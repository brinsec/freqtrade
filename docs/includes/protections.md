## 保护

保护将通过暂时停止一个交易对或所有交易对的交易来保护您的策略免受意外事件和市场条件的影响。
所有保护结束时间都会向上舍入到下一个蜡烛，以避免突然、意外的蜡烛内买入。

!!! Tip "使用提示"
    并非所有保护都适用于所有策略，需要为您的策略调整参数以提高性能。
  
    每个保护都可以使用不同参数配置多次，以允许不同级别的保护（短期/长期）。

!!! Note "回测"
    回测和超参数优化支持保护，但必须通过使用 `--enable-protections` 标志显式启用。

### 可用的保护

* [`StoplossGuard`](#stoploss-guard) 如果在某个时间窗口内发生一定数量的止损，则停止交易。
* [`MaxDrawdown`](#maxdrawdown) 如果达到最大回撤，则停止交易。
* [`LowProfitPairs`](#low-profit-pairs) 锁定利润较低的交易对
* [`CooldownPeriod`](#cooldown-period) 卖出交易后不要立即进入交易。

### 所有保护的通用设置

|  参数 | 描述 |
|------------|-------------|
| `method` | 要使用的保护名称。<br> **数据类型：** String，从[可用的保护](#available-protections)中选择
| `stop_duration_candles` | 锁定应该设置多少个蜡烛？<br> **数据类型：** 正整数（以蜡烛为单位）
| `stop_duration` | 保护应该锁定多少分钟。<br>不能与 `stop_duration_candles` 一起使用。<br> **数据类型：** Float（以分钟为单位）
| `lookback_period_candles` | 只有在过去 `lookback_period_candles` 蜡烛内完成的交易才会被考虑。某些保护可能会忽略此设置。<br> **数据类型：** 正整数（以蜡烛为单位）。
| `lookback_period` | 只有 `current_time - lookback_period` 之后完成的交易才会被考虑。<br>不能与 `lookback_period_candles` 一起使用。<br>某些保护可能会忽略此设置。<br> **数据类型：** Float（以分钟为单位）
| `trade_limit` | 所需的最少交易数（并非所有保护都使用）。<br> **数据类型：** 正整数
| `unlock_at` | 交易将定期解锁的时间（并非所有保护都使用）。<br> **数据类型：** string <br>**输入格式：** "HH:MM"（24 小时制）

!!! Note "持续时间"
    持续时间（`stop_duration*` 和 `lookback_period*` 可以用分钟或蜡烛定义）。
    为了在测试不同时间框架时获得更大的灵活性，下面的所有示例都将使用"蜡烛"定义。

#### 止损保护

`StoplossGuard` 选择在 `lookback_period` 分钟内（或使用 `lookback_period_candles` 时的蜡烛数内）的所有交易。
如果 `trade_limit` 或更多交易导致止损，交易将停止 `stop_duration` 分钟（或使用 `stop_duration_candles` 时的蜡烛数，或使用 `unlock_at` 时直到设定时间）。

这适用于所有交易对，除非 `only_per_pair` 设置为 true，这将一次只查看一个交易对。

同样，此保护默认将查看所有交易（多头和空头）。对于期货机器人，设置 `only_per_side` 将使机器人只考虑一侧，然后只锁定这一侧，允许例如在一系列多头止损后继续空头。

`required_profit` 将确定止损考虑所需的相对利润（或损失）。这通常不应该设置，默认为 0.0 - 这意味着所有亏损的止损都将触发锁定。

下面的示例如果机器人在过去 24 个蜡烛内触发了 4 次止损，则在最后一次交易后停止所有交易对交易 4 个蜡烛。

``` python
@property
def protections(self):
    return [
        {
            "method": "StoplossGuard",
            "lookback_period_candles": 24,
            "trade_limit": 4,
            "stop_duration_candles": 4,
            "required_profit": 0.0,
            "only_per_pair": False,
            "only_per_side": False
        }
    ]
```

!!! Note "注意"
    `StoplossGuard` 考虑所有结果为 `"stop_loss"`、`"stoploss_on_exchange"` 和 `"trailing_stop_loss"` 的交易，如果结果利润为负。
    `trade_limit` 和 `lookback_period` 需要为您的策略进行调整。

#### 最大回撤

`MaxDrawdown` 使用 `lookback_period` 分钟内（或使用 `lookback_period_candles` 时的蜡烛数内）的所有交易来确定最大回撤。如果回撤低于 `max_allowed_drawdown`，交易将在最后一次交易后停止 `stop_duration` 分钟（或使用 `stop_duration_candles` 时的蜡烛数）- 假设机器人需要一些时间让市场恢复。

下面的示例如果在过去 48 个蜡烛内考虑所有交易对 - 最少 `trade_limit` 笔交易 - 最大回撤 > 20%，则停止交易 12 个蜡烛。如果需要，可以使用 `lookback_period` 和/或 `stop_duration`。

``` python
@property
def protections(self):
    return  [
        {
            "method": "MaxDrawdown",
            "lookback_period_candles": 48,
            "trade_limit": 20,
            "stop_duration_candles": 12,
            "max_allowed_drawdown": 0.2
        },
    ]
```

#### 低利润交易对

`LowProfitPairs` 使用交易对在 `lookback_period` 分钟内（或使用 `lookback_period_candles` 时的蜡烛数内）的所有交易来确定总体利润比率。
如果该比率低于 `required_profit`，该交易对将被锁定 `stop_duration` 分钟（或使用 `stop_duration_candles` 时的蜡烛数，或使用 `unlock_at` 时直到设定时间）。

对于期货机器人，设置 `only_per_side` 将使机器人只考虑一侧，然后只锁定这一侧，允许例如在一系列多头亏损后继续空头。

下面的示例如果交易对在过去 6 个蜡烛内没有达到所需的 2% 利润（并且最少 2 笔交易），则将停止交易该交易对 60 分钟。

``` python
@property
def protections(self):
    return [
        {
            "method": "LowProfitPairs",
            "lookback_period_candles": 6,
            "trade_limit": 2,
            "stop_duration": 60,
            "required_profit": 0.02,
            "only_per_pair": False,
        }
    ]
```

#### 冷却期

`CooldownPeriod` 在退出后锁定交易对 `stop_duration` 分钟（或使用 `stop_duration_candles` 时的蜡烛数，或使用 `unlock_at` 时直到设定时间），避免该交易对在 `stop_duration` 分钟内重新进入。

下面的示例将在关闭交易后停止交易该交易对 2 个蜡烛，允许该交易对"冷却"。

``` python
@property
def protections(self):
    return  [
        {
            "method": "CooldownPeriod",
            "stop_duration_candles": 2
        }
    ]
```

!!! Note "注意"
    此保护仅在交易对级别应用，永远不会全局锁定所有交易对。
    此保护不考虑 `lookback_period`，因为它只查看最新交易。

### 保护的完整示例

所有保护都可以随意组合，也可以使用不同的参数，为表现不佳的交易对创建一个递增的壁垒。
所有保护都按照它们定义的顺序进行评估。

下面的示例假设时间框架为 1 小时：

* 在卖出后为每个交易对额外锁定 5 个蜡烛（`CooldownPeriod`），给其他交易对一个成交的机会。
* 如果过去 2 天（`48 * 1h 蜡烛`）有 20 笔交易，导致最大回撤超过 20%，则停止交易 4 小时（`4 * 1h 蜡烛`）。（`MaxDrawdown`）。
* 如果所有交易对在 1 天（`24 * 1h 蜡烛`）内发生超过 4 次止损，则停止交易（`StoplossGuard`）。
* 锁定在过去 6 小时（`6 * 1h 蜡烛`）内有 2 笔交易且合并利润比率低于 0.02（<2%）的所有交易对（`LowProfitPairs`）。
* 锁定在过去 24 小时（`24 * 1h 蜡烛`）内利润低于 0.01（<1%）的所有交易对 2 个蜡烛，最少 4 笔交易。

``` python
from freqtrade.strategy import IStrategy

class AwesomeStrategy(IStrategy)
    timeframe = '1h'
    
    @property
    def protections(self):
        return [
            {
                "method": "CooldownPeriod",
                "stop_duration_candles": 5
            },
            {
                "method": "MaxDrawdown",
                "lookback_period_candles": 48,
                "trade_limit": 20,
                "stop_duration_candles": 4,
                "max_allowed_drawdown": 0.2
            },
            {
                "method": "StoplossGuard",
                "lookback_period_candles": 24,
                "trade_limit": 4,
                "stop_duration_candles": 2,
                "only_per_pair": False
            },
            {
                "method": "LowProfitPairs",
                "lookback_period_candles": 6,
                "trade_limit": 2,
                "stop_duration_candles": 60,
                "required_profit": 0.02
            },
            {
                "method": "LowProfitPairs",
                "lookback_period_candles": 24,
                "trade_limit": 4,
                "stop_duration_candles": 2,
                "required_profit": 0.01
            }
        ]
    # ...
```
