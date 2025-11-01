```
用法: freqtrade backtesting-show [-h] [-v] [--no-color] [--logfile FILE] [-V]
                                  [-c PATH] [-d PATH] [--userdir PATH]
                                  [--backtest-filename PATH]
                                  [--backtest-directory PATH]
                                  [--show-pair-list]
                                  [--breakdown {day,week,month,year,weekday} [{day,week,month,year,weekday} ...]]

选项:
  -h, --help            显示此帮助消息并退出
  --backtest-filename PATH, --export-filename PATH
                        用于回测结果的文件名。示例：
                        `--backtest-
                        filename=backtest_results_2020-09-27_16-20-48.json`。
                        假设 `user_data/backtest_results/` 或
                        `--export-directory` 作为基础目录。
  --backtest-directory PATH, --export-directory PATH
                        用于回测结果的目录。示例：
                        `--export-directory=user_data/backtest_results/`。
  --show-pair-list      显示按利润排序的回测交易对列表。
  --breakdown {day,week,month,year,weekday} [{day,week,month,year,weekday} ...]
                        按 [天、周、月、
                        年、工作日] 显示回测分解。

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

```
