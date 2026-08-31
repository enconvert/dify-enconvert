# Privacy Policy

This plugin is a thin client for the EnConvert API. It is stateless.

## What it transmits

When you run a tool, the plugin sends to `https://api.enconvert.com`:

- Your EnConvert API key, as the `X-API-Key` request header.
- The inputs you supply to the tool — the URL, search query, JSON schema or other parameters
  you or your agent pass — needed to perform the requested conversion or read.
- For the two convert tools, the bytes of the file you wire into the tool.

The plugin contacts `https://api.enconvert.com` and, to inline Perceive's text output, the signed
storage URL that API returns (`nyc3.digitaloceanspaces.com`). Both are declared in `manifest.yaml`
under `network.domains`. URLs you pass to Perceive, Discover or Extract Structured are fetched by
EnConvert's servers, never by the Dify host running this plugin.

## What it collects

Nothing. The plugin does not collect, log, store, or transmit your data anywhere other than the
EnConvert API calls described above. It has no database, no analytics, and no third-party trackers. Your
API key is held only for the duration of a request and is managed by Dify's encrypted credential store.

## Third party

Data you send is processed by EnConvert under its own terms and privacy policy:

- <https://www.enconvert.com/terms>
- <https://www.enconvert.com/privacy>

## Contact

Questions: <https://www.enconvert.com>
