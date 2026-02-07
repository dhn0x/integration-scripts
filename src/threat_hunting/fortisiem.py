from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from .config import Settings
from .query_builder import FortiSIEMQuery


@dataclass
class FortiSIEMResponse:
    query: FortiSIEMQuery
    payload: dict[str, Any]


class FortiSIEMClient:
    def __init__(self, settings: Settings) -> None:
        if not settings.fortisiem_base_url:
            raise ValueError("FORTISIEM_BASE_URL is required")
        self.settings = settings
        self.session = requests.Session()
        if settings.fortisiem_api_token:
            self.session.headers.update(
                {"Authorization": f"Bearer {settings.fortisiem_api_token}"}
            )

    def run_query(self, query: FortiSIEMQuery) -> FortiSIEMResponse:
        url = f"{self.settings.fortisiem_base_url}{self.settings.fortisiem_api_path}"
        auth = None
        if not self.settings.fortisiem_api_token and self.settings.fortisiem_username:
            auth = HTTPBasicAuth(
                self.settings.fortisiem_username, self.settings.fortisiem_password
            )
        payload = {
            "query": query.statement,
            "name": query.name,
        }
        response = self.session.post(
            url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            auth=auth,
            timeout=60,
            verify=self.settings.fortisiem_verify_ssl,
        )
        response.raise_for_status()
        return FortiSIEMResponse(query=query, payload=response.json())
