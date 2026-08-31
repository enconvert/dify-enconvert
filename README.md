# EnConvert for Dify

A [Dify](https://dify.ai) tool plugin for [EnConvert](https://www.enconvert.com). Render web pages and
files into agent-ready data — markdown, structured JSON, screenshots, PDFs — from inside any Dify agent
or workflow. Every page render carries a `render_quality` score from 0.0 to 1.0, so a blocked or empty
page comes back flagged instead of being mistaken for real content.

## Install

Dify Marketplace → search **EnConvert**, or **Plugins → Install plugin → GitHub** with this repository's
[latest release](https://github.com/enconvert/dify-enconvert/releases/latest).

## Tools

| Tool | EnConvert endpoint | What it does |
| --- | --- | --- |
| **Perceive URL** | `POST /v2/perceive` | Render a page into markdown, HTML, a screenshot, a PDF, links, images or structured data, with a `render_quality` score. |
| **Web Search** | `POST /v2/lookup` | Web, news, image, scholar, patent and map search. |
| **Discover URLs** | `POST /v2/discover` | List a site's URLs via sitemap, crawl or hybrid, without rendering. |
| **Extract Structured** | `POST /v2/distill` | Extract fields matching a JSON schema from one or more pages, or from a crawl. |
| **Convert File to Markdown** | `POST /v1/convert/anything-to-markdown` | Turn a document, spreadsheet, presentation, PDF, EPUB or HTML file into markdown. |
| **Convert File to PDF** | `POST /v1/convert/anything-to-pdf` | Convert a document, image, HTML or text file to PDF. |

The two convert tools take a **Dify file** — an uploaded file, or a file variable from an earlier
workflow node. The plugin uploads its bytes to EnConvert as multipart `file` and returns a signed
download URL for the result. That result URL, like any perceive screenshot/PDF URL, must be fetched
**without** the API key. The plugin never fetches a user-supplied URL itself: every URL you pass to
Perceive, Discover or Extract Structured is fetched by EnConvert's servers, not by your Dify host.

## Authentication

One credential: your **private** EnConvert API key (prefix `sk_`, from your
[dashboard](https://www.enconvert.com/dashboard/api-keys)). Every request sends it as the header
`X-API-Key`. Connecting validates it against `GET /v1/whoami`, which rejects public `pk_` keys.

## Resources

- EnConvert API documentation: <https://www.enconvert.com/docs>
- Dify plugin development: <https://docs.dify.ai/plugins>

## Licence

[MIT](LICENSE)
