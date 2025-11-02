# 高级安装后任务

本页解释一些可以在机器人安装后执行的高级任务和配置选项，在某些环境中可能很有用。

如果您不知道这里提到的内容是什么意思，您可能不需要它。

## 运行多个 Freqtrade 实例

本节将向您展示如何在同一台机器上同时运行多个机器人。

### 需要考虑的事项

* 使用不同的数据库文件。
* 使用不同的 Telegram 机器人（需要多个不同的配置文件；仅在启用 Telegram 时适用）。
* 使用不同的端口（仅在启用 Freqtrade REST API Web 服务器时适用）。

### 不同的数据库文件

为了跟踪您的交易、利润等，freqtrade 使用 SQLite 数据库，其中存储各种类型的信息，例如您过去执行的交易以及您随时持有的当前头寸。这允许您跟踪您的利润，但最重要的是，如果机器人进程重新启动或意外终止，跟踪正在进行的活动。

默认情况下，Freqtrade 将为模拟运行和实盘机器人使用单独的数据库文件（这假设在配置中或通过命令行参数都没有给出数据库 URL）。
对于实盘交易模式，默认数据库将是 `tradesv3.sqlite`，对于模拟运行，它将是 `tradesv3.dryrun.sqlite`。

用于指定这些文件路径的交易命令的可选参数是 `--db-url`，它需要有效的 SQLAlchemy URL。
因此，当您在模拟运行模式下仅使用配置和策略参数启动机器人时，以下 2 个命令将产生相同的结果。

``` bash
freqtrade trade -c MyConfig.json -s MyStrategy
# is equivalent to
freqtrade trade -c MyConfig.json -s MyStrategy --db-url sqlite:///tradesv3.dryrun.sqlite
```

这意味着如果您在两个不同的终端中运行交易命令，例如测试以 USDT 交易的策略，在另一个实例中测试以 BTC 交易的策略，您将需要使用不同的数据库运行它们。

如果您指定一个不存在的数据库 URL，freqtrade 将使用您指定的名称创建一个新数据库。因此，要使用 BTC 和 USDT 作为投注货币测试您的自定义策略，您可以使用以下命令（在 2 个单独的终端中）：

``` bash
# Terminal 1:
freqtrade trade -c MyConfigBTC.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesBTC.dryrun.sqlite
# Terminal 2:
freqtrade trade -c MyConfigUSDT.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesUSDT.dryrun.sqlite
```

相反，如果您希望在生产模式下执行相同的操作，您还需要创建至少一个新数据库（除了默认数据库之外）并指定"实盘"数据库的路径，例如：

``` bash
# Terminal 1:
freqtrade trade -c MyConfigBTC.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesBTC.live.sqlite
# Terminal 2:
freqtrade trade -c MyConfigUSDT.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesUSDT.live.sqlite
```

有关使用 sqlite 数据库的更多信息，例如手动输入或删除交易，请参阅 [SQL 速查表](sql_cheatsheet.md)。

### 使用 docker 运行多个实例

要使用 docker 运行多个 freqtrade 实例，您需要编辑 docker-compose.yml 文件，并将所有需要的实例添加为单独的服务。请记住，您可以将配置分离到多个文件中，因此考虑使它们模块化是个好主意，然后如果您需要对所有机器人的共同内容进行编辑，可以在单个配置文件中完成。 
``` yml
---
version: '3'
services:
  freqtrade1:
    image: freqtradeorg/freqtrade:stable
    # image: freqtradeorg/freqtrade:develop
    # Use plotting image
    # image: freqtradeorg/freqtrade:develop_plot
    # Build step - only needed when additional dependencies are needed
    # build:
    #   context: .
    #   dockerfile: "./docker/Dockerfile.custom"
    restart: always
    container_name: freqtrade1
    volumes:
      - "./user_data:/freqtrade/user_data"
    # Expose api on port 8080 (localhost only)
    # Please read the https://www.freqtrade.io/en/latest/rest-api/ documentation
    # before enabling this.
     ports:
     - "127.0.0.1:8080:8080"
    # Default command used when running `docker compose up`
    command: >
      trade
      --logfile /freqtrade/user_data/logs/freqtrade1.log
      --db-url sqlite:////freqtrade/user_data/tradesv3_freqtrade1.sqlite
      --config /freqtrade/user_data/config.json
      --config /freqtrade/user_data/config.freqtrade1.json
      --strategy SampleStrategy
  
  freqtrade2:
    image: freqtradeorg/freqtrade:stable
    # image: freqtradeorg/freqtrade:develop
    # Use plotting image
    # image: freqtradeorg/freqtrade:develop_plot
    # Build step - only needed when additional dependencies are needed
    # build:
    #   context: .
    #   dockerfile: "./docker/Dockerfile.custom"
    restart: always
    container_name: freqtrade2
    volumes:
      - "./user_data:/freqtrade/user_data"
    # Expose api on port 8080 (localhost only)
    # Please read the https://www.freqtrade.io/en/latest/rest-api/ documentation
    # before enabling this.
    ports:
      - "127.0.0.1:8081:8080"
    # Default command used when running `docker compose up`
    command: >
      trade
      --logfile /freqtrade/user_data/logs/freqtrade2.log
      --db-url sqlite:////freqtrade/user_data/tradesv3_freqtrade2.sqlite
      --config /freqtrade/user_data/config.json
      --config /freqtrade/user_data/config.freqtrade2.json
      --strategy SampleStrategy

```

