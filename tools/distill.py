import json
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .enconvert_client import csv_list, post_json

MAX_URLS = 50


class DistillTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials["enconvert_api_key"]

        raw_schema = tool_parameters["schema"]
        if isinstance(raw_schema, str):
            try:
                schema = json.loads(raw_schema)
            except json.JSONDecodeError as exc:
                yield self.create_text_message(f"schema must be valid JSON: {exc}")
                return
        else:
            schema = raw_schema

        urls = csv_list(tool_parameters.get("urls"))
        discover_from_url = tool_parameters.get("discover_from_url")
        if bool(urls) == bool(discover_from_url):
            yield self.create_text_message(
                "Provide exactly one of 'urls' or 'discover_from_url'."
            )
            return

        payload: dict[str, Any] = {"schema": schema}
        if urls:
            payload["urls"] = urls[:MAX_URLS]
        else:
            discover: dict[str, Any] = {"url": discover_from_url}
            if tool_parameters.get("discover_mode"):
                discover["mode"] = tool_parameters["discover_mode"]
            if tool_parameters.get("discover_max_pages") is not None:
                discover["max_pages"] = int(tool_parameters["discover_max_pages"])
            payload["discover_from"] = discover

        result = post_json(api_key, "/v2/distill", payload)
        yield self.create_json_message(result)
        yield self.create_text_message(
            f"Extraction complete (tier: {result.get('extraction_tier')})."
        )
