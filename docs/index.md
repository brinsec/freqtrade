![freqtrade](assets/freqtrade_poweredby.svg)

[![Freqtrade CI](https://github.com/freqtrade/freqtrade/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/freqtrade/freqtrade/actions/)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.04864/status.svg)](https://doi.org/10.21105/joss.04864)
[![Coverage Status](https://coveralls.io/repos/github/freqtrade/freqtrade/badge.svg?branch=develop&service=github)](https://coveralls.io/github/freqtrade/freqtrade?branch=develop)

<!-- GitHub action buttons -->
[:octicons-star-16: Star](https://github.com/freqtrade/freqtrade){ .md-button .md-button--sm }
[:octicons-repo-forked-16: Fork](https://github.com/freqtrade/freqtrade/fork){ .md-button .md-button--sm }
[:octicons-download-16: Download](https://github.com/freqtrade/freqtrade/archive/stable.zip){ .md-button .md-button--sm }

## 简介

Freqtrade 是一个用 Python 编写的免费开源加密货币交易机器人。它旨在支持所有主要交易所，并可通过 Telegram 或 WebUI 进行控制。它包含回测、绘图和资金管理工具，以及通过机器学习进行策略优化。

!!! Danger "免责声明"
    本软件仅供教育用途。不要使用您害怕损失的资金。使用本软件的风险由您自行承担。作者及所有关联方不对您的交易结果承担任何责任。

    始终先在 Dry-run（模拟运行）模式下运行交易机器人，在您了解其工作原理以及应该预期的盈亏之前，不要投入真实资金。

    我们强烈建议您具备基本的编程技能和 Python 知识。不要犹豫，阅读源代码并理解这个机器人的机制、算法和技术实现。

![freqtrade screenshot](assets/freqtrade-screenshot.png)

## 功能特性

- 开发您的策略：使用 [pandas](https://pandas.pydata.org/) 用 Python 编写您的策略。可用的示例策略可在 [策略仓库](https://github.com/freqtrade/freqtrade-strategies) 中找到以激发您的灵感。
- 下载市场数据：下载交易所和您可能想要交易的市场的历史数据。
- 回测：在下载的历史数据上测试您的策略。
- 优化：使用采用机器学习方法的超参数优化为您的策略找到最佳参数。您可以优化买入、卖出、止盈（ROI）、止损和追踪止损参数。
- 选择市场：创建您的静态列表或使用基于最高交易量和/或价格的自动列表（回测期间不可用）。您也可以明确地将不想交易的市场列入黑名单。
- 运行：使用模拟资金（Dry-Run 模式）测试您的策略，或使用真实资金（Live-Trade 模式）部署它。
- 控制/监控：使用 Telegram 或 WebUI（启动/停止机器人、显示盈亏、每日摘要、当前未平仓交易结果等）。
- 分析：可以对回测数据或 Freqtrade 交易历史（SQL 数据库）进行进一步分析，包括自动化标准图表，以及将数据加载到[交互式环境](data-analysis.md)的方法。

## 支持的交易所市场

请阅读 [交易所特定说明](exchanges.md) 以了解每个交易所可能需要的特殊配置。

- [X] [Binance](https://www.binance.com/)
- [X] [BingX](https://bingx.com/invite/0EM9RX)
- [X] [Bitget](https://www.bitget.com/)
- [X] [Bitmart](https://bitmart.com/)
- [X] [Bybit](https://bybit.com/)
- [X] [Gate.io](https://www.gate.io/ref/6266643)
- [X] [HTX](https://www.htx.com/)
- [X] [Hyperliquid](https://hyperliquid.xyz/)（去中心化交易所，即 DEX）
- [X] [Kraken](https://kraken.com/)
- [X] [OKX](https://okx.com/)
- [X] [MyOKX](https://okx.com/) (OKX EEA)
- [ ] [可能还有很多其他交易所通过 <img alt="ccxt" width="30px" src="assets/ccxt-logo.svg" />](https://github.com/ccxt/ccxt/)。_（我们无法保证它们能正常工作）_

### 支持的期货交易所（实验性）

- [X] [Binance](https://www.binance.com/)
- [X] [Bitget](https://www.bitget.com/)
- [X] [Bybit](https://bybit.com/)
- [X] [Gate.io](https://www.gate.io/ref/6266643)
- [X] [Hyperliquid](https://hyperliquid.xyz/)（去中心化交易所，即 DEX）
- [X] [OKX](https://okx.com/)

在使用之前，请确保阅读 [交易所特定说明](exchanges.md) 以及 [杠杆交易](leverage.md) 文档。

### 社区测试

社区确认可以正常工作的交易所：

- [X] [Bitvavo](https://bitvavo.com/)
- [X] [Kucoin](https://www.kucoin.com/)

## Community showcase

--8<-- "includes/showcase.md"

## 要求

### 硬件要求

要运行此机器人，我们建议您使用至少以下配置的 Linux 云实例：

- 2GB RAM
- 1GB 磁盘空间
- 2vCPU

### 软件要求

- Docker（推荐）

或者

- Python 3.11+
- pip (pip3)
- git
- TA-Lib
- virtualenv（推荐）

## 支持

### 帮助 / Discord

对于文档中未涵盖的任何问题，或有关机器人的更多信息，或者只是想与志同道合的人交流，我们鼓励您加入 Freqtrade [Discord 服务器](https://discord.gg/p7nuUNVfP7)。

## 准备尝试？

首先阅读安装指南 [Docker 版本](docker_quickstart.md)（推荐），或 [非 Docker 安装](installation.md)。
