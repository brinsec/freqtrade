# 高级回测分析

## 分析买入/入场和卖出/出场标签

了解策略如何根据用于标记不同买入条件的买入/入场标签运行可能很有帮助。您可能希望看到每个买入和
卖出条件的更复杂统计信息，超出默认回测输出提供的那些。您还可能希望
确定导致交易打开的信号蜡烛上的指标值。

!!! Note "注意"
    以下买入原因分析仅适用于回测，*不适用于超参数优化*。

我们需要运行回测，将 `--export` 选项设置为 `signals` 以启用
信号**和**交易的导出：

``` bash
freqtrade backtesting -c <config.json> --timeframe <tf> --strategy <strategy_name> --timerange=<timerange> --export=signals
```

这将告诉 freqtrade 输出策略、交易对和相应的
导致入场和出场信号的蜡烛 DataFrame 的腌制字典。
根据您的策略产生多少入场，此文件可能变得相当大，因此请定期检查您的 `user_data/backtest_results` 文件夹以删除旧导出。

在运行下一个回测之前，请确保删除旧的回测结果或运行
带有 `--cache none` 选项的回测以确保不使用缓存的结果。

如果一切顺利，您现在应该在 `user_data/backtest_results` 文件夹中看到 `backtest-result-{timestamp}_signals.pkl` 和 `backtest-result-{timestamp}_exited.pkl` 文件。

要分析入场/出场标签，我们现在需要使用 `freqtrade backtesting-analysis` 命令
并提供带有空格分隔参数的 `--analysis-groups` 选项：

``` bash
freqtrade backtesting-analysis -c <config.json> --analysis-groups 0 1 2 3 4 5
```

此命令将从最后的回测结果中读取。`--analysis-groups` 选项用于
指定显示每个组或交易利润的各种表格输出，
从最简单的（0）到最详细的每个交易对、每个买入和每个卖出标签（4）：

* 0：按 enter_tag 的整体胜率和利润摘要
* 1：按 enter_tag 分组的利润摘要
* 2：按 enter_tag 和 exit_tag 分组的利润摘要
* 3：按交易对和 enter_tag 分组的利润摘要
* 4：按交易对、enter_tag 和 exit_tag 分组的利润摘要（这可能会变得相当大）
* 5：按 exit_tag 分组的利润摘要

更多选项可通过运行 `-h` 选项获得。

### 使用 backtest-filename

默认情况下，`backtesting-analysis` 处理 `user_data/backtest_results` 目录中最新的回测结果。
如果您想分析较早的回测结果，请使用 `--backtest-filename` 选项指定所需文件。这允许您通过提供相关回测结果的文件名随时重新访问和重新分析历史回测输出：

``` bash
freqtrade backtesting-analysis -c <config.json> --timeframe <tf> --strategy <strategy_name> --timerange <timerange> --export signals --backtest-filename backtest-result-2025-03-05_20-38-34.zip
```

您应该会在日志中看到一些类似的输出，其中包含导出的带时间戳的文件名：

```
2022-06-14 16:28:32,698 - freqtrade.misc - INFO - dumping json to "mystrat_backtest-2022-06-14_16-28-32.json"
```

然后您可以在 `backtesting-analysis` 中使用该文件名：

```
freqtrade backtesting-analysis -c <config.json> --backtest-filename=mystrat_backtest-2022-06-14_16-28-32.json
```

要使用不同结果目录中的结果，可以使用 `--backtest-directory` 指定目录

``` bash
freqtrade backtesting-analysis -c <config.json> --backtest-directory custom_results/ --backtest-filename mystrat_backtest-2022-06-14_16-28-32.json
```

### 调整要显示的买入和卖出标签

要仅在显示的输出中显示某些买入和卖出标签，请使用以下两个选项：

```
--enter-reason-list : 要分析的入场信号的空格分隔列表。默认："all"
--exit-reason-list : 要分析的出场信号的空格分隔列表。默认："all"
```

例如：

```bash
freqtrade backtesting-analysis -c <config.json> --analysis-groups 0 2 --enter-reason-list enter_tag_a enter_tag_b --exit-reason-list roi custom_exit_tag_a stop_loss
```

### 输出信号蜡烛指标

`freqtrade backtesting-analysis` 的真正强大之处在于能够打印信号蜡烛上存在的指标
值，以允许对买入信号指标进行细粒度调查和调整。要为一组给定指标打印列，请使用 `--indicator-list`
选项：

```bash
freqtrade backtesting-analysis -c <config.json> --analysis-groups 0 2 --enter-reason-list enter_tag_a enter_tag_b --exit-reason-list roi custom_exit_tag_a stop_loss --indicator-list rsi rsi_1h bb_lowerband ema_9 macd macdsignal
```

指标必须存在于策略的主 DataFrame 中（无论是主时间框架还是信息性时间框架），否则它们将在脚本输出中被忽略。

!!! Note "指标列表"
    指标值将显示入场和出场点。如果指定了 `--indicator-list all`，
    则仅显示入场点的指标，以避免过多的列表，这可能会根据策略而发生。

