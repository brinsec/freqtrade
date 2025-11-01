# REST API

## FreqUI

FreqUI 现在有自己的专用[文档部分](freq-ui.md) - 请参阅该部分了解有关 FreqUI 的所有信息。

## 配置

通过将 api_server 部分添加到您的配置并将 `api_server.enabled` 设置为 `true` 来启用 REST API。

示例配置：

``` json
    "api_server": {
        "enabled": true,
        "listen_ip_address": "127.0.0.1",
        "listen_port": 8080,
        "verbosity": "error",
        "enable_openapi": false,
        "jwt_secret_key": "somethingrandom",
        "CORS_origins": [],
        "username": "Freqtrader",
        "password": "SuperSecret1!",
        "ws_token": "sercet_Ws_t0ken"
    },
```

!!! Danger "安全警告"
    默认情况下，配置仅监听 localhost（因此无法从其他系统访问）。我们强烈建议不要将此 API 暴露到互联网，并选择一个强大、唯一的密码，因为其他人可能能够控制您的机器人。

??? Note "在远程服务器上访问 API/UI"
    如果您在 VPS 上运行，您应该考虑使用 ssh 隧道，或设置 VPN（openVPN、wireguard）来连接到您的机器人。
    这将确保 freqUI 不会直接暴露到互联网，出于安全原因不推荐这样做（freqUI 默认不支持 https）。
    设置这些工具不是本教程的一部分，但可以在互联网上找到许多好的教程。

然后，您可以通过在浏览器中访问 `http://127.0.0.1:8080/api/v1/ping` 来访问 API 以检查 API 是否正常运行。
这应该返回响应：

``` output
{"status":"pong"}
```

所有其他端点返回敏感信息并要求身份验证，因此无法通过 Web 浏览器访问。

### 安全

要生成安全密码，最好使用密码管理器，或使用下面的代码。

``` python
import secrets
secrets.token_hex()
```

!!! Hint "JWT 令牌"
    使用相同的方法生成 JWT 密钥（`jwt_secret_key`）。

!!! Danger "密码选择"
    请确保选择一个非常强大、唯一的密码，以保护您的机器人免受未经授权的访问。
    还要将 `jwt_secret_key` 更改为随机值（无需记住此值，但它将用于加密您的会话，所以最好使用唯一的值！）。

### 使用 docker 配置

如果您使用 docker 运行机器人，您需要让机器人监听传入连接。然后安全性由 docker 处理。

``` json
    "api_server": {
        "enabled": true,
        "listen_ip_address": "0.0.0.0",
        "listen_port": 8080,
        "username": "Freqtrader",
        "password": "SuperSecret1!",
        //...
    },
```

确保以下 2 行在您的 docker-compose 文件中可用：

```yml
    ports:
      - "127.0.0.1:8080:8080"
```

!!! Danger "安全警告"
    通过在 docker 端口映射中使用 `"8080:8080"`（或 `"0.0.0.0:8080:8080"`），API 将对在正确端口下连接到服务器的所有人可用，因此其他人可能能够控制您的机器人。
    如果您在安全环境中运行机器人（如您的家庭网络），这**可能**是安全的，但不建议将 API 暴露到互联网。

## REST API

### 使用 API

我们建议使用支持的 `freqtrade-client` 包（也可作为 `scripts/rest_client.py` 使用）来使用 API。

此命令可以通过使用 `pip install freqtrade-client` 独立于任何运行的 freqtrade 机器人安装。

此模块设计为轻量级，仅依赖于 `requests` 和 `python-rapidjson` 模块，跳过 freqtrade 否则需要的所有重依赖项。

``` bash
freqtrade-client <command> [optional parameters]
```

默认情况下，脚本假设使用 `127.0.0.1`（localhost）和端口 `8080`，但您可以指定配置文件来覆盖此行为。

#### 最小化客户端配置

``` json
{
    "api_server": {
        "enabled": true,
        "listen_ip_address": "0.0.0.0",
        "listen_port": 8080,
        "username": "Freqtrader",
        "password": "SuperSecret1!",
        //...
    }
}
```

``` bash
freqtrade-client --config rest_config.json <command> [optional parameters]
```

具有许多参数的命令可能需要关键字参数（为了清晰） - 可以按如下方式提供：

``` bash
freqtrade-client --config rest_config.json forceenter BTC/USDT long enter_tag=GutFeeling
```

此方法适用于所有参数 - 检查 "show" 命令以获取可用参数列表。

