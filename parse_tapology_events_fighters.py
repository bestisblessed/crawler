import os
import re
import csv
import sys

def parse_fighter_urls():
    # Hardcoded paths
    directory = "data/tapology-events-bak"
    output_file = "data/master.csv"
    
    # Regex pattern to match fighter URLs and names
    pattern = r'\[([^\]]+)\]\(https://www\.tapology\.com/fightcenter/events/</fightcenter/fighters/(\d+)[^>]+>\)|https://www\.tapology\.com/fightcenter/events/</fightcenter/fighters/(\d+)[^>]+>'

    fighters = []
    
    try:
        # Walk through all files in the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):  # Only process markdown files
                    file_path = os.path.join(root, file)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = re.finditer(pattern, content)
                        
                        for match in matches:
                            # Get the full raw URL from the match
                            full_url = match.group(0)
                            
                            if match.group(1):  # Markdown link format
                                name = match.group(1)
                                fighter_id = match.group(2)
                            else:  # Plain URL format
                                fighter_id = match.group(3)
                                name = "Unknown"
                            
                            # Only add if not already in list
                            fighter_entry = {
                                'fighter_id': fighter_id,
                                'name': name,
                                'raw_url': full_url
                            }
                            if fighter_entry not in fighters:
                                fighters.append(fighter_entry)

        # Write to CSV
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['fighter_id', 'name', 'raw_url'])
            writer.writeheader()
            writer.writerows(fighters)
            
        print(f"Successfully parsed {len(fighters)} unique fighters to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parse_fighter_urls() 