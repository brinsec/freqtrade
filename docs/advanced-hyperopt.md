# 高级超参数优化

本页解释一些高级超参数优化主题，可能需要比创建普通超参数优化类更高的
编码技能和 Python 知识。

## 创建和使用自定义损失函数

要使用自定义损失函数类，请确保在您的自定义超参数优化损失类中定义了函数 `hyperopt_loss_function`。
对于下面的示例，您需要在超参数优化调用中添加命令行参数 `--hyperopt-loss SuperDuperHyperOptLoss`，以便使用此函数。

下面可以找到一个示例，它与默认的超参数优化损失实现相同。完整的示例可以在 [userdata/hyperopts](https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/templates/sample_hyperopt_loss.py) 找到。

``` python
from datetime import datetime
from typing import Any, Dict

from pandas import DataFrame

from freqtrade.constants import Config
from freqtrade.optimize.hyperopt import IHyperOptLoss

TARGET_TRADES = 600
EXPECTED_MAX_PROFIT = 3.0
MAX_ACCEPTED_TRADE_DURATION = 300

class SuperDuperHyperOptLoss(IHyperOptLoss):
    """
    Defines the default loss function for hyperopt
    """

    @staticmethod
    def hyperopt_loss_function(
        *,
        results: DataFrame,
        trade_count: int,
        min_date: datetime,
        max_date: datetime,
        config: Config,
        processed: dict[str, DataFrame],
        backtest_stats: dict[str, Any],
        starting_balance: float,
        **kwargs,
    ) -> float:
        """
        目标函数，返回较小的数字表示更好的结果
        这是传统算法（在 freqtrade 中一直使用到现在）。
        权重分布如下：
        * 0.4 分配给交易持续时间
        * 0.25：避免交易亏损
        * 1.0 分配给总利润，与上面定义的预期值（`EXPECTED_MAX_PROFIT`）相比
        """
        total_profit = results['profit_ratio'].sum()
        trade_duration = results['trade_duration'].mean()

        trade_loss = 1 - 0.25 * exp(-(trade_count - TARGET_TRADES) ** 2 / 10 ** 5.8)
        profit_loss = max(0, 1 - total_profit / EXPECTED_MAX_PROFIT)
        duration_loss = 0.4 * min(trade_duration / MAX_ACCEPTED_TRADE_DURATION, 1)
        result = trade_loss + profit_loss + duration_loss
        return result
```

当前，参数包括：

* `results`：包含结果交易的 DataFrame。
    结果中提供以下列（对应于使用 `--export trades` 时回测的输出文件）：  
    `pair, profit_ratio, profit_abs, open_date, open_rate, fee_open, close_date, close_rate, fee_close, amount, trade_duration, is_open, exit_reason, stake_amount, min_rate, max_rate, stop_loss_ratio, stop_loss_abs`
* `trade_count`：交易数量（与 `len(results)` 相同）
* `min_date`：使用的时间范围的开始日期
* `max_date`：使用的时间范围的结束日期
* `config`：使用的配置对象（注意：如果它们属于超参数优化空间，则并非所有策略相关参数都会在此处更新）。
* `processed`：以交易对为键的 DataFrame 字典，包含用于回测的数据。
* `backtest_stats`：使用与回测文件"strategy"子结构相同格式的回测统计。可用字段可以在 `optimize_reports.py` 中的 `generate_strategy_stats()` 中查看。
* `starting_balance`：用于回测的起始余额。

此函数需要返回浮点数（`float`）。较小的数字将被解释为更好的结果。此参数和平衡由您决定。

!!! Note "注意"
    此函数每个 epoch 调用一次 - 因此请确保尽可能优化它，以免不必要地减慢超参数优化速度。

!!! Note "`*args` 和 `**kwargs`"
    请在接口中保留参数 `*args` 和 `**kwargs`，以允许我们在将来扩展此接口。

## 覆盖预定义空间

要覆盖预定义空间（`roi_space`、`generate_roi_table`、`stoploss_space`、`trailing_space`、`max_open_trades_space`），请定义一个名为 Hyperopt 的嵌套类，并按如下方式定义所需的空间：

```python
from freqtrade.optimize.space import Categorical, Dimension, Integer, SKDecimal

class MyAwesomeStrategy(IStrategy):
    class HyperOpt:
        # Define a custom stoploss space.
        def stoploss_space():
            return [SKDecimal(-0.05, -0.01, decimals=3, name='stoploss')]

        # Define custom ROI space
        def roi_space() -> List[Dimension]:
            return [
                Integer(10, 120, name='roi_t1'),
                Integer(10, 60, name='roi_t2'),
                Integer(10, 40, name='roi_t3'),
                SKDecimal(0.01, 0.04, decimals=3, name='roi_p1'),
                SKDecimal(0.01, 0.07, decimals=3, name='roi_p2'),
                SKDecimal(0.01, 0.20, decimals=3, name='roi_p3'),
            ]

        def generate_roi_table(params: Dict) -> dict[int, float]:

            roi_table = {}
            roi_table[0] = params['roi_p1'] + params['roi_p2'] + params['roi_p3']
            roi_table[params['roi_t3']] = params['roi_p1'] + params['roi_p2']
            roi_table[params['roi_t3'] + params['roi_t2']] = params['roi_p1']
            roi_table[params['roi_t3'] + params['roi_t2'] + params['roi_t1']] = 0

            return roi_table

        def trailing_space() -> List[Dimension]:
            # 这里的所有参数都是强制性的，您只能修改它们的类型或范围。
            return [
                # 固定为 true，如果优化 trailing_stop，我们假设始终使用追踪止损。
                Categorical([True], name='trailing_stop'),

                SKDecimal(0.01, 0.35, decimals=3, name='trailing_stop_positive'),
                # 'trailing_stop_positive_offset' 应该大于 'trailing_stop_positive'，
                # 因此这个中间参数用作它们之间差值的值。
                # 'trailing_stop_positive_offset' 的值在 generate_trailing_params() 方法中构建。
                # 这类似于用于构建 ROI 表的超空间维度。
                SKDecimal(0.001, 0.1, decimals=3, name='trailing_stop_positive_offset_p1'),

                Categorical([True, False], name='trailing_only_offset_is_reached'),
        ]

        # 定义自定义 max_open_trades 空间
        def max_open_trades_space(self) -> List[Dimension]:
            return [
                Integer(-1, 10, name='max_open_trades'),
            ]
```