??? Note "程序化使用"
    `freqtrade-client` 包（可独立于 freqtrade 安装）可以在您自己的脚本中使用，以与 freqtrade API 交互。
    为此，请使用以下内容：

    ``` python
    from freqtrade_client import FtRestClient
    

    client = FtRestClient(server_url, username, password)

    # 获取机器人的状态
    ping = client.ping()
    print(ping)

    # 将交易对添加到黑名单
    client.blacklist("BTC/USDT", "ETH/USDT")
    # 通过提供列表将交易对添加到黑名单
    client.blacklist(*listPairs)
    # ... 
    ```

    有关可用命令的完整列表，请参阅下面的列表。

可以使用 `help` 命令从 rest-client 脚本列出可能的命令。

``` bash
freqtrade-client help
```

``` output
可能的命令：

available_pairs
    根据时间框架 / 抵押货币选择返回可用交易对（回测数据）

        :param timeframe: 仅包含此时间框架的交易对。
        :param stake_currency: 仅包含此时间框架的交易对

balance
    获取账户余额。

blacklist
    显示当前黑名单。

        :param add: 要添加的币种列表（示例："BNB/BTC"）

cancel_open_order
    取消交易的开放订单。

        :param trade_id: 取消此交易的开放订单。

count
    返回开放交易的数量。

daily
    返回每天的利润和交易数量。

delete_lock
    从数据库中删除（禁用）锁定。

        :param lock_id: 要删除的锁定的 ID

delete_trade
    从数据库中删除交易。
        尝试关闭开放订单。需要在交易所上手动处理此资产。

        :param trade_id: 从数据库中删除具有此 ID 的交易。

forcebuy
    买入资产。

        :param pair: 要买入的交易对（ETH/BTC）
        :param price: 可选 - 买入价格

forceenter
    强制进入交易

        :param pair: 要买入的交易对（ETH/BTC）
        :param side: 'long' 或 'short'
        :param price: 可选 - 买入价格

forceexit
    强制退出交易。

        :param tradeid: 交易的 ID（可以通过 status 命令接收）
        :param ordertype: 要使用的订单类型（必须是 market 或 limit）
        :param amount: 要卖出的数量。如果未给出，则全部卖出

health
    提供运行机器人的快速健康检查。

lock_add
    手动锁定特定交易对

        :param pair: 要锁定的交易对
        :param until: 锁定到此日期（格式 "2024-03-30 16:00:00Z"）
        :param side: 要锁定的一侧（long、short、*）
        :param reason: 锁定的原因        

locks
    返回当前锁定

logs
    显示最新日志。

        :param limit: 将日志消息限制为最后 <limit> 条日志。无限制以获取整个日志。

pair_candles
    返回 <pair><timeframe> 的实时数据框。

        :param pair: 要获取数据的交易对
        :param timeframe: 仅包含此时间框架的交易对。
        :param limit: 将结果限制为最后 n 个蜡烛。

pair_history
    返回历史、已分析的数据框

        :param pair: 要获取数据的交易对
        :param timeframe: 仅包含此时间框架的交易对。
        :param strategy: 要分析并获取值的策略
        :param timerange: 要获取数据的时间范围（与 --timerange 端点相同的格式）

performance
    返回不同币种的性能。

ping
    简单 ping

plot_config
    如果策略定义了绘图配置，则返回绘图配置。

profit
    返回利润摘要。

reload_config
    重新加载配置。

show_config
    返回配置的一部分，与交易操作相关。

start
    如果机器人在停止状态，则启动机器人。

pause
    如果机器人在运行状态，则暂停机器人。如果在停止状态触发，将处理开放头寸。

stats
    返回统计报告（持续时间、卖出原因）。

status
    获取开放交易的状态。

stop
    停止机器人。使用 `start` 重新启动。

stopbuy
    停止买入（但优雅地处理卖出）。使用 `reload_config` 重置。

strategies
    列出可用策略

strategy
    获取策略详细信息

        :param strategy: 策略类名称

sysinfo
    提供系统信息（CPU、RAM 使用情况）

trade
    返回特定交易

        :param trade_id: 指定要获取的交易。

trades
    返回交易历史，按 ID 排序

        :param limit: 将交易限制为最后 X 笔交易。最多 500 笔交易。
        :param offset: 按此数量的交易偏移。

list_open_trades_custom_data
    返回包含开放交易自定义数据的字典

        :param key: str，可选 - 自定义数据的键
        :param limit: 将交易限制为 X 笔交易。
        :param offset: 按此数量的交易偏移。

list_custom_data
    返回指定交易的自定义数据字典

        :param trade_id: int - 交易的 ID
        :param key: str，可选 - 自定义数据的键

version
    返回机器人的版本。

whitelist
    显示当前白名单。


```

