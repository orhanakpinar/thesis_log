import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ResmiGazeteScraper:
    def __init__(self, year):
        self.base_url = 'https://www.resmigazete.gov.tr/eskiler'
        self.year = str(year)
        self.months = [f"{month:02d}" for month in range(1, 13)]
        self.days = [f"{day:02d}" for day in range(1, 32)]
        self.content = ""
        self.last_url = None
        self.last_xpath = None
        self.data = []
        self.df = pd.DataFrame()  # Initialize an empty DataFrame
    def parse_to_dataframe(self):
        lines = self.content.strip().split('\n')
        current_entry = None
        
        for line in lines:
            # Use regex to correctly split the line into key-value pairs
            parts = re.split(r', (?=\b(?:Date|XPath|Tag|Text|Link)\b)', line.strip())
            entry = {key.strip(): value.strip() for part in parts for key, value in [part.split(': ', 1)]}
            
            # Manage appending or creating new entries based on the link continuity
            if current_entry and entry.get('Link') == current_entry.get('Link'):
                # If the same link, concatenate the text
                current_entry['Text'] += " " + entry['Text']
            else:
                # If a different link or a new line, append the current entry and start a new one
                if current_entry:
                    self.data.append(current_entry)
                current_entry = entry
        
        # Ensure the last entry is added
        if current_entry:
            self.data.append(current_entry)
        
        # Create DataFrame from the list of dictionaries
        self.df = pd.DataFrame(self.data)
    def read_and_process_excel(self, filepath):
        df = pd.read_excel(filepath)
        htm_links = df[df['Hyperlinks'].str.endswith(".htm", na=False)]

        for index, row in htm_links.iterrows():
            url = row['Hyperlinks']
            try:
                response = requests.get(url)
                time.sleep(1)  # Delay to avoid hammering the server
                if response.status_code == 200:
                    with open(f"scraped_content_{index}.txt", "w", encoding='utf-8') as file:
                        file.write(response.text)
                        print(f"Saved content from {url} to scraped_content_{index}.txt")
            except requests.RequestException as e:
                print(f"Failed to retrieve content from {url}: {str(e)}")
# Example usage
scraper = ResmiGazeteScraper(year=2022)
scraper.read_and_process_excel('resmigazete_links_2022.xlsx')
