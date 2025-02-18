import re
import pandas as pd
import os
def extract_fight_data_from_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
    fight_data = []
    fighter_name = file_path.split('/')[-1].replace('.md', '')
    fight_sections = re.split(r'\n(?=[WLC]\n)', md_content)
    for section in fight_sections:
        if not section.strip():
            continue
        try:
            fight_info = {
                'Fighter': fighter_name,
                'Result': None,
                'Method': None,
                'Opponent': None,
                'OpponentRecord': None,
                'Event': None,
                'Date': None,
                'Round': None,
                'Time': None,
                'WeightClass': None,
                'WeighIn': None,
                'Location': None,
                'Venue': None,
                'Odds': None,
                'Referee': None
            }
            lines = section.split('\n')
            if lines[0].strip() in ['W', 'L', 'C']:
                fight_info['Result'] = lines[0].strip()
            if len(lines) > 1:
                method = lines[1].strip()
                if method in ['TKO', 'KO', 'SUB', 'DEC', 'UD', 'SD']:
                    fight_info['Method'] = method
            for line in lines:
                if 'Fighter Page' in line:
                    opponent_match = re.search(r'\[(.*?)\]', line)
                    if opponent_match:
                        fight_info['Opponent'] = opponent_match.group(1)
                    record_match = re.search(r'(\d+-\d+)\s+(\d+-\d+)', line)
                    if record_match:
                        fight_info['OpponentRecord'] = record_match.group(2)
                elif 'Event Page' in line:
                    event_match = re.search(r'\[(.*?)\]', line)
                    if event_match:
                        fight_info['Event'] = event_match.group(1)
                elif re.search(r'\[\s*\d{4}\s+[A-Za-z]+\s+\d+\s*\]', line):
                    date_match = re.search(r'\[\s*(\d{4}\s+[A-Za-z]+\s+\d+)\s*\]', line)
                    if date_match:
                        fight_info['Date'] = date_match.group(1)
                elif 'Round' in line and 'Time' in line:
                    round_time = line.split('·')
                    if len(round_time) > 1:
                        fight_info['Round'] = round_time[0].strip()
                        fight_info['Time'] = round_time[1].strip()
                elif 'Weight' in line:
                    weight_parts = line.split('·')
                    if len(weight_parts) > 1:
                        fight_info['WeightClass'] = weight_parts[0].strip()
                        weigh_in = weight_parts[1].strip()
                        if 'Weigh-In:' in weigh_in:
                            fight_info['WeighIn'] = weigh_in.split(':')[1].strip()
                elif 'Location' in line:
                    location_parts = line.split('·')
                    if len(location_parts) > 1:
                        fight_info['Location'] = location_parts[0].strip()
                        fight_info['Venue'] = location_parts[1].strip()
                elif any(x in line for x in ['Favorite', 'Underdog', 'Even']):
                    odds_match = re.search(r'([+-]\d+)\s+([^P]+)', line)
                    if odds_match:
                        fight_info['Odds'] = f"{odds_match.group(1)} {odds_match.group(2).strip()}"
                elif 'Referee:' in line:
                    ref_match = re.search(r'Referee:\s*(.+)', line)
                    if ref_match:
                        fight_info['Referee'] = ref_match.group(1)
            fight_data.append(fight_info)
        except Exception as e:
            print(f"Error parsing fight section: {str(e)}")
            continue
    return fight_data
def clean_and_format_data(fight_data):
    cleaned_data = []
    for fight in fight_data:
        cleaned_fight = {k: v if v is not None else 'N/A' for k, v in fight.items()}
        cleaned_data.append(cleaned_fight)
    return cleaned_data
def process_fight_data(directory_path):
    fight_data = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.md'):
            file_path = os.path.join(directory_path, file_name)
            fight_data.extend(extract_fight_data_from_md(file_path))
    cleaned_fight_data = clean_and_format_data(fight_data)
    df_fight_data = pd.DataFrame(cleaned_fight_data)
    key_columns = ['Opponent', 'OpponentRecord', 'Event', 'Date', 'Round', 'Time', 
                   'WeightClass', 'WeighIn', 'Location', 'Venue', 'Odds', 'Referee']
    df_fight_data = df_fight_data[df_fight_data[key_columns].ne('N/A').any(axis=1)]
    df_fight_data.to_csv('data/master_fighters_fights_ufc.csv', index=False)
    print(f"Total number of fights: {len(df_fight_data)}")
    return df_fight_data
directory_path_md = 'data/tapology-fighters-ufc/'  
df_fight_data = process_fight_data(directory_path_md)
print("Saved to data/master_fighters_fights_ufc.csv")
# print(df_fight_data)
