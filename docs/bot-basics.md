# Freqtrade 基础知识

本页为您介绍 Freqtrade 工作原理和操作的基本概念。

## Freqtrade 术语

* **策略**：您的交易策略，告诉机器人该做什么。
* **交易**：未平仓头寸。
* **未完成订单**：当前已放置在交易所但尚未完成的订单。
* **交易对**：可交易的交易对，通常格式为 Base/Quote（例如现货为 `XRP/USDT`，期货为 `XRP/USDT:USDT`）。
* **时间框架**：使用的蜡烛图长度（例如 `"5m"`、`"1h"` 等）。
* **指标**：技术指标（SMA、EMA、RSI 等）。
* **限价单**：以定义的限价或更优价格执行的限价订单。
* **市价单**：保证成交，可能根据订单大小影响价格。
* **当前利润**：当前待实现（未实现）的利润。这主要在机器人和 UI 中使用。
* **已实现利润**：已实现的利润。仅与[部分退出](strategy-callbacks.md#adjust-trade-position)相关，这也解释了其计算逻辑。
* **总利润**：已实现和未实现利润的总和。相对数字（%）根据该交易的总投资计算。

## 手续费处理

Freqtrade 的所有利润计算都包括手续费。对于回测/超参数优化/模拟运行模式，使用交易所默认手续费（交易所最低层级）。对于实盘操作，使用交易所应用的手续费（包括 BNB 返佣等）。

## 交易对命名

Freqtrade 遵循 [ccxt 命名约定](https://docs.ccxt.com/#/README?id=consistency-of-base-and-quote-currencies)进行货币命名。
在错误的市场上使用错误的命名约定通常会导致机器人无法识别交易对，通常会出现"此交易对不可用"等错误。

### 现货交易对命名

对于现货交易对，命名格式为 `base/quote`（例如 `ETH/USDT`）。

### 期货交易对命名

对于期货交易对，命名格式为 `base/quote:settle`（例如 `ETH/USDT:USDT`）。

## 机器人执行逻辑

在模拟运行或实盘模式下启动 freqtrade（使用 `freqtrade trade`）将启动机器人并开始机器人迭代循环。
这也会运行 `bot_start()` 回调函数。

默认情况下，机器人循环每几秒运行一次（`internals.process_throttle_secs`）并执行以下操作：

* 从持久化存储中获取未平仓交易。
* 计算当前可交易交易对列表。
* 为交易对列表下载 OHLCV 数据，包括所有[信息交易对](strategy-customization.md#get-data-for-non-tradeable-pairs)
  此步骤每个蜡烛图仅执行一次，以避免不必要的网络流量。
* 调用 `bot_loop_start()` 策略回调。
* 按交易对分析策略。
  * 调用 `populate_indicators()`
  * 调用 `populate_entry_trend()`
  * 调用 `populate_exit_trend()`
* 从交易所更新交易的未完成订单状态。
  * 对已成交订单调用 `order_filled()` 策略回调。
  * 检查未完成订单的超时。
    * 对未完成的入场订单调用 `check_entry_timeout()` 策略回调。
    * 对未完成的出场订单调用 `check_exit_timeout()` 策略回调。
    * 对未完成订单调用 `adjust_order_price()` 策略回调。
      * 对未完成的入场订单调用 `adjust_entry_price()` 策略回调。*仅在未实现 `adjust_order_price()` 时调用*
      * 对未完成的出场订单调用 `adjust_exit_price()` 策略回调。*仅在未实现 `adjust_order_price()` 时调用*
* 验证现有头寸并最终下出场订单。
  * 考虑止损、ROI 和出场信号、`custom_exit()` 和 `custom_stoploss()`。
  * 根据 `exit_pricing` 配置设置或使用 `custom_exit_price()` 回调确定出场价格。
  * 在下出场订单之前，调用 `confirm_trade_exit()` 策略回调。
* 如果启用，检查未平仓交易的头寸调整，调用 `adjust_trade_position()` 并在需要时下额外订单。
* 检查交易槽位是否仍可用（如果达到 `max_open_trades`）。
* 验证入场信号，尝试进入新头寸。
  * 根据 `entry_pricing` 配置设置或使用 `custom_entry_price()` 回调确定入场价格。
  * 在保证金和期货模式下，调用 `leverage()` 策略回调以确定所需杠杆。
  * 通过调用 `custom_stake_amount()` 回调确定投注大小。
  * 在下入场订单之前，调用 `confirm_trade_entry()` 策略回调。

此循环将反复执行，直到机器人停止。

## 回测 / 超参数优化执行逻辑

[回测](backtesting.md) 或 [超参数优化](hyperopt.md) 仅执行上述逻辑的一部分，因为大多数交易操作都是完全模拟的。

* 为配置的交易对列表加载历史数据。
* 调用一次 `bot_start()`。
* 计算指标（每个交易对调用一次 `populate_indicators()`）。
* 计算入场/出场信号（每个交易对调用一次 `populate_entry_trend()` 和 `populate_exit_trend()`）。
* 按蜡烛图循环模拟入场和出场点。
  * 调用 `bot_loop_start()` 策略回调。
  * 检查订单超时，通过 `unfilledtimeout` 配置或 `check_entry_timeout()` / `check_exit_timeout()` 策略回调。
  * 对未完成订单调用 `adjust_order_price()` 策略回调。
    * 对未完成的入场订单调用 `adjust_entry_price()` 策略回调。*仅在未实现 `adjust_order_price()` 时调用！*
    * 对未完成的出场订单调用 `adjust_exit_price()` 策略回调。*仅在未实现 `adjust_order_price()` 时调用！*
  * 检查交易入场信号（`enter_long` / `enter_short` 列）。
  * 确认交易入场/出场（如果策略中已实现，则调用 `confirm_trade_entry()` 和 `confirm_trade_exit()`）。
  * 调用 `custom_entry_price()`（如果策略中已实现）以确定入场价格（价格会移动到开盘蜡烛图内）。
  * 在保证金和期货模式下，调用 `leverage()` 策略回调以确定所需杠杆。
  * 通过调用 `custom_stake_amount()` 回调确定投注大小。
  * 如果启用，检查未平仓交易的头寸调整，调用 `adjust_trade_position()` 以确定是否需要额外订单。
  * 对已成交的入场订单调用 `order_filled()` 策略回调。
  * 调用 `custom_stoploss()` 和 `custom_exit()` 以查找自定义出场点。
  * 对于基于出场信号、自定义出场和部分退出的退出：调用 `custom_exit_price()` 以确定出场价格（价格会移动到收盘蜡烛图内）。
  * 对已成交的出场订单调用 `order_filled()` 策略回调。
* 生成回测报告输出

!!! Note "注意"
    回测和超参数优化都包括交易所默认手续费的计算。可以通过指定 `--fee` 参数将自定义手续费传递给回测/超参数优化。

!!! Warning "回调调用频率"
    回测最多每个蜡烛图调用一次每个回调（`--timeframe-detail` 会将此行为修改为每个详细蜡烛图一次）。
    大多数回调在实盘中每次迭代调用一次（通常每 ~5 秒）- 这可能导致回测不匹配。
