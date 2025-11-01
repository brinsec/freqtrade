# Freqtrade 常见问题

## 支持的市场

Freqtrade 支持现货交易，以及某些选定交易所的（隔离）期货交易。请参阅 [文档起始页](index.md#supported-futures-exchanges-experimental) 以获取最新的支持交易所列表。

### 我的机器人可以开空头头寸吗？

Freqtrade 可以在期货市场中开空头头寸。
这需要为策略设计，并在配置中设置 `"trading_mode": "futures"`。
请确保先阅读 [相关文档页面](leverage.md)。

在现货市场中，您在某些情况下可以使用杠杆现货代币，这些代币反映反向交易对（例如 BTCUP/USD、BTCDOWN/USD、ETHBULL/USD、ETHBEAR/USD 等），可以使用 Freqtrade 进行交易。

### 我的机器人可以交易期权或期货吗？

某些交易所支持期货交易。请参阅 [文档起始页](index.md#supported-futures-exchanges-experimental) 以获取最新的支持交易所列表。

## 新手提示和技巧

* 当您使用策略和超参数优化文件时，应使用适当的代码编辑器，如 VSCode 或 PyCharm。好的代码编辑器将提供语法高亮以及行号，使查找语法错误变得容易（Freqtrade 在启动时最有可能指出这些错误）。

## Freqtrade 常见问题

### Freqtrade 可以并行在同一交易对上开多个头寸吗？

不可以。Freqtrade 一次只能为每个交易对开一个头寸。
但是，您可以使用 [`adjust_trade_position()` 回调](strategy-callbacks.md#adjust-trade-position) 来调整未平仓头寸。

回测在 `--eps` 中提供了此选项 - 但这只是为了突出显示"隐藏"信号，在实盘中不起作用。

### 机器人无法启动

使用 `freqtrade trade --config config.json` 运行机器人时显示输出 `freqtrade: command not found`。

这可能是由以下原因引起的：

* 虚拟环境未激活。
  * 运行 `source .venv/bin/activate` 以激活虚拟环境。
* 安装未成功完成。
  * 请检查 [安装文档](installation.md)。

### 机器人启动，但处于 STOPPED 模式

确保在 config.json 中将 `initial_state` 配置选项设置为 `"running"`

### 我已经等了 5 分钟，为什么机器人还没有进行任何交易？

* 根据入场策略、白名单币种数量、市场情况等，找到良好的入场位置可能需要数小时或数天。请耐心等待！

* 回测会告诉您大致预期的交易数量 - 但这不能保证它们会在时间上均匀分布 - 因此您可能在某一天有 20 笔交易，而本周其余时间为 0 笔。

* 这可能是由于配置错误。最好检查日志，它们通常会告诉您机器人是否根本没有收到买入信号（只有心跳消息），或者是否有问题（日志中的错误/异常）。

### 我已经做了 12 笔交易，为什么我的总利润是负数？

我理解您的失望，但不幸的是，12 笔交易不足以说明任何问题。如果您运行回测，您可以看到当前算法确实会让您处于盈利状态，但这是在数千笔交易之后，即使在那里，您也会在特定币种上留下亏损，这些币种您已经交易了数十次甚至数百次。我们当然不断努力提高机器人，但它将_始终_是一场赌博，应该让您在月度基础上获得适度的收益，但您无法从少数交易中得出太多结论。

### 我想更改配置。我可以不杀死机器人就做到这一点吗？

是的。您可以编辑配置并使用 `/reload_config` 命令重新加载配置。机器人将停止，重新加载配置和策略，并使用新的配置和策略重新启动。

### 为什么我的机器人不卖出它购买的所有东西？

这称为"币种零头"，可能发生在所有交易所。
发生这种情况是因为许多交易所从"接收货币"中扣除手续费 - 所以您购买 100 COIN - 但您只能得到 99.9 COIN。
由于 COIN 以整批大小（1COIN 步长）进行交易，您不能卖出 0.9 COIN（或 99.9 COIN）- 但您需要向下舍入到 99 COIN。

这不是机器人问题，但在手动交易时也会发生。

虽然 freqtrade 可以处理这个问题（它会卖出 99 COIN），但手续费通常低于最低可交易批量（您只能交易整 COIN，不能交易 0.9 COIN）。
将零头（0.9 COIN）留在交易所通常是有意义的，因为下次 freqtrade 购买 COIN 时，它会消耗剩余的少量余额，这次会卖出它购买的所有东西，因此零头余额会慢慢下降（尽管它很可能永远不会达到正好 0）。

在可能的情况下（例如在 binance 上），使用交易所的专用手续费货币将解决此问题。
在 binance 上，只需在您的账户中拥有 BNB，并在您的个人资料中启用"使用 BNB 支付手续费"。您的 BNB 余额将慢慢下降（因为它用于支付手续费）- 但您将不再遇到零头（Freqtrade 将在利润计算中包括手续费）。
其他交易所不提供这种可能性，这只是您必须接受或转移到不同交易所的事情。

### 我向交易所存入了更多资金，但我的机器人没有识别这一点

Freqtrade 将在必要时更新交易所余额（在下单之前）。
RPC 调用（Telegram 的 `/balance`、对 `/balance` 的 API 调用）最多每小时可以触发一次更新。

如果启用了 `adjust_trade_position`（并且机器人有符合条件的未平仓交易进行调整）- 那么钱包将每小时刷新一次。
要强制立即更新，您可以使用 `/reload_config` - 这将重启机器人。

### 我想使用不完整的蜡烛图

Freqtrade 不会向策略提供不完整的蜡烛图。使用不完整的蜡烛图会导致重绘，从而导致策略中出现"幽灵"买入，这在回测中以及在发生之后都无法验证。

您可以使用 [dataprovider](strategy-customization.md#orderbookpair-maximum) 的订单簿或行情方法使用"当前"市场数据 - 但这不能在回测期间使用。

### Is there a setting to only Exit the trades being held and not perform any new Entries?

You can use the `/stopentry` command in Telegram to prevent future trade entry, followed by `/forceexit all` (sell all open trades).

### I sold the bot's capital and now there's errors in the log

Freqtrade assumes that the trades it opens are managed only though the bot.  
If you happen to (accidentally) sell the bot's capital, freqtrade will try to recover by trying to re-find on-exchange orders.

This is a best-effort approach, and will not work in all cases, especially when using order types that are not supported by freqtrade (OCO, iceberg, etc.), or when working with older trades (where the exchange no longer provides full order information).
The exact limits will vary between exchanges - with the details usually being documented in the exchange's API documentation.

### I want to run multiple bots on the same machine

Please look at the [advanced setup documentation Page](advanced-setup.md#running-multiple-instances-of-freqtrade).

### I'm getting "Impossible to load Strategy" when starting the bot

This error message is shown when the bot cannot load the strategy.
Usually, you can use `freqtrade list-strategies` to list all available strategies. 
The output of this command will also include a status column, showing if the strategy can be loaded.

Please check the following:

* Are you using the correct strategy name? The strategy name is case-sensitive and must correspond to the Strategy class name (not the filename!).
* Is the strategy in the `user_data/strategies` directory, and has the file-ending `.py`?
* Does the bot show other warnings before this error? Maybe you're missing some dependencies for the strategy - which would be highlighted in the log.
* In case of docker - is the strategy directory mounted correctly (check the volumes part of the docker-compose file)?

### I'm getting "Missing data fillup" messages in the log

This message is just a warning that the latest candles had missing candles in them.
Depending on the exchange, this can indicate that the pair didn't have a trade for the timeframe you are using - and the exchange does only return candles with volume.
On low volume pairs, this is a rather common occurrence.

If this happens for all pairs in the pairlist, this might indicate a recent exchange downtime. Please check your exchange's public channels for details.

Irrespectively of the reason, Freqtrade will fill up these candles with "empty" candles, where open, high, low and close are set to the previous candle close - and volume is empty. In a chart, this will look like a `_` - and is aligned with how exchanges usually represent 0 volume candles.

### I'm getting "Price jump between 2 candles detected"

This message is a warning that the candles had a price jump of > 30%.
This might be a sign that the pair stopped trading, and some token exchange took place (e.g. COCOS in 2021 - where price jumped from 0.0000154 to 0.01621).
This message is often accompanied by ["Missing data fillup"](#im-getting-missing-data-fillup-messages-in-the-log) - as trading on such pairs is often stopped for some time.

### I want to reset the bot's database

To reset the bot's database, you can either delete the database (by default `tradesv3.sqlite` or `tradesv3.dryrun.sqlite`), or use a different database url via `--db-url` (e.g. `sqlite:///mynewdatabase.sqlite`).

### I'm getting "Outdated history for pair xxx" in the log

The bot is trying to tell you that it got an outdated last candle (not the last complete candle).
As a consequence, Freqtrade will not enter a trade for this pair - as trading on old information is usually not what is desired.

This warning can point to one of the below problems:

* Exchange downtime -> Check your exchange status page / blog / twitter feed for details.
* Wrong system time -> Ensure your system-time is correct.
* Barely traded pair -> Check the pair on the exchange webpage, look at the timeframe your strategy uses. If the pair does not have any volume in some candles (usually visualized with a "volume 0" bar, and a "_" as candle), this pair did not have any trades in this timeframe. These pairs should ideally be avoided, as they can cause problems with order-filling.
* API problem -> API returns wrong data (this only here for completeness, and should not happen with supported exchanges).

### I get the message "Couldn't reuse watch for xxx" in the log

This is an informational message that the bot tried to use candles from the websocket, but the exchange didn't provide the right information.
This can happen if there was an interruption to the websocket connection - or if the pair didn't have any trades happen in the timeframe you are using.

Freqtrade will handle this gracefully by falling back to the REST api.
While this makes the iteration slightly slower (due to the REST Api call) - it will not cause any problems to the bot's operation.

### I'm getting the "Exchange XXX does not support market orders." message and cannot run my strategy

As the message says, your exchange does not support market orders and you have one of the [order types](configuration.md/#understand-order_types) set to "market". Your strategy was probably written with other exchanges in mind and sets "market" orders for "stoploss" orders, which is correct and preferable for most of the exchanges supporting market orders (but not for Gate.io).

To fix this, redefine order types in the strategy to use "limit" instead of "market":

``` python
    order_types = {
        ...
        "stoploss": "limit",
        ...
    }
```

The same fix should be applied in the configuration file, if order types are defined in your custom config rather than in the strategy.

### I'm trying to start the bot live, but get an API permission error

Errors like `Invalid API-key, IP, or permissions for action` mean exactly what they actually say.  
Your API key is either invalid (copy/paste error? check for leading/trailing spaces in the config), expired, or the IP you're running the bot from is not enabled in the Exchange's API console.  
Usually, the permission "Spot Trading" (or the equivalent in the exchange you use) will be necessary.  
Futures will usually have to be enabled specifically.

### How do I search the bot logs for something?

By default, the bot writes its log into stderr stream. This is implemented this way so that you can easily separate the bot's diagnostics messages from Backtesting, Edge and Hyperopt results, output from other various Freqtrade utility sub-commands, as well as from the output of your custom `print()`'s you may have inserted into your strategy. So if you need to search the log messages with the grep utility, you need to redirect stderr to stdout and disregard stdout.

* In unix shells, this normally can be done as simple as:
```shell
$ freqtrade --some-options 2>&1 >/dev/null | grep 'something'
```
(note, `2>&1` and `>/dev/null` should be written in this order)

* Bash interpreter also supports so called process substitution syntax, you can grep the log for a string with it as:
```shell
$ freqtrade --some-options 2> >(grep 'something') >/dev/null
```
or
```shell
$ freqtrade --some-options 2> >(grep -v 'something' 1>&2)
```

* You can also write the copy of Freqtrade log messages to a file with the `--logfile` option:
```shell
$ freqtrade --logfile /path/to/mylogfile.log --some-options
```
and then grep it as:
```shell
$ cat /path/to/mylogfile.log | grep 'something'
```
or even on the fly, as the bot works and the log file grows:
```shell
$ tail -f /path/to/mylogfile.log | grep 'something'
```
from a separate terminal window.

On Windows, the `--logfile` option is also supported by Freqtrade and you can use the `findstr` command to search the log for the string of interest:
```
> type \path\to\mylogfile.log | findstr "something"
```

## Hyperopt module

### Why does freqtrade not have GPU support?

First of all, most indicator libraries don't have GPU support - as such, there would be little benefit for indicator calculations.
The GPU improvements would only apply to pandas-native calculations - or ones written by yourself.

GPU's are only good at crunching numbers (floating point operations).
For hyperopt, we need both number-crunching (find next parameters) and running python code (running backtesting).
As such, GPU's are not too well suited for most parts of hyperopt.

The benefit of using GPU would therefore be pretty slim - and will not justify the complexity introduced by trying to add GPU support.

There is however nothing preventing you from using GPU-enabled indicators within your strategy if you think you must have this - you will however probably be disappointed by the slim gain that will give you (compared to the complexity).

### How many epochs do I need to get a good Hyperopt result?

Per default Hyperopt called without the `-e`/`--epochs` command line option will only
run 100 epochs, means 100 evaluations of your triggers, guards, ... Too few
to find a great result (unless if you are very lucky), so you probably
have to run it for 10000 or more. But it will take an eternity to
compute.

Since hyperopt uses Bayesian search, running for too many epochs may not produce greater results.

It's therefore recommended to run between 500-1000 epochs over and over until you hit at least 10000 epochs in total (or are satisfied with the result). You can best judge by looking at the results - if the bot keeps discovering better strategies, it's best to keep on going.

```bash
freqtrade hyperopt --hyperopt-loss SharpeHyperOptLossDaily --strategy SampleStrategy -e 1000
```

### Why does it take a long time to run hyperopt?

* Discovering a great strategy with Hyperopt takes time. Study www.freqtrade.io, the Freqtrade Documentation page, join the Freqtrade [discord community](https://discord.gg/p7nuUNVfP7). While you patiently wait for the most advanced, free crypto bot in the world, to hand you a possible golden strategy specially designed just for you.

* If you wonder why it can take from 20 minutes to days to do 1000 epochs here are some answers:

This answer was written during the release 0.15.1, when we had:

* 8 triggers
* 9 guards: let's say we evaluate even 10 values from each
* 1 stoploss calculation: let's say we want 10 values from that too to be evaluated

The following calculation is still very rough and not very precise
but it will give the idea. With only these triggers and guards there is
already 8\*10^9\*10 evaluations. A roughly total of 80 billion evaluations.
Did you run 100 000 evaluations? Congrats, you've done roughly 1 / 100 000 th
of the search space, assuming that the bot never tests the same parameters more than once.

* The time it takes to run 1000 hyperopt epochs depends on things like: The available cpu, hard-disk, ram, timeframe, timerange, indicator settings, indicator count, amount of coins that hyperopt test strategies on and the resulting trade count - which can be 650 trades in a year or 100000 trades depending if the strategy aims for big profits by trading rarely or for many low profit trades.

Example: 4% profit 650 times vs 0,3% profit a trade 10000 times in a year. If we assume you set the --timerange to 365 days.

Example:
`freqtrade --config config.json --strategy SampleStrategy --hyperopt SampleHyperopt -e 1000 --timerange 20190601-20200601`

## Official channels

Freqtrade is using exclusively the following official channels:

* [Freqtrade discord server](https://discord.gg/p7nuUNVfP7)
* [Freqtrade documentation (https://freqtrade.io)](https://freqtrade.io)
* [Freqtrade github organization](https://github.com/freqtrade)

Nobody affiliated with the freqtrade project will ask you about your exchange keys or anything else exposing your funds to exploitation.
Should you be asked to expose your exchange keys or send funds to some random wallet, then please don't follow these instructions.

Failing to follow these guidelines will not be responsibility of freqtrade.

## Support policy

We provide free support for Freqtrade on our [Discord server](https://discord.gg/p7nuUNVfP7) and via GitHub issues.
We only support the most recent release (e.g. 2025.8) and the current development branch (e.g. 2025.9-dev).

If you're on an older version, please follow the [upgrade instructions](updating.md) and see if your problem has already been addressed.

## "Freqtrade token"

Freqtrade does not have a Crypto token offering.

Token offerings you find on the internet referring Freqtrade, FreqAI or freqUI must be considered to be a scam, trying to exploit freqtrade's popularity for their own, nefarious gains.
