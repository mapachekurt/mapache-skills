---
name: rtrvr-agent
description: AI-powered browser automation and scraping tool resilient to UI changes.
version: 1.0.0
---

# rtrvr-agent

`rtrvr.ai` is an AI agent that controls browsers using the Accessibility Tree API, making it highly resilient to layout changes compared to traditional DOM-based scrapers.

## Core Capabilities

- **Natural Language Control**: Describe tasks in English.
- **Resilience**: Understands page structure logically via accessibility tags.
- **Shared Session Auth**: Uses your existing browser logins via the Chrome extension.
- **Bulk Extraction**: Capable of crawling domains and extracting structured data to Google Sheets.

## CLI Usage

Install via npm:
```bash
npm install -g @rtrvr-ai/cli
```

### Commands

- `rtrvr scrape <url>`: Extract clean Markdown/JSON from a URL.
- `rtrvr agent "<prompt>"`: Run a multi-step browser task.
- `rtrvr crawl <domain>`: Crawl and extract data from a full site.

## API Integration

Base URL: `https://api.rtrvr.ai/v1`
Authentication: Bearer Token (API Key)

### Endpoints
- `/scrape`: Raw content extraction.
- `/agent`: Full agentic workflows.
- `/mcp`: Connect as an Model Context Protocol server.

## Best Practices

- **Use for Auth**: Prefer `rtrvr` for any site where you are already logged in via Chrome.
- **Resilient Selectors**: When sites change their CSS/HTML classes frequently, use `rtrvr`'s natural language agent to find elements.
- **Token Usage**: `rtrvr` is more token-efficient than sending full DOM trees to an LLM.
