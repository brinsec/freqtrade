# 启动机器人

本页说明机器人的不同参数以及如何运行它。

!!! Note "注意"
    如果您使用了 `setup.sh`，在运行 freqtrade 命令之前不要忘记激活您的虚拟环境（`source .venv/bin/activate`）。

!!! Warning "时钟同步"
    运行机器人的系统时钟必须准确，频繁与 NTP 服务器同步，以避免与交易所通信时出现问题。

## 机器人命令

--8<-- "commands/main.md"

### 机器人交易命令

--8<-- "commands/trade.md"

### 如何指定使用哪个配置文件？

机器人允许您通过 `-c/--config` 命令行选项选择要使用的配置文件：

```bash
freqtrade trade -c path/far/far/away/config.json
```

默认情况下，机器人从当前工作目录加载 `config.json` 配置文件。

### 如何使用多个配置文件？

机器人允许您通过在命令行中指定多个 `-c/--config` 选项来使用多个配置文件。后一个配置文件中定义的配置参数会覆盖命令行中更早指定的前一个配置文件中相同名称的参数。

例如，您可以为用于交易的交易所创建一个包含密钥和密钥的单独配置文件，在模拟模式（实际上不需要它们）下运行时指定具有空密钥和密钥值的默认配置文件：

```bash
freqtrade trade -c ./config.json
```

在正常的实盘交易模式下运行时可指定两个配置文件：

```bash
freqtrade trade -c ./config.json -c path/to/secrets/keys.config.json
```

这可以帮助您通过在包含实际密钥的文件上设置适当的文件权限来隐藏本地机器上的私有交易所密钥和交易所密钥，此外，当您在项目问题或互联网上发布配置示例时，可以防止意外泄露敏感私有数据。

请参阅文档页面上有关 [配置](configuration.md) 的更多详细信息及示例。

### 在哪里存储自定义数据

Freqtrade 允许使用 `freqtrade create-userdir --userdir someDirectory` 创建用户数据目录。
此目录将如下所示：

```
user_data/
├── backtest_results
├── data
├── hyperopts
├── hyperopt_results
├── plot
└── strategies
```

您可以在配置中添加 "user_data_dir" 设置，以始终将机器人指向此目录。
或者，在每个命令中传入 `--userdir`。
如果目录不存在，机器人将无法启动，但会创建必要的子目录。

此目录应包含您的自定义策略、自定义超参数优化和超参数优化损失函数、回测历史数据（使用回测命令或下载脚本下载）和绘图输出。

建议使用版本控制来跟踪策略的更改。

### 如何使用 **--strategy**？

此参数允许您加载自定义策略类。
要测试机器人安装，您可以使用 `create-userdir` 子命令安装的 `SampleStrategy`（通常是 `user_data/strategy/sample_strategy.py`）。

机器人将在 `user_data/strategies` 中搜索您的策略文件。
要使用其他目录，请阅读下一节关于 `--strategy-path` 的内容。

要加载策略，只需在此参数中传递类名（例如：`CustomStrategy`）。

**示例：**
在 `user_data/strategies` 中，您有一个文件 `my_awesome_strategy.py`，其中包含一个名为 `AwesomeStrategy` 的策略类，要加载它：

```bash
freqtrade trade --strategy AwesomeStrategy
```

If the bot does not find your strategy file, it will display in an error
message the reason (File not found, or errors in your code).

Learn more about strategy file in
[Strategy Customization](strategy-customization.md).

### How to use **--strategy-path**?

This parameter allows you to add an additional strategy lookup path, which gets
checked before the default locations (The passed path must be a directory!):

```bash
freqtrade trade --strategy AwesomeStrategy --strategy-path /some/directory
```

#### How to install a strategy?

This is very simple. Copy paste your strategy file into the directory
`user_data/strategies` or use `--strategy-path`. And voila, the bot is ready to use it.

### How to use **--db-url**?

When you run the bot in Dry-run mode, per default no transactions are
stored in a database. If you want to store your bot actions in a DB
using `--db-url`. This can also be used to specify a custom database
in production mode. Example command:

```bash
freqtrade trade -c config.json --db-url sqlite:///tradesv3.dry_run.sqlite
```

## Next step

The optimal strategy of the bot will change with time depending of the market trends. The next step is to
[Strategy Customization](strategy-customization.md).
