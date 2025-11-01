# 交易对象

## Trade（交易）

freqtrade 进入的头寸存储在 `Trade` 对象中 - 该对象会持久化到数据库。
这是 freqtrade 的核心概念 - 您会在文档的许多部分中遇到它，这些部分很可能会指向此位置。

它将在许多[策略回调](strategy-callbacks.md)中传递给策略。传递给策略的对象不能直接修改。可能会根据回调结果进行间接修改。

## Trade - 可用属性

以下属性可用于每个单独的交易 - 可以与 `trade.<property>` 一起使用（例如 `trade.pair`）。

|  Attribute | DataType | Description |
|------------|-------------|-------------|
| `pair` | string | Pair of this trade. |
| `safe_base_currency` | string | Compatibility layer for base currency . |
| `safe_quote_currency` | string | Compatibility layer for quote currency. |
| `is_open` | boolean | Is the trade currently open, or has it been concluded. |
| `exchange` | string | Exchange where this trade was executed. |
| `open_rate` | float | Rate this trade was entered at (Avg. entry rate in case of trade-adjustments). |
| `open_rate_requested` | float | The rate that was requested when the trade was opened. |
| `open_trade_value` | float | Value of the open trade including fees. |
| `close_rate` | float | Close rate - only set when is_open = False. |
| `close_rate_requested` | float | The close rate that was requested. |
| `safe_close_rate` | float | Close rate or `close_rate_requested` or 0.0 if neither is available. Only makes sense once the trade is closed. |
| `stake_amount` | float | Amount in Stake (or Quote) currency. |
| `max_stake_amount` | float | Maximum stake amount that was used in this trade (sum of all filled Entry orders). |
| `amount` | float | Amount in Asset / Base currency that is currently owned. Will be 0.0 until the initial order fills. |
| `amount_requested` | float | Amount that was originally requested for this trade as part of the first entry order. |
| `open_date` | datetime | Timestamp when trade was opened **use `open_date_utc` instead** |
| `open_date_utc` | datetime | Timestamp when trade was opened - in UTC. |
| `close_date` | datetime | Timestamp when trade was closed **use `close_date_utc` instead** |
| `close_date_utc` | datetime | Timestamp when trade was closed - in UTC. |
| `close_profit` | float | Relative profit at the time of trade closure. `0.01` == 1% |
| `close_profit_abs` | float | Absolute profit (in stake currency) at the time of trade closure. |
| `realized_profit` | float | Absolute already realized profit (in stake currency) while the trade is still open. |
| `leverage` | float | Leverage used for this trade - defaults to 1.0 in spot markets. |
| `enter_tag` | string | Tag provided on entry via the `enter_tag` column in the dataframe. |
| `exit_reason` | string | Reason why the trade was exited. |
| `exit_order_status` | string | Status of the exit order. |
| `strategy` | string | Strategy name that was used for this trade. |
| `timeframe` | int | Timeframe used for this trade. |
| `is_short` | boolean | True for short trades, False otherwise. |
| `orders` | Order[] | List of order objects attached to this trade (includes both filled and cancelled orders). |
| `date_last_filled_utc` | datetime | Time of the last filled order. |
| `date_entry_fill_utc` | datetime | Date of the first filled entry order. |
| `entry_side` | "buy" / "sell" | Order Side the trade was entered. |
| `exit_side` | "buy" / "sell" | Order Side that will result in a trade exit / position reduction. |
| `trade_direction` | "long" / "short" | Trade direction in text - long or short. |
| `max_rate` | float | Highest price reached during this trade. Not 100% accurate. |
| `min_rate` | float | Lowest price reached during this trade. Not 100% accurate. |
| `nr_of_successful_entries` | int | Number of successful (filled) entry orders. |
| `nr_of_successful_exits` | int | Number of successful (filled) exit orders. |
| `has_open_position` | boolean | True if there is an open position (amount > 0) for this trade. Only false while the initial entry order is unfilled. |
| `has_open_orders` | boolean | Has the trade open orders (excluding stoploss orders). |
| `has_open_sl_orders` | boolean | True if there are open stoploss orders for this trade. |
| `open_orders` | Order[] | All open orders for this trade excluding stoploss orders. |
| `open_sl_orders` | Order[] | All open stoploss orders for this trade. |
| `fully_canceled_entry_order_count` | int | Number of fully canceled entry orders. |
| `canceled_exit_order_count` | int | Number of canceled exit orders. |

### Stop Loss related attributes

|  Attribute | DataType | Description |
|------------|-------------|-------------|
| `stop_loss` | float | Absolute value of the stop loss. |
| `stop_loss_pct` | float | Relative value of the stop loss. |
| `initial_stop_loss` | float | Absolute value of the initial stop loss. |
| `initial_stop_loss_pct` | float | Relative value of the initial stop loss. |
| `stoploss_last_update_utc` | datetime | Timestamp of the last stoploss on exchange order update. |
| `stoploss_or_liquidation` | float | Returns the more restrictive of stoploss or liquidation price and corresponds to the price a stoploss would trigger at. |

### 期货/保证金交易属性

|  属性 | 数据类型 | 描述 |
|------------|-------------|-------------|
| `liquidation_price` | float | 杠杆交易的清算价格。 |
| `interest_rate` | float | 保证金交易的利率。 |
| `funding_fees` | float | 期货交易的总资金费率。 |

