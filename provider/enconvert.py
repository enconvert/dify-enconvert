import requests
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

WHOAMI_URL = "https://api.enconvert.com/v1/whoami"


class EnconvertProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict) -> None:
        api_key = credentials.get("enconvert_api_key")
        if not api_key:
            raise ToolProviderCredentialValidationError("EnConvert API key is required.")
        try:
            resp = requests.get(WHOAMI_URL, headers={"X-API-Key": api_key}, timeout=30)
        except requests.RequestException as exc:
            raise ToolProviderCredentialValidationError(
                f"Could not reach EnConvert: {exc}"
            ) from exc
        if resp.status_code != 200:
            raise ToolProviderCredentialValidationError(
                "Invalid EnConvert API key. Use a private key (prefix sk_) from "
                "https://www.enconvert.com/dashboard/api-keys — public pk_ keys are rejected."
            )
