# 杠杆交易

!!! Warning "Beta 功能"
    此功能仍处于测试阶段。如果您注意到您认为有问题的地方，请通过 Discord 或 Github Issue 告诉我们。

!!! Note "一个账户上的多个机器人"
    您不能在具有杠杆的同一账户上运行 2 个机器人。对于杠杆/保证金交易，freqtrade 假设它是账户的唯一用户，所有清算水平都是基于此假设计算的。

!!! Danger "杠杆交易风险很大"
    不要使用杠杆 > 1 进行交易，如果策略在使用现货市场的实盘运行中没有显示积极结果。检查您的策略的止损。杠杆为 2 时，止损为 0.5（50%）会太低，这些交易将在达到该止损之前被清算。
    我们不对使用此软件或此模式发生的任何损失承担责任。

    请仅在您知道 freqtrade（和您的策略）如何工作时才使用高级交易模式。
    此外，永远不要冒险超过您能承受的损失。

如果您已有现有策略，请阅读[策略迁移指南](strategy_migration.md#strategy-migration-between-v2-and-v3)，将您的策略从 freqtrade v2 策略迁移到可以做空和交易期货的版本 3 策略。

## 做空

当 [`trading_mode`](#leverage-trading-modes) 设置为 `spot` 时，无法做空。要进行做空交易，`trading_mode` 必须设置为 `margin`（当前不可用）或 [`futures`](#futures)，并且 [`margin_mode`](#margin-mode) 设置为 [`cross`](#cross-margin-mode) 或 [`isolated`](#isolated-margin-mode）

策略要做空，策略类必须设置类变量 `can_short = True`

请阅读[策略自定义](strategy-customization.md#entry-signal-rules)了解如何设置做空交易的入场和出场信号。

## 了解 `trading_mode`

可能的值是：`spot`（默认）、`margin`（*当前不可用*）或 `futures`。

### Spot（现货）

常规交易模式（低风险）

- 仅多头交易（无空头交易）。
- 无杠杆。
- 无清算。
- 获得的/损失的利润等于资产价值的变化（减去交易手续费）。

### 杠杆交易模式

使用杠杆，交易者从交易所借入资金。资金必须完全偿还给交易所（可能有利息），交易者保留使用借入资金进行的任何交易的任何利润，或支付任何损失。

因为资金必须始终偿还，交易所将在杠杆账户中的资产总价值下降到某一点（损失总价值小于交易者在杠杆账户中实际拥有的抵押品价值的点）时**清算**（强制卖出交易者的资产）使用借入资金进行的交易，以确保交易者有足够的资金将借入的资产偿还给交易所。交易所还将收取**清算费**，增加交易者的损失。

因此，**如果您不知道自己在做什么，请不要使用杠杆进行交易。杠杆交易风险很高，可能导致您的资产价值迅速降至 0，并且没有再次增加价值的机会。**

#### Margin（保证金）（当前不可用）

交易在现货市场进行，但交易所向您借出等于所选杠杆的资金。您将借入的金额连同利息一起偿还给交易所，您的利润/损失按指定的杠杆倍数。

#### Futures（期货）

永续掉期（也称为永续期货）是以与其基础资产密切相关的价格交易的合约（例如）。您不是在交易实际资产，而是在交易衍生品合约。永续掉期合约可以无限期持续，与期货或期权合约不同。

除了期货合约价格变化带来的收益/损失外，交易者还交换_资金费率_，这是从期货合约与其基础资产之间的价格差异得出的收益/损失。期货合约与基础资产之间的价格差异因交易所而异。

要在期货市场交易，您必须将 `trading_mode` 设置为 "futures"。
您还必须选择"保证金模式"（下面的解释）- freqtrade 目前仅支持独立保证金。

``` json
"trading_mode": "futures",
"margin_mode": "isolated"
```

##### 交易对命名

Freqtrade 遵循 [ccxt 期货命名约定](https://docs.ccxt.com/#/README?id=perpetual-swap-perpetual-future)。
因此，期货交易对将具有 `base/quote:settle` 的命名（例如 `ETH/USDT:USDT`）。

### 保证金模式

除了 `trading_mode` - 您还必须配置您的 `margin_mode`。
虽然 freqtrade 目前仅支持一种保证金模式，但这会改变，通过现在配置它，您已为未来的更新做好准备。

可能的值是：`isolated` 或 `cross`。

#### 独立保证金模式

每个市场（交易对）在单独的账户中保留抵押品

``` json
"margin_mode": "isolated"
```

#### 全仓保证金模式

一个账户用于在市场（交易对）之间共享抵押品。在需要时从总账户余额中提取保证金以避免清算。

``` json
"margin_mode": "cross"
```

请阅读[交易所特定说明](exchanges.md)了解支持此模式的交易所及其差异。

!!! Warning "增加清算风险"
    全仓保证金模式增加了完全账户清算的风险，因为所有交易共享相同的抵押品。
    一个交易的损失可能影响其他交易的清算价格。
    此外，全仓头寸影响可能在模拟运行或回测模式中无法完全模拟。

## 设置要使用的杠杆

不同的策略和风险状况将需要不同水平的杠杆。
虽然您可以配置一个静态杠杆值 - freqtrade 为您提供了通过[策略杠杆回调](strategy-callbacks.md#leverage-callback)调整此值的灵活性 - 这允许您按交易对使用不同的杠杆，或基于其他有利于您策略结果的因素。

如果未实现，杠杆默认为 1 倍（无杠杆）。

!!! Warning "警告"
    更高的杠杆也等于更高的风险 - 请确保您完全理解使用杠杆的影响！

## 了解 `liquidation_buffer`

*默认为 `0.05`*

指定在清算价格和止损之间放置多大的安全网以防止头寸达到清算价格的比率。
这个人工清算价格计算为：

`freqtrade_liquidation_price = liquidation_price ± (abs(open_rate - liquidation_price) * liquidation_buffer)`

- `±` = `+` 对于多头交易
- `±` = `-` 对于空头交易

可能的值是 0.0 和 0.99 之间的任何浮点数

**示例：** 如果交易以 10 coin/USDT 的价格入场，并且此交易的清算价格是 8 coin/USDT，那么将 `liquidation_buffer` 设置为 `0.05`，此交易的最小止损将是 $8 + ((10 - 8) * 0.05) = 8 + 0.1 = 8.1$

!!! Danger "`liquidation_buffer` 为 0.0 或较低的 `liquidation_buffer` 可能导致清算和清算费用"
    目前 Freqtrade 能够计算清算价格，但不计算清算费用。将 `liquidation_buffer` 设置为 0.0，或使用较低的 `liquidation_buffer` 可能导致您的头寸被清算。Freqtrade 不跟踪清算费用，因此清算将导致机器人不准确的盈亏结果。如果您使用较低的 `liquidation_buffer`，建议使用 `stoploss_on_exchange`（如果您的交易所支持此功能）。

## 不可用的资金费率

对于期货数据，交易所通常提供期货蜡烛图、标记和资金费率。然而，虽然蜡烛图和标记可能可用，但资金费率通常不可用。这可能会影响回测时间范围，即您可能只能测试最近的时间范围而不能测试更早的时间范围，遇到 `No data found. Terminating.` 错误。要解决此问题，请添加 [configuration.md](configuration.md) 中列出的 `futures_funding_rate` 配置选项，建议您将其设置为 `0`，除非您知道您的交易对、交易所和时间范围的给定特定资金费率。将此设置为除 `0` 之外的任何值都可能对策略中的利润计算产生重大影响，例如在 `custom_exit`、`custom_stoploss` 等函数中。

!!! Warning "这意味着您的回测不准确。"
    这不会覆盖交易所提供的可用资金费率，但请记住，设置错误的资金费率将意味着对于资金费率不可用的历史时间范围，回测结果将不准确。

### Developer

#### Margin mode

For shorts, the currency which pays the interest fee for the `borrowed` currency is purchased at the same time of the closing trade (This means that the amount purchased in short closing trades is greater than the amount sold in short opening trades).

For longs, the currency which pays the interest fee for the `borrowed` will already be owned by the user and does not need to be purchased. The interest is subtracted from the `close_value` of the trade.

All Fees are included in `current_profit` calculations during the trade.

#### Futures mode

Funding fees are either added or subtracted from the total amount of a trade
