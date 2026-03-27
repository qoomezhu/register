from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


DEFAULT_CONFIG_PATH = Path("config.json")


@dataclass
class Settings:
    browser_path: Optional[str] = None
    proxy: Optional[str] = None
    bot_protection_wait: float = 12.0
    max_captcha_retries: int = 2
    concurrent_flows: int = 5
    max_tasks: int = 50
    enable_oauth2: bool = False
    client_id: str = ""
    redirect_url: str = ""
    scopes: List[str] = field(
        default_factory=lambda: [
            "offline_access",
            "https://graph.microsoft.com/Mail.ReadWrite",
            "https://graph.microsoft.com/Mail.Send",
            "https://graph.microsoft.com/User.Read",
        ]
    )
    headless: bool = False
    locale: str = "zh-CN"
    results_dir: Path = Path("accounts")
    log_level: str = "INFO"

    @staticmethod
    def from_file(path: Path) -> "Settings":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return Settings.from_dict(data)

    @staticmethod
    def from_dict(data: dict) -> "Settings":
        return Settings(
            browser_path=data.get("browser_path") or None,
            proxy=data.get("proxy") or None,
            bot_protection_wait=float(data.get("Bot_protection_wait", data.get("bot_protection_wait", 12.0))),
            max_captcha_retries=int(data.get("max_captcha_retries", 2)),
            concurrent_flows=int(data.get("concurrent_flows", 5)),
            max_tasks=int(data.get("max_tasks", 50)),
            enable_oauth2=bool(data.get("enable_oauth2", False)),
            client_id=data.get("client_id", ""),
            redirect_url=data.get("redirect_url", ""),
            scopes=data.get("Scopes") or data.get("scopes") or Settings().scopes,
            headless=bool(data.get("headless", False)),
            locale=data.get("locale", "zh-CN"),
            results_dir=Path(data.get("results_dir", "accounts")),
            log_level=str(data.get("log_level", "INFO")).upper(),
        )

    def to_dict(self) -> dict:
        return {
            "browser_path": self.browser_path,
            "proxy": self.proxy,
            "bot_protection_wait": self.bot_protection_wait,
            "max_captcha_retries": self.max_captcha_retries,
            "concurrent_flows": self.concurrent_flows,
            "max_tasks": self.max_tasks,
            "enable_oauth2": self.enable_oauth2,
            "client_id": self.client_id,
            "redirect_url": self.redirect_url,
            "scopes": self.scopes,
            "headless": self.headless,
            "locale": self.locale,
            "results_dir": str(self.results_dir),
            "log_level": self.log_level,
        }


def load_settings(config_path: Optional[Path] = None, overrides: Optional[dict] = None) -> Settings:
    path = config_path or DEFAULT_CONFIG_PATH
    base = Settings()
    if path.exists():
        base = Settings.from_file(path)

    overrides = overrides or {}
    merged = base.to_dict()
    merged.update({k: v for k, v in overrides.items() if v is not None})
    return Settings.from_dict(merged)


def ensure_results_dir(settings: Settings) -> Path:
    path = settings.results_dir
    path.mkdir(parents=True, exist_ok=True)
    return path
