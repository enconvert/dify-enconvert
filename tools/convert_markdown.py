from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .enconvert_client import convert_upload


class ConvertToMarkdownTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials["enconvert_api_key"]
        file = tool_parameters["file"]

        result = convert_upload(api_key, file, "/v1/convert/anything-to-markdown")
        yield self.create_json_message(result)

        url = result.get("presigned_url")
        if url:
            yield self.create_link_message(url)
            yield self.create_text_message(
                f"Converted to Markdown. Download (no API key, valid ~15 min): {url}"
            )
        else:
            yield self.create_text_message("Conversion complete.")
