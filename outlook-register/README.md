# outlook-register

Outlook 自动注册脚本，基于 Playwright 驱动浏览器完成 Microsoft Outlook 邮箱注册；可选启用 OAuth2，注册成功后进一步获取 refresh token / access token 并写入结果文件。

## 环境要求
- Python 3.10+
- 已安装 `uv`
- 已安装可执行浏览器（推荐 Chromium）

## 安装
```bash
cd outlook-register
uv sync
# 首次需要安装浏览器内核（Chromium）
uv run playwright install chromium
```

## 配置
默认读取当前目录的 `config.json`，也可以用 `--config` 指定路径。

最小配置示例：
```json
{
  "proxy": "http://127.0.0.1:7890",
  "concurrent_flows": 5,
  "max_tasks": 50,
  "headless": false,
  "results_dir": "accounts",
  "log_level": "INFO",
  "locale": "zh-CN"
}
```

如需注册后自动获取 OAuth2 token，额外配置：
```json
{
  "enable_oauth2": true,
  "client_id": "YOUR_CLIENT_ID",
  "redirect_url": "YOUR_REDIRECT_URL",
  "scopes": [
    "offline_access",
    "https://graph.microsoft.com/Mail.ReadWrite",
    "https://graph.microsoft.com/Mail.Send",
    "https://graph.microsoft.com/User.Read"
  ]
}
```

### 主要配置项说明
- `browser_path`：自定义浏览器可执行文件路径，可不填
- `proxy`：代理地址，例如 `http://127.0.0.1:7890`
- `bot_protection_wait`：防机器人等待时间（秒），默认 `12.0`
- `max_captcha_retries`：验证码最大重试次数，默认 `2`
- `concurrent_flows`：并发数，默认 `5`
- `max_tasks`：总任务数，默认 `50`
- `enable_oauth2`：是否启用 OAuth2 token 获取，默认 `false`
- `client_id`：OAuth2 应用 `client_id`
- `redirect_url`：OAuth2 回调地址
- `scopes`：OAuth2 scopes 列表
- `headless`：是否无头运行，默认 `false`
- `locale`：浏览器语言，默认 `zh-CN`
- `results_dir`：结果输出目录，默认 `accounts`
- `log_level`：日志级别，默认 `INFO`

## 运行
### 基础注册
```bash
cd outlook-register
uv run python cli.py --config config.json
```

### 常用参数示例
启用无头模式：
```bash
uv run python cli.py --config config.json --headless
```

临时覆盖代理、并发和任务数：
```bash
uv run python cli.py \
  --config config.json \
  --proxy http://127.0.0.1:7890 \
  --concurrent 3 \
  --max-tasks 10
```

启用 OAuth2：
```bash
uv run python cli.py \
  --config config.json \
  --oauth2 \
  --client-id YOUR_CLIENT_ID \
  --redirect-url YOUR_REDIRECT_URL
```

输出日志到文件：
```bash
uv run python cli.py \
  --config config.json \
  --log-file run.log
```

## 输出
默认输出到 `accounts/` 目录：
- `unlogged_email.txt`：注册成功、未启用 OAuth2 的账号
- `logged_email.txt`：注册成功且已拿到 OAuth2 token 的账号
- `outlook_token.txt`：OAuth2 token 明细（格式：`邮箱@outlook.com---密码---refresh_token---access_token---过期时间戳`）

## 工作流摘要
1. 启动浏览器并打开 Outlook 注册页
2. 自动生成邮箱名前缀和强密码
3. 填写出生日期、姓名等资料
4. 处理页面中的风控/验证码流程
5. 注册成功后写入账号结果
6. 若启用 OAuth2，则继续授权并换取 token 后写入文件

## 常见问题
- 直接 `python cli.py` 报相对导入错误：现在入口统一用 `uv run python cli.py`
- `ModuleNotFoundError: No module named 'playwright'`：先执行 `uv sync`，再执行 `uv run playwright install chromium`
- 浏览器启动失败：确保已安装 Chromium，或通过 `browser_path` 指定本机浏览器路径
- 注册页进不去 / 频繁异常活动：多半是代理质量问题，换 IP 再试
- OAuth2 没拿到 token：检查 `client_id`、`redirect_url`、`scopes` 是否正确，以及代理是否稳定