### 可用端点

如果您希望通过其他路由手动调用 REST API，例如直接通过 `curl`，下表显示了相关的 URL 端点和参数。
下表中的所有端点都需要以 API 的基础 URL 为前缀，例如 `http://127.0.0.1:8080/api/v1/` - 因此命令变为 `http://127.0.0.1:8080/api/v1/<command>`。

|  端点 | 方法 | 描述 / 参数 |
|-----------|--------|--------------------------|
| `/ping` | GET | 测试 API 就绪状态的简单命令 - 不需要身份验证。
| `/start` | POST | 启动交易者。
| `/pause` | POST | 暂停交易者。根据规则优雅地处理开放交易。不进入新头寸。
| `/stop` | POST | 停止交易者。
| `/stopbuy` | POST | 停止交易者打开新交易。根据规则优雅地关闭开放交易。
| `/reload_config` | POST | 重新加载配置文件。
| `/trades` | GET | 列出最后交易。每次调用限制为 500 笔交易。
| `/trade/<tradeid>` | GET | 获取特定交易。<br/>*参数：*<br/>- `tradeid` (`int`)
| `/trades/<tradeid>` | DELETE | 从数据库中删除交易。尝试关闭开放订单。需要在交易所上手动处理此交易。<br/>*参数：*<br/>- `tradeid` (`int`)
| `/trades/<tradeid>/open-order` | DELETE | 取消此交易的开放订单。<br/>*参数：*<br/>- `tradeid` (`int`)
| `/trades/<tradeid>/reload` | POST | 从交易所重新加载交易。仅在实盘模式下工作，可能有助于恢复在交易所上手动卖出的交易。<br/>*参数：*<br/>- `tradeid` (`int`)
| `/show_config` | GET | 显示当前配置的一部分，包含与操作相关的设置。
| `/logs` | GET | 显示最后日志消息。
| `/status` | GET | 列出所有开放交易。
| `/count` | GET | 显示已使用和可用的交易数量。
| `/entries` | GET | 显示给定交易对（或如果未给出交易对，则显示所有交易对）的每个入场标签的利润统计。交易对是可选的。<br/>*参数：*<br/>- `pair` (`str`)
| `/exits` | GET | 显示给定交易对（或如果未给出交易对，则显示所有交易对）的每个出场原因的利润统计。交易对是可选的。<br/>*参数：*<br/>- `pair` (`str`)
| `/mix_tags` | GET | 显示给定交易对（或如果未给出交易对，则显示所有交易对）的每个入场标签 + 出场原因组合的利润统计。交易对是可选的。<br/>*参数：*<br/>- `pair` (`str`)
| `/locks` | GET | 显示当前锁定的交易对。
| `/locks` | POST | 锁定交易对直到 "until"。（Until 将向上舍入到最近的时间框架）。Side 是可选的，为 `long` 或 `short`（默认为 `long`）。Reason 是可选的。<br/>*参数：*<br/>- `<pair>` (`str`)<br/>- `<until>` (`datetime`)<br/>- `[side]` (`str`)<br/>- `[reason]` (`str`)
| `/locks/<lockid>` | DELETE | 按 id 删除（禁用）锁定。<br/>*参数：*<br/>- `lockid` (`int`)
| `/profit` | GET | 显示来自已关闭交易的利润/损失摘要以及有关您表现的一些统计信息。
| `/forceexit` | POST | 立即退出给定交易（忽略 `minimum_roi`），使用给定的订单类型（"market" 或 "limit"，如果未指定则使用您的配置设置），以及所选数量（如果未指定则全部卖出）。如果 `all` 作为 `tradeid` 提供，则所有当前开放交易都将被强制退出。<br/>*参数：*<br/>- `<tradeid>` (`int` 或 `str`)<br/>- `<ordertype>` (`str`)<br/>- `[amount]` (`float`)
| `/forceenter` | POST | 立即进入给定交易对。Side 是可选的，为 `long` 或 `short`（默认为 `long`）。Rate 是可选的。（`force_entry_enable` 必须设置为 True）<br/>*参数：*<br/>- `<pair>` (`str`)<br/>- `<side>` (`str`)<br/>- `[rate]` (`float`)
| `/performance` | GET | 显示按交易对分组的每个已完成交易的性能。
| `/balance` | GET | 显示每种货币的账户余额。
| `/daily` | GET | 显示过去 n 天每天（n 默认为 7）的利润或损失。<br/>*参数：*<br/>- `timescale` (`int`)
| `/weekly` | GET | 显示过去 n 天每周（n 默认为 4）的利润或损失。<br/>*参数：*<br/>- `timescale` (`int`)
| `/monthly` | GET | 显示过去 n 天每月（n 默认为 3）的利润或损失。<br/>*参数：*<br/>- `timescale` (`int`)
| `/stats` | GET | 显示利润/损失原因摘要以及平均持有时间。
| `/whitelist` | GET | 显示当前白名单。
| `/blacklist` | GET | 显示当前黑名单。
| `/blacklist` | POST | 将指定交易对添加到黑名单。<br/>*参数：*<br/>- `blacklist` (`str`)
| `/blacklist` | DELETE | 从黑名单中删除指定的交易对列表。<br/>*参数：*<br/>- `[pair,pair]` (`list[str]`)
| `/pair_candles` | GET | 在机器人运行时返回交易对/时间框架组合的数据框。**Alpha**
| `/pair_candles` | POST | 在机器人运行时返回交易对/时间框架组合的数据框，按提供的列列表进行过滤以返回。**Alpha**<br/>*参数：*<br/>- `<column_list>` (`list[str]`)
| `/pair_history` | GET | 返回给定时间范围的分析数据框，由给定策略分析。**Alpha**
| `/pair_history` | POST | 返回给定时间范围的分析数据框，由给定策略分析，按提供的列列表进行过滤以返回。**Alpha**<br/>*参数：*<br/>- `<column_list>` (`list[str]`)
| `/plot_config` | GET | 从策略获取绘图配置（如果未配置则返回空）。**Alpha**
| `/strategies` | GET | 列出策略目录中的策略。**Alpha**
| `/strategy/<strategy>` | GET | 按策略类名称获取特定策略内容。**Alpha**<br/>*参数：*<br/>- `<strategy>` (`str`)
| `/available_pairs` | GET | 列出可用回测数据。**Alpha**
| `/version` | GET | 显示版本。
| `/sysinfo` | GET | 显示有关系统负载的信息。
| `/health` | GET | 显示机器人健康状态（最后一次机器人循环）。