您可以使用任何命名约定，freqtrade1 和 2 是任意的。请注意，如上所述，您需要为每个实例使用不同的数据库文件、端口映射和 Telegram 配置。

## 使用不同的数据库系统

Freqtrade 使用 SQLAlchemy，它支持多种不同的数据库系统。因此，应支持多种数据库系统。
Freqtrade 不依赖或安装任何额外的数据库驱动程序。请在 [SQLAlchemy 文档](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls) 中查阅各个数据库系统的安装说明。

以下系统已经过测试并已知可与 freqtrade 一起使用：

* sqlite（默认）
* PostgreSQL
* MariaDB

!!! Warning
    通过使用以下数据库系统之一，您承认您了解如何管理这样的系统。freqtrade 团队不会提供有关以下数据库系统的设置或维护（或备份）的任何支持。

### PostgreSQL

安装：
`pip install "psycopg[binary]"`

用法：
`... --db-url postgresql+psycopg://<username>:<password>@localhost:5432/<database>`

Freqtrade 将在启动时自动创建必要的表。

如果您运行不同的 Freqtrade 实例，您必须为每个实例设置一个数据库，或者为连接使用不同的用户/架构。

### MariaDB / MySQL

Freqtrade 通过使用 SQLAlchemy 支持 MariaDB，该工具支持多种不同的数据库系统。

安装：
`pip install pymysql`

用法：
`... --db-url mysql+pymysql://<username>:<password>@localhost:3306/<database>`



## 将机器人配置为作为 systemd 服务运行

将 `freqtrade.service` 文件复制到您的 systemd 用户目录（通常是 `~/.config/systemd/user`）并更新 `WorkingDirectory` 和 `ExecStart` 以匹配您的设置。

!!! Note
    某些系统（如 Raspbian）不会从用户目录加载服务单元文件。在这种情况下，将 `freqtrade.service` 复制到 `/etc/systemd/user/`（需要超级用户权限）。

然后，您可以使用以下命令启动守护进程：

```bash
systemctl --user start freqtrade
```

要使此操作持久化（在用户注销时运行），您需要为您的 freqtrade 用户启用 `linger`。

```bash
sudo loginctl enable-linger "$USER"
```

如果您将机器人作为服务运行，您可以使用 systemd 服务管理器作为软件看门狗来监控 freqtrade 机器人状态，并在发生故障时重新启动它。如果配置中的 `internals.sd_notify` 参数设置为 true，或使用 `--sd-notify` 命令行选项，机器人将使用 sd_notify（systemd 通知）协议向 systemd 发送保持活动 ping 消息，并在状态更改时告诉 systemd 其当前状态（运行中、暂停或停止）。

`freqtrade.service.watchdog` 文件包含一个使用 systemd 作为看门狗的服务单元配置示例。

!!! Note
    如果机器人在 Docker 容器中运行，机器人与 systemd 服务管理器之间的 sd_notify 通信将不起作用。

## 高级日志

Freqtrade 使用 Python 提供的默认日志模块。
Python 允许在这方面进行广泛的[日志配置](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig)——远超此处可涵盖的内容。

如果您的 freqtrade 配置中未提供 `log_config`，则默认设置彩色终端输出的日志格式。
使用 `--logfile logfile.log` 将启用 RotatingFileHandler。

如果您对日志格式或为 RotatingFileHandler 提供的默认设置不满意，可以通过向 freqtrade 配置文件添加 `log_config` 配置来自定义日志。

