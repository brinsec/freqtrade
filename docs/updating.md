# 如何更新

要更新您的 freqtrade 安装，请使用以下方法之一，对应于您的安装方法。

!!! Note "跟踪更改"
    破坏性更改/更改的行为将在随每次发布发布的更改日志中记录。
    对于 develop 分支，请关注 PR 以避免被更改所惊讶。

## Docker

!!! Note "使用 `master` 镜像的传统安装"
    我们正在将发布镜像从 master 切换到 stable - 请调整您的 docker 文件并将 `freqtradeorg/freqtrade:master` 替换为 `freqtradeorg/freqtrade:stable`

``` bash
docker compose pull
docker compose up -d
```

## 通过安装脚本安装

``` bash
./setup.sh --update
```

!!! Note "注意"
    确保在禁用虚拟环境的情况下运行此命令！

## 普通原生安装

请确保您也更新依赖项 - 否则可能会在您没有注意到的情况下出现问题。

``` bash
git pull
pip install -U -r requirements.txt
pip install -e .

# 确保 freqUI 是最新版本
freqtrade install-ui 
```

### 更新问题

更新问题通常来自缺少依赖项（您没有遵循上述说明）- 或来自更新的依赖项，这些依赖项安装失败（例如 TA-lib）。
请参阅相应的安装部分（下面链接的常见问题）
