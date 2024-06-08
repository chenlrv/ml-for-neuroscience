import requests
import pandas as pd
from bs4 import BeautifulSoup

metadata_df = pd.read_csv('metadata.tsv', delimiter='\t')
unique_journals = set(metadata_df['journal'].unique())
journals_set = {journal.lower() for journal in unique_journals}
journals_data = []
journals_found = set()

response = requests.get('https://exaly.com/journals/citations')
soup = BeautifulSoup(response.content, 'html.parser')
pages_number = 5417

for i in range(1, pages_number):
   table = soup.find('table')  

   for row in table.find_all('tr'):
        cells = list(row.find_all('td'))
        journal_name = cells[1].get_text()
        journal_name_lower = journal_name.lower()

        if (journal_name_lower in journals_set) & (not journal_name in journals_found):
            impact_factor = float(cells[4].get_text().replace(',', ''))
            h_index  = int(cells[5].get_text().replace(',', ''))

            journals_data.append({
                'journal': journal_name,
                'journal_impact_factor': impact_factor,
                'journal_h_index': h_index
            })
            journals_found.add(journal_name)

   url = f'https://exaly.com/journals/citations/{i}'
   response = requests.get(url)
   soup = BeautifulSoup(response.content, 'html.parser')
        

journals_df = pd.DataFrame(journals_data)
journals_df.to_csv('journals.csv')     