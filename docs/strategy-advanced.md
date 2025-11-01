# 高级策略

本页解释了策略中可用的一些高级概念。
如果您刚刚开始，请先熟悉 [Freqtrade 基础知识](bot-basics.md) 和 [策略自定义](strategy-customization.md) 中描述的方法。

这里描述的方法的调用顺序在 [机器人执行逻辑](bot-basics.md#bot-execution-logic) 中有说明。这些文档也有助于决定哪种方法最适合您的自定义需求。

!!! Note "注意"
    回调方法应该*仅在*策略使用它们时实现。

!!! Tip "提示"
    通过运行 `freqtrade new-strategy --strategy MyAwesomeStrategy --template advanced` 从包含所有可用回调方法的策略模板开始。

## 存储信息（持久化）

Freqtrade 允许在数据库中存储/检索与特定交易关联的用户自定义信息。

使用交易对象，可以使用 `trade.set_custom_data(key='my_key', value=my_value)` 存储信息，并使用 `trade.get_custom_data(key='my_key')` 检索信息。每个数据条目都与交易和用户提供的键（`string` 类型）关联。这意味着这只能在也提供交易对象的回调中使用。

为了使数据能够存储在数据库中，freqtrade 必须序列化数据。这是通过将数据转换为 JSON 格式字符串来完成的。
Freqtrade 将尝试在检索时反转此操作，因此从策略角度来看，这应该不相关。

```python
from freqtrade.persistence import Trade
from datetime import timedelta

class AwesomeStrategy(IStrategy):

    def bot_loop_start(self, **kwargs) -> None:
        for trade in Trade.get_open_order_trades():
            fills = trade.select_filled_orders(trade.entry_side)
            if trade.pair == 'ETH/USDT':
                trade_entry_type = trade.get_custom_data(key='entry_type')
                if trade_entry_type is None:
                    trade_entry_type = 'breakout' if 'entry_1' in trade.enter_tag else 'dip'
                elif fills > 1:
                    trade_entry_type = 'buy_up'
                trade.set_custom_data(key='entry_type', value=trade_entry_type)
        return super().bot_loop_start(**kwargs)

    def adjust_entry_price(self, trade: Trade, order: Order | None, pair: str,
                           current_time: datetime, proposed_rate: float, current_order_rate: float,
                           entry_tag: str | None, side: str, **kwargs) -> float:
        # Limit orders to use and follow SMA200 as price target for the first 10 minutes since entry trigger for BTC/USDT pair.
        if (
            pair == 'BTC/USDT' 
            and entry_tag == 'long_sma200' 
            and side == 'long' 
            and (current_time - timedelta(minutes=10)) > trade.open_date_utc 
            and order.filled == 0.0
        ):
            dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
            current_candle = dataframe.iloc[-1].squeeze()
            # store information about entry adjustment
            existing_count = trade.get_custom_data('num_entry_adjustments', default=0)
            if not existing_count:
                existing_count = 1
            else:
                existing_count += 1
            trade.set_custom_data(key='num_entry_adjustments', value=existing_count)

            # adjust order price
            return current_candle['sma_200']

        # default: maintain existing order
        return current_order_rate

    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float, current_profit: float, **kwargs):

        entry_adjustment_count = trade.get_custom_data(key='num_entry_adjustments')
        trade_entry_type = trade.get_custom_data(key='entry_type')
        if entry_adjustment_count is None:
            if current_profit > 0.01 and (current_time - timedelta(minutes=100) > trade.open_date_utc):
                return True, 'exit_1'
        else
            if entry_adjustment_count > 0 and if current_profit > 0.05:
                return True, 'exit_2'
            if trade_entry_type == 'breakout' and current_profit > 0.1:
                return True, 'exit_3

        return False, None
```

上面是一个简单的示例 - 有更简单的方法来检索交易数据，如入场调整。

!!! Note "注意"
    建议使用简单的数据类型 `[bool, int, float, str]` 以确保在序列化需要存储的数据时不会出现问题。
    存储大量数据可能导致意外的副作用，例如数据库变大（因此也会变慢）。

!!! Warning "不可序列化的数据"
    如果提供的数据无法序列化，将记录警告，并且指定 `key` 的条目将包含 `None` 作为数据。

??? Note "所有属性"
    custom-data 通过 Trade 对象具有以下访问器（下面假设为 `trade`）：

    * `trade.get_custom_data(key='something', default=0)` - 以提供的类型返回实际值。
    * `trade.get_custom_data_entry(key='something')` - 返回条目 - 包括元数据。值可通过 `.value` 属性访问。
    * `trade.set_custom_data(key='something', value={'some': 'value'})` - 设置或更新此交易的相应键。值必须可序列化 - 我们建议保持存储的数据相对较小。

    "value" 可以是任何类型（在设置和接收时）- 但必须是 json 可序列化的。

## 存储信息（非持久化）

!!! Warning "已弃用"
    这种存储信息的方法已被弃用，我们建议不要使用非持久化存储。
    请改用 [持久化存储](#storing-information-persistent)。

    因此其内容已折叠。

??? Abstract "存储信息"
    可以通过在策略类中创建新字典来完成信息存储。

    变量的名称可以随意选择，但应该以 `custom_` 为前缀，以避免与预定义的策略变量发生命名冲突。

    ```python
    class AwesomeStrategy(IStrategy):
        # 创建自定义字典
        custom_info = {}

        def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            # 检查条目是否已存在
            if not metadata["pair"] in self.custom_info:
                # 为此交易对创建空条目
                self.custom_info[metadata["pair"]] = {}

            if "crosstime" in self.custom_info[metadata["pair"]]:
                self.custom_info[metadata["pair"]]["crosstime"] += 1
            else:
                self.custom_info[metadata["pair"]]["crosstime"] = 1
    ```

    !!! Warning "警告"
        数据在机器人重启（或配置重新加载）后不会持久化。此外，数据量应保持较小（不要使用 DataFrame 等），否则机器人将开始消耗大量内存并最终耗尽内存并崩溃。

    !!! Note "注意"
        如果数据是特定于交易对的，请确保使用交易对作为字典中的键之一。

## Dataframe 访问

您可以通过从数据提供者查询来在各种策略函数中访问 dataframe。

``` python
from freqtrade.exchange import timeframe_to_prev_date

class AwesomeStrategy(IStrategy):
    def confirm_trade_exit(self, pair: str, trade: 'Trade', order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: 'datetime', **kwargs) -> bool:
        # Obtain pair dataframe.
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)

        # Obtain last available candle. Do not use current_time to look up latest candle, because 
        # current_time points to current incomplete candle whose data is not available.
        last_candle = dataframe.iloc[-1].squeeze()
        # <...>

        # In dry/live runs trade open date will not match candle open date therefore it must be 
        # rounded.
        trade_date = timeframe_to_prev_date(self.timeframe, trade.open_date_utc)
        # Look up trade candle.
        trade_candle = dataframe.loc[dataframe['date'] == trade_date]
        # trade_candle may be empty for trades that just opened as it is still incomplete.
        if not trade_candle.empty:
            trade_candle = trade_candle.squeeze()
            # <...>
```

!!! Warning "Using .iloc[-1]"
    You can use `.iloc[-1]` here because `get_analyzed_dataframe()` only returns candles that backtesting is allowed to see.
    This will not work in `populate_*` methods, so make sure to not use `.iloc[]` in that area.
    Also, this will only work starting with version 2021.5.

***

## Enter Tag

When your strategy has multiple entry signals, you can name the signal that triggered.
Then you can access your entry signal on `custom_exit`

```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe["enter_tag"] = ""
    signal_rsi = (qtpylib.crossed_above(dataframe["rsi"], 35))
    signal_bblower = (dataframe["bb_lowerband"] < dataframe["close"])
    # Additional conditions
    dataframe.loc[
        (
            signal_rsi
            | signal_bblower
            # ... additional signals to enter a long position
        )
        & (dataframe["volume"] > 0)
            , "enter_long"
        ] = 1
    # Concatenate the tags so all signals are kept
    dataframe.loc[signal_rsi, "enter_tag"] += "long_signal_rsi "
    dataframe.loc[signal_bblower, "enter_tag"] += "long_signal_bblower "

    return dataframe

def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                current_profit: float, **kwargs):
    dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
    last_candle = dataframe.iloc[-1].squeeze()
    if "long_signal_rsi" in trade.enter_tag and last_candle["rsi"] > 80:
        return "exit_signal_rsi"
    if "long_signal_bblower" in trade.enter_tag and last_candle["high"] > last_candle["bb_upperband"]:
        return "exit_signal_bblower"
    # ...
    return None

```

!!! Note "注意"
    `enter_tag` 限制为 255 个字符，剩余数据将被截断。

!!! Warning "警告"
    只有一个 `enter_tag` 列，用于多头和空头交易。
    因此，此列必须被视为"最后写入获胜"（它毕竟只是一个 dataframe 列）。
    在复杂情况下，多个信号冲突（或如果信号基于不同条件再次停用），这可能导致错误的结果，将错误的标签应用于入场信号。
    这些结果是策略覆盖先前标签的结果 - 最后一个标签将"粘住"，并且将是 freqtrade 将使用的标签。

## 出场标签

类似于[入场标签](#enter-tag)，您也可以指定出场标签。

``` python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe["exit_tag"] = ""
    rsi_exit_signal = (dataframe["rsi"] > 70)
    ema_exit_signal  = (dataframe["ema20"] < dataframe["ema50"])
    # 附加条件
    dataframe.loc[
        (
            rsi_exit_signal
            | ema_exit_signal
            # ... 退出多头头寸的附加信号
        ) &
        (dataframe["volume"] > 0)
        ,
    "exit_long"] = 1
    # 连接标签以便保留所有信号
    dataframe.loc[rsi_exit_signal, "exit_tag"] += "exit_signal_rsi "
    dataframe.loc[rsi_exit_signal2, "exit_tag"] += "exit_signal_rsi "

    return dataframe
```

提供的出场标签然后用作出场原因 - 并在回测结果中显示为如此。

!!! Note "注意"
    `exit_reason` 限制为 100 个字符，剩余数据将被截断。

## 策略版本

您可以通过使用 "version" 方法来实现自定义策略版本控制，并返回您希望此策略具有的版本。

``` python
def version(self) -> str:
    """
    返回策略的版本。
    """
    return "1.1"
```

!!! Note "注意"
    您应该确保同时实现适当的版本控制（如 git 仓库），因为 freqtrade 不会保留策略的历史版本，所以由用户最终能够回滚到策略的先前版本。

## 派生策略

策略可以从其他策略派生。这避免了自定义策略代码的重复。您可以使用此技术覆盖主策略的一小部分，保持其余部分不变：

``` python title="user_data/strategies/myawesomestrategy.py"
class MyAwesomeStrategy(IStrategy):
    ...
    stoploss = 0.13
    trailing_stop = False
    # 所有其他属性和方法都在这里，因为
    # 它们应该在任何自定义策略中...
    ...

```

``` python title="user_data/strategies/MyAwesomeStrategy2.py"
from myawesomestrategy import MyAwesomeStrategy
class MyAwesomeStrategy2(MyAwesomeStrategy):
    # 覆盖某些内容
    stoploss = 0.08
    trailing_stop = True
```

属性和方法都可以被覆盖，以您需要的方式改变原始策略的行为。

虽然在技术上可以在同一文件中保留子类，但这可能导致超参数优化参数文件的一些问题，因此我们建议使用单独的策略文件，并如上所示导入父策略。

## Embedding Strategies

Freqtrade provides you with an easy way to embed the strategy into your configuration file.
This is done by utilizing BASE64 encoding and providing this string at the strategy configuration field,
in your chosen config file.

### Encoding a string as BASE64

This is a quick example, how to generate the BASE64 string in python

```python
from base64 import urlsafe_b64encode

with open(file, 'r') as f:
    content = f.read()
content = urlsafe_b64encode(content.encode('utf-8'))
```

The variable 'content', will contain the strategy file in a BASE64 encoded form. Which can now be set in your configurations file as following

```json
"strategy": "NameOfStrategy:BASE64String"
```

Please ensure that 'NameOfStrategy' is identical to the strategy name!

## Performance warning

When executing a strategy, one can sometimes be greeted by the following in the logs

> PerformanceWarning: DataFrame is highly fragmented.

This is a warning from [`pandas`](https://github.com/pandas-dev/pandas) and as the warning continues to say:
use `pd.concat(axis=1)`.
This can have slight performance implications, which are usually only visible during hyperopt (when optimizing an indicator).

For example:

```python
for val in self.buy_ema_short.range:
    dataframe[f'ema_short_{val}'] = ta.EMA(dataframe, timeperiod=val)
```

should be rewritten to

```python
frames = [dataframe]
for val in self.buy_ema_short.range:
    frames.append(DataFrame({
        f'ema_short_{val}': ta.EMA(dataframe, timeperiod=val)
    }))

# Combine all dataframes, and reassign the original dataframe column
dataframe = pd.concat(frames, axis=1)
```

Freqtrade does however also counter this by running `dataframe.copy()` on the dataframe right after the `populate_indicators()` method - so performance implications of this should be low to non-existent.
