import asyncio
import csv
import aiofiles
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from tqdm.asyncio import tqdm
import os

os.makedirs('data/tapology-fighters-ufc', exist_ok=True)

async def save_file(filepath, content):
    async with aiofiles.open(filepath, "w", encoding="utf-8") as f:
        await f.write(content)

async def process_url(crawler, run_config, url, id, name, semaphore):
    async with semaphore:  # Limit concurrent requests
        try:
            print(f"Processing: {url}")
            result = await crawler.arun(url=url, config=run_config)
            
            # Save files asynchronously
            tasks = [
                save_file(f"data/tapology-fighters-ufc/{id}-{name}.md", result.markdown),
                save_file(f"data/tapology-fighters-ufc/cleaned_{id}-{name}.html", result.cleaned_html),
                save_file(f"data/tapology-fighters-ufc/raw_{id}-{name}.html", result.html)
            ]
            await asyncio.gather(*tasks)
            return True
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return False

async def main():
    browser_config = BrowserConfig()
    run_config = CrawlerRunConfig(pdf=False, screenshot=False)
    
    # Create semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(3)
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        tasks = []
        
        # Read CSV and create tasks
        with open('data/fighters-with-urls.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            fighters = [row for row in reader if row['full_url'].strip().startswith('http')]
            total_fighters = len(fighters)
            
            # Create batch of tasks
            for row in fighters:
                url = row['full_url'].strip()
                task = process_url(
                    crawler, 
                    run_config, 
                    url, 
                    row['fighter_id'], 
                    row['name'], 
                    semaphore
                )
                tasks.append(task)
            
            # Process all tasks concurrently with progress bar
            results = await tqdm.gather(*tasks, desc="Processing fighters", total=total_fighters)
            processed_count = sum(1 for r in results if r)
            print(f"\nSuccessfully processed {processed_count}/{total_fighters} fighters")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Process interrupted by user")
