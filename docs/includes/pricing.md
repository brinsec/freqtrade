## 用于订单的价格

常规订单的价格可以通过参数结构 `entry_pricing`（用于交易入场）和 `exit_pricing`（用于交易出场）来控制。
价格总是在下订单之前立即检索，通过查询交易所行情或使用订单簿数据。

!!! Note "注意"
    Freqtrade 使用的订单簿数据是通过 ccxt 的 `fetch_order_book()` 函数从交易所检索的数据，即通常来自 L2 聚合订单簿的数据，而行情数据是由 ccxt 的 `fetch_ticker()`/`fetch_tickers()` 函数返回的结构。有关更多详细信息，请参阅 ccxt 库[文档](https://github.com/ccxt/ccxt/wiki/Manual#market-data)。

!!! Warning "使用市价单"
    使用市价单时，请阅读[市价单定价](#market-order-pricing)部分。

### 入场价格

#### 入场价格侧

配置设置 `entry_pricing.price_side` 定义机器人在买入时查看的订单簿侧。

以下显示订单簿：

``` explanation
...
103
102
101  # ask
-------------Current spread
99   # bid
98
97
...
```

如果 `entry_pricing.price_side` 设置为 `"bid"`，则机器人将使用 99 作为入场价格。  
与此一致，如果 `entry_pricing.price_side` 设置为 `"ask"`，则机器人将使用 101 作为入场价格。

根据订单方向（_long_/_short_），这将导致不同的结果。因此，我们建议为此配置改用 `"same"` 或 `"other"`。
这将导致以下定价矩阵：

| 方向 | 订单 | 设置 | 价格 | 跨越价差 |
|------ |--------|-----|-----|-----|
| long  | buy  | ask   | 101 | 是 |
| long  | buy  | bid   | 99  | 否  |
| long  | buy  | same  | 99  | 否  |
| long  | buy  | other | 101 | 是 |
| short | sell | ask   | 101 | 否  |
| short | sell | bid   | 99  | 是 |
| short | sell | same  | 101 | 否  |
| short | sell | other | 99  | 是 |

使用订单簿的另一侧通常保证更快的订单成交，但机器人最终也可能支付比必要金额更多的费用。
即使使用限价买入订单，也可能适用接受者费用而不是制造者费用。
此外，价差"另一侧"的价格高于订单簿中"买价"侧的价格，因此订单行为类似于市价单（但有最大价格）。

#### 启用订单簿时的入场价格

使用启用的订单簿进入交易时（`entry_pricing.use_order_book=True`），Freqtrade 从订单簿获取 `entry_pricing.order_book_top` 条目，并使用指定为 `entry_pricing.order_book_top` 的条目，从配置的侧（`entry_pricing.price_side`）的订单簿。1 指定订单簿中的最顶层条目，而 2 将使用订单簿中的第 2 个条目，依此类推。

#### 未启用订单簿时的入场价格

以下部分使用 `side` 作为配置的 `entry_pricing.price_side`（默认为 `"same"`）。

不使用订单簿时（`entry_pricing.use_order_book=False`），如果行情中的最佳 `side` 价格低于行情中的 `last` 交易价格，Freqtrade 使用该价格。否则（当 `side` 价格高于 `last` 价格时），它根据 `entry_pricing.price_last_balance` 计算 `side` 和 `last` 价格之间的比率。

`entry_pricing.price_last_balance` 配置参数控制此行为。值为 `0.0` 将使用 `side` 价格，而 `1.0` 将使用 `last` 价格，介于两者之间的值在卖价和最后价格之间插值。

#### 检查市场深度

启用检查市场深度时（`entry_pricing.check_depth_of_market.enabled=True`），入场信号根据每个订单簿侧的市场深度（所有金额的总和）进行过滤。

然后订单簿 `bid`（买入）侧深度除以订单簿 `ask`（卖出）侧深度，将得到的增量与 `entry_pricing.check_depth_of_market.bids_to_ask_delta` 参数的值进行比较。仅当订单簿增量大于或等于配置的增量值时，才执行入场订单。

!!! Note "注意"
    小于 1 的增量值意味着 `ask`（卖出）订单簿侧深度大于 `bid`（买入）订单簿侧的深度，而大于 1 的值意味着相反（买入侧的深度高于卖出侧的深度）。

### 出场价格

#### 出场价格侧

配置设置 `exit_pricing.price_side` 定义机器人在退出交易时查看的价差侧。

以下显示订单簿：

``` explanation
...
103
102
101  # ask
-------------当前价差
99   # bid
98
97
...
```

如果 `exit_pricing.price_side` 设置为 `"ask"`，则机器人将使用 101 作为出场价格。  
与此一致，如果 `exit_pricing.price_side` 设置为 `"bid"`，则机器人将使用 99 作为出场价格。

根据订单方向（_long_/_short_），这将导致不同的结果。因此，我们建议为此配置改用 `"same"` 或 `"other"`。
这将导致以下定价矩阵：

| 方向 | 订单 | 设置 | 价格 | 跨越价差 |
|------ |--------|-----|-----|-----|
| long  | sell | ask   | 101 | 否  |
| long  | sell | bid   | 99  | 是 |
| long  | sell | same  | 101 | 否  |
| long  | sell | other | 99  | 是 |
| short | buy  | ask   | 101 | 是 |
| short | buy  | bid   | 99  | 否  |
| short | buy  | same  | 99  | 否  |
| short | buy  | other | 101 | 是 |

#### 启用订单簿时的出场价格

使用启用的订单簿退出时（`exit_pricing.use_order_book=True`），Freqtrade 从订单簿获取 `exit_pricing.order_book_top` 条目，并使用从配置的侧（`exit_pricing.price_side`）指定为 `exit_pricing.order_book_top` 的条目作为交易出场价格。

1 指定订单簿中的最顶层条目，而 2 将使用订单簿中的第 2 个条目，依此类推。

#### 未启用订单簿时的出场价格

以下部分使用 `side` 作为配置的 `exit_pricing.price_side`（默认为 `"ask"`）。

不使用订单簿时（`exit_pricing.use_order_book=False`），如果行情中的最佳 `side` 价格高于行情中的 `last` 交易价格，Freqtrade 使用该价格。否则（当 `side` 价格低于 `last` 价格时），它根据 `exit_pricing.price_last_balance` 计算 `side` 和 `last` 价格之间的比率。

`exit_pricing.price_last_balance` 配置参数控制此行为。值为 `0.0` 将使用 `side` 价格，而 `1.0` 将使用最后价格，介于两者之间的值在 `side` 和最后价格之间插值。

### 市价单定价

使用市价单时，应配置价格以使用订单簿的"正确"侧，以允许真实的定价检测。
假设入场和出场都使用市价单，必须使用类似以下的配置

``` jsonc
  "order_types": {
    "entry": "market",
    "exit": "market"
    // ...
  },
  "entry_pricing": {
    "price_side": "other",
    // ...
  },
  "exit_pricing":{
    "price_side": "other",
    // ...
  },
```

显然，如果只有一侧使用限价单，可以使用不同的定价组合。
