import pandas as pd
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

    def update_hyperlinks(self, filepath, start_date, end_date):
        # Load the DataFrame from the given Excel file
        hyper_df = pd.read_excel(filepath)
        hyper_df['Date'] = pd.to_datetime(hyper_df['Date'])  # Ensure Date column is in datetime format
        
        # Filter the DataFrame based on the provided date range
        filtered_df = hyper_df[(hyper_df['Date'] >= pd.to_datetime(start_date)) & (hyper_df['Date'] <= pd.to_datetime(end_date))]
        
        # Process each row in the filtered DataFrame to extract hyperlinks
        for index, row in filtered_df.iterrows():
            url = row['Link']
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'lxml')
                    links = [urljoin(url, tag.get('href', '')) for tag in soup.find_all('a', href=True)]
                    links_str = '; '.join(links)  # Join all links with a semicolon
                    hyper_df.at[index, 'Hyperlinks'] = links_str  # Update the DataFrame
            except requests.RequestException as e:
                print(f"Failed to retrieve {url}: {str(e)}")

        # Convert Date column back to string format without time component
        hyper_df['Date'] = hyper_df['Date'].dt.strftime('%Y-%m-%d')
        
        # Save the updated DataFrame back to the same Excel file
        hyper_df.to_excel(filepath, index=False)
        print(f"Updated Excel file saved to {filepath}")

    # Other methods...

# Example usage:
scraper = ResmiGazeteScraper(year=2022)
scraper.update_hyperlinks('path_to_your_excel_file.xlsx', '2022-01-01', '2022-12-31')
