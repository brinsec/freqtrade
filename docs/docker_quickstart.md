# 使用 Docker 运行 Freqtrade

本页说明如何使用 Docker 运行机器人。它不能开箱即用。您仍需要阅读文档并了解如何正确配置。

## 安装 Docker

首先为您的平台下载并安装 Docker / Docker Desktop：

* [Mac](https://docs.docker.com/docker-for-mac/install/)
* [Windows](https://docs.docker.com/docker-for-windows/install/)
* [Linux](https://docs.docker.com/install/)

!!! Info "Docker compose 安装"
    Freqtrade 文档假定使用 Docker desktop（或 docker compose 插件）。
    虽然独立的 docker-compose 安装仍然有效，但需要将所有 `docker compose` 命令从 `docker compose` 更改为 `docker-compose` 才能工作（例如 `docker compose up -d` 将变为 `docker-compose up -d`）。

??? Warning "Windows 上的 Docker"
    如果您刚刚在 Windows 系统上安装了 docker，请确保重新启动系统，否则可能会遇到与 docker 容器网络连接相关的无法解释的问题。

## 使用 Docker 运行 Freqtrade

Freqtrade 在 [Dockerhub](https://hub.docker.com/r/freqtradeorg/freqtrade/) 上提供官方 Docker 镜像，以及可供使用的 [docker compose 文件](https://github.com/freqtrade/freqtrade/blob/stable/docker-compose.yml)。

!!! Note "注意"
    - 以下部分假定已安装 `docker` 并且登录用户可以使用。
    - 以下所有命令都使用相对目录，必须从包含 `docker-compose.yml` 文件的目录执行。

### Docker 快速开始

创建一个新目录并将 [docker-compose 文件](https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml) 放在此目录中。

``` bash
mkdir ft_userdata
cd ft_userdata/
# 从仓库下载 docker-compose 文件
curl https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml

# 拉取 freqtrade 镜像
docker compose pull

# 创建用户目录结构
docker compose run --rm freqtrade create-userdir --userdir user_data

# 创建配置 - 需要回答交互式问题
docker compose run --rm freqtrade new-config --config user_data/config.json
```

上面的代码片段创建了一个名为 `ft_userdata` 的新目录，下载最新的 compose 文件并拉取 freqtrade 镜像。
代码片段中的最后 2 个步骤创建包含 `user_data` 的目录，以及（交互式）根据您的选择创建默认配置。

!!! Question "如何编辑机器人配置？"
    您可以随时编辑配置，使用上述配置时，配置在 `user_data/config.json`（在 `ft_userdata` 目录内）中可用。

    您还可以通过编辑 `docker-compose.yml` 文件的命令部分来更改策略和命令。

#### 添加自定义策略

1. 配置现在在 `user_data/config.json` 中可用
2. 将自定义策略复制到目录 `user_data/strategies/`
3. 将策略类名添加到 `docker-compose.yml` 文件

默认运行 `SampleStrategy`。

!!! Danger "`SampleStrategy` 只是一个演示！"
    `SampleStrategy` 仅供参考，为您自己的策略提供思路。
    请务必在冒真实资金风险之前对您的策略进行回测并在一段时间内使用模拟运行！
    您可以在 [策略文档](strategy-customization.md) 中找到有关策略开发的更多信息。

完成此操作后，您就可以在交易模式下启动机器人（模拟运行或实盘交易，取决于您对上面相应问题的回答）。

``` bash
docker compose up -d
```

!!! Warning "默认配置"
    虽然生成的配置大多是功能性的，但在启动机器人之前，您仍需要验证所有选项是否符合您的需求（如定价、交易对列表等）。

#### 访问 UI

如果您在 `new-config` 步骤中选择了启用 FreqUI，您将在端口 `localhost:8080` 上拥有 freqUI。

您现在可以通过在浏览器中键入 localhost:8080 来访问 UI。

??? Note "在远程服务器上访问 UI"
    如果您在 VPS 上运行，您应该考虑使用 ssh 隧道或设置 VPN（openVPN、wireguard）来连接到您的机器人。
    这将确保 freqUI 不会直接暴露到互联网，出于安全原因不推荐这样做（freqUI 默认不支持 https）。
    这些工具的设置不是本教程的一部分，但可以在互联网上找到许多好的教程。
    还请阅读 [使用 docker 的 API 配置](rest-api.md#configuration-with-docker) 部分以了解有关此配置的更多信息。

#### 监控机器人

您可以使用 `docker compose ps` 检查正在运行的实例。
这应该将服务 `freqtrade` 列为 `running`。如果不是这样，最好检查日志（请参阅下一点）。

#### Docker compose 日志

日志将写入：`user_data/logs/freqtrade.log`。
您还可以使用命令 `docker compose logs -f` 查看最新日志。

#### 数据库

数据库将位于：`user_data/tradesv3.sqlite`

#### 使用 docker 更新 freqtrade

使用 `docker` 更新 freqtrade 就像运行以下 2 个命令一样简单：

``` bash
# 下载最新镜像
docker compose pull
# 重启镜像
docker compose up -d
```

这将首先拉取最新镜像，然后使用刚刚拉取的版本重启容器。

!!! Warning "检查更新日志"
    您应该始终检查更新日志以了解破坏性更改/所需的手动干预，并确保机器人在更新后正确启动。

### 编辑 docker-compose 文件

高级用户可以进一步编辑 docker-compose 文件以包含所有可能的选项或参数。

所有 freqtrade 参数都可通过运行 `docker compose run --rm freqtrade <command> <optional arguments>` 获得。

!!! Warning "交易命令的 `docker compose`"
    交易命令（`freqtrade trade <...>`）不应通过 `docker compose run` 运行 - 而应使用 `docker compose up -d`。
    这确保容器正确启动（包括端口转发），并确保容器在系统重启后重启。
    如果您打算使用 freqUI，请确保相应地调整 [配置](rest-api.md#configuration-with-docker)，否则 UI 将不可用。

!!! Note "`docker compose run --rm`"
    包含 `--rm` 将在完成后删除容器，强烈建议用于除交易模式（使用 `freqtrade trade` 命令运行）以外的所有模式。

??? Note "不使用 docker compose 使用 docker"
    "`docker compose run --rm`" 需要提供 compose 文件。
    一些不需要身份验证的 freqtrade 命令（如 `list-pairs`）可以改用 "`docker run --rm`" 运行。
    例如 `docker run --rm freqtradeorg/freqtrade:stable list-pairs --exchange binance --quote BTC --print-json`。
    这对于获取交易所信息以添加到您的 `config.json` 而不会影响正在运行的容器很有用。

#### 示例：使用 docker 下载数据

从 Binance 下载 ETH/BTC 交易对和 1h 时间框架的 5 天回测数据。数据将存储在主机上的 `user_data/data/` 目录中。

``` bash
docker compose run --rm freqtrade download-data --pairs ETH/BTC --exchange binance --days 5 -t 1h
```

前往 [数据下载文档](data-download.md) 了解更多下载数据的详细信息。

#### 示例：使用 docker 回测

在 docker 容器中为 SampleStrategy 和指定的历史数据时间范围运行回测，时间框架为 5m：

``` bash
docker compose run --rm freqtrade backtesting --config user_data/config.json --strategy SampleStrategy --timerange 20190801-20191001 -i 5m
```

前往 [回测文档](backtesting.md) 了解更多。

### 使用 docker 的额外依赖项

如果您的策略需要默认镜像中未包含的依赖项 - 则需要在主机上构建镜像。
为此，请创建一个包含额外依赖项安装步骤的 Dockerfile（请查看 [docker/Dockerfile.custom](https://github.com/freqtrade/freqtrade/blob/develop/docker/Dockerfile.custom) 作为示例）。

然后您还需要修改 `docker-compose.yml` 文件并取消注释构建步骤，以及重命名镜像以避免命名冲突。

``` yaml
    image: freqtrade_custom
    build:
      context: .
      dockerfile: "./Dockerfile.<yourextension>"
```

然后您可以运行 `docker compose build --pull` 来构建 docker 镜像，并使用上面描述的命令运行它。

### 使用 docker 绘图

通过将 `docker-compose.yml` 文件中的镜像更改为 `*_plot`，可以使用命令 `freqtrade plot-profit` 和 `freqtrade plot-dataframe`（[文档](plotting.md)）。
然后您可以按如下方式使用这些命令：

``` bash
docker compose run --rm freqtrade plot-dataframe --strategy AwesomeStrategy -p BTC/ETH --timerange=20180801-20180805
```

输出将存储在 `user_data/plot` 目录中，可以使用任何现代浏览器打开。

### 使用 docker compose 进行数据分析

Freqtrade 提供了一个启动 jupyter lab 服务器的 docker-compose 文件。
您可以使用以下命令运行此服务器：

``` bash
docker compose -f docker/docker-compose-jupyter.yml up
```

这将创建一个运行 jupyter lab 的 docker 容器，可通过 `https://127.0.0.1:8888/lab` 访问。
启动后请使用控制台中打印的链接以便简化登录。

由于此镜像的一部分是在您的机器上构建的，建议不时重新构建镜像以保持 freqtrade（和依赖项）的最新状态。

``` bash
docker compose -f docker/docker-compose-jupyter.yml build --no-cache
```

## 故障排除

### Windows 上的 Docker

* 错误：`"Timestamp for this request is outside of the recvWindow."`
  市场 API 请求需要同步时钟，但 docker 容器中的时间会随着时间的推移略微向后偏移。
  要临时修复此问题，您需要运行 `wsl --shutdown` 并重新启动 docker（Windows 10 上的弹出窗口将要求您这样做）。
  永久解决方案是在 Linux 主机上托管 docker 容器或使用调度程序不时重启 wsl。

  ``` bash
  taskkill /IM "Docker Desktop.exe" /F
  wsl --shutdown
  start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
  ```

* 无法连接到 API (Windows)
  如果您在 Windows 上并且刚刚安装了 Docker (desktop)，请确保重新启动系统。Docker 可能在不重启的情况下出现网络连接问题。
  您显然还应该确保相应地设置 [设置](#accessing-the-ui)。

!!! Warning "警告"
    由于上述原因，我们不建议在 Windows 上使用 docker 进行生产设置，仅用于实验、数据下载和回测。
    最好使用 Linux-VPS 可靠地运行 freqtrade。
