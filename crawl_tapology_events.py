import asyncio
import csv
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

async def process_url(crawler, run_config, url, counter):
    # Create a sanitized filename from the URL
    path_part = url.split("www.", 1)[-1]  # Get everything after www.
    sanitized_path = path_part.replace("/", "_").replace(":", "_")[:100]  # Sanitize remaining path

    # Process the URL
    result = await crawler.arun(
        url=url,
        config=run_config
    )

    # Save markdown and HTML content
    print(f"Processing: {url} ({counter})")
    with open(f"data/tapology-events/{sanitized_path}.md", "w", encoding="utf-8") as f:
        f.write(result.markdown)
    with open(f"data/tapology-events/cleaned_{sanitized_path}.html", "w", encoding="utf-8") as f:
        f.write(result.cleaned_html)

async def main():
    # Initialize crawler configuration
    browser_config = BrowserConfig()   
    run_config = CrawlerRunConfig(
        pdf=False,        # Disable PDF generation
        screenshot=False  # Disable screenshot capture
    )    
    crawler = AsyncWebCrawler(config=browser_config)
    
    # Start the crawler
    await crawler.__aenter__()
    
    # Read and process URLs from CSV
    # with open('data/fighter_info_with_urls.csv', 'r') as csvfile:
    with open('data/event_urls_tapology_ufc.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        counter = 0  # Initialize counter
        for row in reader:
            url = row['URL'].strip()
            if url.startswith('http'):  # Verify it's a valid URL
                try:
                    counter += 1  # Increment counter for each processed URL
                    await process_url(crawler, run_config, url, counter)
                    await asyncio.sleep(2)  # Sleep for 1 second after each URL
                except Exception as e:
                    print(f"Error processing {url}: {str(e)}")
    
    # Clean up
    await crawler.__aexit__(None, None, None)

if __name__ == "__main__":
    # Updated event loop handling to avoid deprecation warning
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Process interrupted by user")