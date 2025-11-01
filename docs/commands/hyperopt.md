```
用法: freqtrade hyperopt [-h] [-v] [--no-color] [--logfile FILE] [-V]
                          [-c PATH] [-d PATH] [--userdir PATH] [-s NAME]
                          [--strategy-path PATH] [--recursive-strategy-search]
                          [--freqaimodel NAME] [--freqaimodel-path PATH]
                          [-i TIMEFRAME] [--timerange TIMERANGE]
                          [--data-format-ohlcv {json,jsongz,feather,parquet}]
                          [--max-open-trades INT]
                          [--stake-amount STAKE_AMOUNT] [--fee FLOAT]
                          [-p PAIRS [PAIRS ...]] [--hyperopt-path PATH]
                          [--eps] [--enable-protections]
                          [--dry-run-wallet DRY_RUN_WALLET]
                          [--timeframe-detail TIMEFRAME_DETAIL] [-e INT]
                          [--spaces {all,buy,sell,roi,stoploss,trailing,protection,trades,default} [{all,buy,sell,roi,stoploss,trailing,protection,trades,default} ...]]
                          [--print-all] [--print-json] [-j JOBS]
                          [--random-state INT] [--min-trades INT]
                          [--hyperopt-loss NAME] [--disable-param-export]
                          [--ignore-missing-spaces] [--analyze-per-epoch]
                          [--early-stop INT]

选项:
  -h, --help            显示此帮助消息并退出
  -i TIMEFRAME, --timeframe TIMEFRAME
                        指定时间框架（`1m`、`5m`、`30m`、`1h`、`1d`）。
  --timerange TIMERANGE
                        指定要使用的数据时间范围。
  --data-format-ohlcv {json,jsongz,feather,parquet}
                        下载的蜡烛图（OHLCV）数据的存储格式。
                        （默认：`feather`）。
  --max-open-trades INT
                        覆盖 `max_open_trades`
                        配置设置的值。
  --stake-amount STAKE_AMOUNT
                        覆盖 `stake_amount` 配置
                        设置的值。
  --fee FLOAT           指定手续费比率。将应用两次（在交易
                        入场和出场时）。
  -p PAIRS [PAIRS ...], --pairs PAIRS [PAIRS ...]
                        将此命令限制为这些交易对。交易对用空格分隔。
  --hyperopt-path PATH  为超参数优化损失
                        函数指定其他查找路径。
  --eps, --enable-position-stacking
                        允许多次买入同一交易对（头寸
                        堆叠）。
  --enable-protections, --enableprotections
                        为回测启用保护。会大大减慢
                        回测速度，但会
                        包含配置的保护
  --dry-run-wallet DRY_RUN_WALLET, --starting-balance DRY_RUN_WALLET
                        起始余额，用于回测 / 超参数优化和
                        模拟运行。
  --timeframe-detail TIMEFRAME_DETAIL
                        指定回测的详细时间框架（`1m`、`5m`、
                        `30m`、`1h`、`1d`）。
  -e INT, --epochs INT  指定 epoch 数量（默认：100）。
  --spaces {all,buy,sell,roi,stoploss,trailing,protection,trades,default} [{all,buy,sell,roi,stoploss,trailing,protection,trades,default} ...]
                        指定要超参数优化的参数。空格分隔的
                        列表。
  --print-all           打印所有结果，而不仅仅是最佳结果。
  --print-json          以 JSON 格式打印输出。
  -j JOBS, --job-workers JOBS
                        用于超参数优化的并发运行作业数量
                        （超参数优化工作进程）。如果是 -1
                        （默认），使用所有 CPU，如果是 -2，使用除一个之外的所有 CPU，等等。
                        如果给定 1，则不使用任何并行计算代码。
  --random-state INT    将随机状态设置为某个正整数以
                        获得可重复的超参数优化结果。
  --min-trades INT      为评估设置最小期望交易数量
                        在超参数优化路径中（默认：1）。
  --hyperopt-loss NAME, --hyperoptloss NAME
                        指定超参数优化损失函数的类名
                        （IHyperOptLoss）。不同的函数可以
                        产生完全不同的结果，因为
                        优化的目标不同。内置的
                        超参数优化损失函数有：
                        ShortTradeDurHyperOptLoss、OnlyProfitHyperOptLoss、
                        SharpeHyperOptLoss、SharpeHyperOptLossDaily、
                        SortinoHyperOptLoss、SortinoHyperOptLossDaily、
                        CalmarHyperOptLoss、MaxDrawDownHyperOptLoss、
                        MaxDrawDownRelativeHyperOptLoss、
                        MaxDrawDownPerPairHyperOptLoss、
                        ProfitDrawDownHyperOptLoss、MultiMetricHyperOptLoss
  --disable-param-export
                        禁用自动超参数优化参数导出。
  --ignore-missing-spaces, --ignore-unparameterized-spaces
                        抑制任何请求的超参数优化空间的错误，这些空间
                        不包含任何参数。
  --analyze-per-epoch   每个 epoch 运行一次 populate_indicators。
  --early-stop INT      如果在（默认：
                        0）个 epoch 后没有改进，则提前停止超参数优化。

通用参数:
  -v, --verbose         详细模式（-vv 获取更多信息，-vvv 获取所有消息）。
  --no-color            禁用超参数优化结果的着色。如果您将
                        输出重定向到文件，这可能很有用。
  --logfile FILE, --log-file FILE
                        记录到指定的文件。特殊值为：
                        'syslog'、'journald'。有关更多详细信息，请参阅文档。
  -V, --version         显示程序版本号并退出
  -c PATH, --config PATH
                        指定配置文件（默认：
                        `userdir/config.json` 或 `config.json`，以存在者为准）。
                        可以使用多个 --config 选项。可以
                        设置为 `-` 以从 stdin 读取配置。
  -d PATH, --datadir PATH, --data-dir PATH
                        包含历史回测数据的交易所基础目录路径。
                        要查看期货数据，请另外使用交易模式。
  --userdir PATH, --user-data-dir PATH
                        用户数据目录路径。

策略参数:
  -s NAME, --strategy NAME
                        指定机器人将使用的策略类名称。
  --strategy-path PATH  指定其他策略查找路径。
  --recursive-strategy-search
                        在策略文件夹中递归搜索策略。
  --freqaimodel NAME    指定自定义 freqaimodels。
  --freqaimodel-path PATH
                        为 freqaimodels 指定其他查找路径。

```
