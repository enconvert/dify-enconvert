from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .enconvert_client import post_json


class SearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials["enconvert_api_key"]
        payload: dict[str, Any] = {"query": tool_parameters["query"]}
        for key in ("category", "country", "locale", "location", "time_filter"):
            if tool_parameters.get(key):
                payload[key] = tool_parameters[key]
        for key in ("num_results", "page"):
            if tool_parameters.get(key) is not None:
                payload[key] = int(tool_parameters[key])
        if tool_parameters.get("autocorrect") is not None:
            payload["autocorrect"] = tool_parameters["autocorrect"]

        result = post_json(api_key, "/v2/lookup", payload)
        yield self.create_json_message(result)

        results = result.get("results") or []
        yield self.create_text_message(f'{len(results)} result(s) for "{payload["query"]}".')
