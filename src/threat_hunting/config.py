from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


@dataclass(frozen=True)
class Settings:
    threat_news_url: str
    threat_news_api_key: str
    fortisiem_base_url: str
    fortisiem_api_path: str
    fortisiem_api_token: str
    fortisiem_username: str
    fortisiem_password: str
    fortisiem_verify_ssl: bool


    @classmethod
    def from_env(cls) -> "Settings":
        env_path = Path(os.getenv("THREAT_HUNTING_ENV", ".env"))
        load_env_file(env_path)

        return cls(
            threat_news_url=os.getenv(
                "THREAT_NEWS_URL", "https://example.com/threat-news.json"
            ),
            threat_news_api_key=os.getenv("THREAT_NEWS_API_KEY", ""),
            fortisiem_base_url=os.getenv("FORTISIEM_BASE_URL", "").rstrip("/"),
            fortisiem_api_path=os.getenv("FORTISIEM_API_PATH", "/phoenix/rest/query"),
            fortisiem_api_token=os.getenv("FORTISIEM_API_TOKEN", ""),
            fortisiem_username=os.getenv("FORTISIEM_USERNAME", ""),
            fortisiem_password=os.getenv("FORTISIEM_PASSWORD", ""),
            fortisiem_verify_ssl=os.getenv("FORTISIEM_VERIFY_SSL", "true").lower()
            != "false",
        )
