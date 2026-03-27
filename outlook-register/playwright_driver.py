from __future__ import annotations

import logging
from typing import Optional, Tuple
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, Browser


logger = logging.getLogger(__name__)


def launch_browser(
    playwright: Playwright,
    browser_path: Optional[str],
    proxy: Optional[str],
    headless: bool,
    locale: str,
) -> Browser:
    chromium = playwright.chromium
    launch_kwargs = {
        "headless": headless,
        "args": [f"--lang={locale}"],
    }
    if browser_path:
        launch_kwargs["executable_path"] = browser_path
    if proxy:
        launch_kwargs["proxy"] = {"server": proxy, "bypass": "localhost"}
    return chromium.launch(**launch_kwargs)


def open_browser(
    browser_path: Optional[str],
    proxy: Optional[str],
    headless: bool,
    locale: str,
) -> Tuple[Browser, Playwright]:
    p = sync_playwright().start()
    browser = launch_browser(p, browser_path=browser_path, proxy=proxy, headless=headless, locale=locale)
    return browser, p


def close_browser(browser: Browser, playwright: Playwright) -> None:
    browser.close()
    playwright.stop()
