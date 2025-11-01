```
用法: freqtrade edge [-h] [-v] [--no-color] [--logfile FILE] [-V] [-c PATH]
                      [-d PATH] [--userdir PATH] [-s NAME]
                      [--strategy-path PATH] [--recursive-strategy-search]
                      [--freqaimodel NAME] [--freqaimodel-path PATH]
                      [-i TIMEFRAME] [--timerange TIMERANGE]
                      [--data-format-ohlcv {json,jsongz,feather,parquet}]
                      [--max-open-trades INT] [--stake-amount STAKE_AMOUNT]
                      [--fee FLOAT] [-p PAIRS [PAIRS ...]]

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
