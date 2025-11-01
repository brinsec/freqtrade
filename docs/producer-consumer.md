# 生产者 / 消费者模式

freqtrade 提供一种机制，其中实例（也称为 `consumer`）可以使用消息 WebSocket 监听来自上游 freqtrade 实例（也称为 `producer`）的消息。主要是 `analyzed_df` 和 `whitelist` 消息。这允许在多个机器人中重用计算的指标（和信号），而无需多次计算它们。

请参阅 REST API 文档中的[消息 WebSocket](rest-api.md#message-websocket) 来设置消息 WebSocket 的 `api_server` 配置（这将是您的生产者）。

!!! Note "注意"
    我们强烈建议将 `ws_token` 设置为只有您自己知道的随机值，以避免未经授权访问您的机器人。

## 配置

通过将 `external_message_consumer` 部分添加到消费者配置文件中来启用订阅实例。

```json
{
    //...
   "external_message_consumer": {
        "enabled": true,
        "producers": [
            {
                "name": "default", // This can be any name you'd like, default is "default"
                "host": "127.0.0.1", // The host from your producer's api_server config
                "port": 8080, // The port from your producer's api_server config
                "secure": false, // Use a secure websockets connection, default false
                "ws_token": "sercet_Ws_t0ken" // The ws_token from your producer's api_server config
            }
        ],
        // The following configurations are optional, and usually not required
        // "wait_timeout": 300,
        // "ping_timeout": 10,
        // "sleep_time": 10,
        // "remove_entry_exit_signals": false,
        // "message_size_limit": 8
    }
    //...
}
```

|  参数 | 描述 |
|------------|-------------|
| `enabled` | **必需。** 启用消费者模式。如果设置为 false，本节中的所有其他设置将被忽略。<br>*默认为 `false`。*<br> **数据类型：** boolean。
| `producers` | **必需。** 生产者列表 <br> **数据类型：** Array。
| `producers.name` | **必需。** 此生产者的名称。如果使用多个生产者，必须在调用 `get_producer_pairs()` 和 `get_producer_df()` 时使用此名称。<br> **数据类型：** string
| `producers.host` | **必需。** 来自生产者的主机名或 IP 地址。<br> **数据类型：** string
| `producers.port` | **必需。** 与上述主机匹配的端口。<br>*默认为 `8080`。*<br> **数据类型：** Integer
| `producers.secure` | **可选。** 在 websockets 连接中使用 ssl。默认 False。<br> **数据类型：** string
| `producers.ws_token` | **必需。** 在生产者上配置的 `ws_token`。<br> **数据类型：** string
| | **可选设置**
| `wait_timeout` | 如果没有收到消息，超时直到我们再次 ping。<br>*默认为 `300`。*<br> **数据类型：** Integer - 以秒为单位。
| `ping_timeout` | Ping 超时 <br>*默认为 `10`。*<br> **数据类型：** Integer - 以秒为单位。
| `sleep_time` | 重试连接之前的睡眠时间。<br>*默认为 `10`。*<br> **数据类型：** Integer - 以秒为单位。
| `remove_entry_exit_signals` | 在收到 dataframe 时从 dataframe 中删除信号列（将它们设置为 0）。<br>*默认为 `false`。*<br> **数据类型：** Boolean。
| `initial_candle_limit` | 从生产者期望的初始蜡烛数。<br>*默认为 `1500`。*<br> **数据类型：** Integer - 蜡烛数。
| `message_size_limit` | 每条消息的大小限制<br>*默认为 `8`。*<br> **数据类型：** Integer - 兆字节。

与在 `populate_indicators()` 中计算指标不同（或除此之外），跟随者实例监听连接到生产者实例的消息（或在高级配置中的多个生产者实例），并请求生产者针对活动白名单中每个交易对最近分析的数据框。

然后，消费者实例将拥有已分析数据框的完整副本，无需自己计算它们。

## Examples

### 示例 - 生产者策略

一个包含多个指标的简单策略。策略本身不需要特殊考虑。

```py
class ProducerStrategy(IStrategy):
    #...
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Calculate indicators in the standard freqtrade way which can then be broadcast to other instances
        """
        dataframe['rsi'] = ta.RSI(dataframe)
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        dataframe['tema'] = ta.TEMA(dataframe, timeperiod=9)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populates the entry signal for the given dataframe
        """
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], self.buy_rsi.value)) &
                (dataframe['tema'] <= dataframe['bb_middleband']) &
                (dataframe['tema'] > dataframe['tema'].shift(1)) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe
```

!!! Tip "FreqAI"
    您可以使用它在强大的机器上设置 [FreqAI](freqai.md)，同时在像树莓派这样的简单机器上运行消费者，这些机器可以以不同的方式解释生产者生成的信号。


### 示例 - 消费者策略

一个逻辑上等效的策略，它本身不计算指标，但将具有相同的已分析数据框，以基于生产器中计算的指标做出交易决策。在此示例中，消费者具有相同的入场标准，但这并非必需。消费者可以使用不同的逻辑进入/退出交易，并且仅使用指定的指标。

```py
class ConsumerStrategy(IStrategy):
    #...
    process_only_new_candles = False # required for consumers

    _columns_to_expect = ['rsi_default', 'tema_default', 'bb_middleband_default']

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Use the websocket api to get pre-populated indicators from another freqtrade instance.
        Use `self.dp.get_producer_df(pair)` to get the dataframe
        """
        pair = metadata['pair']
        timeframe = self.timeframe

        producer_pairs = self.dp.get_producer_pairs()
        # You can specify which producer to get pairs from via:
        # self.dp.get_producer_pairs("my_other_producer")

        # This func returns the analyzed dataframe, and when it was analyzed
        producer_dataframe, _ = self.dp.get_producer_df(pair)
        # You can get other data if the producer makes it available:
        # self.dp.get_producer_df(
        #   pair,
        #   timeframe="1h",
        #   candle_type=CandleType.SPOT,
        #   producer_name="my_other_producer"
        # )

        if not producer_dataframe.empty:
            # If you plan on passing the producer's entry/exit signal directly,
            # specify ffill=False or it will have unintended results
            merged_dataframe = merge_informative_pair(dataframe, producer_dataframe,
                                                      timeframe, timeframe,
                                                      append_timeframe=False,
                                                      suffix="default")
            return merged_dataframe
        else:
            dataframe[self._columns_to_expect] = 0

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populates the entry signal for the given dataframe
        """
        # Use the dataframe columns as if we calculated them ourselves
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi_default'], self.buy_rsi.value)) &
                (dataframe['tema_default'] <= dataframe['bb_middleband_default']) &
                (dataframe['tema_default'] > dataframe['tema_default'].shift(1)) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe
```

!!! Tip "Using upstream signals"
    By setting `remove_entry_exit_signals=false`, you can also use the producer's signals directly. They should be available as `enter_long_default` (assuming `suffix="default"` was used) - and can be used as either signal directly, or as additional indicator.
