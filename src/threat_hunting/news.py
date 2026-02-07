from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import requests

from .config import Settings


@dataclass(frozen=True)
class ThreatNewsItem:
    title: str
    summary: str
    indicators: tuple[str, ...]


class ThreatNewsClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def fetch(self, limit: int = 10) -> list[ThreatNewsItem]:
        headers = {}
        if self.settings.threat_news_api_key:
            headers["Authorization"] = self.settings.threat_news_api_key
        response = requests.get(
            self.settings.threat_news_url, headers=headers, timeout=30
        )
        response.raise_for_status()
        payload = response.json()
        items = payload.get("items", [])
        parsed: list[ThreatNewsItem] = []
        for item in items[:limit]:
            parsed.append(self._parse_item(item))
        return parsed

    def _parse_item(self, data: dict) -> ThreatNewsItem:
        title = str(data.get("title", "Untitled"))
        summary = str(data.get("summary", ""))
        indicators = data.get("indicators", []) or []
        return ThreatNewsItem(title=title, summary=summary, indicators=tuple(indicators))


def to_keywords(items: Iterable[ThreatNewsItem]) -> list[str]:
    keywords: list[str] = []
    for item in items:
        keywords.extend(item.indicators)
        if item.title:
            keywords.append(item.title)
    return [keyword for keyword in keywords if keyword]
