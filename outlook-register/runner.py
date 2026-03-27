from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

from playwright.sync_api import Page

from config import Settings, ensure_results_dir
from logging_setup import setup_logging
from oauth import get_access_token
from playwright_driver import close_browser, open_browser
from register import perform_registration
from utils import pick_email_and_password

logger = logging.getLogger(__name__)


def save_account(results_dir: Path, filename: str, email: str, password: str) -> None:
    path = results_dir / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(f"{email}@outlook.com: {password}\n")


def save_tokens(results_dir: Path, email: str, password: str, refresh_token: str, access_token: str, expire_at: float) -> None:
    path = results_dir / "outlook_token.txt"
    with path.open("a", encoding="utf-8") as f:
        f.write(f"{email}@outlook.com---{password}---{refresh_token}---{access_token}---{expire_at}\n")


def process_single_flow(settings: Settings) -> bool:
    browser = None
    playwright = None
    try:
        browser, playwright = open_browser(
            browser_path=settings.browser_path,
            proxy=settings.proxy,
            headless=settings.headless,
            locale=settings.locale,
        )
        page: Page = browser.new_page()

        email, password = pick_email_and_password()
        success = perform_registration(
            page=page,
            email=email,
            password=password,
            bot_protection_wait_ms=settings.bot_protection_wait * 1000,
            max_captcha_retries=settings.max_captcha_retries,
        )

        if not success:
            return False

        if not settings.enable_oauth2:
            save_account(settings.results_dir, "unlogged_email.txt", email, password)
            return True

        ok, refresh_token, access_token, expire_at = get_access_token(
            page=page,
            email=email,
            client_id=settings.client_id,
            redirect_url=settings.redirect_url,
            scopes=settings.scopes,
            proxy=settings.proxy,
        )
        if ok and refresh_token and access_token and expire_at:
            save_account(settings.results_dir, "logged_email.txt", email, password)
            save_tokens(settings.results_dir, email, password, refresh_token, access_token, expire_at)
            return True
        return False

    except Exception as exc:  # noqa: BLE001
        logger.error("任务失败: %s", exc)
        return False
    finally:
        if browser and playwright:
            close_browser(browser, playwright)


def run(settings: Settings, log_file: Optional[Path] = None) -> None:
    setup_logging(level=settings.log_level, log_file=log_file)
    ensure_results_dir(settings)

    task_counter = 0
    succeeded_tasks = 0
    failed_tasks = 0

    with ThreadPoolExecutor(max_workers=settings.concurrent_flows) as executor:
        running_futures = set()

        while task_counter < settings.max_tasks or len(running_futures) > 0:
            done_futures = {f for f in running_futures if f.done()}
            for future in done_futures:
                try:
                    result = future.result()
                    if result:
                        succeeded_tasks += 1
                    else:
                        failed_tasks += 1
                except Exception as exc:  # noqa: BLE001
                    failed_tasks += 1
                    logger.error("任务异常: %s", exc)
                running_futures.remove(future)

            while len(running_futures) < settings.concurrent_flows and task_counter < settings.max_tasks:
                time.sleep(0.2)
                future = executor.submit(process_single_flow, settings)
                running_futures.add(future)
                task_counter += 1

            time.sleep(0.5)

    logger.info("完成 %s 个任务，成功 %s，失败 %s", settings.max_tasks, succeeded_tasks, failed_tasks)