!!! Warning "Alpha 状态"
    上面标记为 *Alpha 状态* 的端点可能随时更改，恕不另行通知。

### 消息 WebSocket

API 服务器包括一个 websocket 端点，用于订阅来自 freqtrade 机器人的 RPC 消息。
这可用于使用来自机器人的实时数据，例如入场/出场成交消息、白名单更改、交易对的已填充指标等。

这也用于在 Freqtrade 中设置[生产者/消费者模式](producer-consumer.md)。

假设您的 rest API 设置为端口 `8080` 上的 `127.0.0.1`，端点可在 `http://localhost:8080/api/v1/message/ws` 使用。

要访问 websocket 端点，端点 URL 中需要 `ws_token` 作为查询参数。

要生成安全的 `ws_token`，您可以运行以下代码：

``` python
>>> import secrets
>>> secrets.token_urlsafe(25)
'hZ-y58LXyX_HZ8O1cJzVyN6ePWrLpNQv4Q'
```

然后您将在 `api_server` 配置下的 `ws_token` 中添加该令牌。如下所示：

``` json
"api_server": {
    "enabled": true,
    "listen_ip_address": "127.0.0.1",
    "listen_port": 8080,
    "verbosity": "error",
    "enable_openapi": false,
    "jwt_secret_key": "somethingrandom",
    "CORS_origins": [],
    "username": "Freqtrader",
    "password": "SuperSecret1!",
    "ws_token": "hZ-y58LXyX_HZ8O1cJzVyN6ePWrLpNQv4Q" // <-----
},
```

您现在可以在 `http://localhost:8080/api/v1/message/ws?token=hZ-y58LXyX_HZ8O1cJzVyN6ePWrLpNQv4Q` 连接到端点。

!!! Danger "重用示例令牌"
    请不要使用上面的示例令牌。为确保您的安全，请生成一个全新的令牌。

#### 使用 WebSocket

连接到 WebSocket 后，机器人将向订阅它们的任何人广播 RPC 消息。要订阅消息列表，您必须通过 WebSocket 发送 JSON 请求，如下所示。`data` 键必须是消息类型字符串的列表。

``` json
{
  "type": "subscribe",
  "data": ["whitelist", "analyzed_df"] // 字符串消息类型的列表
}
```

有关消息类型列表，请参阅 `freqtrade/enums/rpcmessagetype.py` 中的 RPCMessageType 枚举

