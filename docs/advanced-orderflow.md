# 订单流数据

本指南将引导您如何在 Freqtrade 中利用公共交易数据进行高级订单流分析。

!!! Warning "实验性功能"
    订单流功能目前处于测试阶段，可能在未来的版本中发生更改。请在 [Freqtrade GitHub 仓库](https://github.com/freqtrade/freqtrade/issues) 上报告任何问题或反馈。
    它目前也还没有与 freqAI 一起测试 - 结合这两个功能目前被认为是超出范围的。

!!! Warning "性能"
    订单流需要原始交易数据。此数据相当大，当 freqtrade 需要为最后 X 根蜡烛下载交易数据时，可能导致初始启动缓慢。此外，启用此功能将导致内存使用增加。请确保有足够的资源可用。

## 开始使用

### 启用公共交易

在您的 `config.json` 文件中，在 `exchange` 部分将 `use_public_trades` 选项设置为 true。

```json
"exchange": {
   ...
   "use_public_trades": true,
}
```

### 配置订单流处理

在 config.json 的 orderflow 部分定义您所需的订单流处理设置。在这里，您可以调整以下因素：

- `cache_size`：有多少先前的订单流蜡烛保存到缓存中，而不是每根新蜡烛都计算
- `max_candles`：过滤您希望获取交易数据的蜡烛数量。
- `scale`：这控制足迹图表的价格区间大小。
- `stacked_imbalance_range`：定义考虑所需的最小连续不平衡价格水平。
- `imbalance_volume`：过滤掉低于此阈值的不平衡交易量。
- `imbalance_ratio`：过滤掉比率（卖价和买价交易量之间的差异）低于此值的不平衡。

```json
"orderflow": {
    "cache_size": 1000, 
    "max_candles": 1500, 
    "scale": 0.5, 
    "stacked_imbalance_range": 3, //  needs at least this amount of imbalance next to each other
    "imbalance_volume": 1, //  filters out below
    "imbalance_ratio": 3 //  filters out ratio lower than
  },
```

## 为回测下载交易数据

要下载历史交易数据以进行回测，请在 freqtrade download-data 命令中使用 --dl-trades 标志。

```bash
freqtrade download-data -p BTC/USDT:USDT --timerange 20230101- --trading-mode futures --timeframes 5m --dl-trades
```

!!! Warning "数据可用性"
    并非所有交易所都提供公共交易数据。对于支持的交易所，如果您开始使用 `--dl-trades` 标志下载数据，freqtrade 将在公共交易数据不可用时警告您。

## 访问订单流数据

激活后，您的数据框中将提供几个新列：

``` python

dataframe["trades"] # 包含每个单独交易的信息。
dataframe["orderflow"] # 表示足迹图表字典（见下文）
dataframe["imbalances"] # 包含订单流中不平衡的信息。
dataframe["bid"] # 总买量 
dataframe["ask"] # 总卖量
dataframe["delta"] # 卖量和买量之间的差异。
dataframe["min_delta"] # 蜡烛内的最小 delta
dataframe["max_delta"] # 蜡烛内的最大 delta
dataframe["total_trades"] # 交易总数
dataframe["stacked_imbalances_bid"] # 堆叠买价不平衡范围开始的价格水平列表
dataframe["stacked_imbalances_ask"] # 堆叠卖价不平衡范围开始的价格水平列表
```

您可以在策略代码中访问这些列以进行进一步分析。这是一个示例：

``` python
def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    # 计算累积 delta
    dataframe["cum_delta"] = cumulative_delta(dataframe["delta"])
    # 访问总交易数
    total_trades = dataframe["total_trades"]
    ...

def cumulative_delta(delta: Series):
    cumdelta = delta.cumsum()
    return cumdelta

```

### 足迹图表 (`dataframe["orderflow"]`)

此列提供不同价格水平的买卖订单的详细细分，提供对订单流动态的宝贵见解。配置中的 `scale` 参数确定此表示的价格区间大小

`orderflow` 列包含具有以下结构的字典：

``` output
{
    "price": {
        "bid_amount": 0.0,
        "ask_amount": 0.0,
        "bid": 0,
        "ask": 0,
        "delta": 0.0,
        "total_volume": 0.0,
        "total_trades": 0
    }
}
```

#### 订单流列说明

- key: 价格区间 - 按 `scale` 间隔分箱
- `bid_amount`: 每个价格水平购买的总量。
- `ask_amount`: 每个价格水平售出的总量。
- `bid`: 每个价格水平的买入订单数量。
- `ask`: 每个价格水平的卖出订单数量。
- `delta`: 每个价格水平卖量和买量之间的差异。
- `total_volume`: 每个价格水平的总量（卖量 + 买量）。
- `total_trades`: 每个价格水平的总交易数（卖 + 买）。

通过利用这些功能，您可以基于订单流分析获得对市场情绪和潜在交易机会的宝贵见解。

### 原始交易数据 (`dataframe["trades"]`)

包含在蜡烛期间发生的单个交易的列表。此数据可用于更细粒度的订单流动态分析。

每个单独条目包含具有以下键的字典：

- `timestamp`: 交易的时间戳。
- `date`: 交易的日期。
- `price`: 交易的价格。
- `amount`: 交易的交易量。
- `side`: 买入或卖出。
- `id`: 交易的唯一标识符。
- `cost`: 交易的总成本（价格 * 交易量）。

### 不平衡 (`dataframe["imbalances"]`)

此列提供包含订单流中不平衡信息的字典。当给定价格水平的卖量和买量之间存在显著差异时，会发生不平衡。

每行如下所示 - 以价格为索引，相应的买卖不平衡值作为列

``` output
{
    "price": {
        "bid_imbalance": False,
        "ask_imbalance": False
    }
}
```
