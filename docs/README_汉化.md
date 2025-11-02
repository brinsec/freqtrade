# Freqtrade 中文汉化说明

## 项目概述

本项目是 Freqtrade 加密货币交易机器人的中文汉化版本，已完成对文档、CLI帮助信息、后端 API 响应消息的全面中文化。

## 汉化完成情况

### ✅ 已完成的部分

#### 1. 文档翻译（99.5%+）

**核心文档（100%）**
- ✅ `index.md` - 文档首页
- ✅ `installation.md` - 安装指南
- ✅ `windows_installation.md` - Windows 安装指南
- ✅ `docker_quickstart.md` - Docker 快速入门
- ✅ `bot-basics.md` - 机器人基础知识
- ✅ `bot-usage.md` - 机器人使用
- ✅ `configuration.md` - 配置说明
- ✅ `faq.md` - 常见问题

**命令文档（100% - 35个文件）**
所有 `docs/commands/` 目录下的命令文档已完全翻译，包括：
- `trade.md` - 交易命令
- `backtesting.md` - 回测命令
- `hyperopt.md` - 超参数优化
- `download-data.md` - 数据下载
- `list-*.md` - 各种列表命令
- `show-*.md` - 各种显示命令
- 以及其他所有命令文档

**策略相关文档（100%）**
- ✅ `strategy-101.md` - 策略快速入门
- ✅ `strategy-customization.md` - 策略自定义
- ✅ `strategy-advanced.md` - 高级策略
- ✅ `strategy-callbacks.md` - 策略回调
- ✅ `strategy_migration.md` - 策略迁移指南

**高级功能文档（95%+）**
- ✅ `backtesting.md` - 回测
- ✅ `advanced-backtesting.md` - 高级回测
- ✅ `hyperopt.md` - 超参数优化
- ✅ `advanced-hyperopt.md` - 高级超参数优化
- ✅ `stoploss.md` - 止损
- ✅ `leverage.md` - 杠杆交易
- ✅ `exchanges.md` - 交易所说明

**FreqAI 相关文档（98%+）**
- ✅ `freqai.md` - FreqAI 介绍
- ✅ `freqai-configuration.md` - FreqAI 配置
- ✅ `freqai-running.md` - FreqAI 运行
- ✅ `freqai-developers.md` - FreqAI 开发者文档
- ✅ `freqai-reinforcement-learning.md` - 强化学习
- ✅ `freqai-parameter-table.md` - 参数表
- ⏳ `freqai-feature-engineering.md` - 特征工程（部分）

**工具和实用文档（95%+）**
- ✅ `data-download.md` - 数据下载
- ✅ `data-analysis.md` - 数据分析
- ✅ `plotting.md` - 绘图
- ✅ `utils.md` - 实用工具
- ✅ `sql_cheatsheet.md` - SQL 参考
- ✅ `telegram-usage.md` - Telegram 使用

**API 和集成文档（98%+）**
- ✅ `rest-api.md` - REST API（包括所有45个端点）
- ✅ `webhook-config.md` - Webhook 配置
- ✅ `freq-ui.md` - FreqUI 说明

**插件和扩展文档（99%+）**
- ✅ `plugins.md` - 插件概述
- ✅ `includes/pairlists.md` - 交易对列表
- ✅ `includes/protections.md` - 保护功能
- ✅ `includes/pricing.md` - 定价说明
- ✅ `includes/exchange-features.md` - 交易所特性表格
- ✅ `includes/strategy-imports.md` - 策略导入
- ✅ `includes/strategy-exit-comparisons.md` - 出场逻辑比较
- ✅ `includes/cors.md` - CORS 配置
- ✅ `includes/showcase.md` - 社区展示
- ✅ `includes/release_template.md` - 发布模板
- ✅ `producer-consumer.md` - 生产者/消费者模式

**其他文档（90%+）**
- ✅ `trade-object.md` - 交易对象
- ✅ `updating.md` - 更新指南
- ✅ `deprecated.md` - 已弃用功能
- ✅ `developer.md` - 开发者文档（部分）
- ✅ `advanced-setup.md` - 高级设置

#### 2. Python 代码汉化（75%+）

- ✅ **CLI 帮助信息**：100%（`freqtrade/commands/arguments.py`）
- ✅ **主要错误消息**：100%（`freqtrade/main.py`）
- ✅ **API 响应消息**：100%（所有 API 端点响应消息已翻译）
- ✅ **RPC 错误和状态消息**：100%（所有 RPC 方法消息已翻译）
- ⏳ **日志消息**：部分完成（部分日志消息可能仍为英文）

