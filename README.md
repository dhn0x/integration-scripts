# Threat Hunting Model Automation for FortiSIEM

This repository provides a lightweight automation workflow that:

1. Pulls threat news from a configurable source.
2. Builds FortiSIEM search queries based on the threat indicators.
3. Calls the FortiSIEM API to execute those queries.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

```bash
cp .env.example .env
# edit .env with your FortiSIEM credentials + threat news feed URL
```

```bash
fortisiem-hunt --limit 5
```

## Configuration

Set configuration through environment variables or a `.env` file:

| Variable | Description | Default |
| --- | --- | --- |
| `THREAT_NEWS_URL` | URL returning JSON threat news objects. | `https://example.com/threat-news.json` |
| `THREAT_NEWS_API_KEY` | Optional API key header value for threat news source. | (empty) |
| `FORTISIEM_BASE_URL` | Base URL for FortiSIEM (ex: `https://fortisiem.example.com`). | (required) |
| `FORTISIEM_API_PATH` | Path for query API endpoint. | `/phoenix/rest/query` |
| `FORTISIEM_API_TOKEN` | Bearer token for FortiSIEM API authentication. | (empty) |
| `FORTISIEM_USERNAME` | Username for basic auth (used if token missing). | (empty) |
| `FORTISIEM_PASSWORD` | Password for basic auth (used if token missing). | (empty) |
| `FORTISIEM_VERIFY_SSL` | `true` or `false` to verify SSL certs. | `true` |

## Threat News Format

The threat news source should return JSON shaped like:

```json
{
  "items": [
    {
      "title": "New ransomware campaign",
      "summary": "Ransomware targets healthcare sector",
      "indicators": ["ransomware", "healthcare"]
    }
  ]
}
```

## Notes

- The query builder in `threat_hunting/query_builder.py` is intentionally generic. Update it to fit your FortiSIEM schema.
- If your FortiSIEM deployment uses a different API endpoint or payload, adjust `FORTISIEM_API_PATH` and payload builder.
