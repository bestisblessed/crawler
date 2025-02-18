import os
import re
import csv
import sys

def parse_fighter_urls():
    # Hardcoded paths
    directory = "data/tapology-events-bak"
    output_file = "data/master-fighters.csv"
    
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
    


# CLEAN URLS    
# import re

# # Open the input file and the output file
# with open('inputfile.txt', 'r') as infile, open('outputfile.txt', 'w') as outfile:
#     for line in infile:
#         # Use regex to extract the relevant part of the URL
#         match = re.search(r'(/fightcenter/fighters/[a-z0-9-]+)', line)
#         if match:
#             # Write only the matched part to the output file
#             outfile.write(match.group(0) + '\n')
import pandas as pd
import re

# Path to your input CSV file
input_file = 'data/master-fighters.csv'
output_file = 'data/fighters-with-urls.csv'

# Base URL for Tapology
base_url = 'https://www.tapology.com'

# Read the CSV into a pandas DataFrame
df = pd.read_csv(input_file)

# Assuming the URL column is named 'url', adjust if necessary
# Extract relevant part of the URL using regex
df['cleaned_url'] = df['raw_url'].apply(lambda x: re.search(r'(/fightcenter/fighters/[a-z0-9-]+)', x).group(0) if isinstance(x, str) else '')

# Create the full URL column
df['full_url'] = base_url + df['cleaned_url']

# Save the result to a new CSV
df.to_csv(output_file, index=False)

print(f"Cleaned data saved to {output_file}")
