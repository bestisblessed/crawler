import re
import os
import pandas as pd

# Define function to extract fight details
def extract_fight_details(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Print first 500 chars for debugging
    print(f"Preview of {file_path} content:\n", content[:500])
    
    # Regex pattern to extract fight details
    fight_pattern = re.compile(
        r'W\s+\[(.*?)\].*?Up to (\d+-\d+(?:-\d+)?).*?L\s+\[(.*?)\].*?Down to (\d+-\d+(?:-\d+)?)',
        re.DOTALL
    )
    
    fights = fight_pattern.findall(content)
    
    fight_data = []
    for fight in fights:
        winner, winner_record, loser, loser_record = fight
        fight_data.append({
            "Winner": winner.strip(),
            "Winner Record": winner_record.strip(),
            "Loser": loser.strip(),
            "Loser Record": loser_record.strip()
        })
    
    # Debugging output
    print(f"Extracted fights from {file_path}: {fight_data}")
    return fight_data

# Loop through entire directory to find all .md files
directory_path = 'data/tapology-events/'
all_fight_data = []
for file_name in os.listdir(directory_path):
    if file_name.endswith('.md'):
        file_path = os.path.join(directory_path, file_name)
        if os.path.exists(file_path):
            all_fight_data.extend(extract_fight_details(file_path))

# Convert results to DataFrame and save to a single CSV file
df = pd.DataFrame(all_fight_data)
df.to_csv('master.csv', index=False)
