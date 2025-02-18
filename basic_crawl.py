import asyncio
import base64
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

loop = asyncio.get_event_loop()
browser_config = BrowserConfig()   
run_config = CrawlerRunConfig(
    pdf=True,        # Enable PDF generation
    screenshot=True  # Enable screenshot capture
)    
crawler = AsyncWebCrawler(config=browser_config)
loop.run_until_complete(crawler.__aenter__())

url = "https://www.tapology.com/fightcenter/fighters/jon-jones-bones"
path_part = url.split("www.", 1)[-1]  # Get everything after www.
sanitized_path = path_part.replace("/", "_").replace(":", "_")[:100]  # Sanitize remaining path

result = loop.run_until_complete(
    crawler.arun(
        url=url,
        config=run_config
    )
)

print("Markdown:\n", result.markdown)
with open(f"data/{sanitized_path}.md", "w", encoding="utf-8") as f:
    f.write(result.markdown)
# with open(f"data/raw_{sanitized_path}.html", "w", encoding="utf-8") as f:
#     f.write(result.html)
# with open(f"data/cleaned_{sanitized_path}.html", "w", encoding="utf-8") as f:
#     f.write(result.cleaned_html)
# if result.pdf is not None:
#     with open(f"data/{sanitized_path}.pdf", "wb") as f:
#         f.write(result.pdf)
# else:
#     print("PDF content is None, skipping file write.")
# if result.screenshot is not None:
#     screenshot_data = base64.b64decode(result.screenshot)
#     with open(f"data/screenshot_{sanitized_path}.png", "wb") as f:
#         f.write(screenshot_data)
# else:
#     print("Screenshot content is None, skipping file write.")
    
loop.run_until_complete(crawler.__aexit__(None, None, None))
loop.close()