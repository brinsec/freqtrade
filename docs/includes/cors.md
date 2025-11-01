## CORS

整个部分仅在跨域情况下需要（您在 `localhost:8081`、`localhost:8082` 等上运行多个机器人 API，并希望将它们合并到一个 FreqUI 实例中）。

??? info "技术说明"
    所有基于 Web 的前端都受 [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)（跨域资源共享）约束。
    由于大多数对 Freqtrade API 的请求必须经过身份验证，适当的 CORS 策略是避免安全问题的关键。
    此外，标准不允许对带凭证的请求使用 `*` CORS 策略，因此必须适当设置此设置。

用户可以通过 `CORS_origins` 配置设置允许来自不同源 URL 对机器人 API 的访问。
它由允许使用机器人 API 资源的允许 URL 列表组成。

假设您的应用程序部署为 `https://frequi.freqtrade.io/home/` - 这意味着需要以下配置：

```jsonc
{
    //...
    "jwt_secret_key": "somethingrandom",
    "CORS_origins": ["https://frequi.freqtrade.io"],
    //...
}
```

在以下（非常常见的）情况下，FreqUI 可在 `http://localhost:8080/trade` 访问（这是您在导航到 freqUI 时在导航栏中看到的）。
![freqUI url](assets/frequi_url.png)

此情况的正确配置是 `http://localhost:8080` - URL 的主要部分，包括端口。

```jsonc
{
    //...
    "jwt_secret_key": "somethingrandom",
    "CORS_origins": ["http://localhost:8080"],
    //...
}
```

!!! Tip "尾部斜杠"
    `CORS_origins` 配置中不允许尾部斜杠（例如 `"http://localhots:8080/"`）。
    这样的配置将不会生效，并且 cors 错误将仍然存在。

!!! Note "注意"
    我们强烈建议将 `jwt_secret_key` 设置为随机值，并且只有您自己知道，以避免对您的机器人进行未经授权的访问。
