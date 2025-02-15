import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

async def main():
    browser_config = BrowserConfig()
    run_config = CrawlerRunConfig() 
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="http://ufcstats.com/fighter-details/07f72a2a7591b409",
            config=run_config
        )
        print(result.markdown)
        with open("data/output.md", "w", encoding="utf-8") as f:
            f.write(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())