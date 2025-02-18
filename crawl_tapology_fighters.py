import asyncio
import csv
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

async def process_url(crawler, run_config, url, id, name):
    # Create a sanitized filename from the URL and fighter's ID and name
    sanitized_filename = f"{id}-{name.replace(' ', '_').replace('-', '_')[:100]}.md"  # Sanitize name

    # Process the URL
    result = await crawler.arun(
        url=url,
        config=run_config
    )

    # Save markdown and HTML content
    print(f"Processing: {url}")
    with open(f"data/tapology-fighters-ufc/{id}-{name}.md", "w", encoding="utf-8") as f:
        f.write(result.markdown)
    with open(f"data/tapology-fighters-ufc/cleaned_{id}-{name}.md", "w", encoding="utf-8") as f:
        f.write(result.fit_markdown)
    with open(f"data/tapology-fighters-ufc/cleaned_{id}-{name}.html", "w", encoding="utf-8") as f:
        f.write(result.cleaned_html)
    with open(f"data/tapology-fighters-ufc/raw_{id}-{name}.html", "w", encoding="utf-8") as f:
        f.write(result.html)

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
    with open('data/fighters-with-urls.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        total_fighters = sum(1 for row in reader)  # Get total count
        csvfile.seek(0)  # Reset file pointer
        next(reader)  # Skip header
        processed_count = 0  # Initialize a counter for processed fighters
        
        for row in reader:
            url = row['full_url'].strip()
            id = row['fighter_id']
            name = row['name']
            if url.startswith('http'):  # Verify it's a valid URL
                try:
                    await process_url(crawler, run_config, url, id, name)
                    processed_count += 1  # Increment the counter
                    print(f"Processed {processed_count}/{total_fighters} fighters.")
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