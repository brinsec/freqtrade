```
用法: freqtrade strategy-updater [-h] [-v] [--no-color] [--logfile FILE] [-V]
                                  [-c PATH] [-d PATH] [--userdir PATH]
                                  [--strategy-list STRATEGY_LIST [STRATEGY_LIST ...]]
                                  [--strategy-path PATH]
                                  [--recursive-strategy-search]

选项:
  -h, --help            显示此帮助消息并退出
  --strategy-list STRATEGY_LIST [STRATEGY_LIST ...]
                        提供要回测的策略的空格分隔列表。
                        请注意，需要在配置中或通过命令行设置时间框架。
                        当将此选项与 `--export trades` 一起使用时，策略名称是
                        注入到文件名中（因此 `backtest-data.json`
                        变为 `backtest-data-SampleStrategy.json`
  --strategy-path PATH  指定其他策略查找路径。
  --recursive-strategy-search
                        在策略文件夹中递归搜索策略。

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
