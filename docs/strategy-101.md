# Freqtrade 策略 101：策略开发快速入门

为了本快速入门的目的，我们假设您熟悉交易的基础知识，并已阅读 [Freqtrade 基础知识](bot-basics.md) 页面。

## 所需知识

Freqtrade 中的策略是一个 Python 类，定义了买卖加密货币 `资产` 的逻辑。

资产定义为 `交易对`，代表 `币种` 和 `投注货币`。币种是您使用另一种货币作为投注货币进行交易的资产。

数据由交易所以 `蜡烛图` 的形式提供，由六个值组成：`date`、`open`、`high`、`low`、`close` 和 `volume`。

`技术分析` 函数使用各种计算和统计公式分析蜡烛图数据，并产生称为 `指标` 的次要值。

在资产交易对的蜡烛图上分析指标以生成 `信号`。

信号在加密货币 `交易所` 上转换为 `订单`，即 `交易`。

我们使用 `入场` 和 `出场` 术语而不是 `买入` 和 `卖出`，因为 Freqtrade 支持 `多头` 和 `空头` 交易。

- **多头**：您基于投注货币购买币种，例如使用 USDT 作为您的投注货币购买币种 BTC，通过以高于您支付的价格出售币种来获利。在多头交易中，利润是通过币种价值相对于投注货币上涨来实现的。
- **空头**：您从交易所借入币种形式的资本，稍后偿还币种的投注货币价值。在空头交易中，利润是通过币种价值相对于投注货币下跌来实现的（您以较低的利率偿还贷款）。

虽然 Freqtrade 支持某些交易所的现货和期货市场，但为了简单起见，我们只关注现货（多头）交易。

## 基本策略的结构

### 主数据框

Freqtrade 策略使用称为 `dataframe` 的行列表格数据结构来生成入场和出场交易的信号。

您配置的交易对列表中的每个交易对都有自己的 dataframe。Dataframes 由 `date` 列索引，例如 `2024-06-31 12:00`。

接下来的 5 列代表 `open`、`high`、`low`、`close` 和 `volume`（OHLCV）数据。

### 填充指标值

`populate_indicators` 函数向 dataframe 添加表示技术分析指标值的列。

常见指标的示例包括相对强弱指数、布林带、资金流量指数、移动平均线和平均真实波幅。

通过调用技术分析函数（例如 ta-lib 的 RSI 函数 `ta.RSI()`）并将它们分配给列名（例如 `rsi`）来向 dataframe 添加列。

```python
dataframe['rsi'] = ta.RSI(dataframe)
```

