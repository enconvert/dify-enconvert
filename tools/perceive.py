from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .enconvert_client import csv_list, fetch_text, post_json

# Every artifact comes back as a 15-minute signed URL. Text ones are worth
# reading for the agent; the rest can only be handed over as a link.
TEXT_OUTPUTS = {"markdown", "html_cleaned", "html_raw"}


class PerceiveTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials["enconvert_api_key"]
        payload: dict[str, Any] = {"url": tool_parameters["url"]}
        outputs = csv_list(tool_parameters.get("outputs"))
        if outputs:
            payload["outputs"] = outputs
        if tool_parameters.get("only_main_content") is not None:
            payload["only_main_content"] = tool_parameters["only_main_content"]

        result = post_json(api_key, "/v2/perceive", payload)
        yield self.create_json_message(result)

        quality = result.get("render_quality")
        outs = result.get("outputs") or {}
        # Billing contract: a detected block is a 200 with empty outputs and no charge.
        flags = []
        if result.get("is_blocked") is True:
            flags.append("BLOCKED: content-free page, do not treat as content")
        if result.get("billed") is False:
            flags.append("not billed")
        suffix = f" {'; '.join(flags)}." if flags else ""
        yield self.create_text_message(
            f"Perceived {payload['url']} — render_quality {quality} "
            f"(0 = blocked/empty, 1 = clean). Outputs: {', '.join(outs) or 'none'}.{suffix}"
        )
        for name, data in outs.items():
            url = data.get("url") if isinstance(data, dict) else None
            if not url:
                continue
            if name in TEXT_OUTPUTS:
                text = fetch_text(url)
                if text is not None:
                    yield self.create_text_message(f"--- {name} ---\n{text}")
                    continue
            yield self.create_link_message(url)
