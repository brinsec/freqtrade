# Windows 安装

我们**强烈**建议 Windows 用户使用 [Docker](docker_quickstart.md)，因为这将更加容易和顺畅（也更安全）。

如果不可能，请尝试使用 Windows Linux 子系统（WSL）- Ubuntu 说明应该可以工作。
否则，请按照下面的说明操作。

所有说明都假定已安装并可用 python 3.11+。

## 克隆 git 仓库

首先通过运行以下命令克隆仓库：

``` powershell
git clone https://github.com/freqtrade/freqtrade.git
```

现在，选择您的安装方法，通过脚本自动安装（推荐）或按照相应说明手动安装。

## 自动安装 freqtrade

### 运行安装脚本

脚本将询问您一些问题以确定应安装哪些部分。

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass
cd freqtrade
. .\setup.ps1
```

## 手动安装 freqtrade

!!! Note "64 位 Python 版本"
    请确保使用 64 位 Windows 和 64 位 Python，以避免由于 32 位应用程序在 Windows 下的内存限制而导致回测或超参数优化问题。
    32 位 python 版本在 Windows 下不再受支持。

!!! Hint "提示"
    在 Windows 下使用 [Anaconda 发行版](https://www.anaconda.com/distribution/) 可以大大帮助解决安装问题。查看文档中的 [Anaconda 安装部分](installation.md#installation-with-conda) 了解更多信息。

### Windows 安装期间的错误

``` bash
error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": http://landinghub.visualstudio.com/visual-cpp-build-tools
```

不幸的是，许多需要编译的包不提供预构建的 wheel。因此，必须为您的 python 环境安装并提供 C/C++ 编译器。

您可以从[这里](https://visualstudio.microsoft.com/visual-cpp-build-tools/)下载 Visual C++ 构建工具，并在其默认配置中安装"使用 C++ 的桌面开发"。不幸的是，这是一个大型下载/依赖项，因此您可能想首先考虑 WSL2 或 [docker compose](docker_quickstart.md)。

![Windows installation](assets/windows_install.png)

---
