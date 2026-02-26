---
name: firecrawl-cli
description: Standardized Firecrawl CLI skill for web scraping, crawling, and AI-powered research.
license: MIT
---

# Firecrawl CLI Skill

This skill provides a standardized CLI for AI agents to interact with Firecrawl, enabling high-quality web scraping, crawling, and AI-powered research.

## When to use this skill
- When you need to extract clean, LLM-ready markdown from a specific URL.
- When you need to crawl entire websites to build a knowledge base.
- When you need to perform AI-powered research across the web.
- When you need to discover sitemaps or link structures of a domain.

## How to use it

### Authentication
Ensure you are logged in or have a `FIRECRAWL_API_KEY` set.
- `firecrawl login`: Login via browser.
- `firecrawl login --key <your-api-key>`: Login with an API key.

### Basic Commands
- `firecrawl scrape <url>`: Scrape a single URL and get markdown output.
- `firecrawl crawl <url>`: Start a crawl job for a domain.
- `firecrawl map <url>`: Map the pages of a website.
- `firecrawl search "<query>"`: Search the web and get results.

### AI Agent Command
The `agent` command is powerful for complex research tasks:
- `firecrawl agent "Find the top 5 AI startups and their funding amounts" --wait`: Performs research and provides structured answers.

### Options
- `--json`: Output results in JSON format.
- `--pretty`: Format JSON output for readability.
- `--output <path>`: Save result to a file.
- `-o <path>`: Alias for `--output`.

## Example Patterns

### Simple Scrape
```bash
firecrawl scrape https://docs.firecrawl.dev -o firecrawl_docs.md
```

### Research Workflow
```bash
firecrawl agent "Compare pricing for Vercel, Netlify, and AWS Amplify" --urls https://vercel.com/pricing,https://www.netlify.com/pricing --wait
```

## Review Checklist
- Check `firecrawl version` to ensure the tool is up to date.
- Verify that `FIRECRAWL_API_KEY` is available if running in automated environments.
- Ensure output files follow the project's naming conventions.

## Notes
- Created: 2026-02-09
- Author: Kurt Anderson
- Version: 1.0.0