现在，只要连接处于活动状态，机器人中发送的那些类型的 RPC 消息都会通过 WebSocket 接收。它们通常采用与请求相同的形式：

``` json
{
  "type": "analyzed_df",
  "data": {
      "key": ["NEO/BTC", "5m", "spot"],
      "df": {}, // 数据框
      "la": "2022-09-08 22:14:41.457786+00:00"
  }
}
```

#### 反向代理设置

使用 [Nginx](https://nginx.org/en/docs/) 时，WebSocket 需要以下配置（注意此配置不完整，缺少一些信息，不能直接使用）：

请确保将 `<freqtrade_listen_ip>`（以及随后的端口）替换为与您的配置/设置匹配的 IP 和端口。

```
http {
    map $http_upgrade $connection_upgrade {
        default upgrade;
        '' close;
    }

    #...

    server {
        #...

        location / {
            proxy_http_version 1.1;
            proxy_pass http://<freqtrade_listen_ip>:8080;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
        }
    }
}
```

要正确配置您的反向代理（安全地），请查阅其文档以了解如何代理 websocket。

- **Traefik**：Traefik 开箱即用地支持 websocket，请参阅[文档](https://doc.traefik.io/traefik/)
- **Caddy**：Caddy v2 开箱即用地支持 websocket，请参阅[文档](https://caddyserver.com/docs/v2-upgrade#proxy)

!!! Tip "SSL 证书"
    您可以使用 certbot 等工具设置 ssl 证书，通过使用上述任何反向代理通过加密连接访问机器人的 UI。
    虽然这将保护传输中的数据，但我们不建议在您的专用网络（VPN、SSH 隧道）之外运行 freqtrade API。

### OpenAPI 接口

要启用内置的 openAPI 接口（Swagger UI），请在 api_server 配置中指定 `"enable_openapi": true`。
这将在 `/docs` 端点启用 Swagger UI。默认情况下，它在 <http://localhost:8080/docs> 运行 - 但这取决于您的设置。

### 使用 JWT 令牌的高级 API 使用

!!! Note "注意"
    以下应在应用程序（通过 API 获取信息的 Freqtrade REST API 客户端）中完成，不打算定期使用。

Freqtrade 的 REST API 还提供 JWT（JSON Web 令牌）。
您可以使用以下命令登录，然后使用生成的 access_token。

``` bash
> curl -X POST --user Freqtrader http://localhost:8080/api/v1/token/login
{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk2ODEsIm5iZiI6MTU4OTExOTY4MSwianRpIjoiMmEwYmY0NWUtMjhmOS00YTUzLTlmNzItMmM5ZWVlYThkNzc2IiwiZXhwIjoxNTg5MTIwNTgxLCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.qt6MAXYIa-l556OM7arBvYJ0SDI9J8bIk3_glDujF5g","refresh_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk2ODEsIm5iZiI6MTU4OTExOTY4MSwianRpIjoiZWQ1ZWI3YjAtYjMwMy00YzAyLTg2N2MtNWViMjIxNWQ2YTMxIiwiZXhwIjoxNTkxNzExNjgxLCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJ0eXBlIjoicmVmcmVzaCJ9.d1AT_jYICyTAjD0fiQAr52rkRqtxCjUGEMwlNuuzgNQ"}

> access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk2ODEsIm5iZiI6MTU4OTExOTY4MSwianRpIjoiMmEwYmY0NWUtMjhmOS00YTUzLTlmNzItMmM5ZWVlYThkNzc2IiwiZXhwIjoxNTg5MTIwNTgxLCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.qt6MAXYIa-l556OM7arBvYJ0SDI9J8bIk3_glDujF5g"
# 使用 access_token 进行身份验证
> curl -X GET --header "Authorization: Bearer ${access_token}" http://localhost:8080/api/v1/count

```

由于访问令牌有短超时（15 分钟）- 应定期使用 `token/refresh` 请求以获取新的访问令牌：

``` bash
> curl -X POST --header "Authorization: Bearer ${refresh_token}"http://localhost:8080/api/v1/token/refresh
{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk5NzQsIm5iZiI6MTU4OTExOTk3NCwianRpIjoiMDBjNTlhMWUtMjBmYS00ZTk0LTliZjAtNWQwNTg2MTdiZDIyIiwiZXhwIjoxNTg5MTIwODc0LCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.1seHlII3WprjjclY6DpRhen0rqdF4j6jbvxIhUFaSbs"}
```

--8<-- "includes/cors.md"
