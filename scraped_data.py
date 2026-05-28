import requests as req
from bs4 import BeautifulSoup
import pandas as pd

'''
Data is being scraped from the NFL website. The website itself is broken up into offense and defense, then passing and
rushing for both sides of the ball. Right now, I am only focusing on scraping offensive passing data from the 2025 NFL 
season.
'''

'''
Use the following import of the data to check if the import is functioning correctly
r = req.get('https://www.nfl.com/stats/team-stats/offense/passing/2025/reg/all')
'''


years = ['2024',
         '2025']

for year in years:
    url = f'https://www.nfl.com/stats/team-stats/offense/passing/{year}/reg/all'
    df = pd.read_html(url)
    print(df)

