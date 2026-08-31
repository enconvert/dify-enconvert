from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .enconvert_client import csv_list, post_json


class DiscoverTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials["enconvert_api_key"]
        payload: dict[str, Any] = {"url": tool_parameters["url"]}
        if tool_parameters.get("mode"):
            payload["mode"] = tool_parameters["mode"]
        for key in ("max_urls", "max_depth"):
            if tool_parameters.get(key) is not None:
                payload[key] = int(tool_parameters[key])
        for key in ("include_patterns", "exclude_patterns"):
            patterns = csv_list(tool_parameters.get(key))
            if patterns:
                payload[key] = patterns
        for key in ("same_domain_only", "respect_robots"):
            if tool_parameters.get(key) is not None:
                payload[key] = tool_parameters[key]

        result = post_json(api_key, "/v2/discover", payload)
        yield self.create_json_message(result)

        urls = result.get("urls") or []
        total = result.get("total", len(urls))
        yield self.create_text_message(f"Discovered {total} URL(s) from {payload['url']}.")