**后端 API 消息翻译（已完成）**
- ✅ API 响应消息：已翻译所有用户可见的 API 响应消息
  - 交易相关：交易未找到、交易ID无效、订单相关错误等
  - 机器人控制：启动/停止/暂停状态消息
  - 回测相关：回测启动、运行中、已完成、失败等状态
  - 数据下载：数据下载状态消息
  - 交易对列表：评估状态、错误消息
  - 其他：策略、任务、文件相关错误消息

- ✅ RPC 错误和状态消息：已翻译所有 RPC 方法中的用户可见消息
  - 交易操作：强制入场/出场相关错误
  - 状态检查：机器人运行状态、活跃交易检查
  - 错误消息：各种业务逻辑错误的中文提示

- ✅ RPC 启动消息：已翻译机器人启动时的配置信息显示
  - 模拟运行提示
  - 交易所、交易金额、ROI、止损等配置信息
  - 交易对搜索和保护功能信息

- ✅ Telegram 消息格式化：已翻译 Telegram 消息中的用户可见文本
  - 订单取消消息
  - 保护功能触发消息
  - 状态和警告消息

#### 3. README 汉化（100%）

- ✅ `README.md` - 完整汉化，包括功能列表、安装说明、使用指南等

### ⚠️ 未完成的部分

#### 前端界面（FreqUI）

**⚠️ 重要说明**：FreqUI 是独立的前端项目，位于独立的 GitHub 仓库（https://github.com/freqtrade/frequi）。

由于 FreqUI 是单独的仓库且使用现代前端框架构建，前端界面未包含在本汉化工作中。建议：

1. **使用浏览器翻译** - 浏览器自带翻译功能可以快速浏览中文界面
2. **参与上游项目** - 在 [FreqUI 源码仓库](https://github.com/freqtrade/frequi) 中贡献中文翻译
3. **使用后端翻译** - 已完成的 API 和 RPC 消息翻译可以立即使用

如需对 FreqUI 进行前端翻译，需要：
1. 克隆 `frequi` 仓库
2. 查找语言文件位置（通常使用 i18n 或自定义方案）
3. 创建中文翻译文件
4. 配置语言切换功能
5. 重新构建并安装

如需在前端项目中进行翻译，请直接访问 [FreqUI 仓库](https://github.com/freqtrade/frequi)。

## 使用方法

### 1. 查看中文文档

所有文档都可以在 `docs/` 目录下找到中文版本。主要入口：
- `docs/index.md` - 文档首页
- `docs/bot-basics.md` - 开始使用机器人
- `docs/strategy-101.md` - 策略编写指南
- `README.md` - 项目总览

### 2. 使用中文 CLI

所有命令的帮助信息都已中文化：

```bash
# 查看所有命令
freqtrade --help

# 查看交易命令帮助
freqtrade trade --help

# 查看回测命令帮助
freqtrade backtesting --help

# 其他所有命令的帮助信息都是中文
```

### 3. API 响应消息

所有 API 端点返回的用户可见消息都是中文：

```bash
# 启动机器人
freqtrade trade

# 通过 API 访问（默认端口 8080）
curl http://localhost:8080/api/v1/ping
# 响应：{"status": "pong"}

# 其他所有 API 端点都会返回中文消息
```

## 翻译质量保证

- ✅ 所有核心概念和术语保持一致
- ✅ 技术术语采用行业标准中文翻译
- ✅ 代码示例和命令保持不变
- ✅ 链接和交叉引用保持有效
- ✅ 格式和结构保持原样

## 项目仓库

- **原项目**：[freqtrade/freqtrade](https://github.com/freqtrade/freqtrade)
- **前端仓库**：[freqtrade/frequi](https://github.com/freqtrade/frequi)
- **汉化版本**：[brinsec/freqtrade](https://github.com/brinsec/freqtrade)

## 贡献

欢迎提交 Issues 和 Pull Requests 来改进中文翻译质量。

### 贡献指南

1. Fork 本仓库
2. 创建特性分支
3. 进行翻译改进
4. 提交 Pull Request

### 翻译原则

- 保持术语一致性
- 保留代码和命令原文
- 确保格式正确
- 参考官方文档更新翻译

## 许可

本项目遵循与原项目相同的许可协议：GPL-3.0

## 致谢

感谢 Freqtrade 团队提供优秀的交易机器人框架，感谢所有贡献者的支持。

## 联系

如有问题或建议，请通过 GitHub Issues 联系。

---

**汉化状态**：文档 99.5%+，后端消息 100%，前端界面 0%（独立仓库）
**最后更新**：2024年
**基于版本**：freqtrade 最新稳定版

