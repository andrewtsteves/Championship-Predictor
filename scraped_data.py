import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import time

'''
Data is being scraped from the NFL website. The website itself is broken up into offense and defense, then passing and
rushing for both sides of the ball. Right now, I am only focusing on scraping offensive passing data from the 2025 NFL 
season.
'''

'''
Use the following import of the data to check if the import is functioning correctly
r = req.get('https://www.nfl.com/stats/team-stats/offense/passing/2025/reg/all')
'''
teams = ['49ers', 'Bears', 'Bengals', 'Bills',
         'Broncos', 'Browns', 'Buccaneers', 'Cardinals',
         'Chargers', 'Chiefs', 'Colts', 'Commanders',
         'Cowboys', 'Dolphins', 'Eagles','Falcons',
         'Giants', 'Jaguars', 'Jets', 'Lions',
         'Packers', 'Panthers', 'Patriots', 'Raiders',
         'Rams', 'Ravens', 'Saints', 'Seahawks',
         'Steelers', 'Texans', 'Titans', 'Vikings']

#Stats for both offensive and defensive rushing and passing are the same
passing_stats = ['Att', 'Cmp', 'Cmp %', 'Yds/Att',
         'Pass Yds', 'TD', 'INT',
         'Rate', '1st',
         '1st %', '20+',
         '40+', 'Lng',
         'Sck', 'SckY']

rushing_stats = ['Att', 'Rush Yds', 'YPC', 'TD',
                 '20+', '40+', 'Lng', 'Rush 1st', 'Rush 1st%',
                 'Rush FUM']

years = ['2025', '2024', '2023', '2022']

#Only looking at either passing or rushing currently
part_of_game = ['Passing', 'Rushing']

starttime = time.time()

dfs = []

#Offensive Stats
for year in years:
    #List of both offensive passing and rushing stats from each team in one year.
    df_offenseive_stats = []
    for type in part_of_game:
        url = f'https://www.nfl.com/stats/team-stats/offense/{type}/{year}/reg/all'
        df = pd.read_html(url)[0]
        df.index = df['Team']
        df = df.drop(columns = 'Team')
        df = df.sort_values(by = 'Team')
        df_offenseive_stats.append(df)
        #print(df)
    df_all_offensive_stats = pd.concat([df_offenseive_stats[0], df_offenseive_stats[1]], axis = 1)
    #Indices of each element of df_offenseive_stats can be left as either 0 or 1 because this is only looking at either
    #passing or rushing.
    dfs.append(df_all_offensive_stats)



data = pd.concat(dfs)
print(data.to_string())

print(f"{(time.time() - starttime):3f} seconds")
