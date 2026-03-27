from __future__ import annotations

import base64
import hashlib
import json
import logging
import secrets
import string
from datetime import datetime
from typing import Optional, Tuple
from urllib.parse import parse_qs, quote

import requests
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


def generate_code_verifier(length: int = 128) -> str:
    alphabet = string.ascii_letters + string.digits + "-._~"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_code_challenge(code_verifier: str) -> str:
    sha256_hash = hashlib.sha256(code_verifier.encode()).digest()
    return base64.urlsafe_b64encode(sha256_hash).decode().rstrip("=")


def handle_oauth2_form(page: Page, email: str) -> None:
    try:
        page.locator('[name="loginfmt"]').fill(f"{email}@outlook.com", timeout=20000)
        page.locator('#idSIButton9').click(timeout=7000)
        page.locator('[data-testid="appConsentPrimaryButton"]').click(timeout=20000)
    except Exception as exc:  # noqa: BLE001
        logger.debug("handle_oauth2_form ignored error: %s", exc)


def build_proxy(proxy: Optional[str]) -> Optional[dict]:
    if not proxy:
        return None
    return {"http": proxy, "https": proxy}


def get_access_token(
    page: Page,
    email: str,
    client_id: str,
    redirect_url: str,
    scopes: list[str],
    proxy: Optional[str] = None,
) -> Tuple[bool, Optional[str], Optional[str], Optional[float]]:
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    scope = " ".join(scopes)
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_url,
        "scope": scope,
        "response_mode": "query",
        "prompt": "select_account",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    try:
        page.wait_for_timeout(250)
        url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?" + "&".join(
            f"{k}={quote(v)}" for k, v in params.items()
        )
        page.goto(url)
    except Exception as exc:  # noqa: BLE001
        logger.error("OAuth2 navigation failed: %s", exc)
        return False, None, None, None

    with page.expect_response(lambda response: redirect_url in response.url, timeout=50000) as response_info:
        handle_oauth2_form(page, email)
        response = response_info.value
        callback_url = response.url

    if "code=" not in callback_url:
        logger.error("Authorization failed: no code in callback URL")
        return False, None, None, None

    auth_code = parse_qs(callback_url.split("?")[1])["code"][0]

    token_data = {
        "client_id": client_id,
        "code": auth_code,
        "redirect_uri": redirect_url,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
        "scope": scope,
    }

    try:
        response = requests.post(
            "https://login.microsoftonline.com/common/oauth2/v2.0/token",
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            proxies=build_proxy(proxy),
            timeout=30,
        )
        response.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        logger.error("Token request failed: %s", exc)
        return False, None, None, None

    payload = response.json()
    if "refresh_token" not in payload:
        logger.error("Token response missing refresh_token: %s", json.dumps(payload, ensure_ascii=False))
        return False, None, None, None

    refresh_token = payload["refresh_token"]
    access_token = payload.get("access_token", "")
    expire_at = datetime.now().timestamp() + payload.get("expires_in", 0)
    return True, refresh_token, access_token, expire_at
