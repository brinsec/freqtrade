```
用法: freqtrade lookahead-analysis [-h] [-v] [--no-color] [--logfile FILE]
                                    [-V] [-c PATH] [-d PATH] [--userdir PATH]
                                    [-s NAME] [--strategy-path PATH]
                                    [--recursive-strategy-search]
                                    [--freqaimodel NAME]
                                    [--freqaimodel-path PATH] [-i TIMEFRAME]
                                    [--timerange TIMERANGE]
                                    [--data-format-ohlcv {json,jsongz,feather,parquet}]
                                    [--max-open-trades INT]
                                    [--stake-amount STAKE_AMOUNT]
                                    [--fee FLOAT] [-p PAIRS [PAIRS ...]]
                                    [--enable-protections]
                                    [--enable-dynamic-pairlist]
                                    [--dry-run-wallet DRY_RUN_WALLET]
                                    [--timeframe-detail TIMEFRAME_DETAIL]
                                    [--strategy-list STRATEGY_LIST [STRATEGY_LIST ...]]
                                    [--export {none,trades,signals}]
                                    [--backtest-filename PATH]
                                    [--backtest-directory PATH]
                                    [--freqai-backtest-live-models]
                                    [--minimum-trade-amount INT]
                                    [--targeted-trade-amount INT]
                                    [--lookahead-analysis-exportfilename LOOKAHEAD_ANALYSIS_EXPORTFILENAME]
                                    [--allow-limit-orders]

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
  --enable-protections, --enableprotections
                        为回测启用保护。会大大减慢
                        回测速度，但会
                        包含配置的保护
  --enable-dynamic-pairlist
                        在回测中启用动态交易对列表刷新。
                        如果您使用支持此功能的交易对列表处理器，例如 ShuffleFilter，
                        交易对列表将为每个新蜡烛生成。
  --dry-run-wallet DRY_RUN_WALLET, --starting-balance DRY_RUN_WALLET
                        起始余额，用于回测 / 超参数优化和
                        模拟运行。
  --timeframe-detail TIMEFRAME_DETAIL
                        指定回测的详细时间框架（`1m`、`5m`、
                        `30m`、`1h`、`1d`）。
  --strategy-list STRATEGY_LIST [STRATEGY_LIST ...]
                        提供要回测的策略的空格分隔列表。
                        请注意，需要在配置中或通过命令行设置时间框架。
                        当将此选项与 `--export trades` 一起使用时，策略名称是
                        注入到文件名中（因此 `backtest-data.json`
                        变为 `backtest-data-SampleStrategy.json`
  --export {none,trades,signals}
                        导出回测结果（默认：trades）。
  --backtest-filename PATH, --export-filename PATH
                        用于回测结果的文件名。示例：
                        `--backtest-
                        filename=backtest_results_2020-09-27_16-20-48.json`。
                        假设 `user_data/backtest_results/` 或
                        `--export-directory` 作为基础目录。
  --backtest-directory PATH, --export-directory PATH
                        用于回测结果的目录。示例：
                        `--export-directory=user_data/backtest_results/`。
  --freqai-backtest-live-models
                        使用就绪的模型运行回测。
  --minimum-trade-amount INT
                        前瞻分析的最小交易数量
  --targeted-trade-amount INT
                        前瞻分析的目标交易数量
  --lookahead-analysis-exportfilename LOOKAHEAD_ANALYSIS_EXPORTFILENAME
                        使用此 csv 文件名存储前瞻分析
                        结果
  --allow-limit-orders  在前瞻分析中允许限价订单（可能导致
                        前瞻分析结果中出现误报）。

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
