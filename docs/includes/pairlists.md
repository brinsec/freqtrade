## 交易对列表和交易对列表处理器

交易对列表处理器定义机器人应该交易的交易对列表（pairlist）。它们在配置设置的 `pairlists` 部分中配置。

在您的配置中，您可以使用静态交易对列表（由 [`StaticPairList`](#static-pair-list) 交易对列表处理器定义）和动态交易对列表（由 [`VolumePairList`](#volume-pair-list) 和 [`PercentChangePairList`](#percent-change-pair-list) 交易对列表处理器定义）。

此外，[`AgeFilter`](#agefilter)、[`DelistFilter`](#delistfilter)、[`PrecisionFilter`](#precisionfilter)、[`PriceFilter`](#pricefilter)、[`ShuffleFilter`](#shufflefilter)、[`SpreadFilter`](#spreadfilter) 和 [`VolatilityFilter`](#volatilityfilter) 充当交易对列表过滤器，删除某些交易对和/或移动它们在交易对列表中的位置。

如果使用多个交易对列表处理器，它们会被链接，所有交易对列表处理器的组合形成机器人用于交易和回测的最终交易对列表。交易对列表处理器按照它们配置的顺序执行。您可以将 `StaticPairList`、`VolumePairList`、`ProducerPairList`、`RemotePairList`、`MarketCapPairList` 或 `PercentChangePairList` 定义为起始交易对列表处理器。

非活跃市场总是从最终交易对列表中删除。明确列入黑名单的交易对（`pair_blacklist` 配置设置中的那些）也总是从最终交易对列表中删除。

### 交易对黑名单

交易对黑名单（通过配置中的 `exchange.pair_blacklist` 配置）禁止某些交易对进行交易。
这可以简单到排除 `DOGE/BTC` - 这将完全删除此交易对。

交易对黑名单还支持通配符（正则表达式风格）- 因此 `BNB/.*` 将排除所有以 BNB 开头的交易对。
您也可以使用类似 `.*DOWN/BTC` 或 `.*UP/BTC` 的内容来排除杠杆代币（请检查您交易所的交易对命名约定！）

### 可用的交易对列表处理器

* [`StaticPairList`](#static-pair-list)（默认，如果未另行配置）
* [`VolumePairList`](#volume-pair-list)
* [`PercentChangePairList`](#percent-change-pair-list)
* [`ProducerPairList`](#producerpairlist)
* [`RemotePairList`](#remotepairlist)
* [`MarketCapPairList`](#marketcappairlist)
* [`AgeFilter`](#agefilter)
* [`DelistFilter`](#delistfilter)
* [`FullTradesFilter`](#fulltradesfilter)
* [`OffsetFilter`](#offsetfilter)
* [`PerformanceFilter`](#performancefilter)
* [`PrecisionFilter`](#precisionfilter)
* [`PriceFilter`](#pricefilter)
* [`ShuffleFilter`](#shufflefilter)
* [`SpreadFilter`](#spreadfilter)
* [`RangeStabilityFilter`](#rangestabilityfilter)
* [`VolatilityFilter`](#volatilityfilter)

!!! Tip "测试交易对列表"
    交易对列表配置可能很难正确配置。最好在 [webserver 模式](freq-ui.md#webserver-mode) 中使用 freqUI 或使用 [`test-pairlist`](utils.md#test-pairlist) 实用子命令快速测试您的交易对列表配置。

#### 静态交易对列表

默认情况下，使用 `StaticPairList` 方法，它使用配置中静态定义的交易对白名单。交易对列表还支持通配符（正则表达式风格）- 因此 `.*/BTC` 将包括所有以 BTC 作为抵押的交易对。

它使用来自 `exchange.pair_whitelist` 和 `exchange.pair_blacklist` 的配置，在下面的示例中，将交易 BTC/USDT 和 ETH/USDT - 并阻止 BNB/USDT 交易。

`pair_*list` 参数都支持正则表达式 - 因此像 `.*/USDT` 这样的值将启用交易不在黑名单中的所有交易对。

```json
"exchange": {
    "name": "...",
    // ... 
    "pair_whitelist": [
        "BTC/USDT",
        "ETH/USDT",
        // ...
    ],
    "pair_blacklist": [
        "BNB/USDT",
        // ...
    ]
},
"pairlists": [
    {"method": "StaticPairList"}
],
```

默认情况下，只允许当前启用的交易对。
要跳过对活跃市场的交易对验证，请在 `StaticPairList` 配置中设置 `"allow_inactive": true`。
这对于回测过期的交易对（如季度现货市场）很有用。

当在"后续"位置使用（例如在 VolumePairlist 之后）时，`'pair_whitelist'` 中的所有交易对将被添加到交易对列表的末尾。

#### 成交量交易对列表

`VolumePairList` 根据交易对的交易量进行排序/过滤。它根据 `sort_key`（只能是 `quoteVolume`）选择 `number_assets` 个顶级交易对。

当在交易对列表处理器链中的非主要位置使用（在 StaticPairList 和其他交易对列表过滤器之后）时，`VolumePairList` 考虑先前交易对列表处理器的输出，根据交易量添加其排序/选择的交易对。

当在交易对列表处理器链的主要位置使用时，`pair_whitelist` 配置设置将被忽略。相反，`VolumePairList` 从交易所上所有可用市场中匹配抵押货币的顶级资产中选择。

`refresh_period` 设置允许定义交易对列表刷新的周期（以秒为单位）。默认为 1800 秒（30 分钟）。
`VolumePairList` 上的交易对列表缓存（`refresh_period`）仅适用于生成交易对列表。
过滤实例（列表中的非第一个位置）不会应用任何缓存（除了在高级模式下缓存蜡烛持续时间内的蜡烛），并将始终使用最新数据。

`VolumePairList` 默认基于交易所的行情数据，如 ccxt 库报告的那样：

* `quoteVolume` 是过去 24 小时内交易的报价（抵押）货币数量（买入或卖出）。

```json
"pairlists": [
    {
        "method": "VolumePairList",
        "number_assets": 20,
        "sort_key": "quoteVolume",
        "min_value": 0,
        "max_value": 8000000,
        "refresh_period": 1800
    }
],
```

您可以使用 `min_value` 定义最小成交量 - 这将过滤掉在指定时间范围内成交量低于指定值的交易对。
此外，您还可以使用 `max_value` 定义最大成交量 - 这将过滤掉在指定时间范围内成交量高于指定值的交易对。

##### VolumePairList 高级模式

`VolumePairList` 还可以在高级模式下运行，以在指定蜡烛大小的给定时间范围内构建成交量。它利用交易所历史蜡烛数据，构建典型价格（通过 (open+high+low)/3 计算），并将典型价格与每个蜡烛的成交量相乘。总和是给定范围内的 `quoteVolume`。这允许不同的场景，当使用更长范围与更大的蜡烛大小时，可以获得更平滑的成交量，或者当使用短范围与小蜡烛时则相反。

为了方便，可以指定 `lookback_days`，这将意味着将使用 1d 蜡烛进行回看。在下面的示例中，交易对列表将基于过去 7 天创建：

```json
"pairlists": [
    {
        "method": "VolumePairList",
        "number_assets": 20,
        "sort_key": "quoteVolume",
        "min_value": 0,
        "refresh_period": 86400,
        "lookback_days": 7
    }
],
```

!!! Warning "范围回看和刷新周期"
    当与 `lookback_days` 和 `lookback_timeframe` 结合使用时，`refresh_period` 不能小于以秒为单位的蜡烛大小。因为这会导致对交易所 API 的不必要请求。

!!! Warning "使用回看范围时的性能影响"
    如果在第一个位置与回看结合使用，基于范围的成交量计算可能会消耗时间和资源，因为它会为所有可交易对下载蜡烛。因此，强烈建议使用标准方法配合 `VolumeFilter` 缩小交易对列表以进行进一步的范围成交量计算。

??? Tip "不支持的交易所"
    在某些交易所（如 Gemini），常规 VolumePairList 不起作用，因为 API 本身不提供 24 小时成交量。这可以通过使用蜡烛数据构建成交量来解决。
    要大致模拟 24 小时成交量，您可以使用以下配置。
    请注意，这些交易对列表每天只会刷新一次。

    ```json
    "pairlists": [
        {
            "method": "VolumePairList",
            "number_assets": 20,
            "sort_key": "quoteVolume",
            "min_value": 0,
            "refresh_period": 86400,
            "lookback_days": 1
        }
    ],
    ```

可以使用更复杂的方法，通过使用 `lookback_timeframe` 作为蜡烛大小和指定蜡烛数量的 `lookback_period`。此示例将基于 3 天的 1 小时蜡烛滚动周期构建成交量交易对：

```json
"pairlists": [
    {
        "method": "VolumePairList",
        "number_assets": 20,
        "sort_key": "quoteVolume",
        "min_value": 0,
        "refresh_period": 3600,
        "lookback_timeframe": "1h",
        "lookback_period": 72
    }
],
```

!!! Note "注意"
    `VolumePairList` 不支持回测模式。

#### 百分比变化交易对列表

`PercentChangePairList` 根据交易对在过去 24 小时或任何定义的时间框架内的价格百分比变化来过滤和排序交易对，作为高级选项的一部分。这允许交易者专注于经历了显著价格波动的资产，无论是正面的还是负面的。

**配置选项**

* `number_assets`：指定基于 24 小时百分比变化选择的顶级交易对数量。
* `min_value`：设置最小百分比变化阈值。百分比变化低于此值的交易对将被过滤掉。
* `max_value`：设置最大百分比变化阈值。百分比变化高于此值的交易对将被过滤掉。
* `sort_direction`：指定根据百分比变化对交易对进行排序的顺序。接受两个值：`asc` 表示升序，`desc` 表示降序。
* `refresh_period`：定义交易对列表刷新的间隔（以秒为单位）。默认值为 1800 秒（30 分钟）。
* `lookback_days`：要回看的天数。选择 `lookback_days` 时，`lookback_timeframe` 默认为 1 天。
* `lookback_timeframe`：用于回看周期的时间框架。
* `lookback_period`：要回看的周期数。

当 PercentChangePairList 在其他交易对列表处理器之后使用时，它将对那些处理器的输出进行操作。如果它是主要的交易对列表处理器，它将从所有可用市场中选择具有指定抵押货币的交易对。

`PercentChangePairList` 使用来自交易所的行情数据，通过 ccxt 库提供：
百分比变化计算为过去 24 小时内的价格变化。

??? Note "不支持的交易所"
    在某些交易所（如 HTX），常规 PercentChangePairList 不起作用，因为 API 本身不提供 24 小时价格百分比变化。这可以通过使用蜡烛数据计算百分比变化来解决。要大致模拟 24 小时百分比变化，您可以使用以下配置。请注意，这些交易对列表每天只会刷新一次。
    ```json
    "pairlists": [
        {
            "method": "PercentChangePairList",
            "number_assets": 20,
            "min_value": 0,
            "refresh_period": 86400,
            "lookback_days": 1
        }
    ],
    ```

**从行情读取的示例配置**

```json
"pairlists": [
    {
        "method": "PercentChangePairList",
        "number_assets": 15,
        "min_value": -10,
        "max_value": 50
    }
],
```

在此配置中：

1. 根据过去 24 小时内价格百分比变化最高的交易对选择前 15 个交易对。
2. 只考虑百分比变化在 -10% 和 50% 之间的交易对。

**从蜡烛读取的示例配置**

```json
"pairlists": [
    {
        "method": "PercentChangePairList",
        "number_assets": 15,
        "sort_key": "percentage",
        "min_value": 0,
        "refresh_period": 3600,
        "lookback_timeframe": "1h",
        "lookback_period": 72
    }
],
```

此示例通过使用 `lookback_timeframe` 作为蜡烛大小和指定蜡烛数量的 `lookback_period`，基于 3 天的 1 小时蜡烛滚动周期构建百分比变化交易对。

价格百分比变化使用以下公式计算，该公式表示当前蜡烛收盘价与前一蜡烛收盘价之间的百分比差异，由指定的时间框架和回看周期定义：

$$ Percent Change = (\frac{Current Close - Previous Close}{Previous Close}) * 100 $$

!!! Warning "范围回看和刷新周期"
    当与 `lookback_days` 和 `lookback_timeframe` 结合使用时，`refresh_period` 不能小于以秒为单位的蜡烛大小。因为这会导致对交易所 API 的不必要请求。

!!! Warning "使用回看范围时的性能影响"
    如果在第一个位置与回看结合使用，基于范围的百分比变化计算可能会消耗时间和资源，因为它会为所有可交易对下载蜡烛。因此，强烈建议使用标准方法配合 `PercentChangePairList` 缩小交易对列表以进行进一步的百分比变化计算。

!!! Note "回测"
    `PercentChangePairList` 不支持回测模式。

#### ProducerPairList

使用 `ProducerPairList`，您可以重用来自[生产者](producer-consumer.md)的交易对列表，而无需在每个消费者上显式定义交易对列表。

此交易对列表需要[消费者模式](producer-consumer.md)才能工作。

交易对列表将对活动交易对执行检查，以针对当前交易所配置，避免尝试在无效市场上交易。

您可以使用可选参数 `number_assets` 限制交易对列表的长度。使用 `"number_assets"=0` 或省略此键将导致重用当前设置有效的所有生产者交易对。

```json
"pairlists": [
    {
        "method": "ProducerPairList",
        "number_assets": 5,
        "producer_name": "default",
    }
],
```

!!! Tip "组合交易对列表"
    此交易对列表可以与所有其他交易对列表和过滤器组合以进一步减少交易对列表，也可以作为"附加"交易对列表，在已定义的交易对之上。
    `ProducerPairList` 也可以多次顺序使用，组合来自多个生产者的交易对。
    显然，在这种复杂配置中，生产者可能不会为所有交易对提供数据，因此策略必须适合此情况。

#### RemotePairList

它允许用户从远程服务器或 freqtrade 目录内本地存储的 json 文件获取交易对列表，从而实现动态更新和交易对列表的自定义。

RemotePairList 在配置设置的 pairlists 部分中定义。它使用以下配置选项：

```json
"pairlists": [
    {
        "method": "RemotePairList",
        "mode": "whitelist",
        "processing_mode": "filter",
        "pairlist_url": "https://example.com/pairlist",
        "number_assets": 10,
        "refresh_period": 1800,
        "keep_pairlist_on_failure": true,
        "read_timeout": 60,
        "bearer_token": "my-bearer-token",
        "save_to_file": "user_data/filename.json" 
    }
]
```

可选的 `mode` 选项指定交易对列表应作为 `blacklist` 还是 `whitelist` 使用。默认值为 "whitelist"。

RemotePairList 配置中的可选 `processing_mode` 选项确定如何处理检索到的交易对列表。它可以有两个值："filter" 或 "append"。默认值为 "filter"。

在 "filter" 模式下，检索到的交易对列表用作过滤器。只有同时存在于原始交易对列表和检索到的交易对列表中的交易对才会包含在最终交易对列表中。其他交易对被过滤掉。

在 "append" 模式下，检索到的交易对列表会添加到原始交易对列表中。两个列表中的所有交易对都包含在最终交易对列表中，无需任何过滤。

`pairlist_url` 选项指定交易对列表所在的远程服务器的 URL，或本地文件的路径（如果前缀为 file:///）。这允许用户使用远程服务器或本地文件作为交易对列表的源。

当提供有效文件名时，`save_to_file` 选项将处理后的交易对列表以 JSON 格式保存到该文件。此选项是可选的，默认情况下，交易对列表不会保存到文件。

??? Example "多机器人共享交易对列表示例"

    可以使用 `save_to_file` 将交易对列表保存到 Bot1 的文件中：

    ```json
    "pairlists": [
        {
            "method": "RemotePairList",
            "mode": "whitelist",
            "pairlist_url": "https://example.com/pairlist",
            "number_assets": 10,
            "refresh_period": 1800,
            "keep_pairlist_on_failure": true,
            "read_timeout": 60,
            "save_to_file": "user_data/filename.json" 
        }
    ]
    ```

    此保存的交易对列表文件可以由 Bot2 或任何具有此配置的附加机器人加载：

    ```json
    "pairlists": [
        {
            "method": "RemotePairList",
            "mode": "whitelist",
            "pairlist_url": "file:///user_data/filename.json",
            "number_assets": 10,
            "refresh_period": 10,
            "keep_pairlist_on_failure": true,
        }
    ]
    ```    

用户负责提供返回以下结构的 JSON 对象的服务器或本地文件：

```json
{
    "pairs": ["XRP/USDT", "ETH/USDT", "LTC/USDT"],
    "refresh_period": 1800
}
```

`pairs` 属性应包含机器人要使用的交易对字符串列表。`refresh_period` 属性是可选的，指定交易对列表在刷新之前应缓存的秒数。

可选的 `keep_pairlist_on_failure` 指定如果远程服务器无法访问或返回错误，是否应使用先前接收的交易对列表。默认值为 true。

可选的 `read_timeout` 指定等待远程源响应的最长时间（以秒为单位），默认值为 60。

可选的 `bearer_token` 将包含在请求的 Authorization Header 中。

!!! Note "注意"
    如果服务器出错，如果 `keep_pairlist_on_failure` 设置为 true，将保留最后接收的交易对列表，如果设置为 false，则返回空交易对列表。

#### MarketCapPairList

`MarketCapPairList` 根据 CoinGecko 的市值排名对交易对进行排序/过滤。返回的交易对列表将根据其市值排名进行排序。

```json
"pairlists": [
    {
        "method": "MarketCapPairList",
        "number_assets": 20,
        "max_rank": 50,
        "refresh_period": 86400,
        "categories": ["layer-1"]
    }
]
```

`number_assets` 定义交易对列表返回的最大交易对数量。`max_rank` 将确定在创建/过滤交易对列表时使用的最大排名。预计在排名前 `max_rank` 市值中的一些币种不会包含在结果交易对列表中，因为并非所有交易对在您首选的市场/抵押/交易所组合中都有活跃的交易对。
虽然支持使用大于 250 的 `max_rank`，但不推荐，因为它会导致对 CoinGecko 进行多次 API 调用，这可能导致速率限制问题。

`refresh_period` 设置定义刷新市值排名数据的间隔（以秒为单位）。默认为 86,400 秒（1 天）。交易对列表缓存（`refresh_period`）适用于生成交易对列表（在列表中的第一个位置时）和过滤实例（不在列表中的第一个位置时）。

`categories` 设置指定从哪些 [coingecko 类别](https://www.coingecko.com/en/categories) 中选择币种。默认为空列表 `[]`，意味着不应用类别过滤。
如果选择了错误的类别字符串，插件将打印来自 CoinGecko 的可用类别并失败。类别应该是类别的 ID，例如，对于 `https://www.coingecko.com/en/categories/layer-1`，类别 ID 将是 `layer-1`。您可以传递多个类别，例如 `["layer-1", "meme-token"]`，以从多个类别中进行选择。

像 1000PEPE/USDT 或 KPEPE/USDT:USDT 这样的币种是在尽力而为的基础上检测的，使用前缀 `1000` 和 `K` 来识别它们。

!!! Warning "多个类别"
    每个添加的类别对应一次对 CoinGecko 的 API 调用。您添加的类别越多，交易对列表生成所需的时间越长，可能导致速率限制问题。

!!! Danger "coingecko 中的重复符号"
    Coingecko 经常有重复符号，同一符号用于不同的币种。Freqtrade 将按原样使用符号并尝试在交易所上搜索它。如果符号存在 - 它将被使用。但是，Freqtrade 不会检查*预期的*符号是否是 coingecko 指的那个。这有时可能导致意外结果，特别是在低交易量币种或 meme 币类别中。

#### AgeFilter

删除在交易所上市少于 `min_days_listed` 天（默认为 `10`）或超过 `max_days_listed` 天（默认为 `None` 表示无限）的交易对。

当交易对首次在交易所上市时，它们可能在最初几天经历巨大的价格下跌和波动
在交易对经历价格发现期间。机器人经常
在交易对完成价格下跌之前就被抓住买入。

此过滤器允许 freqtrade 忽略交易对，直到它们至少上市 `min_days_listed` 天并在 `max_days_listed` 之前上市。

#### DelistFilter

删除将在从现在起最多 `max_days_from_now` 天内在交易所下市的交易对（默认为 `0`，这将删除所有未来下市的交易对，无论距离现在多远）。目前此过滤器仅支持以下交易所：

!!! Note "可用交易所"
    下市过滤器仅在 Binance 上可用，其中 Binance Futures 将在模拟和实盘模式下工作，而 Binance Spot 仅限于实盘模式（由于技术原因）。

!!! Warning "回测"
    `DelistFilter` 不支持回测模式。

#### FullTradesFilter

当交易槽位已满时（当配置中 `max_open_trades` 未设置为 `-1` 时），将白名单缩小为仅包含交易中的交易对。

当交易槽位已满时，无需计算其余交易对的指标（信息性交易对除外），因为无法打开新交易。通过将白名单缩小为仅交易中的交易对，您可以提高计算速度并减少 CPU 使用。当交易槽位空闲时（交易关闭或配置中的 `max_open_trades` 值增加），白名单将恢复正常状态。

当使用多个交易对列表过滤器时，建议将此过滤器放在主要交易对列表下方的第二个位置，这样当交易槽位已满时，机器人不必为其余过滤器下载数据。

!!! Warning "回测"
    `FullTradesFilter` 不支持回测模式。

#### OffsetFilter

通过给定的 `offset` 值偏移传入的交易对列表。

例如，它可以与 `VolumeFilter` 结合使用以删除前 X 个成交量交易对。或者将更大的交易对列表拆分为两个机器人实例。

示例删除交易对列表中的前 10 个交易对，并取接下来的 20 个（取初始列表的项目 10-30）：

```json
"pairlists": [
    // ...
    {
        "method": "OffsetFilter",
        "offset": 10,
        "number_assets": 20
    }
],
```

!!! Warning "警告"
    当 `OffsetFilter` 与 `VolumeFilter` 结合用于在多个机器人之间拆分更大的交易对列表时
    不能保证交易对不会重叠，因为 `VolumeFilter` 的刷新间隔略有不同。

!!! Note "注意"
    大于传入交易对列表总长度的偏移将导致空交易对列表。

#### PerformanceFilter

按过去的交易表现对交易对进行排序，如下：

1. 正表现。
2. 尚未有已关闭交易。
3. 负表现。

交易计数用作决胜局。

您可以使用 `minutes` 参数仅考虑过去 X 分钟的表现（滚动窗口）。
不定义此参数（或将其设置为 0）将使用全时表现。

可选的 `min_profit`（作为比率 -> 设置为 `0.01` 对应于 1%）参数定义交易对必须具有的最小利润才能被考虑。
低于此水平的交易对将被过滤掉。
强烈不鼓励在没有 `minutes` 的情况下使用此参数，因为这可能导致空交易对列表且无法恢复。

```json
"pairlists": [
    // ...
    {
        "method": "PerformanceFilter",
        "minutes": 1440,  // 滚动 24 小时
        "min_profit": 0.01  // 最小利润 1%
    }
],
```

由于此过滤器使用机器人的过去表现，它会有一些启动期 - 应该仅在机器人数据库中有几百笔交易后使用。

!!! Warning "回测"
    `PerformanceFilter` 不支持回测模式。

#### PrecisionFilter

过滤不允许设置止损的低价值币种。

即，如果止损价格的 1% 或更多差异是由交易所的精度舍入引起的，即 `rounded(stop_price) <= rounded(stop_price * 0.99)`，则交易对被列入黑名单。这样做的目的是避免价值非常接近其较低交易边界的币种，不允许设置适当的止损。

!!! Tip "PrecisionFilter 对期货交易毫无意义"
    以上不适用于空头。对于多头，理论上交易将首先被清算。

!!! Warning "回测"
    `PrecisionFilter` 不支持使用多个策略的回测模式。

#### PriceFilter

`PriceFilter` 允许按价格过滤交易对。目前支持以下价格过滤器：

* `min_price`
* `max_price`
* `max_value`
* `low_price_ratio`

`min_price` 设置删除价格低于指定价格的交易对。如果您希望避免交易非常低价的交易对，这很有用。
默认情况下禁用此选项，仅在设置为 > 0 时适用。

`max_price` 设置删除价格高于指定价格的交易对。如果您希望仅交易低价交易对，这很有用。
默认情况下禁用此选项，仅在设置为 > 0 时适用。

`max_value` 设置删除最小价值变化高于指定值的交易对。
当交易所具有不平衡限制时，这很有用。例如，如果步长 = 1（因此您只能买入 1、2 或 3，但不能买入 1.1 个币）- 并且价格相当高（如 20 美元），因为币自上次限制调整以来急剧上涨。
由于上述原因，您只能以 20 美元或 40 美元购买 - 但不能以 25 美元购买。
在从接收货币中扣除费用的交易所（例如 binance）上 - 这可能导致高价值币/金额无法出售，因为金额略低于限制。

`low_price_ratio` 设置删除价格上涨 1 个价格单位（点）高于 `low_price_ratio` 比率的交易对。
默认情况下禁用此选项，仅在设置为 > 0 时适用。

对于 `PriceFilter`，必须应用其 `min_price`、`max_price` 或 `low_price_ratio` 设置中的至少一个。

计算示例：

SHITCOIN/BTC 的最小价格精度为 8 位小数。如果其价格为 0.00000011 - 一个价格步骤向上将是 0.00000012，这比先前的价格值高约 9%。您可以通过将 PriceFilter 与设置为 0.09（9%）的 `low_price_ratio` 或相应地设置为 0.00000011 的 `min_price` 来过滤掉此交易对。

!!! Warning "低价交易对"
    具有高"1 点变动"的低价交易对是危险的，因为它们通常缺乏流动性，并且也可能无法设置所需的止损，这通常可能导致高损失，因为价格需要舍入到下一个可交易价格 - 因此，不是有 -5% 的止损，您可能会因为价格舍入而最终有 -9% 的止损。

#### ShuffleFilter

随机打乱交易对列表中的交易对。当您希望所有交易对以相同优先级处理时，可用于防止机器人更频繁地交易某些交易对。

默认情况下，ShuffleFilter 将每个蜡烛打乱一次交易对。
要在每次迭代时打乱，将 `"shuffle_frequency"` 设置为 `"iteration"`，而不是默认的 `"candle"`。

``` json
    {
        "method": "ShuffleFilter", 
        "shuffle_frequency": "candle",
        "seed": 42
    }

```

!!! Tip "提示"
    您可以为此交易对列表设置 `seed` 值以获得可重现的结果，这对于重复的回测会话很有用。如果未设置 `seed`，交易对将以不可重复的随机顺序打乱。ShuffleFilter 会自动检测运行模式，并且仅在有 `seed` 值设置时，将 `seed` 应用于回测模式。

#### SpreadFilter

删除买卖价差高于指定比率 `max_spread_ratio`（默认为 `0.005`）的交易对。

示例：

如果 `DOGE/BTC` 最大买价为 0.00000026，最小卖价为 0.00000027，则比率计算为：`1 - bid/ask ~= 0.037`，即 `> 0.005`，此交易对将被过滤掉。

#### RangeStabilityFilter

删除在过去 `lookback_days` 天内最低低点和最高高点之间的差异低于 `min_rate_of_change` 或高于 `max_rate_of_change` 的交易对。由于这是一个需要额外数据的过滤器，结果将缓存 `refresh_period`。

在下面的示例中：
如果过去 10 天的交易范围 <1% 或 >99%，则从白名单中删除该交易对。

```json
"pairlists": [
    {
        "method": "RangeStabilityFilter",
        "lookback_days": 10,
        "min_rate_of_change": 0.01,
        "max_rate_of_change": 0.99,
        "refresh_period": 86400
    }
]
```

添加 `"sort_direction": "asc"` 或 `"sort_direction": "desc"` 为此交易对列表启用排序。

!!! Tip "提示"
    此过滤器可用于自动删除稳定币交易对，这些交易对的交易范围非常低，因此极难盈利交易。
    此外，它还可以用于自动删除在给定时间内具有极高/极低方差的交易对。

#### VolatilityFilter

波动率是交易对随时间的历史变化程度，通过对数日收益的标准差来测量。收益假设为正态分布，尽管实际分布可能不同。在正态分布中，68% 的观测值落在一个标准差内，95% 的观测值落在两个标准差内。假设波动率为 0.05 意味着预期 30 天中有 20 天的收益预期小于 5%（一个标准差）。波动率是预期收益偏差的正比率，可以大于 1.00。请参阅维基百科的[`波动率`](https://en.wikipedia.org/wiki/Volatility_(finance))定义。

如果过去 `lookback_days` 天的平均波动率低于 `min_volatility` 或高于 `max_volatility`，此过滤器将删除交易对。由于这是一个需要额外数据的过滤器，结果将缓存 `refresh_period`。

此过滤器可用于将您的交易对缩小到某个波动率或避免非常波动的交易对。

在下面的示例中：
如果过去 10 天的波动率不在 0.05-0.50 范围内，则从白名单中删除该交易对。过滤器每 24 小时应用一次。

```json
"pairlists": [
    {
        "method": "VolatilityFilter",
        "lookback_days": 10,
        "min_volatility": 0.05,
        "max_volatility": 0.50,
        "refresh_period": 86400
    }
]
```

添加 `"sort_direction": "asc"` 或 `"sort_direction": "desc"` 为此交易对列表启用排序模式。

### 交易对列表处理器的完整示例

下面的示例将 `BNB/BTC` 列入黑名单，使用 `VolumePairList`，有 `20` 个资产，按 `quoteVolume` 对交易对进行排序，然后使用 [`DelistFilter`](#delistfilter) 和 [`AgeFilter`](#agefilter) 过滤未来下市的交易对，删除上市少于 10 天的交易对。之后应用 [`PrecisionFilter`](#precisionfilter) 和 [`PriceFilter`](#pricefilter)，过滤所有 1 个价格单位 > 1% 的资产。然后应用 [`SpreadFilter`](#spreadfilter) 和 [`VolatilityFilter`](#volatilityfilter)，最后使用设置为某个预定义值的随机种子对交易对进行打乱。

```json
"exchange": {
    "pair_whitelist": [],
    "pair_blacklist": ["BNB/BTC"]
},
"pairlists": [
    {
        "method": "VolumePairList",
        "number_assets": 20,
        "sort_key": "quoteVolume"
    },
    {
        "method": "DelistFilter",
        "max_days_from_now": 0,
    },
    {"method": "AgeFilter", "min_days_listed": 10},
    {"method": "PrecisionFilter"},
    {"method": "PriceFilter", "low_price_ratio": 0.01},
    {"method": "SpreadFilter", "max_spread_ratio": 0.005},
    {
        "method": "RangeStabilityFilter",
        "lookback_days": 10,
        "min_rate_of_change": 0.01,
        "refresh_period": 86400
    },
    {
        "method": "VolatilityFilter",
        "lookback_days": 10,
        "min_volatility": 0.05,
        "max_volatility": 0.50,
        "refresh_period": 86400
    },
    {"method": "ShuffleFilter", "seed": 42}
],
```
