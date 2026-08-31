"""Thin HTTP client shared by every EnConvert tool.

One place for the base URL, the X-API-Key header, and the multipart upload the
two file-conversion tools need.
"""

from __future__ import annotations

from typing import Any

import requests

BASE_URL = "https://api.enconvert.com"
TIMEOUT = 120


def post_json(api_key: str, path: str, payload: dict) -> dict:
    resp = requests.post(
        f"{BASE_URL}{path}",
        headers={"X-API-Key": api_key},
        json=payload,
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def file_part(file: Any) -> tuple[str, bytes]:
    """Dify File -> (filename, bytes). The API sniffs the input format from the
    extension, so the name has to survive the trip."""
    if not hasattr(file, "blob"):
        raise ValueError(
            "Expected an uploaded file. Wire a file variable (or an uploaded "
            "file) into this parameter, not a URL string."
        )
    name = getattr(file, "filename", None) or f"file{getattr(file, 'extension', '') or ''}"
    return name, file.blob


def convert_upload(api_key: str, file: Any, path: str) -> dict:
    """POST a file as multipart `file` to an EnConvert convert endpoint.

    `direct_download=false` is required: the default returns the converted bytes,
    and these tools want the JSON envelope with the presigned URL.
    """
    filename, content = file_part(file)
    resp = requests.post(
        f"{BASE_URL}{path}",
        headers={"X-API-Key": api_key},
        files={"file": (filename, content)},
        data={"direct_download": "false"},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def csv_list(value) -> list[str] | None:
    """Accept a list or a comma-separated string; return a cleaned list or None."""
    if not value:
        return None
    items = value if isinstance(value, list) else str(value).split(",")
    cleaned = [str(item).strip() for item in items if str(item).strip()]
    return cleaned or None
