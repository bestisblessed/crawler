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
result = loop.run_until_complete(
    crawler.arun(
        url="http://ufcstats.com/fighter-details/07f72a2a7591b409",
        config=run_config
    )
)
print("Markdown:\n", result.markdown)
with open("data/output.md", "w", encoding="utf-8") as f:
    f.write(result.markdown)
with open("data/output_raw.html", "w", encoding="utf-8") as f:
    f.write(result.html)
with open("data/output_cleaned.html", "w", encoding="utf-8") as f:
    f.write(result.cleaned_html)
if result.pdf is not None:
    with open("data/output.pdf", "wb") as f:
        f.write(result.pdf)
else:
    print("PDF content is None, skipping file write.")
if result.screenshot is not None:
    screenshot_data = base64.b64decode(result.screenshot)
    with open("data/output_screenshot.png", "wb") as f:
        f.write(screenshot_data)
else:
    print("Screenshot content is None, skipping file write.")
    
loop.run_until_complete(crawler.__aexit__(None, None, None))
loop.close()