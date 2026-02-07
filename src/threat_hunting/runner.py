from __future__ import annotations

from dataclasses import dataclass

from .config import Settings
from .fortisiem import FortiSIEMClient, FortiSIEMResponse
from .news import ThreatNewsClient, to_keywords
from .query_builder import build_queries


@dataclass
class RunResult:
    responses: list[FortiSIEMResponse]


def run_hunt(settings: Settings, limit: int = 10) -> RunResult:
    news_client = ThreatNewsClient(settings)
    items = news_client.fetch(limit=limit)
    keywords = to_keywords(items)
    queries = build_queries(keywords)
    fortisiem_client = FortiSIEMClient(settings)

    responses: list[FortiSIEMResponse] = []
    for query in queries:
        responses.append(fortisiem_client.run_query(query))

    return RunResult(responses=responses)
