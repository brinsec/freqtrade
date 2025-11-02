# 已弃用的功能

本页包含已被机器人开发团队声明为已弃用且不再支持的命令行参数、配置参数和机器人功能的描述。请在配置中避免使用它们。

## 已移除功能

### `--refresh-pairs-cached` 命令行选项

在回测、超参数优化和 edge 的上下文中，`--refresh-pairs-cached` 允许刷新用于回测的蜡烛图数据。
由于这导致了许多混乱并减慢了回测速度（虽然它不是回测的一部分），它已被单独列为 freqtrade 子命令 `freqtrade download-data`。

此命令行选项在 2019.7-dev（develop 分支）中已被弃用，并在 2019.9 中移除。

### **--dynamic-whitelist** 命令行选项

此命令行选项在 2018 年已被弃用，并在 freqtrade 2019.6-dev（develop 分支）和 freqtrade 2019.7 中移除。
请改为参考 [pairlists](plugins.md#pairlists-and-pairlist-handlers)。

### `--live` 命令行选项

在回测上下文中，`--live` 允许下载最新的报价数据用于回测。
只下载最新的 500 根蜡烛图，因此无法有效获取良好的回测数据。
在 2019-7-dev（develop 分支）和 freqtrade 2019.8 中移除。

### `ticker_interval`（现在为 `timeframe`）

对 `ticker_interval` 术语的支持在 2020.6 中已弃用，改为 `timeframe`——兼容性代码在 2022.3 中移除。

### 允许按顺序运行多个 pairlist

配置中以前的 `"pairlist"` 部分已被移除，并被 `"pairlists"` 取代——指定 pairlist 序列的列表。

旧的配置参数部分（`"pairlist"`）在 2019.11 中已弃用，并在 2020.4 中移除。

### volume-pairlist 中 bidVolume 和 askVolume 的弃用

由于只能在资产之间比较 quoteVolume，其他选项（bidVolume、askVolume）在 2020.4 中已弃用，并在 2020.9 中移除。

### 使用订单簿步进获取出场价格

使用 `order_book_min` 和 `order_book_max` 过去允许步进订单簿并尝试找到下一个 ROI 槽——尝试提前下卖出订单。
然而，由于这增加了风险且没有任何好处，它已在 2021.7 中出于可维护性目的而被移除。

### 传统 Hyperopt 模式

使用单独的 hyperopt 文件在 2021.4 中已弃用，并在 2021.9 中移除。
请切换到新的[参数化策略](hyperopt.md)以从新的 hyperopt 界面中受益。

## V2 和 V3 之间的策略更改

隔离期货/空头交易在 2022.4 中引入。这需要对配置设置、策略接口等进行重大更改。

我们已经付出了巨大的努力来保持与现有策略的兼容性，因此如果您只是想继续在现货市场中使用 freqtrade，则无需更改。
虽然我们可能在未来某个时候放弃对当前接口的支持，但我们将单独宣布这一点并设置适当的过渡期。

请遵循[策略迁移](strategy_migration.md)指南将您的策略迁移到新格式以开始使用新功能。

### webhooks - 2022.4 的更改

#### `buy_tag` 已重命名为 `enter_tag`

这应仅适用于您的策略，并且可能适用于 webhooks。
我们将为 1-2 个版本保留兼容性层（因此 `buy_tag` 和 `enter_tag` 都将仍然有效），但此后对 webhooks 的支持将消失。

#### 命名更改

Webhook 术语已从"卖出"更改为"出场"，从"买入"更改为"入场"，在此过程中移除了"webhook"。

* `webhookbuy`、`webhookentry` -> `entry`
* `webhookbuyfill`、`webhookentryfill` -> `entry_fill`
* `webhookbuycancel`、`webhookentrycancel` -> `entry_cancel`
* `webhooksell`、`webhookexit` -> `exit`
* `webhooksellfill`、`webhookexitfill` -> `exit_fill`
* `webhooksellcancel`、`webhookexitcancel` -> `exit_cancel`

## 移除 `populate_any_indicators`

版本 2023.3 中移除了 `populate_any_indicators`，改为使用用于特征工程和目标的分拆方法。请阅读[迁移文档](strategy_migration.md#freqai-strategy)以获取完整详细信息。

## 从配置中移除 `protections`

通过 `"protections": []` 从配置中设置 protections 在 2024.10 中已移除，此前已发出弃用警告超过 3 年。

## hdf5 数据存储

使用 hdf5 作为数据存储在 2024.12 中已弃用，并在 2025.1 中移除。我们建议切换到 feather 数据格式。

请在更新之前使用 [`convert-data` 子命令](data-download.md#sub-command-convert-data)将现有数据转换为受支持的格式之一。

## 通过配置配置高级日志

分别通过 `--logfile systemd` 和 `--logfile journald` 配置 syslog 和 journald 在 2025.3 中已弃用。
请改用基于配置的[日志设置](advanced-setup.md#advanced-logging)。

## 移除 edge 模块

edge 模块在 2023.9 中已弃用，并在 2025.6 中移除。
edge 的所有功能已移除，配置 edge 将导致错误。
