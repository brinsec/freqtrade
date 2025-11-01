# 交易所特定说明

本页结合了特定于交易所的常见问题和信息，这些信息很可能不适用于其他交易所。

## 支持的交易所功能快速概览

--8<-- "includes/exchange-features.md"

## 交易所配置

Freqtrade 基于支持 100 多个加密货币交易所市场和交易 API 的 [CCXT 库](https://github.com/ccxt/ccxt)。完整的最新列表可以在
[CCXT 仓库主页](https://github.com/ccxt/ccxt/tree/master/python)找到。
但是，机器人仅由开发团队在少数几个交易所进行了测试。
这些交易所的当前列表可以在本文档的"主页"部分找到。

欢迎测试其他交易所并提交您的反馈或 PR 以改进机器人或确认完美运行的交易所。

某些交易所需要特殊配置，可以在下面找到。

### 示例交易所配置

"binance" 的交易所配置如下所示：

```json
"exchange": {
    "name": "binance",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "ccxt_config": {},
    "ccxt_async_config": {},
    // ...
```

### 设置速率限制

通常，CCXT 设置的速率限制是可靠的并且工作良好。
如果遇到与速率限制相关的问题（通常是日志中的 DDOS 异常），很容易将 rateLimit 设置更改为其他值。

```json
"exchange": {
    "name": "kraken",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "ccxt_config": {"enableRateLimit": true},
    "ccxt_async_config": {
        "enableRateLimit": true,
        "rateLimit": 3100
    },
```

此配置启用 kraken，以及速率限制以避免被交易所封禁。
`"rateLimit": 3100` 定义每次调用之间等待 3.1 秒的事件。也可以通过将 `"enableRateLimit"` 设置为 false 来完全禁用它。

!!! Note "注意"
    速率限制的最佳设置取决于交易所和白名单的大小，因此理想参数会根据许多其他设置而变化。
    我们尽可能为每个交易所提供合理的默认值，如果您遇到封禁，请确保启用了 `"enableRateLimit"` 并逐步增加 `"rateLimit"` 参数。

## Binance（币安）

!!! Warning "服务器位置和地理位置 IP 限制"
    请注意，Binance 根据服务器国家/地区限制 API 访问。当前和非详尽的被阻止国家/地区包括加拿大、马来西亚、荷兰和美国。请访问 [binance 条款 > b. 资格](https://www.binance.com/en/terms) 查找最新列表。

Binance 支持 [time_in_force](configuration.md#understand-order_time_in_force)。

!!! Tip "交易所止损"
    Binance 支持 `stoploss_on_exchange` 并使用 `stop-loss-limit` 订单。它提供了巨大的优势，因此我们建议通过在交易所启用止损来从中受益。
    在期货上，Binance 同时支持 `stop-limit` 和 `stop-market` 订单。您可以在 `order_types.stoploss` 配置设置中使用 `"limit"` 或 `"market"` 来决定使用哪种类型。

### Binance 黑名单建议

对于 Binance，建议将 `"BNB/<STAKE>"` 添加到您的黑名单以避免问题，除非您愿意维护足够的额外 `BNB` 在账户上，或者除非您愿意禁用使用 `BNB` 作为手续费。
Binance 账户可能使用 `BNB` 作为手续费，如果交易恰好是 `BNB`，进一步的交易可能会消耗此头寸，并使初始 BNB 交易无法卖出，因为预期金额不再存在。

如果没有足够的 `BNB` 可用于支付交易手续费，则手续费将不会由 `BNB` 支付，也不会发生手续费减少。Freqtrade 永远不会购买 BNB 来支付手续费。BNB 需要为此目的手动购买和监控。

### Binance 站点

Binance 已分为 2 个，用户必须为其交易所使用正确的 ccxt 交易所 ID，否则 API 密钥不会被识别。

* [binance.com](https://www.binance.com/) - 国际用户。使用交易所 id：`binance`。
* [binance.us](https://www.binance.us/) - 美国用户。使用交易所 id：`binanceus`。

### Binance RSA 密钥

Freqtrade 支持 binance RSA API 密钥。

我们建议将它们用作环境变量。

``` bash
export FREQTRADE__EXCHANGE__SECRET="$(cat ./rsa_binance.private)"
```

但是，它们也可以通过配置文件进行配置。由于 json 不支持多行字符串，您必须将所有换行符替换为 `\n` 才能拥有有效的 json 文件。

``` json
// ...
 "key": "<someapikey>",
 "secret": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBABACAFQA<...>s8KX8=\n-----END PRIVATE KEY-----"
// ...
```

### Binance Futures

Binance has specific (unfortunately complex) [Futures Trading Quantitative Rules](https://www.binance.com/en/support/faq/4f462ebe6ff445d4a170be7d9e897272) which need to be followed, and which prohibit a too low stake-amount (among others) for too many orders.
Violating these rules will result in a trading restriction.

When trading on Binance Futures market, orderbook must be used because there is no price ticker data for futures.

``` jsonc
  "entry_pricing": {
      "use_order_book": true,
      "order_book_top": 1,
      "check_depth_of_market": {
          "enabled": false,
          "bids_to_ask_delta": 1
      }
  },
  "exit_pricing": {
      "use_order_book": true,
      "order_book_top": 1
  },
```

#### Binance isolated futures settings

Users will also have to have the futures-setting "Position Mode" set to "One-way Mode", and "Asset Mode" set to "Single-Asset Mode".
These settings will be checked on startup, and freqtrade will show an error if this setting is wrong.

![Binance futures settings](assets/binance_futures_settings.png)

Freqtrade will not attempt to change these settings.

#### Binance BNFCR futures

BNFCR mode are a special type of futures mode on Binance to work around regulatory issues in Europe.  
To use BNFCR futures, you will have to have the following combination of settings:

``` jsonc
{
    // ...
    "trading_mode": "futures",
    "margin_mode": "cross",
    "proxy_coin": "BNFCR",
    "stake_currency": "USDT" // or "USDC"
    // ...
}
```

The `stake_currency` setting defines the markets the bot will be operating in. This choice is really arbitrary.

On the exchange, you'll have to use "Multi-asset Mode" - and "Position Mode set to "One-way Mode".  
Freqtrade will check these settings on startup, but won't attempt to change them.

## Bingx

BingX supports [time_in_force](configuration.md#understand-order_time_in_force) with settings "GTC" (good till cancelled), "IOC" (immediate-or-cancel) and "PO" (Post only) settings.

!!! Tip "Stoploss on Exchange"
    Bingx supports `stoploss_on_exchange` and can use both stop-limit and stop-market orders. It provides great advantages, so we recommend to benefit from it by enabling stoploss on exchange.

## Kraken

Kraken supports [time_in_force](configuration.md#understand-order_time_in_force) with settings "GTC" (good till cancelled), "IOC" (immediate-or-cancel) and "PO" (Post only) settings.

!!! Tip "Stoploss on Exchange"
    Kraken supports `stoploss_on_exchange` and can use both stop-loss-market and stop-loss-limit orders. It provides great advantages, so we recommend to benefit from it.
    You can use either `"limit"` or `"market"` in the `order_types.stoploss` configuration setting to decide which type to use.

### Historic Kraken data

The Kraken API does only provide 720 historic candles, which is sufficient for Freqtrade dry-run and live trade modes, but is a problem for backtesting.
To download data for the Kraken exchange, using `--dl-trades` is mandatory, otherwise the bot will download the same 720 candles over and over, and you'll not have enough backtest data.

To speed up downloading, you can download the [trades zip files](https://support.kraken.com/hc/en-us/articles/360047543791-Downloadable-historical-market-data-time-and-sales-) kraken provides.
These are usually updated once per quarter. Freqtrade expects these files to be placed in `user_data/data/kraken/trades_csv`.

A structure as follows can make sense if using incremental files, with the "full" history in one directory, and incremental files in different directories.
The assumption for this mode is that the data is downloaded and unzipped keeping filenames as they are.
Duplicate content will be ignored (based on timestamp) - though the assumption is that there is no gap in the data.

This means, if your "full" history ends in Q4 2022 - then both incremental updates Q1 2023 and Q2 2023 are available.
Not having this will lead to incomplete data, and therefore invalid results while using the data.

```
└── trades_csv
    ├── Kraken_full_history
    │   ├── BCHEUR.csv
    │   └── XBTEUR.csv
    ├── Kraken_Trading_History_Q1_2023
    │   ├── BCHEUR.csv
    │   └── XBTEUR.csv
    └── Kraken_Trading_History_Q2_2023
        ├── BCHEUR.csv
        └── XBTEUR.csv
```

You can convert these files into freqtrade files:

``` bash
freqtrade convert-trade-data --exchange kraken --format-from kraken_csv --format-to feather
# Convert trade data to different ohlcv timeframes
freqtrade trades-to-ohlcv -p BTC/EUR BCH/EUR --exchange kraken -t 1m 5m 15m 1h
```

The converted data also makes downloading data possible, and will start the download after the latest loaded trade.

``` bash
freqtrade download-data --exchange kraken --dl-trades -p BTC/EUR BCH/EUR 
```

!!! Warning "Downloading data from kraken"
    Downloading kraken data will require significantly more memory (RAM) than any other exchange, as the trades-data needs to be converted into candles on your machine.
    It will also take a long time, as freqtrade will need to download every single trade that happened on the exchange for the pair / timerange combination, therefore please be patient.

!!! Warning "rateLimit tuning"
    Please pay attention that rateLimit configuration entry holds delay in milliseconds between requests, NOT requests/sec rate.
    So, in order to mitigate Kraken API "Rate limit exceeded" exception, this configuration should be increased, NOT decreased.

## Kucoin

Kucoin requires a passphrase for each api key, you will therefore need to add this key into the configuration so your exchange section looks as follows:

```json
"exchange": {
    "name": "kucoin",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```

Kucoin supports [time_in_force](configuration.md#understand-order_time_in_force) with settings "GTC" (good till cancelled), "FOK" (full-or-cancel) and "IOC" (immediate-or-cancel) settings.

!!! Tip "Stoploss on Exchange"
    Kucoin supports `stoploss_on_exchange` and can use both stop-loss-market and stop-loss-limit orders. It provides great advantages, so we recommend to benefit from it.
    You can use either `"limit"` or `"market"` in the `order_types.stoploss` configuration setting to decide which type of stoploss shall be used.

### Kucoin Blacklists

For Kucoin, it is suggested to add `"KCS/<STAKE>"` to your blacklist to avoid issues, unless you are willing to maintain enough extra `KCS` on the account or unless you're willing to disable using `KCS` for fees. 
Kucoin accounts may use `KCS` for fees, and if a trade happens to be on `KCS`, further trades may consume this position and make the initial `KCS` trade unsellable as the expected amount is not there anymore.

## HTX

!!! Tip "Stoploss on Exchange"
    HTX supports `stoploss_on_exchange` and uses `stop-limit` orders. It provides great advantages, so we recommend to benefit from it by enabling stoploss on exchange.

## OKX

OKX requires a passphrase for each api key, you will therefore need to add this key into the configuration so your exchange section looks as follows:

```json
"exchange": {
    "name": "okx",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```

If you've registered with OKX on the host my.okx.com (OKX EAA)- you will need to use `"myokx"` as the exchange name.
Using the wrong exchange will result in the error "OKX Error 50119: API key doesn't exist" - as the 2 are separate entities.

!!! Warning
    OKX only provides 100 candles per api call. Therefore, the strategy will only have a pretty low amount of data available in backtesting mode.

!!! Warning "Futures"
    OKX Futures has the concept of "position mode" - which can be "Buy/Sell" or long/short (hedge mode).
    Freqtrade supports both modes (we recommend to use Buy/Sell mode) - but changing the mode mid-trading is not supported and will lead to exceptions and failures to place trades.
    OKX also only provides MARK candles for the past ~3 months. Backtesting futures prior to that date will therefore lead to slight deviations, as funding-fees cannot be calculated correctly without this data.

## Gate.io

!!! Tip "Stoploss on Exchange"
    Gate.io supports `stoploss_on_exchange` and uses `stop-loss-limit` orders. It provides great advantages, so we recommend to benefit from it by enabling stoploss on exchange.

Gate.io supports [time_in_force](configuration.md#understand-order_time_in_force) with settings "GTC" (good till cancelled), and "IOC" (immediate-or-cancel) settings.

Gate.io allows the use of `POINT` to pay for fees. As this is not a tradable currency (no regular market available), automatic fee calculations will fail (and default to a fee of 0).
The configuration parameter `exchange.unknown_fee_rate` can be used to specify the exchange rate between Point and the stake currency. Obviously, changing the stake-currency will also require changes to this value.

Gate API keys require the following permissions on top of the market type you want to trade:

* "Spot Trade" _or_ "Perpetual Futures" (Read and Write) (either select both, or the one matching the market you want to trade)
* "Wallet" (read only)
* "Account" (read only)

Without these permissions, the bot will not start correctly and show errors like "permission missing".

## Bybit

!!! Tip "Stoploss on Exchange"
    Bybit (futures only) supports `stoploss_on_exchange` and uses `stop-loss-limit` orders. It provides great advantages, so we recommend to benefit from it by enabling stoploss on exchange.
    On futures, Bybit supports both `stop-limit` as well as `stop-market` orders. You can use either `"limit"` or `"market"` in the `order_types.stoploss` configuration setting to decide which type to use.

Bybit supports [time_in_force](configuration.md#understand-order_time_in_force) with settings "GTC" (good till cancelled), "FOK" (full-or-cancel), "IOC" (immediate-or-cancel) and "PO" (Post only) settings.

!!! Warning "Unified accounts"
    Freqtrade assumes accounts to be dedicated to the bot.
    We therefore recommend the usage of one subaccount per bot. This is especially important when using unified accounts.  
    Other configurations (multiple bots on one account, manual non-bot trades on the bot account) are not supported and may lead to unexpected behavior.

### Bybit Futures

Futures trading on bybit is supported for isolated futures mode.

On startup, freqtrade will set the position mode to "One-way Mode" for the whole (sub)account. This avoids making this call over and over again (slowing down bot operations), but means that manual changes to this setting may result in exceptions and errors.

As bybit doesn't provide funding rate history, the dry-run calculation is used for live trades as well.

API Keys for live futures trading must have the following permissions:

* Read-write
* Contract - Orders
* Contract - Positions

We do strongly recommend to limit all API keys to the IP you're going to use it from.


## Bitmart

Bitmart requires the API key Memo (the name you give the API key) to go along with the exchange key and secret.
It's therefore required to pass the UID as well.

```json
"exchange": {
    "name": "bitmart",
    "uid": "your_bitmart_api_key_memo",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```

!!! Warning "Necessary Verification"
    Bitmart requires Verification Lvl2 to successfully trade on the spot market through the API - even though trading via UI works just fine with just Lvl1 verification.

## Bitget

Bitget requires a passphrase for each api key, you will therefore need to add this key into the configuration so your exchange section looks as follows:

```json
"exchange": {
    "name": "bitget",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```

Bitget supports [time_in_force](configuration.md#understand-order_time_in_force) with settings "GTC" (good till cancelled), "FOK" (full-or-cancel), "IOC" (immediate-or-cancel) and "PO" (Post only) settings.

!!! Tip "Stoploss on Exchange"
    Bitget supports `stoploss_on_exchange` and can use both stop-loss-market and stop-loss-limit orders. It provides great advantages, so we recommend to benefit from it.
    You can use either `"limit"` or `"market"` in the `order_types.stoploss` configuration setting to decide which type of stoploss shall be used.

### Bitget Futures

Futures trading on bitget is supported for isolated futures mode.

On startup, freqtrade will set the position mode to "One-way Mode" for the whole (sub)account. This avoids making this call over and over again (slowing down bot operations), but means that manual changes to this setting may result in exceptions and errors.

## Hyperliquid

!!! Tip "Stoploss on Exchange"
    Hyperliquid supports `stoploss_on_exchange` and uses `stop-loss-limit` orders. It provides great advantages, so we recommend to benefit from it.

Hyperliquid is a Decentralized Exchange (DEX). Decentralized exchanges work a bit different compared to normal exchanges. Instead of authenticating private API calls using an API key, private API calls need to be signed with the private key of your wallet (We recommend using an api Wallet for this, generated either on Hyperliquid or in your wallet of choice).
This needs to be configured like this:

```json
"exchange": {
    "name": "hyperliquid",
    "walletAddress": "your_eth_wallet_address",  // This should NOT be your API Wallet Address!
    "privateKey": "your_api_private_key",
    // ...
}
```

* walletAddress in hex format: `0x<40 hex characters>` - Can be easily copied from your wallet - and should be your main wallet address, not your API Wallet Address.
* privateKey in hex format: `0x<64 hex characters>` - Use the key the API Wallet shows on creation.

Hyperliquid handles deposits and withdrawals on the Arbitrum One chain, a Layer 2 scaling solution built on top of Ethereum. Hyperliquid uses USDC as quote / collateral. The process of depositing USDC on Hyperliquid requires a couple of steps, see [how to start trading](https://hyperliquid.gitbook.io/hyperliquid-docs/onboarding/how-to-start-trading) for details on what steps are needed.

!!! Note "Hyperliquid general usage Notes"
    Hyperliquid does not support market orders, however ccxt will simulate market orders by placing limit orders with a maximum slippage of 5%.  
    Unfortunately, hyperliquid only offers 5000 historic candles, so backtesting will either need to build candles historically (by waiting and downloading the data incrementally over time) - or will be limited to the last 5000 candles.

!!! Info "Some general best practices (non exhaustive)"
    * Beware of supply chain attacks, like pip package poisoning etcetera. Whenever you use your private key, make sure your environment is safe.
    * Don't use your actual wallet private key for trading. Use the Hyperliquid [API generator](https://app.hyperliquid.xyz/API) to create a separate API wallet.
    * Don't store your actual wallet private key on the server you use for freqtrade. Use the API wallet private key instead. This key won't allow withdrawals, only trading.
    * Always keep your mnemonic phrase and private key private.
    * Don't use the same mnemonic as the one you had to backup when initializing a hardware wallet, using the same mnemonic basically deletes the security of your hardware wallet.
    * Create a different software wallet, only transfer the funds you want to trade with to that wallet, and use that wallet to trade on Hyperliquid.
    * If you have funds you don't want to use for trading (after making a profit for example), transfer them back to your hardware wallet.

### Hyperliquid Vault / Subaccount

Hyperliquid allows you to create either a vault or a subaccount.  
To use these with Freqtrade, you will need to use the following configuration pattern:

``` json
"exchange": {
    "name": "hyperliquid",
    "walletAddress": "your_vault_address",  // Vault or subaccount address
    "privateKey": "your_api_private_key",
    "ccxt_config": {
        "options": {
            "vaultAddress": "your_vault_address" // Optional, only if you want to use a vault or subaccount
        }
    },
    // ...
}
```

Your balance and trades will now be used from your vault / subaccount - and no longer from your main account.

### Historic Hyperliquid data

The Hyperliquid API does not provide historic data beyond the single call to fetch current data, so downloading data is not possible, as the downloaded data would not constitute proper historic data.

## Bitvavo

If your account is required to use an operatorId, you can set it in the configuration file as follows:

``` json
"exchange": {
        "name": "bitvavo",
        "key": "",
        "secret": "",
        "ccxt_config": {
            "options": {
                "operatorId": "123567"
            }
        },
   }
```

Bitvavo expects the `operatorId` to be an integer.

## All exchanges

Should you experience constant errors with Nonce (like `InvalidNonce`), it is best to regenerate the API keys. Resetting Nonce is difficult and it's usually easier to regenerate the API keys.

## Random notes for other exchanges

* The Ocean (exchange id: `theocean`) exchange uses Web3 functionality and requires `web3` python package to be installed:

```shell
pip3 install web3
```

### Getting latest price / Incomplete candles

Most exchanges return current incomplete candle via their OHLCV/klines API interface.
By default, Freqtrade assumes that incomplete candle is fetched from the exchange and removes the last candle assuming it's the incomplete candle.

Whether your exchange returns incomplete candles or not can be checked using [the helper script](developer.md#incomplete-candles) from the Contributor documentation.

Due to the danger of repainting, Freqtrade does not allow you to use this incomplete candle.

However, if it is based on the need for the latest price for your strategy - then this requirement can be acquired using the [data provider](strategy-customization.md#possible-options-for-dataprovider) from within the strategy.

### Advanced Freqtrade Exchange configuration

Advanced options can be configured using the `_ft_has_params` setting, which will override Defaults and exchange-specific behavior.

Available options are listed in the exchange-class as `_ft_has_default`.

For example, to test the order type `FOK` with Kraken, and modify candle limit to 200 (so you only get 200 candles per API call):

```json
"exchange": {
    "name": "kraken",
    "_ft_has_params": {
        "order_time_in_force": ["GTC", "FOK"],
        "ohlcv_candle_limit": 200
        }
    //...
}
```

!!! Warning
    Please make sure to fully understand the impacts of these settings before modifying them.
    Using `_ft_has_params` overrides may lead to unexpected behavior, and may even break your bot. 
    We will not be able to provide support for issues caused by custom settings in `_ft_has_params`.
