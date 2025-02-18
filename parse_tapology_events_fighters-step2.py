import os
import pandas as pd
from bs4 import BeautifulSoup
import re
def extract_fighter_details_updated(soup):
    fighter_details = {
        "Given Name": None,
        "Nickname": None,
        "Pro MMA Record": None,
        "Current MMA Streak": None,
        "Age": None,
        "Date of Birth": None,
        "Height": None,
        "Reach": None,
        "Weight Class": None,
        # "Last Weigh-In": None,
        "Affiliation": None,
        "Last Fight": None,
        "Career Disclosed Earnings": None,
        "Born": None,
        "Fighting out of": None,
        "Fighter Name": None
    }
    labels = {
        "Given Name": "Given Name:",
        "Nickname": "Nickname:",
        "Pro MMA Record": "Pro MMA Record:",
        "Current MMA Streak": "Current MMA Streak:",
        "Age": "Age:",
        "Date of Birth": "| Date of Birth:",
        "Height": "Height:",
        "Reach": "Reach:",
        "Weight Class": "Weight Class:",
        # "Last Weigh-In": "Last Weigh-In:",
        "Affiliation": "Affiliation:",
        "Last Fight": "Last Fight:",
        "Career Disclosed Earnings": "Career Disclosed Earnings:",
        "Born": "Born:",
        "Fighting out of": "Fighting out of:"
    }
    for key, label in labels.items():
        element = soup.find(string=label)
        if element:
            parent = element.find_parent()
            value = parent.find_next_sibling('div') or parent.find_next_sibling('span')
            if value:
                value_text = value.get_text(strip=True)
                if key == "Height" and "(" in value_text and ")" in value_text:
                    height_match = re.match(r"(\d+'[\d\"]*)\s\((\d+cm)\)", value_text)
                    if height_match:
                        fighter_details["Height"] = height_match.group(1)
                        fighter_details["Reach"] = height_match.group(2)
                    else:
                        fighter_details["Height"] = value_text  
                else:
                    fighter_details[key] = value_text
    return fighter_details
    # return fighter_details
directory_path = 'data/tapology-fighters-ufc/'  
all_fighter_details = []
for filename in os.listdir(directory_path):
    if filename.endswith('.html'):
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
        fighter_details = extract_fighter_details_updated(soup)
        fighter_details["Fighter Name"] = filename.replace('.html', '')  
        all_fighter_details.append(fighter_details)
fighters_df = pd.DataFrame(all_fighter_details)
fighters_df.to_csv('data/master_fighters_ufc.csv', index=False)
print("Fighter details saved to 'master_fighters_ufc.csv'")
