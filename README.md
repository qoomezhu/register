# Register

项目汇总：

- `openai-register/`：OpenAI 自动注册脚本（已统一为 `uv` 管理，详见目录内 README）
- `grok-register/`：Grok (x.ai) 注册机（已统一为 `uv` 管理，详见目录内 README）
- `exa-register/`：Exa 自动注册脚本（已统一为 `uv` 管理，详见目录内 README）
- `qwen-register/`：Qwen 自动注册脚本（已使用 `uv` 管理，详见目录内 README）
- `tavily-register/`：Tavily 自动注册脚本（已使用 `uv` 管理，目前不可用，详见目录内 README）

## 统一使用方式

现在各子项目都建议使用 `uv` 管理依赖与运行：

```bash
cd <项目目录>
uv sync
uv run python <脚本名>.py
```

其中 `openai-register/` 的 CPA 清理相关功能需要额外可选依赖：

```bash
cd openai-register
uv sync --extra cpa
```

### 📢 关注我的频道

分享有趣的技术原理、实用玩法和产品使用体验，欢迎关注：

[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@MasterAlanLab)
[![Bilibili](https://img.shields.io/badge/Bilibili-00A1D6?style=for-the-badge&logo=bilibili&logoColor=white)](https://space.bilibili.com/3691004225914941)
[![Douyin](https://img.shields.io/badge/Douyin-000000?style=for-the-badge&logo=tiktok&logoColor=white)](https://v.douyin.com/LzR5Sns8mQU)
[![Kuaishou](https://img.shields.io/badge/Kuaishou-FF6600?style=for-the-badge&logo=video&logoColor=white)](https://www.kuaishou.com/profile/3x77ra8rcg7fpne)
[![Telegram](https://img.shields.io/badge/Telegram-0088CC?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/MasterAlanLab_Channel)

### 🔧 资源推荐
- [YesCaptcha](https://yescaptcha.com/i/tlkF6o)（自动验证码识别工具）
- [IPFoxy](https://www.ipfoxy.com/invite/masteralan)（IP 代理服务）

### ⚠️ 重要提示
- Tavily 官方目前已关闭邮箱注册，原有注册机目前不可用，后续更新请关注上方频道

### 💬 交流与反馈
- TG 频道：https://t.me/MasterAlanLab
- 商务合作：masteralanlab@gmail.com

如果对你有帮助，记得点个 ⭐ 支持一下！