??? Hint "技术分析库"
    不同的库以不同的方式生成指标值。请查看每个库的文档以了解如何将其集成到您的策略中。您还可以查看 [Freqtrade 示例策略](https://github.com/freqtrade/freqtrade-strategies) 以获得想法。

### 填充入场信号

`populate_entry_trend` 函数定义入场信号的条件。

向 dataframe 添加 dataframe 列 `enter_long`，当此列中的值为 `1` 时，Freqtrade 看到一个入场信号。

??? Hint "做空"
    要进入空头交易，请使用 `enter_short` 列。

### 填充出场信号

`populate_exit_trend` 函数定义出场信号的条件。

向 dataframe 添加 dataframe 列 `exit_long`，当此列中的值为 `1` 时，Freqtrade 看到一个出场信号。

??? Hint "做空"
    要退出空头交易，请使用 `exit_short` 列。

## 一个简单的策略

这是一个 Freqtrade 策略的最小示例：

```python
from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta

class MyStrategy(IStrategy):

    timeframe = '15m'

    # 将初始止损设置为 -10%
    stoploss = -0.10

    # 当利润大于 1% 时随时退出盈利头寸
    minimal_roi = {"0": 0.01}

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 生成技术分析指标的值
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 根据指标值生成入场信号
        dataframe.loc[
            (dataframe['rsi'] < 30),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 根据指标值生成出场信号
        dataframe.loc[
            (dataframe['rsi'] > 70),
            'exit_long'] = 1

        return dataframe
```

## 进行交易

当找到信号时（入场或出场列中的 `1`），Freqtrade 将尝试下订单，即 `交易` 或 `头寸`。

每个新交易头寸占用一个 `槽位`。槽位表示可以打开的并发新交易的最大数量。

槽位的数量由 `max_open_trades` [配置](configuration.md) 选项定义。

但是，可能存在一系列场景，其中生成信号并不总是创建交易订单。这些包括：

- 没有足够的剩余投注金额来购买资产，或钱包中的资金来出售资产（包括任何手续费）
- 没有足够的剩余空闲槽位来打开新交易（您打开的头寸数量等于 `max_open_trades` 选项）
- 交易对已经有未平仓交易（Freqtrade 不能堆叠头寸 - 但它可以 [调整现有头寸](strategy-callbacks.md#adjust-trade-position)）
- 如果同一根蜡烛上存在入场和出场信号，它们被认为是 [冲突](strategy-customization.md#colliding-signals)，不会下订单
- 策略由于您通过使用相关的 [入场](strategy-callbacks.md#trade-entry-buy-order-confirmation) 或 [出场](strategy-callbacks.md#trade-exit-sell-order-confirmation) 回调之一指定的逻辑而主动拒绝交易订单

阅读 [策略定制](strategy-customization.md) 文档了解更多详情。

## 回测和前瞻测试

策略开发可能是一个漫长且令人沮丧的过程，因为将我们人类的"直觉"转化为有效的计算机控制（"算法"）策略并不总是直截了当的。

因此，应该测试策略以验证它是否按预期工作。

Freqtrade 有两种测试模式：

- **回测**：使用您[从交易所下载](data-download.md)的历史数据，回测是评估策略性能的快速方法。然而，很容易扭曲结果，使策略看起来比实际情况更有利可图。查看 [回测文档](backtesting.md) 了解更多信息。
- **模拟运行**：通常称为_前瞻测试_，模拟运行使用来自交易所的实时数据。但是，任何会导致交易 signal 的信号都由 Freqtrade 正常跟踪，但不会在交易所本身打开任何交易。前瞻测试实时运行，因此虽然需要更长的时间才能获得结果，但它比回测更可靠地指示**潜在**性能。

通过将配置中的 `dry_run` 设置为 true 来启用模拟运行（[配置](configuration.md#using-dry-run-mode)）。

!!! Warning "回测可能非常不准确"
    回测结果可能与现实不符的原因有很多。请查看 [回测假设](backtesting.md#assumptions-made-by-backtesting) 和 [常见策略错误](strategy-customization.md#common-mistakes-when-developing-strategies) 文档。
    一些列出和排名 Freqtrade 策略的网站显示了令人印象深刻回测结果。不要假设这些结果是可实现的或现实的。

??? Hint "有用的命令"
    Freqtrade 包括两个有用的命令来检查策略中的基本缺陷：[lookahead-analysis](lookahead-analysis.md) 和 [recursive-analysis](recursive-analysis.md)。

### 评估回测和模拟运行结果

在回测后始终对策略进行模拟运行，以查看回测和模拟运行结果是否足够相似。

如果有任何显著差异，请验证您的入场和出场信号是否一致，并在两种模式之间的同一根蜡烛上出现。但是，模拟运行和回测之间总是存在差异：

- 回测假设所有订单都会成交。在模拟运行中，如果使用限价订单或交易所没有交易量，这可能不是这种情况。
- 在蜡烛收盘时跟随入场信号，回测假设交易在下一根蜡烛的开盘价进入（除非您的策略中有自定义定价回调）。在模拟运行中，信号和交易开盘之间通常会有延迟。
  这是因为当您的主要时间框架上出现新蜡烛时，例如每 5 分钟，Freqtrade 需要时间来分析所有交易对 dataframe。因此，Freqtrade 将在蜡烛开盘后几秒钟（理想情况下延迟尽可能小）尝试打开交易。
- 由于模拟运行中的入场率可能与回测不匹配，这意味着利润计算也会不同。因此，如果 ROI、止损、追踪止损和回调退出不完全相同，这是正常的。
- 新蜡烛出现与您的信号被触发和交易被打开之间的计算"延迟"越多，价格不可预测性就越大。确保您的计算机足够强大，可以在合理的时间内处理交易对列表中的交易对数量。如果存在显著的数据处理延迟，Freqtrade 会在日志中警告您。

## 控制或监控运行中的机器人

一旦您的机器人在模拟或实盘模式下运行，Freqtrade 有六种机制来控制或监控运行中的机器人：

- **[FreqUI](freq-ui.md)**：最容易上手，FreqUI 是一个 Web 界面，用于查看和控制机器人的当前活动。
- **[Telegram](telegram-usage.md)**：在移动设备上，Telegram 集成可用于获取有关机器人活动的警报并控制某些方面。
- **[FTUI](https://github.com/freqtrade/ftui)**：FTUI 是 Freqtrade 的终端（命令行）界面，仅允许监控运行中的机器人。
- **[freqtrade-client](rest-api.md#consuming-the-api)**：REST API 的 Python 实现，使从您的 Python 应用程序或命令行发出请求和使用机器人响应变得容易。
- **[REST API 端点](rest-api.md#available-endpoints)**：REST API 允许程序员开发自己的工具来与 Freqtrade 机器人交互。
- **[Webhooks](webhook-config.md)**：Freqtrade 可以通过 webhooks 向其他服务（例如 discord）发送信息。

### 日志

Freqtrade 生成广泛的调试日志以帮助您了解正在发生的事情。请熟悉您可能在机器人日志中看到的信息和错误消息。

默认情况下，日志记录发生在标准输出（命令行）上。如果您想改为写入文件，许多 freqtrade 命令，包括 `trade` 命令，接受 `--logfile` 选项以写入文件。

查看 [FAQ](faq.md#how-do-i-search-the-bot-logs-for-something) 以获取示例。

## 最终想法

算法交易很困难，大多数公共策略由于需要时间和精力才能使策略在多种情况下盈利而表现不佳。

因此，采用公共策略并使用回测作为评估性能的方法通常是有问题的。然而，Freqtrade 提供了有用的方法来帮助您做出决策并进行尽职调查。

实现盈利的方法有很多，没有单一的技巧、诀窍或配置选项可以修复表现不佳的策略。

Freqtrade 是一个拥有大型且乐于助人的社区的开源平台 - 请务必访问我们的 [discord 频道](https://discord.gg/p7nuUNVfP7) 与他人讨论您的策略！

一如既往，只投资您愿意损失的资金。

## 结论

在 Freqtrade 中开发策略涉及根据技术指标定义入场和出场信号。通过遵循上述结构和方法，您可以创建和测试自己的交易策略。

常见问题和答案可在我们的 [FAQ](faq.md) 中找到。

要继续，请参考更深入的 [Freqtrade 策略定制文档](strategy-customization.md)。
