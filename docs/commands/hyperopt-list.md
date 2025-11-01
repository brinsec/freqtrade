```
用法: freqtrade hyperopt-list [-h] [-v] [--no-color] [--logfile FILE] [-V]
                               [-c PATH] [-d PATH] [--userdir PATH] [--best]
                               [--profitable] [--min-trades INT]
                               [--max-trades INT] [--min-avg-time FLOAT]
                               [--max-avg-time FLOAT] [--min-avg-profit FLOAT]
                               [--max-avg-profit FLOAT]
                               [--min-total-profit FLOAT]
                               [--max-total-profit FLOAT]
                               [--min-objective FLOAT] [--max-objective FLOAT]
                               [--print-json] [--no-details]
                               [--hyperopt-filename FILENAME]
                               [--export-csv FILE]

选项:
  -h, --help            显示此帮助消息并退出
  --best                仅选择最佳 epoch。
  --profitable          仅选择盈利的 epoch。
  --min-trades INT      选择交易次数超过 INT 的 epoch。
  --max-trades INT      选择交易次数少于 INT 的 epoch。
  --min-avg-time FLOAT  选择平均时间高于此值的 epoch。
  --max-avg-time FLOAT  选择平均时间低于此值的 epoch。
  --min-avg-profit FLOAT
                        选择平均利润高于此值的 epoch。
  --max-avg-profit FLOAT
                        选择平均利润低于此值的 epoch。
  --min-total-profit FLOAT
                        选择总利润高于此值的 epoch。
  --max-total-profit FLOAT
                        选择总利润低于此值的 epoch。
  --min-objective FLOAT
                        选择目标值高于此值的 epoch。
  --max-objective FLOAT
                        选择目标值低于此值的 epoch。
  --print-json          以 JSON 格式打印输出。
  --no-details          不打印最佳 epoch 详细信息。
  --hyperopt-filename FILENAME
                        超参数优化结果文件名。示例：`--hyperopt-
                        filename=hyperopt_results_2020-09-27_16-20-48.pickle`
  --export-csv FILE    导出到 CSV 文件。这将禁用表格打印。
                        示例：--export-csv hyperopt.csv

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
