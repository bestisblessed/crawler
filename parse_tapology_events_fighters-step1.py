import os
import re
import csv
import sys
def parse_fighter_urls():
    directory = "data/tapology-events"
    output_file = "data/master-fighters.csv"
    pattern = r'\[([^\]]+)\]\(https://www\.tapology\.com/fightcenter/events/</fightcenter/fighters/(\d+)[^>]+>\)|https://www\.tapology\.com/fightcenter/events/</fightcenter/fighters/(\d+)[^>]+>'
    fighters = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):  
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            full_url = match.group(0)
                            if match.group(1):  
                                name = match.group(1)
                                fighter_id = match.group(2)
                            else:  
                                fighter_id = match.group(3)
                                name = "Unknown"
                            fighter_entry = {
                                'fighter_id': fighter_id,
                                'name': name,
                                'raw_url': full_url
                            }
                            if fighter_entry not in fighters:
                                fighters.append(fighter_entry)
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
import pandas as pd
import re
input_file = 'data/master-fighters.csv'
output_file = 'data/fighters-with-urls.csv'
base_url = 'https://www.tapology.com'
df = pd.read_csv(input_file)
df['cleaned_url'] = df['raw_url'].apply(lambda x: re.search(r'(/fightcenter/fighters/[a-z0-9-]+)', x).group(0) if isinstance(x, str) else '')
df['full_url'] = base_url + df['cleaned_url']
df.to_csv(output_file, index=False)
print(f"Cleaned data saved to {output_file}")
os.remove('data/master-fighters.csv')