默认配置大致如下，提供文件处理程序但未启用，因为 `filename` 被注释掉了。
取消注释此行并提供有效的路径/文件名以启用它。

``` json hl_lines="5-7 13-16 27"
{
  "log_config": {
      "version": 1,
      "formatters": {
          "basic": {
              "format": "%(message)s"
          },
          "standard": {
              "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
          }
      },
      "handlers": {
          "console": {
              "class": "freqtrade.loggers.ft_rich_handler.FtRichHandler",
              "formatter": "basic"
          },
          "file": {
              "class": "logging.handlers.RotatingFileHandler",
              "formatter": "standard",
              // "filename": "someRandomLogFile.log",
              "maxBytes": 10485760,
              "backupCount": 10
          }
      },
      "root": {
          "handlers": [
              "console",
              // "file"
          ],
          "level": "INFO",
      }
  }
}
```

!!! Note "highlighted lines"
    以上代码块中高亮的行定义了 Rich 处理器，它们属于一起。
    格式化器 "standard" 和 "file" 将属于 FileHandler。

每个处理器必须使用定义的格式化器之一（按名称），其类必须可用，并且必须是有效的日志类。
要实际使用处理器，它必须在 "root" 段内的 "handlers" 部分。
如果省略此部分，freqtrade 将不提供任何输出（在未配置的处理器中，无论如何）。

