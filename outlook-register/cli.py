from __future__ import annotations

import argparse
import logging
from pathlib import Path

from config import Settings, load_settings
from runner import run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Outlook Register")
    parser.add_argument("--config", type=Path, default=Path("config.json"), help="配置文件路径")
    parser.add_argument("--headless", action="store_true", help="启用无头模式")
    parser.add_argument("--proxy", type=str, help="代理地址，例如 http://127.0.0.1:7890")
    parser.add_argument("--concurrent", type=int, help="并发数")
    parser.add_argument("--max-tasks", type=int, help="最大任务数")
    parser.add_argument("--results-dir", type=Path, help="结果输出目录")
    parser.add_argument("--bot-wait", type=float, help="防机器人等待时间（秒）")
    parser.add_argument("--max-captcha-retries", type=int, help="验证码最大重试次数")
    parser.add_argument("--browser-path", type=str, help="浏览器可执行文件路径")
    parser.add_argument("--oauth2", action="store_true", help="启用 OAuth2 并获取 token")
    parser.add_argument("--client-id", type=str, help="OAuth2 client_id")
    parser.add_argument("--redirect-url", type=str, help="OAuth2 redirect_url")
    parser.add_argument("--scopes", type=str, nargs="*", help="OAuth2 scopes 列表")
    parser.add_argument("--log-level", type=str, default=None, help="日志级别，例如 INFO/DEBUG")
    parser.add_argument("--log-file", type=Path, default=None, help="日志文件输出路径，可选")
    parser.add_argument("--locale", type=str, default=None, help="浏览器 locale，默认 zh-CN")
    return parser


def parse_args(argv: list[str] | None = None) -> tuple[Settings, Path | None]:
    parser = build_parser()
    args = parser.parse_args(argv)

    overrides = {
        "browser_path": args.browser_path,
        "proxy": args.proxy,
        "concurrent_flows": args.concurrent,
        "max_tasks": args.max_tasks,
        "results_dir": args.results_dir,
        "bot_protection_wait": args.bot_wait,
        "max_captcha_retries": args.max_captcha_retries,
        "enable_oauth2": args.oauth2,
        "client_id": args.client_id,
        "redirect_url": args.redirect_url,
        "scopes": args.scopes,
        "headless": args.headless,
        "log_level": args.log_level,
        "locale": args.locale,
    }

    settings = load_settings(config_path=args.config, overrides=overrides)
    return settings, args.log_file


def main(argv: list[str] | None = None) -> None:
    settings, log_file = parse_args(argv)
    logging.getLogger(__name__).debug("Using settings: %s", settings)
    run(settings, log_file=log_file)


if __name__ == "__main__":
    main()
