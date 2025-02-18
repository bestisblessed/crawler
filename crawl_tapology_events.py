import asyncio
import csv
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import os
import shutil
os.makedirs('data/tapology-events', exist_ok=True)
shutil.copy('../mma-ai/Scrapers/data/tapology/event_urls_tapology_ufc.csv', 'data/')
async def process_url(crawler, run_config, url, counter):
    path_part = url.split("www.", 1)[-1]  
    sanitized_path = path_part.replace("/", "_").replace(":", "_")[:100]  
    result = await crawler.arun(
        url=url,
        config=run_config
    )
    print(f"Processing: {url} ({counter})")
    with open(f"data/tapology-events/{sanitized_path}.md", "w", encoding="utf-8") as f:
        f.write(result.markdown)
    with open(f"data/tapology-events/cleaned_{sanitized_path}.html", "w", encoding="utf-8") as f:
        f.write(result.cleaned_html)
async def main():
    browser_config = BrowserConfig()   
    run_config = CrawlerRunConfig(
        pdf=False,        
        screenshot=False  
    )    
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.__aenter__()
    with open('data/event_urls_tapology_ufc.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        counter = 0  
        for row in reader:
            url = row['URL'].strip()
            if url.startswith('http'):  
                try:
                    counter += 1  
                    await process_url(crawler, run_config, url, counter)
                    await asyncio.sleep(2)  
                except Exception as e:
                    print(f"Error processing {url}: {str(e)}")
    await crawler.__aexit__(None, None, None)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Process interrupted by user")