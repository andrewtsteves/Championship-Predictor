import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import time

'''
Data is being scraped from the NFL website. The website itself is broken up into offense and defense, then passing and
rushing for both sides of the ball. The data is given as data frames broken up into offensive and defensive tables,
with passing stats represented first (left most), and rushing stats represented second (right most). The distinction 
comes when attempts (Att) is repeated the first time. Wins, losses, ties, and win percentage will be placed in the
first 3 columns of the table. 
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

omitted_stats = ['PF', 'PA', 'Net Pts', 'Home', 'Road', 'Div',
                  'Pct', 'Conf', 'Pct', 'Non-Conf', 'Strk', 'Last 5', 'Pct.1']

'''
years = ['2025', '2024', '2023', '2022',
         '2021', '2020', '2019', '2018',
         '2017', '2016', '2015', '2014',
         '2013', '2012', '2011', '2010',
         '2009', '2008', '2007', '2006',
         '2005', '2004', '2003', '2002']
'''
years = ['2025', '2021', '2019']

#Only looking at either passing or rushing currently
part_of_game = ['Passing', 'Rushing']

start_time = time.time()

dfs_win_loss_tie = []

for year in years:
    if year == '2021':
        teams[teams.index('Commanders')] = 'Football Team'
        teams.sort()
    elif year == '2019':
        teams[teams.index('Football Team')] = 'Redskins'
        teams.sort()

    url = f'https://www.nfl.com/standings/league/{year}/REG'
    df = pd.read_html(url)[0]
    #df = df.drop(columns = 'NFL Team')

    df = df.drop(columns = omitted_stats)
    dfs_win_loss_tie.append(df)
    print(df.to_string())




'''
#Offensive Stats
dfs_offense = []
for year in years:

    # Handling the Washington Commanders name Changes in 2019 and 2021
    if year == '2025':
        teams[teams.index('Redskins')] = 'Commanders'
    if year == '2021':
        teams[teams.index('Commanders')] = 'Football Team'
        teams.sort()
    elif year == '2019':
        teams[teams.index('Football Team')] = 'Redskins'
        teams.sort()

    #List of both offensive passing and rushing stats from each team in one year.
    df_offensive_stats = []
    for type in part_of_game:
        url = f'https://www.nfl.com/stats/team-stats/offense/{type}/{year}/reg/all'
        df = pd.read_html(url)[0]
        df = df.sort_values(by = 'Team')
        df.index = teams
        df = df.drop(columns = 'Team')
        #df.index = teams
        df_offensive_stats.append(df)
    df_all_offensive_stats = pd.concat([df_offensive_stats[0], df_offensive_stats[1]], axis = 1)
    #Indices of each element of df_offensive_stats can be left as either 0 or 1 because this is only looking at either
    #passing or rushing.

    dfs_offense.append(df_all_offensive_stats)



#Denensive Stats
dfs_defense = []
for year in years:

    # Handling the Washington Commanders name Changes in 2019 and 2021
    if year == '2025':
        teams[teams.index('Redskins')] = 'Commanders'
    if year == '2021':
        teams[teams.index('Commanders')] = 'Football Team'
        teams.sort()
    elif year == '2019':
        teams[teams.index('Football Team')] = 'Redskins'
        teams.sort()


    #List of both offensive passing and rushing stats from each team in one year.
    df_defensive_stats = []
    for type in part_of_game:
        url = f'https://www.nfl.com/stats/team-stats/defense/{type}/{year}/reg/all'
        df = pd.read_html(url)[0]
        df = df.sort_values(by='Team')
        df.index = teams
        df = df.drop(columns = 'Team')
        #df.index = teams
        df_defensive_stats.append(df)
    df_all_offensive_stats = pd.concat([df_defensive_stats[0], df_defensive_stats[1]], axis = 1)

    dfs_defense.append(df_all_offensive_stats)
'''

#offensive_data = pd.concat(dfs_offense)
#defensive_data = pd.concat(dfs_defense)

#Uncomment each file to save it to directory
#offensive_data.to_csv('offensive_data.csv')
#defensive_data.to_csv('defensive_data.csv')

print(f"{(time.time() - start_time):3f} seconds")