## 类方法

以下是类方法 - 它们返回通用信息，通常会导致对数据库的显式查询。
它们可以作为 `Trade.<method>` 使用 - 例如 `open_trades = Trade.get_open_trade_count()`

!!! Warning "回测/超参数优化"
    大多数方法在回测/超参数优化和实盘/模拟模式下都能工作。
    在回测期间，它仅限于在[策略回调](strategy-callbacks.md)中使用。在 `populate_*()` 方法中使用不受支持，将导致错误的结果。

### get_trades_proxy

当您的策略需要有关现有（开放或关闭）交易的一些信息时 - 最好使用 `Trade.get_trades_proxy()`。

用法：

``` python
from freqtrade.persistence import Trade
from datetime import timedelta

# ...
trade_hist = Trade.get_trades_proxy(pair='ETH/USDT', is_open=False, open_date=current_date - timedelta(days=2))

```

`get_trades_proxy()` 支持以下关键字参数。所有参数都是可选的 - 不带参数调用 `get_trades_proxy()` 将返回数据库中的所有交易列表。

* `pair` 例如 `pair='ETH/USDT'`
* `is_open` 例如 `is_open=False`
* `open_date` 例如 `open_date=current_date - timedelta(days=2)`
* `close_date` 例如 `close_date=current_date - timedelta(days=5)`

### get_open_trade_count

获取当前开放交易的数量

``` python
from freqtrade.persistence import Trade
# ...
open_trades = Trade.get_open_trade_count()
```

### get_total_closed_profit

检索机器人到目前为止产生的总利润。
汇总所有已关闭交易的 `close_profit_abs`。

``` python
from freqtrade.persistence import Trade

# ...
profit = Trade.get_total_closed_profit()
```

### total_open_trades_stakes

检索当前交易中的总 stake_amount。

``` python
from freqtrade.persistence import Trade

# ...
profit = Trade.total_open_trades_stakes()
```

## 回测/超参数优化中不支持的类方法

以下类方法在回测/超参数优化模式下不受支持。

### get_overall_performance

检索整体性能 - 类似于 `/performance` telegram 命令。

``` python
from freqtrade.persistence import Trade

# ...
if self.config['runmode'].value in ('live', 'dry_run'):
    performance = Trade.get_overall_performance()
```

示例返回值：ETH/BTC 有 5 笔交易，总利润为 1.5%（比率为 0.015）。

``` json
{"pair": "ETH/BTC", "profit": 0.015, "count": 5}
```

### get_trading_volume

根据订单获取总交易量。

``` python
from freqtrade.persistence import Trade

# ...
volume = Trade.get_trading_volume()
```

## 订单对象

`Order` 对象表示交易所上的订单（或模拟模式下的模拟订单）。
`Order` 对象将始终与其对应的 [`Trade`](#trade-object) 绑定，并且仅在交易上下文中才有意义。

### Order - 可用属性

订单对象通常附加到交易。
这里的大多数属性可以是 None，因为它们依赖于交易所响应。

|  Attribute | DataType | Description |
|------------|-------------|-------------|
| `trade` | Trade | Trade object this order is attached to |
| `ft_pair` | string | Pair this order is for |
| `ft_is_open` | boolean | is the order still open? |
| `ft_order_side` | string | Order side ('buy', 'sell', or 'stoploss') |
| `ft_cancel_reason` | string | Reason why the order was canceled |
| `ft_order_tag` | string | Custom order tag |
| `order_id` | string | Exchange order ID |
| `order_type` | string | Order type as defined on the exchange - usually market, limit or stoploss |
| `status` | string | Status as defined by [ccxt's order structure](https://docs.ccxt.com/#/README?id=order-structure). Usually open, closed, expired, canceled or rejected |
| `side` | string | buy or sell |
| `price` | float | Price the order was placed at |
| `average` | float | Average price the order filled at |
| `amount` | float | Amount in base currency |
| `filled` | float | Filled amount (in base currency) (use `safe_filled` instead) |
| `safe_filled` | float | Filled amount (in base currency) - guaranteed to not be None |
| `safe_amount` | float | Amount - falls back to ft_amount if None |
| `safe_price` | float | Price - falls back through average, price, stop_price, ft_price |
| `safe_placement_price` | float | Price at which the order was placed |
| `remaining` | float | Remaining amount (use `safe_remaining` instead) |
| `safe_remaining` | float | Remaining amount - either taken from the exchange or calculated. |
| `safe_cost` | float | Cost of the order - guaranteed to not be None |
| `safe_fee_base` | float | Fee in base currency - guaranteed to not be None |
| `safe_amount_after_fee` | float | Amount after deducting fees |
| `cost` | float | Cost of the order - usually average * filled (*Exchange dependent on futures trading, may contain the cost with or without leverage and may be in contracts.*) |
| `stop_price` | float | Stop price for stop orders. Empty for non-stoploss orders. |
| `stake_amount` | float | Stake amount used for this order. |
| `stake_amount_filled` | float | Filled Stake amount used for this order. |
| `order_date` | datetime | Order creation date **use `order_date_utc` instead** |
| `order_date_utc` | datetime | Order creation date (in UTC) |
| `order_filled_date` | datetime |  Order fill date **use `order_filled_utc` instead** |
| `order_filled_utc` | datetime | Order fill date |
| `order_update_date` | datetime | Last order update date |