!!! Tip "显式日志配置"
    我们建议从主 freqtrade 配置文件中提取日志配置，并通过[多个配置文件](configuration.md#multiple-configuration-files)功能将其提供给您的机器人。这将避免不必要的代码重复。

---

在许多 Linux 系统上，可以将机器人配置为将其日志消息发送到 `syslog` 或 `journald` 系统服务。在 Windows 上也可以记录到远程 `syslog` 服务器。`--logfile` 命令行选项的特殊值可用于此目的。

### 日志记录到 syslog

要将 Freqtrade 日志消息发送到本地或远程 `syslog` 服务，请使用 `"log_config"` 设置选项来配置日志记录。

``` json
{
  // ...
  "log_config": {
    "version": 1,
    "formatters": {
      "syslog_fmt": {
        "format": "%(name)s - %(levelname)s - %(message)s"
      }
    },
    "handlers": {
      // Other handlers? 
      "syslog": {
         "class": "logging.handlers.SysLogHandler",
          "formatter": "syslog_fmt",
          // Use one of the other options above as address instead? 
          "address": "/dev/log"
      }
    },
    "root": {
      "handlers": [
        // other handlers
        "syslog",
        
      ]
    }

  }
}
```

可能需要配置[额外的日志处理器](#advanced-logging)，例如在控制台中也有日志输出。

#### Syslog 使用

日志消息以 `user` 设施发送到 `syslog`。因此，您可以使用以下命令查看它们：

* `tail -f /var/log/user`，或
* 安装一个全面的图形查看器（例如，Ubuntu 的 'Log File Viewer'）。

在许多系统上，`syslog` (`rsyslog`) 从 `journald` 获取数据（反之亦然），因此可以使用 syslog 或 journald，并通过 `journalctl` 和 syslog 查看器实用程序查看消息。您可以用任何更适合的方式组合这些。

对于 `rsyslog`，来自机器人的消息可以重定向到单独的专用日志文件。要实现此目的，请添加

```
if $programname startswith "freqtrade" then -/var/log/freqtrade.log
```

到 rsyslog 配置文件之一，例如在 `/etc/rsyslog.d/50-default.conf` 的末尾。

对于 `syslog` (`rsyslog`)，可以开启缩减模式。这将减少重复消息的数量。例如，当机器人没有其他事情发生时，多个机器人心跳消息将缩减为单个消息。要实现此目的，请在 `/etc/rsyslog.conf` 中设置：

```
# Filter duplicated messages
$RepeatedMsgReduction on
```

#### Syslog 寻址

syslog 地址可以是 Unix 域套接字（套接字文件名）或 UDP 套接字规范，由 IP 地址和 UDP 端口组成，用 `:` 字符分隔。

因此，以下是一些可能的地址示例：

* `"address": "/dev/log"` -- 使用 `/dev/log` 套接字记录到 syslog (rsyslog)，适用于大多数系统。
* `"address": "/var/run/syslog"` -- 使用 `/var/run/syslog` 套接字记录到 syslog (rsyslog)。在 MacOS 上使用此选项。
* `"address": "localhost:514"` -- 使用 UDP 套接字记录到本地 syslog，如果它在端口 514 上监听。
* `"address": "<ip>:514"` -- 在 IP 地址和端口 514 上记录到远程 syslog。这在 Windows 上可用于远程记录到外部 syslog 服务器。

??? Info "已弃用 - 通过命令行配置 syslog"
    `--logfile syslog:<syslog_address>` -- 使用 `<syslog_address>` 作为 syslog 地址将日志消息发送到 `syslog` 服务。

    syslog 地址可以是 Unix 域套接字（套接字文件名）或 UDP 套接字规范，由 IP 地址和 UDP 端口组成，用 `:` 字符分隔。

    因此，以下是一些可能用法的示例：

    * `--logfile syslog:/dev/log` -- 使用 `/dev/log` 套接字记录到 syslog (rsyslog)，适用于大多数系统。
    * `--logfile syslog` -- 同上，是 `/dev/log` 的快捷方式。
    * `--logfile syslog:/var/run/syslog` -- 使用 `/var/run/syslog` 套接字记录到 syslog (rsyslog)。在 MacOS 上使用此选项。
    * `--logfile syslog:localhost:514` -- 使用 UDP 套接字记录到本地 syslog，如果它在端口 514 上监听。
    * `--logfile syslog:<ip>:514` -- 在 IP 地址和端口 514 上记录到远程 syslog。这在 Windows 上可用于远程记录到外部 syslog 服务器。

### 日志记录到 journald

这需要安装 `cysystemd` python 包作为依赖项（`pip install cysystemd`），该包在 Windows 上不可用。因此，整个 journald 日志记录功能不适用于在 Windows 上运行的机器人。

要将 Freqtrade 日志消息发送到 `journald` 系统服务，请将以下配置片段添加到您的配置中。

``` json
{
  // ...
  "log_config": {
    "version": 1,
    "formatters": {
      "journald_fmt": {
        "format": "%(name)s - %(levelname)s - %(message)s"
      }
    },
    "handlers": {
      // Other handlers? 
      "journald": {
         "class": "cysystemd.journal.JournaldLogHandler",
          "formatter": "journald_fmt",
      }
    },
    "root": {
      "handlers": [
        // .. 
        "journald",
        
      ]
    }

  }
}
```

可能需要配置[额外的日志处理器](#advanced-logging)，例如在控制台中也有日志输出。

日志消息以 `user` 设施发送到 `journald`。因此，您可以使用以下命令查看它们：

* `journalctl -f` -- 显示发送到 `journald` 的 Freqtrade 日志消息以及由 `journald` 获取的其他日志消息。
* `journalctl -f -u freqtrade.service` -- 当机器人作为 `systemd` 服务运行时，可以使用此命令。

`journalctl` 实用程序中有许多其他选项可过滤消息，请参阅该实用程序的手册页。

在许多系统上，`syslog` (`rsyslog`) 从 `journald` 获取数据（反之亦然），因此可以使用 `--logfile syslog` 或 `--logfile journald`，并通过 `journalctl` 和 syslog 查看器实用程序查看消息。您可以用任何更适合的方式组合这些。

??? Info "已弃用 - 通过命令行配置 journald"
    要将 Freqtrade 日志消息发送到 `journald` 系统服务，请使用 `--logfile` 命令行选项，格式如下：

    `--logfile journald` -- 将日志消息发送到 `journald`。

### JSON 日志格式

您还可以将默认输出流配置为使用 JSON 格式。
"fmt_dict" 属性定义 JSON 输出的键——以及 [python 日志 LogRecord 属性](https://docs.python.org/3/library/logging.html#logrecord-attributes)。

以下配置将默认输出更改为 JSON。但是，也可以将相同的格式化器与 `RotatingFileHandler` 结合使用。
我们建议保留一种人类可读的格式。

``` json
{
  // ...
  "log_config": {
    "version": 1,
    "formatters": {
       "json": {
          "()": "freqtrade.loggers.json_formatter.JsonFormatter",
          "fmt_dict": {
              "timestamp": "asctime",
              "level": "levelname",
              "logger": "name",
              "message": "message"
          }
      }
    },
    "handlers": {
      // Other handlers? 
      "jsonStream": {
          "class": "logging.StreamHandler",
          "formatter": "json"
      }
    },
    "root": {
      "handlers": [
        // .. 
        "jsonStream",
        
      ]
    }

  }
}
```