!!! Note "注意"
    所有覆盖都是可选的，可以根据需要进行混合/匹配。

### 动态参数

参数也可以动态定义，但必须在调用 [`bot_start()` 回调](strategy-callbacks.md#bot-start) 后对实例可用。

``` python

class MyAwesomeStrategy(IStrategy):

    def bot_start(self, **kwargs) -> None:
        self.buy_adx = IntParameter(20, 30, default=30, optimize=True)

    # ...
```

!!! Warning "警告"
    以这种方式创建的参数不会显示在 `list-strategies` 参数计数中。

### 覆盖基础估计器

您可以通过在 Hyperopt 子类中实现 `generate_estimator()` 来为 Hyperopt 定义自己的 optuna 采样器。

```python
class MyAwesomeStrategy(IStrategy):
    class HyperOpt:
        def generate_estimator(dimensions: List['Dimension'], **kwargs):
            return "NSGAIIISampler"

```

可能的值是 "NSGAIISampler"、"TPESampler"、"GPSampler"、"CmaEsSampler"、"NSGAIIISampler"、"QMCSampler" 之一（详细信息可以在 [optuna-samplers 文档](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html) 中找到），或者"继承自 `optuna.samplers.BaseSampler` 的类的实例"。

需要一些研究来查找额外的采样器（例如来自 optunahub）。

!!! Note "注意"
    虽然可以提供自定义估计器，但由您作为用户来研究可能的参数并分析/理解应该使用哪些参数。
    如果您不确定这一点，最好使用默认值之一（`"NSGAIIISampler"` 已被证明是最通用的），无需进一步参数。

??? Example "Using `AutoSampler` from Optunahub"

    [AutoSampler docs](https://hub.optuna.org/samplers/auto_sampler/)
    
    Install the necessary dependencies 
    ``` bash
    pip install optunahub cmaes torch scipy
    ```
    Implement `generate_estimator()`  in your strategy

    ``` python
    # ...
    from freqtrade.strategy.interface import IStrategy
    from typing import List
    import optunahub
    # ... 

    class my_strategy(IStrategy):
        class HyperOpt:
            def generate_estimator(dimensions: List["Dimension"], **kwargs):
                if "random_state" in kwargs.keys():
                    return optunahub.load_module("samplers/auto_sampler").AutoSampler(seed=kwargs["random_state"])
                else:
                    return optunahub.load_module("samplers/auto_sampler").AutoSampler()

    ```

    Obviously the same approach will work for all other Samplers optuna supports.


## 空间选项

对于附加空间，scikit-optimize（结合 Freqtrade）提供以下空间类型：

* `Categorical` - 从类别列表中选择（例如 `Categorical(['a', 'b', 'c'], name="cat")`）
* `Integer` - 从整数范围中选择（例如 `Integer(1, 10, name='rsi')`）
* `SKDecimal` - 从有限精度的十进制数范围中选择（例如 `SKDecimal(0.1, 0.5, decimals=3, name='adx')`）。*仅适用于 freqtrade*。
* `Real` - 从完整精度的十进制数范围中选择（例如 `Real(0.1, 0.5, name='adx')`）

您可以从 `freqtrade.optimize.space` 导入所有这些，尽管 `Categorical`、`Integer` 和 `Real` 只是其相应 scikit-optimize Spaces 的别名。`SKDecimal` 由 freqtrade 提供，用于更快的优化。

``` python
from freqtrade.optimize.space import Categorical, Dimension, Integer, SKDecimal, Real  # noqa
```

!!! Hint "SKDecimal vs. Real"
    我们建议在几乎所有情况下使用 `SKDecimal` 而不是 `Real` 空间。虽然 Real 空间提供完整精度（最多约 16 位小数）- 但这种精度很少需要，并且会导致不必要的长超参数优化时间。

    假设定义了一个相当小的空间（`SKDecimal(0.10, 0.15, decimals=2, name='xxx')`）- SKDecimal 将有 5 种可能性（`[0.10, 0.11, 0.12, 0.13, 0.14, 0.15]`）。

    另一方面，相应的 real 空间 `Real(0.10, 0.15 name='xxx')` 具有几乎无限数量的可能性（`[0.10, 0.010000000001, 0.010000000002, ... 0.014999999999, 0.01500000000]`）。
