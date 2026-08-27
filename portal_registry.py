"""Validated, data-driven registry used by the public Streamlit portal."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse


REGISTRY_PATH = Path(__file__).resolve().with_name("portal_apps.json")
REQUIRED_FIELDS = ("name", "description", "url", "button")


def _is_allowed_streamlit_url(value: str) -> bool:
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    return parsed.scheme == "https" and host.endswith(".streamlit.app")


def load_portal_apps(path: Path | None = None) -> tuple[dict[str, str], ...]:
    registry_path = path or REGISTRY_PATH
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    raw_apps = payload.get("apps")
    if not isinstance(raw_apps, list) or not raw_apps:
        raise ValueError("portal_apps.json must contain a non-empty apps list")

    apps: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    for index, raw_app in enumerate(raw_apps, start=1):
        if not isinstance(raw_app, dict):
            raise ValueError(f"Portal app #{index} must be an object")

        app = {
            str(key): str(value).strip()
            for key, value in raw_app.items()
            if value is not None
        }
        missing = [field for field in REQUIRED_FIELDS if not app.get(field)]
        if missing:
            raise ValueError(f"Portal app #{index} is missing: {', '.join(missing)}")

        url = app["url"]
        if not _is_allowed_streamlit_url(url):
            raise ValueError(f"Portal app #{index} has an invalid Streamlit URL")
        if url in seen_urls:
            raise ValueError(f"Duplicate portal URL: {url}")

        admin_url = app.get("admin_url")
        if admin_url and not _is_allowed_streamlit_url(admin_url):
            raise ValueError(f"Portal app #{index} has an invalid admin URL")

        seen_urls.add(url)
        apps.append(app)

    return tuple(apps)
