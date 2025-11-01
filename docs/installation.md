# 安装

本页说明如何准备运行机器人的环境。

freqtrade 文档描述了多种安装 freqtrade 的方法

* [Docker 镜像](docker_quickstart.md)（单独页面）
* [脚本安装](#script-installation)
* [手动安装](#manual-installation)
* [使用 Conda 安装](#installation-with-conda)

在评估 freqtrade 的工作原理时，请考虑使用预构建的 [docker 镜像](docker_quickstart.md) 快速开始。

------

## 信息

对于 Windows 安装，请使用 [Windows 安装指南](windows_installation.md)。

安装和运行 Freqtrade 的最简单方法是克隆机器人的 Github 仓库，然后运行 `./setup.sh` 脚本（如果您的平台支持）。

!!! Note "版本说明"
    克隆仓库时，默认工作分支名为 `develop`。此分支包含所有最新功能（由于自动化测试，可以认为是相对稳定的）。
    `stable` 分支包含最新版本的代码（通常每月一次，基于大约一周前的 `develop` 分支快照，以防止打包错误，因此可能更稳定）。

!!! Note "注意"
    假设已安装 [uv](https://docs.astral.sh/uv/) 或 Python3.11 或更高版本以及相应的 `pip`。如果不是这样，安装脚本会警告您并停止。还需要 `git` 来克隆 Freqtrade 仓库。
    此外，必须安装 python 头文件（`python<yourversion>-dev` / `python<yourversion>-devel`）才能成功完成安装。

!!! Warning "时钟同步"
    运行机器人的系统时钟必须准确，频繁与 NTP 服务器同步，以避免与交易所通信时出现问题。

------

## 要求

这些要求适用于 [脚本安装](#script-installation) 和 [手动安装](#manual-installation)。

!!! Note "ARM64 系统"
    如果您运行 ARM64 系统（如 MacOS M1 或 Oracle VM），请使用 [docker](docker_quickstart.md) 运行 freqtrade。
    虽然可以通过一些手动操作进行原生安装，但目前不支持。

### 安装指南

* [Python >= 3.11](http://docs.python-guide.org/en/latest/starting/installation/)
* [pip](https://pip.pypa.io/en/stable/installing/)
* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html)（推荐）

### 安装代码

我们已包含/收集了 Ubuntu、MacOS 和 Windows 的安装说明。这些是指南，您在其他发行版上的成功情况可能有所不同。
首先列出特定操作系统的步骤，下面的通用部分对所有系统都是必需的。

!!! Note "注意"
    假设已安装 Python3.11 或更高版本以及相应的 pip。

=== "Debian/Ubuntu"
    #### 安装必要的依赖

    ```bash
    # 更新仓库
    sudo apt-get update

    # 安装软件包
    sudo apt install -y python3-pip python3-venv python3-dev python3-pandas git curl
    ```

=== "MacOS"
    #### 安装必要的依赖

    如果您还没有安装，请安装 [Homebrew](https://brew.sh/)。

    ```bash
    # 安装软件包
    brew install gettext libomp
    ```
    !!! Note "注意"
        `setup.sh` 脚本会为您安装这些依赖 - 假设您的系统上已安装 brew。

=== "RaspberryPi/Raspbian"
    以下假设使用最新的 [Raspbian Buster lite 镜像](https://www.raspberrypi.org/downloads/raspbian/)。
    此镜像预装了 python3.11，使 freqtrade 易于启动和运行。

    使用 Raspbian Buster lite 镜像的 Raspberry Pi 3 进行测试，所有更新已应用。


    ```bash
    sudo apt-get install python3-venv libatlas-base-dev cmake curl libffi-dev
    # 使用 piwheels.org 加速安装
    sudo echo "[global]\nextra-index-url=https://www.piwheels.org/simple" > tee /etc/pip.conf

    git clone https://github.com/freqtrade/freqtrade.git
    cd freqtrade

    bash setup.sh -i
    ```

    !!! Note "安装时长"
        根据您的网络速度和 Raspberry Pi 版本，安装可能需要数小时才能完成。
        因此，我们建议通过遵循 [Docker 快速开始文档](docker_quickstart.md) 使用预构建的 Raspberry docker 镜像。

    !!! Note "注意"
        以上不会安装 hyperopt 依赖。要安装这些，请使用 `python3 -m pip install -e .[hyperopt]`。
        我们不建议在 Raspberry Pi 上运行 hyperopt，因为这是一个资源密集型操作，应该在功能强大的机器上完成。

------

## Freqtrade 仓库

Freqtrade 是一个开源加密货币交易机器人，其代码托管在 `github.com` 上

```bash
# 下载 freqtrade 仓库的 `develop` 分支
git clone https://github.com/freqtrade/freqtrade.git

# 进入下载的目录
cd freqtrade

# 您的选择 (1)：新手用户
git checkout stable

# 您的选择 (2)：高级用户
git checkout develop
```

(1) 此命令将克隆的仓库切换到使用 `stable` 分支。如果您希望保留在 (2) `develop` 分支上，则不需要此操作。

您以后可以随时使用 `git checkout stable`/`git checkout develop` 命令在分支之间切换。

??? Note "从 pypi 安装"
    安装 Freqtrade 的另一种方法是从 [pypi](https://pypi.org/project/freqtrade/) 安装。缺点是此方法需要事先正确安装 ta-lib，因此目前不是推荐的安装 Freqtrade 的方法。

    ``` bash
    pip install freqtrade
    ```

------

## 脚本安装

安装 Freqtrade 的第一种方法是使用提供的 Linux/MacOS `./setup.sh` 脚本，该脚本会安装所有依赖并帮助您配置机器人。

确保您满足 [要求](#requirements) 并已下载 [Freqtrade 仓库](#freqtrade-repository)。

### 使用 /setup.sh -install (Linux/MacOS)

如果您在 Debian、Ubuntu 或 MacOS 上，freqtrade 提供了安装 freqtrade 的脚本。

```bash
# --install，从头开始安装 freqtrade
./setup.sh -i
```

### 激活您的虚拟环境

每次打开新终端时，您必须运行 `source .venv/bin/activate` 来激活您的虚拟环境。

```bash
# 激活虚拟环境
source ./.venv/bin/activate
```

[您现在已准备好](#you-are-ready) 运行机器人。

### /setup.sh 脚本的其他选项

您还可以使用 `./script.sh` 更新、配置和重置机器人的代码库

```bash
# --update，执行 git pull 更新。
./setup.sh -u
# --reset，硬重置您的 develop/stable 分支。
./setup.sh -r
```

```
** --install **

使用此选项，脚本将安装机器人和大多数依赖项：
您需要事先安装 git 和 python3.11+ 才能使用。

* 必需软件：`ta-lib`
* 在 `.venv/` 下设置您的 virtualenv

此选项是安装任务和 `--reset` 的组合

** --update **

此选项将拉取当前分支的最新版本并更新您的 virtualenv。定期使用此选项运行脚本以更新您的机器人。

** --reset **

此选项将硬重置您的分支（仅当您在 `stable` 或 `develop` 上时）并重新创建您的 virtualenv。
```

-----

## Manual Installation

Make sure you fulfill the [Requirements](#requirements) and have downloaded the [Freqtrade repository](#freqtrade-repository).

### Setup Python virtual environment (virtualenv)

You will run freqtrade in separated `virtual environment`

```bash
# create virtualenv in directory /freqtrade/.venv
python3 -m venv .venv

# run virtualenv
source .venv/bin/activate
```

### Install python dependencies

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
# install freqtrade
python3 -m pip install -e .
```

[You are now ready](#you-are-ready) to run the bot.

### (Optional) Post-installation Tasks

!!! Note 
    If you run the bot on a server, you should consider using [Docker](docker_quickstart.md) or a terminal multiplexer like `screen` or [`tmux`](https://en.wikipedia.org/wiki/Tmux) to avoid that the bot is stopped on logout.

On Linux with software suite `systemd`, as an optional post-installation task, you may wish to setup the bot to run as a `systemd service` or configure it to send the log messages to the `syslog`/`rsyslog` or `journald` daemons. See [Advanced Logging](advanced-setup.md#advanced-logging) for details.

------

## Installation with Conda

Freqtrade can also be installed with Miniconda or Anaconda. We recommend using Miniconda as it's installation footprint is smaller. Conda will automatically prepare and manage the extensive library-dependencies of the Freqtrade program.

### What is Conda?

Conda is a package, dependency and environment manager for multiple programming languages: [conda docs](https://docs.conda.io/projects/conda/en/latest/index.html)

### Installation with conda

#### Install Conda

[Installing on linux](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html#install-linux-silent)

[Installing on windows](https://conda.io/projects/conda/en/latest/user-guide/install/windows.html)

Answer all questions. After installation, it is mandatory to turn your terminal OFF and ON again.

#### Freqtrade download

Download and install freqtrade.

```bash
# download freqtrade
git clone https://github.com/freqtrade/freqtrade.git

# enter downloaded directory 'freqtrade'
cd freqtrade      
```

#### Freqtrade install: Conda Environment

```bash
conda create --name freqtrade python=3.12
```

!!! Note "Creating Conda Environment"
    The conda command `create -n` automatically installs all nested dependencies for the selected libraries, general structure of installation command is:

    ```bash
    # choose your own packages
    conda env create -n [name of the environment] [python version] [packages]
    ```

#### Enter/exit freqtrade environment

To check available environments, type

```bash
conda env list
```

Enter installed environment

```bash
# enter conda environment
conda activate freqtrade

# exit conda environment - don't do it now
conda deactivate
```

Install last python dependencies with pip

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```

[You are now ready](#you-are-ready) to run the bot.

### Important shortcuts

```bash
# list installed conda environments
conda env list

# activate base environment
conda activate

# activate freqtrade environment
conda activate freqtrade

#deactivate any conda environments
conda deactivate                              
```

### Further info on anaconda

!!! Info "New heavy packages"
    It may happen that creating a new Conda environment, populated with selected packages at the moment of creation takes less time than installing a large, heavy library or application, into previously set environment.

!!! Warning "pip install within conda"
    The documentation of conda says that pip should NOT be used within conda, because internal problems can occur.
    However, they are rare. [Anaconda Blogpost](https://www.anaconda.com/blog/using-pip-in-a-conda-environment)

    Nevertheless, that is why, the `conda-forge` channel is preferred:

    * more libraries are available (less need for `pip`)
    * `conda-forge` works better with `pip`
    * the libraries are newer

Happy trading!

-----

## You are ready

You've made it this far, so you have successfully installed freqtrade.

### Initialize the configuration

```bash
# Step 1 - Initialize user folder
freqtrade create-userdir --userdir user_data

# Step 2 - Create a new configuration file
freqtrade new-config --config user_data/config.json
```

You are ready to run, read [Bot Configuration](configuration.md), remember to start with `dry_run: True` and verify that everything is working.

To learn how to setup your configuration, please refer to the [Bot Configuration](configuration.md) documentation page.

### Start the Bot

```bash
freqtrade trade --config user_data/config.json --strategy SampleStrategy
```

!!! Warning
    You should read through the rest of the documentation, backtest the strategy you're going to use, and use dry-run before enabling trading with real money.

-----

## Troubleshooting

### Common problem: "command not found"

If you used (1)`Script` or (2)`Manual` installation, you need to run the bot in virtual environment. If you get error as below, make sure venv is active.

```bash
# if:
bash: freqtrade: command not found

# then activate your virtual environment
source ./.venv/bin/activate
```

### MacOS installation error

Newer versions of MacOS may have installation failed with errors like `error: command 'g++' failed with exit status 1`.

This error will require explicit installation of the SDK Headers, which are not installed by default in this version of MacOS.
For MacOS 10.14, this can be accomplished with the below command.

```bash
open /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg
```

If this file is inexistent, then you're probably on a different version of MacOS, so you may need to consult the internet for specific resolution details.
