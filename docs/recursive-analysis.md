# 递归分析

本页解释如何验证策略中由于某些指标的递归问题而导致的不准确性。

递归公式定义序列的任何项相对于其前一项（或几项）。递归公式的一个例子是 a<sub>n</sub> = a<sub>n-1</sub> + b。

这对 Freqtrade 为什么重要？在回测中，机器人将根据指定的时间范围获取交易对的完整数据。但在模拟/实盘运行中，机器人将受到每个交易所提供的数据量限制。

例如，要计算一个非常基本的指标 `steps`，第一行的值始终为 0，而后续行的值等于前一行加 1 的值。如果我使用最新的 1000 根蜡烛来计算它，那么第一行的 `steps` 值是 0，最后关闭蜡烛的 `steps` 值是 999。

如果计算仅使用最新的 500 根蜡烛会发生什么？那么最后关闭蜡烛的 `steps` 值是 499，而不是 999。值的差异意味着您的回测结果可能与您的模拟/实盘运行结果不同。

`recursive-analysis` 命令需要历史数据可用。要了解如何获取您感兴趣的交易对和交易所的数据，请转到文档的[数据下载](data-download.md)部分。

此命令基于准备不同长度的数据并基于它们计算指标。
这不会回测策略本身，而只是计算指标。在计算不同启动蜡烛值（`startup_candle_count`）的指标完成后，会比较所有指定的 `startup_candle_count` 的最后一行值，以查看它们与基础计算相比显示多少差异。

命令设置：

- 使用 `-p` 选项设置您要分析的交易对。由于我们只查看指标值，使用多个交易对是多余的。最好使用价格相对较高且至少具有中等波动性的交易对，例如 BTC 或 ETH，以避免可能使结果不准确的舍入问题。如果命令中未设置交易对，则用于此分析的交易对是白名单中的第一个交易对。
- 建议设置较长的时间范围（至少 5000 根蜡烛），以便将要用作基准的初始指标计算本身具有非常小或没有递归问题。例如，对于 5 分钟时间框架，5000 根蜡烛的时间范围等于 18 天。
- `--cache` 被强制设置为 "none"，以避免自动加载先前的指标计算。

除了递归公式检查外，此命令还对指标值进行简单的前瞻偏差检查。要进行完整的前瞻检查，请使用[前瞻分析](lookahead-analysis.md)。

## 递归分析命令参考

--8<-- "commands/recursive-analysis.md"

### 为什么使用奇数默认启动蜡烛？

启动蜡烛的默认值是奇数。当机器人从交易所的 API 获取蜡烛数据时，最后一根蜡烛是机器人正在检查的蜡烛，其余数据是"启动蜡烛"。

例如，Binance 每次 API 调用允许 1000 根蜡烛。当机器人接收 1000 根蜡烛时，最后一根蜡烛是"当前蜡烛"，前面的 999 根蜡烛是"启动蜡烛"。通过将启动蜡烛计数设置为 1000 而不是 999，机器人将尝试获取 1001 根蜡烛。然后，交易所 API 将以分页形式发送蜡烛数据，即在 Binance API 的情况下，这将是两个组 - 一个长度为 1000，另一个长度为 1。这导致机器人认为策略需要 1001 根蜡烛的数据，因此它将下载 2000 根蜡烛的数据，这意味着将有 1 根"当前蜡烛"和 1999 根"启动蜡烛"。

此外，交易所限制连续批量 API 调用的数量，例如 Binance 允许 5 次调用。在这种情况下，只能从 Binance API 下载 5000 根蜡烛而不会达到 API 速率限制，这意味着您可以拥有的最大 `startup_candle_count` 是 4999。

请注意，交易所可能会在未来更改此蜡烛限制，恕不另行通知。

### 命令如何工作？

- 首先使用提供的时间范围进行初始指标计算，以生成指标值的基准。
- 设置基准后，它将为每个不同的启动蜡烛计数值执行额外的运行。
- 然后命令将比较最后蜡烛行的指标值并在表格中报告差异。

## 理解递归分析输出

这是一个输出结果表示例，其中至少有一个指标具有递归公式问题：

```
| indicators   | 20      | 40      | 80     | 100    | 150     | 300     | 999    |
|--------------+---------+---------+--------+--------+---------+---------+--------|
| rsi_30       | nan%    | -6.025% | 0.612% | 0.828% | -0.140% | 0.000%  | 0.000% |
| rsi_14       | 24.141% | -0.876% | 0.070% | 0.007% | -0.000% | -0.000% | -      |
```

The column headers indicate the different `startup_candle_count` used in the analysis. The values in the table indicate the variance of the calculated indicators compared to the benchmark value.

`nan%` means the value of that indicator cannot be calculated due to lack of data. In this example, you cannot calculate RSI with length 30 with just 21 candles (1 current candle + 20 startup candles).

Users should assess the table per indicator to decide if the specified `startup_candle_count` results in a sufficiently small variance so that the indicator does not have any effect on entries and/or exits.

As such, aiming for absolute zero variance (shown by `-` value) might not be the best option, because some indicators might require you to use such a long `startup_candle_count` to have zero variance.

## Caveats

- `recursive-analysis` will only calculate and compare the indicator values at the last row. The output table reports the percentage differences between the different startup candle count calculations and the original benchmark calculation. Whether it has any actual impact on your entries and exits is not included.
- The ideal scenario is that indicators will have no variance (or at least very close to 0%) despite the startup candle being varied. In reality, indicators such as EMA are using a recursive formula to calculate indicator values, so the goal is not necessarily to have zero percentage variance, but to have the variance low enough (and therefore `startup_candle_count` high enough) that the recursion inherent in the indicator will not have any real impact on trading decisions.
- `recursive-analysis` will only run calculations on `populate_indicators` and `@informative` decorator(s). If you put any indicator calculation on `populate_entry_trend` or `populate_exit_trend`, it won't be calculated.
