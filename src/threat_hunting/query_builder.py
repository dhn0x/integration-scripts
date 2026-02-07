from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class FortiSIEMQuery:
    name: str
    statement: str


def build_queries(keywords: Iterable[str]) -> list[FortiSIEMQuery]:
    queries: list[FortiSIEMQuery] = []
    for keyword in keywords:
        sanitized = keyword.replace("'", "''")
        statement = (
            "SELECT * FROM Event WHERE"  # Adjust this statement to your schema.
            f"(eventType LIKE '%{sanitized}%' OR rawEvent LIKE '%{sanitized}%')"
        )
        queries.append(FortiSIEMQuery(name=keyword, statement=statement))
    return queries
