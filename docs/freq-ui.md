# FreqUI

Freqtrade 提供了一个内置的 Web 服务器，可以服务于 [FreqUI](https://github.com/freqtrade/frequi)，即 freqtrade 前端。

默认情况下，UI 会作为安装的一部分自动安装（脚本、docker）。
freqUI 也可以通过使用 `freqtrade install-ui` 命令手动安装。
此命令也可用于将 freqUI 更新到新版本。

一旦机器人在交易/模拟运行模式下启动（使用 `freqtrade trade`）- UI 将在配置的 API 端口下可用（默认 `http://127.0.0.1:8080`）。

??? Note "想为 freqUI 做贡献？"
    开发者不应使用此方法，而应克隆相应的仓库，使用 [freqUI 仓库](https://github.com/freqtrade/frequi) 中描述的方法来获取 freqUI 的源代码。需要安装 node 才能构建前端。

!!! tip "freqUI 不是运行 freqtrade 所必需的"
    freqUI 是 freqtrade 的可选组件，运行机器人不需要它。
    它是一个可用于监控机器人并与之交互的前端 - 但 freqtrade 本身在没有它的情况下也能完美运行。

## 配置

FreqUI 没有自己的配置文件 - 但假设 [rest-api](rest-api.md) 的可用设置。
请参阅相应的文档页面以设置 freqUI

## UI

FreqUI 是一个现代化的响应式 Web 应用程序，可用于监控您的机器人并与之交互。

FreqUI 提供浅色和深色主题。
可以通过页面顶部的突出按钮轻松切换主题。
此页面上截图的主题将适应当前选中的文档主题，因此要查看深色（或浅色）版本，请切换文档的主题。

### 登录

下面的截图显示了 freqUI 的登录界面。

![FreqUI - login](assets/frequi-login-CORS.png#only-dark)
![FreqUI - login](assets/frequi-login-CORS-light.png#only-light)

!!! Hint "CORS"
    此截图中显示的 Cors 错误是由于 UI 运行在与 API 不同的端口上，并且 [CORS](#cors) 尚未正确设置。

### 交易视图

交易视图允许您可视化机器人正在进行的交易并与机器人交互。
在此页面上，您还可以通过启动和停止机器人来与之交互，以及 - 如果配置了 - 强制交易入场和出场。

![FreqUI - trade view](assets/freqUI-trade-pane-dark.png#only-dark)
![FreqUI - trade view](assets/freqUI-trade-pane-light.png#only-light)

### 图表配置器

FreqUI 图表可以通过策略中的 `plot_config` 配置对象（可以通过"from strategy"按钮加载）或通过 UI 进行配置。
可以创建多个图表配置并随意切换 - 允许灵活、不同的图表视图。

可以通过交易视图右上角的"Plot Configurator"（齿轮图标）按钮访问图表配置。

![FreqUI - plot configuration](assets/freqUI-plot-configurator-dark.png#only-dark)
![FreqUI - plot configuration](assets/freqUI-plot-configurator-light.png#only-light)

### 设置

可以通过访问设置页面来更改几个与 UI 相关的设置。

您可以更改的内容（其中包括）：

* UI 的时区
* 将未平仓交易可视化为 favicon（浏览器标签）的一部分
* 蜡烛图颜色（上涨/下跌 -> 红色/绿色）
* 启用/禁用应用内通知类型

![FreqUI - Settings view](assets/frequi-settings-dark.png#only-dark)
![FreqUI - Settings view](assets/frequi-settings-light.png#only-light)

## Web 服务器模式

当 freqtrade 在 [webserver 模式](utils.md#webserver-mode) 下启动（使用 `freqtrade webserver` 启动 freqtrade）时，Web 服务器将以特殊模式启动，允许使用其他功能，例如：

* 下载数据
* 测试交易对列表
* [回测策略](#backtesting)
* ...待扩展

### 回测

当 freqtrade 在 [webserver 模式](utils.md#webserver-mode) 下启动（使用 `freqtrade webserver` 启动 freqtrade）时，回测视图变为可用。
此视图允许您回测策略并可视化结果。

您还可以加载和可视化之前的回测结果，以及相互比较结果。

![FreqUI - Backtesting](assets/freqUI-backtesting-dark.png#only-dark)
![FreqUI - Backtesting](assets/freqUI-backtesting-light.png#only-light)


--8<-- "includes/cors.md"
