![freqai-logo](assets/freqai_doc_logo.svg)

# FreqAI

## 介绍

FreqAI 是一种软件，旨在自动化与训练预测性机器学习模型相关的各种任务，以根据一组输入信号生成市场预测。总的来说，FreqAI 旨在成为一个沙盒，用于在实时数据上轻松部署强大的机器学习库（[详细信息](#freqai-position-in-open-source-machine-learning-landscape)）。

!!! Note "注意"
    FreqAI 是并且将永远是一个非营利、开源项目。FreqAI *没有*加密代币，FreqAI *不*出售信号，并且 FreqAI 除了当前的 [freqtrade 文档](https://www.freqtrade.io/en/latest/freqai/) 之外没有其他域名。

功能包括：

* **自适应重训练** - 在[实盘部署](freqai-running.md#live-deployments)期间重训练模型，以监督方式自适应市场
* **快速特征工程** - 基于简单的用户创建策略创建大型丰富的[特征集](freqai-feature-engineering.md#feature-engineering)（10k+ 特征）
* **高性能** - 线程允许在单独的线程（或 GPU，如果可用）上进行自适应模型重训练，与模型推理（预测）和机器人交易操作分离。最新的模型和数据保存在 RAM 中以进行快速推理
* **真实回测** - 使用自动重训练的[回测模块](freqai-running.md#backtesting)在历史数据上模拟自适应训练
* **可扩展性** - 通用且强大的架构允许合并 Python 中可用的任何[机器学习库/方法](freqai-configuration.md#using-different-prediction-models)。目前提供了八个示例，包括分类器、回归器和卷积神经网络
* **智能异常值移除** - 使用各种[异常检测技术](freqai-feature-engineering.md#outlier-detection)从训练和预测数据集中移除异常值
* **崩溃恢复** - 将训练好的模型存储到磁盘，以便从崩溃中快速轻松地重新加载，并为持续模拟/实盘运行[清除过时文件](freqai-running.md#purging-old-model-data)
* **自动数据规范化** - 以智能且统计安全的方式[规范化数据](freqai-feature-engineering.md#building-the-data-pipeline)
* **自动数据下载** - 计算数据下载的时间范围并更新历史数据（在实盘部署中）
* **传入数据清理** - 在训练和模型推理之前安全地处理 NaNs
* **降维** - 通过[主成分分析](freqai-feature-engineering.md#data-dimensionality-reduction-with-principal-component-analysis)减少训练数据的大小
* **部署机器人舰队** - 设置一个机器人训练模型，同时一组[消费者](producer-consumer.md)使用信号。

## 快速开始

快速测试 FreqAI 的最简单方法是在模拟模式下使用以下命令运行：

```bash
freqtrade trade --config config_examples/config_freqai.example.json --strategy FreqaiExampleStrategy --freqaimodel LightGBMRegressor --strategy-path freqtrade/templates
```

您将看到自动数据下载的启动过程，然后是同时训练和交易。

!!! Danger "不用于生产"
    随 Freqtrade 源代码提供的示例策略旨在展示/测试各种 FreqAI 功能。它也设计为在小型计算机上运行，以便可以用作开发人员和用户之间的基准。它*不*设计用于生产。

可以用作起点的示例策略、预测模型和配置可以在
`freqtrade/templates/FreqaiExampleStrategy.py`、`freqtrade/freqai/prediction_models/LightGBMRegressor.py` 和
`config_examples/config_freqai.example.json` 中找到。

## 一般方法

您为 FreqAI 提供一组自定义*基础指标*（与[典型的 Freqtrade 策略](strategy-customization.md)中的方式相同）以及目标值（*标签*）。对于白名单中的每个交易对，FreqAI 训练一个模型，根据自定义指标的输入预测目标值。然后定期重训练模型，以预先确定的频率适应市场条件。FreqAI 提供了回测策略（通过在历史数据上定期重训练来模拟现实）和部署模拟/实盘运行的能力。在模拟/实盘条件下，FreqAI 可以设置为在后台线程中持续重训练，以尽可能保持模型最新。

算法的概述，解释数据处理管道和模型使用，如下所示。

![freqai-algo](assets/freqai_algo.jpg)

### 重要的机器学习词汇

**特征（Features）** - 基于历史数据的参数，模型在这些参数上进行训练。单个蜡烛的所有特征存储为向量。在 FreqAI 中，您可以从策略中构造的任何内容构建特征数据集。

**标签（Labels）** - 模型训练的目标值。每个特征向量与您在策略中定义的单个标签关联。这些标签有意向前看，是您训练模型能够预测的内容。

**训练（Training）** - "教"模型将特征集与相关标签匹配的过程。不同类型的模型以不同的方式"学习"，这意味着对于一个特定应用，一个可能比另一个更好。有关 FreqAI 中已实现的不同模型的更多信息可以在[这里](freqai-configuration.md#using-different-prediction-models)找到。

**训练数据（Train data）** - 特征数据集的子集，在训练期间提供给模型以"教"模型如何预测目标。此数据直接影响模型中的权重连接。

**测试数据（Test data）** - 用于在训练后评估模型性能的特征数据集的子集。此数据不影响模型内的节点权重。

**推理（Inferencing）** - 向训练好的模型提供新的未见数据，模型将对其进行预测的过程。 

## 安装先决条件

正常的 Freqtrade 安装过程会询问您是否要安装 FreqAI 依赖项。如果您希望使用 FreqAI，应该回答"是"。如果您没有回答是，可以在安装后使用以下命令手动安装这些依赖项：

``` bash
pip install -r requirements-freqai.txt
```

!!! Note "注意"
    Catboost 不会在低功耗 ARM 设备（树莓派）上安装，因为它不为该平台提供 wheel。

### 与 docker 一起使用

如果您使用 docker，带有 FreqAI 依赖项的专用标签可作为 `:freqai` 使用。因此 - 您可以将 docker compose 文件中的镜像行替换为 `image: freqtradeorg/freqtrade:stable_freqai`。此镜像包含常规 FreqAI 依赖项。与原生安装类似，Catboost 在基于 ARM 的设备上将不可用。如果您想使用 PyTorch 或强化学习，应该使用 torch 或 RL 标签，`image: freqtradeorg/freqtrade:stable_freqaitorch`、`image: freqtradeorg/freqtrade:stable_freqairl`。

!!! Note "docker-compose-freqai.yml"
    我们确实在 `docker/docker-compose-freqai.yml` 中为此提供了一个明确的 docker-compose 文件 - 可以通过 `docker compose -f docker/docker-compose-freqai.yml run ...` 使用 - 或者可以复制以替换原始 docker 文件。此 docker-compose 文件还包含一个（禁用的）部分，以在 docker 容器内启用 GPU 资源。这显然假设系统具有可用的 GPU 资源。

### FreqAI 在开源机器学习领域中的位置

预测基于混沌时间序列的系统（如股票/加密货币市场）需要一套广泛的工具，用于测试各种假设。幸运的是，强大的机器学习库（例如 `scikit-learn`）的近期成熟为广泛的研究可能性打开了大门。来自不同领域的科学家现在可以轻松地在大量已建立的机器学习算法上原型化他们的研究。同样，这些用户友好的库使"公民科学家"能够使用他们的基本 Python 技能进行数据探索。但是，在历史和实时混沌数据源上利用这些机器学习库可能在逻辑上困难且昂贵。此外，强大的数据收集、存储和处理提出了不同的挑战。[`FreqAI`](#freqai) 旨在提供一个通用且可扩展的开源框架，用于市场预测的自适应建模的实时部署。`FreqAI` 框架实际上是丰富的开源机器学习库世界的沙盒。在 `FreqAI` 沙盒中，用户发现他们可以结合各种各样的第三方库来在免费的实时 24/7 混沌数据源（加密货币交易所数据）上测试创造性假设。 

### 引用 FreqAI

FreqAI [已发表在开源软件杂志](https://joss.theoj.org/papers/10.21105/joss.04864)上。如果您在研究中发现 FreqAI 有用，请使用以下引用：

```bibtex
@article{Caulk2022, 
    doi = {10.21105/joss.04864},
    url = {https://doi.org/10.21105/joss.04864},
    year = {2022}, publisher = {The Open Journal},
    volume = {7}, number = {80}, pages = {4864},
    author = {Robert A. Caulk and Elin Törnquist and Matthias Voppichler and Andrew R. Lawless and Ryan McMullan and Wagner Costa Santos and Timothy C. Pogue and Johan van der Vlugt and Stefan P. Gehring and Pascal Schmidt},
    title = {FreqAI: generalizing adaptive modeling for chaotic time-series market forecasts},
    journal = {Journal of Open Source Software} } 
```

## 常见陷阱

FreqAI 不能与动态 `VolumePairlists`（或任何动态添加和删除交易对的交易对列表过滤器）结合使用。
这是出于性能原因 - FreqAI 依赖于进行快速预测/重训练。为了有效地做到这一点，
它需要在模拟/实盘实例开始时下载所有训练数据。FreqAI 自动存储并追加
新蜡烛以供将来重训练。这意味着如果由于成交量交易对列表而在模拟运行中稍后出现新交易对，它将没有准备好数据。但是，FreqAI 确实可以与 `ShufflePairlist` 或保持总交易对列表恒定（但根据成交量重新排序交易对）的 `VolumePairlist` 一起工作。

## 其他学习材料

这里我们编译了一些外部材料，提供对 FreqAI 各个组件的更深入了解：

- [实时正面交锋：使用 XGBoost 和 CatBoost 对金融市场数据进行自适应建模](https://emergentmethods.medium.com/real-time-head-to-head-adaptive-modeling-of-financial-market-data-using-xgboost-and-catboost-995a115a7495)
- [FreqAI - 从价格到预测](https://emergentmethods.medium.com/freqai-from-price-to-prediction-6fadac18b665)


## 支持

您可以在各种地方找到 FreqAI 的支持，包括 [Freqtrade discord](https://discord.gg/Jd8JYeWHc4)、专用的 [FreqAI discord](https://discord.gg/7AMWACmbjT) 以及 [github issues](https://github.com/freqtrade/freqtrade/issues)。

## 致谢

FreqAI 由一群个人开发，他们都为项目贡献了特定技能。

构思和软件开发：
Robert Caulk @robcaulk

理论头脑风暴和数据分析：
Elin Törnquist @th0rntwig

代码审查和软件架构头脑风暴：
@xmatthias

软件开发：
Wagner Costa @wagnercosta
Emre Suzen @aemr3
Timothy Pogue @wizrds

Beta 测试和错误报告：
Stefan Gehring @bloodhunter4rc, @longyu, Andrew Lawless @paranoidandy, Pascal Schmidt @smidelis, Ryan McMullan @smarmau, Juha Nykänen @suikula, Johan van der Vlugt @jooopiert, Richárd Józsa @richardjosza