有一些蜡烛和交易相关字段包含在分析中，因此通过将它们包含在指标列表中可以自动访问，这些包括：

- **open_date     :** 交易开盘日期时间
- **close_date    :** 交易收盘日期时间
- **min_rate      :** 头寸期间看到的最低价格
- **max_rate      :** 头寸期间看到的最高价格
- **open          :** 信号蜡烛开盘价
- **close         :** 信号蜡烛收盘价
- **high          :** 信号蜡烛最高价
- **low           :** 信号蜡烛最低价
- **volume        :** 信号蜡烛成交量
- **profit_ratio  :** 交易利润比率
- **profit_abs    :** 交易的绝对利润回报

#### 指标值示例输出

```bash
freqtrade backtesting-analysis -c user_data/config.json --analysis-groups 0 --indicator-list chikou_span tenkan_sen 
```

在此示例中，
我们旨在显示交易入场和出场点的 `chikou_span` 和 `tenkan_sen` 指标值。

指标的示例输出可能如下所示：

| pair      | open_date                 | enter_reason | exit_reason | chikou_span (entry) | tenkan_sen (entry) | chikou_span (exit) | tenkan_sen (exit) |
|-----------|---------------------------|--------------|-------------|---------------------|--------------------|--------------------|-------------------|
| DOGE/USDT | 2024-07-06 00:35:00+00:00 |              | exit_signal | 0.105               | 0.106              | 0.105              | 0.107             |
| BTC/USDT  | 2024-08-05 14:20:00+00:00 |              | roi         | 54643.440           | 51696.400          | 54386.000          | 52072.010         |

如表所示，`chikou_span (entry)` 表示交易入场时的指标值，
而 `chikou_span (exit)` 反映其在出场时的值。
这种详细的指标值视图增强了分析。

`(entry)` 和 `(exit)` 后缀被添加到指标中
以区分交易入场和出场点的值。

!!! Note "交易范围的指标"
    某些交易范围的指标没有 `(entry)` 或 `(exit)` 后缀。这些指标包括：`pair`、`stake_amount`、
    `max_stake_amount`、`amount`、`open_date`、`close_date`、`open_rate`、`close_rate`、`fee_open`、`fee_close`、`trade_duration`、
    `profit_ratio`、`profit_abs`、`exit_reason`、`initial_stop_loss_abs`、`initial_stop_loss_ratio`、`stop_loss_abs`、`stop_loss_ratio`、
    `min_rate`、`max_rate`、`is_open`、`enter_tag`、`leverage`、`is_short`、`open_timestamp`、`close_timestamp` 和 `orders`

#### 基于入场或出场信号过滤指标

默认情况下，`--indicator-list` 选项显示入场和出场信号的指标值。要仅过滤入场信号的指标值，可以使用 `--entry-only` 参数。同样，要仅显示出场信号的指标值，请使用 `--exit-only` 参数。

示例：显示入场信号的指标值：

```bash
freqtrade backtesting-analysis -c user_data/config.json --analysis-groups 0 --indicator-list chikou_span tenkan_sen --entry-only
```

示例：显示出场信号的指标值：

```bash
freqtrade backtesting-analysis -c user_data/config.json --analysis-groups 0 --indicator-list chikou_span tenkan_sen --exit-only
```

!!! Note "注意"
    使用这些过滤器时，指标名称将不会带有 `(entry)` 或 `(exit)` 后缀。

### 按日期过滤交易输出

要仅显示回测时间范围内日期之间的交易，请以 `YYYYMMDD-[YYYYMMDD]` 格式提供通常的 `timerange` 选项：

```
--timerange : 用于过滤输出交易的时间范围，开始日期包含，结束日期不包含。例如 20220101-20221231
```

例如，如果您的回测时间范围是 `20220101-20221231`，但您只想输出 1 月份的交易：

```bash
freqtrade backtesting-analysis -c <config.json> --timerange 20220101-20220201
```

### 打印被拒绝的信号

使用 `--rejected-signals` 选项打印被拒绝的信号。

```bash
freqtrade backtesting-analysis -c <config.json> --rejected-signals
```

### 将表格写入 CSV

某些表格输出可能会变得很大，因此将它们打印到终端不是首选。
使用 `--analysis-to-csv` 选项禁用将表格打印到标准输出，并将它们写入 CSV 文件。

```bash
freqtrade backtesting-analysis -c <config.json> --analysis-to-csv
```

默认情况下，这将为您在 `backtesting-analysis` 命令中指定的每个输出表写入一个文件，例如

```bash
freqtrade backtesting-analysis -c <config.json> --analysis-to-csv --rejected-signals --analysis-groups 0 1
```

这将写入 `user_data/backtest_results`：

* rejected_signals.csv
* group_0.csv
* group_1.csv

要覆盖文件写入的位置，还请指定 `--analysis-csv-path` 选项。

```bash
freqtrade backtesting-analysis -c <config.json> --analysis-to-csv --analysis-csv-path another/data/path/
```
