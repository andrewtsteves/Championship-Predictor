import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

'''
Data is being scraped from the NFL website. The website itself is broken up into offense and defense, then passing and
rushing for both sides of the ball. The data is given as data frames broken up into offensive and defensive tables,
with passing stats represented first (left most), and rushing stats represented second (right most). The distinction 
comes when attempts (Att) is repeated the first time. Wins, losses, ties, and win percentage will be placed in the
first 3 columns of the table. There are multiple loops over the set years to separate offensive and defensive stats, as
as well as team records. For records, team names are given with city first. For team stats, team names are only team
names without the city. 
'''

'''
Use the following import of the data to check if the import is functioning correctly
r = req.get('https://www.nfl.com/stats/team-stats/offense/passing/2025/reg/all')
'''

teams = {'49ers': ['San Francisco 49ers 49ers', 'San Francisco 49ers49ers', 'San Francisco 49ersNiners',
                   'San Francisco 49ers Niners', '49ers49ers'],
         'Bears': ['Chicago BearsBears', 'Chicago Bears Bears', 'BearsBears'],
         'Bengals': ['Cincinnati BengalsBengals', 'Cincinnati Bengals Bengals', 'BengalsBengals'],
         'Bills': ['Buffalo Bills Bills', 'Buffalo BillsBills', 'BillsBills'],
         'Broncos': ['Denver Broncos Broncos', 'Denver BroncosBroncos', 'BroncosBroncos'],
         'Browns': ['Cleveland BrownsBrowns', 'Cleveland Browns Browns', 'BrownsBrowns'],
         'Buccaneers': ['Tampa Bay Buccaneers Buccaneers', 'Tampa Bay BuccaneersBuccaneers', 'BuccaneersBuccaneers'],
         'Cardinals': ['Arizona CardinalsCardinals', 'Arizona Cardinals Cardinals', 'CardinalsCardinals'],
         'Chargers': ['Los Angeles Chargers Chargers', 'Los Angeles ChargersChargers', 'ChargersChargers'],
         'Chiefs': ['Kansas City ChiefsChiefs', 'Kansas City Chiefs Chiefs', 'ChiefsChiefs'],
         'Colts': ['Indianapolis Colts Colts', 'Indianapolis ColtsColts', 'ColtsColts'],
         'Commanders': ['Washington CommandersCommanders', 'Washington Commanders Commanders', 'CommandersCommanders',
                        'Washington CommandersFootball Team', 'Washington Commanders Football Team', 'Football TeamFootball Team',
                        'Washington CommandersRedskins', 'Washington Commanders Redskins', 'RedskinsRedskins'],
         'Cowboys': ['Dallas CowboysCowboys', 'Dallas Cowboys Cowboys', 'CowboysCowboys'],
         'Dolphins': ['Miami DolphinsDolphins', 'Miami Dolphins Dolphins', 'DolphinsDolphins'],
         'Eagles': ['Philadelphia Eagles Eagles', 'Philadelphia EaglesEagles', 'EaglesEagles'],
         'Falcons': ['Atlanta Falcons Falcons', 'Atlanta FalconsFalcons', 'FalconsFalcons'],
         'Giants': ['New York GiantsGiants', 'New York Giants Giants', 'GiantsGiants'],
         'Jaguars': ['Jacksonville Jaguars Jaguars', 'Jacksonville JaguarsJaguars', 'JaguarsJaguars'],
         'Jets': ['New York Jets Jets', 'New York JetsJets', 'JetsJets'],
         'Lions': ['Detroit Lions Lions', 'Detroit LionsLions', 'LionsLions'],
         'Packers': ['Green Bay Packers Packers', 'Green Bay PackersPackers', 'PackersPackers'],
         'Panthers': ['Carolina Panthers Panthers', 'Carolina PanthersPanthers', 'PanthersPanthers'],
         'Patriots': ['New England Patriots Patriots', 'New England PatriotsPatriots', 'PatriotsPatriots'],
         'Raiders': ['Las Vegas RaidersRaiders', 'Las Vegas Raiders Raiders', 'RaidersRaiders'],
         'Rams': ['Los Angeles Rams Rams', 'Los Angeles RamsRams', 'RamsRams'],
         'Ravens': ['Baltimore Ravens Ravens', 'Baltimore RavensRavens', 'RavensRavens'],
         'Saints': ['New Orleans Saints Saints', 'New Orleans SaintsSaints', 'SaintsSaints'],
         'Seahawks': ['Seattle Seahawks Seahawks', 'Seattle SeahawksSeahawks', 'SeahawksSeahawks'],
         'Steelers': ['Pittsburgh Steelers Steelers', 'Pittsburgh SteelersSteelers', 'SteelersSteelers'],
         'Texans': ['Houston Texans Texans', 'Houston TexansTexans', 'TexansTexans'],
         'Titans': ['Tennessee Titans Titans', 'Tennessee TitansTitans', 'TitansTitans'],
         'Vikings': ['Minnesota Vikings Vikings', 'Minnesota VikingsVikings', 'VikingsVikings']
         }

reverse_items = {v: k for k, vals in teams.items() for v in vals}

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

omitted_stats = ['NFL Team', 'PF', 'PA', 'Net Pts', 'Home', 'Road', 'Div',
                  'Pct', 'Conf', 'Pct', 'Non-Conf', 'Strk', 'Last 5', 'Pct.1']

years = {'2025': 'Seahawks', '2024': 'Eagles', '2023': 'Chiefs', '2022': 'Chiefs',
                     '2021': 'Rams', '2020': 'Buccaneers', '2019': 'Chiefs', '2018': 'Patriots',
                     '2017': 'Eagles', '2016': 'Patriots', '2015': 'Broncos', '2014': 'Patriots',
                     '2013': 'Seahawks', '2012': 'Ravens', '2011': 'Giants', '2010': 'Packers',
                     '2009': 'Saints', '2008': 'Steelers', '2007': 'Giants', '2006': 'Colts',
                     '2005': 'Steelers', '2004': 'Giants', '2003': 'Patriots', '2002': 'Patriots'
                     }
df = pd.DataFrame({'SB Winner': 0}, index = pd.Index(teams.keys(), name = 'Team'))
df.loc['49ers'] = 1



#Only looking at either passing or rushing currently
part_of_game = ['Passing', 'Rushing']

start_time = time.time()

#Records of all NFL teams from 2002-2025
dfs_win_loss_tie = []
for year in years.keys():
    url = f'https://www.nfl.com/standings/league/{year}/REG'
    #The website comes preloaded with NFL teams sorted by win percentage lowest to highest
    df = pd.read_html(url)[0]
    df['NFL Team'] = df['NFL Team'].str.replace(r'xz|xy|[*]', '', regex=True)
    df['NFL Team'] = df['NFL Team'].str.strip().replace(reverse_items)
    df = df.sort_values(by=['NFL Team'], ascending=True)
    df.index = teams
    df = df.drop(columns = omitted_stats)

    dfs_win_loss_tie.append(df)


def get_stats(side: str, valid_years: dict, NFL_teams: dict, reverse_items: dict) -> pd.DataFrame:
    '''
    Scraping offensive and defensive stats. Parameters:
    side: side of ball, either offense or defense
    valid_years: years desired, strings in dictionary
    reverse_items: reversed dictionary of teams with all entries as strings
    '''
    dfs = []
    for year in valid_years:
        # List of both offensive passing and rushing stats from each team in one year.
        year_stats = []
        for stat_type in part_of_game:
            url = f'https://www.nfl.com/stats/team-stats/{side}/{stat_type}/{year}/reg/all'
            df = pd.read_html(url)[0]
            df['Team'] = df['Team'].replace(reverse_items)
            df = df.sort_values(by=['Team'], ascending=True).set_index(pd.Index(NFL_teams.keys()))
            df = df.drop(columns='Team')
            year_stats.append(df)
        dfs.append(pd.concat(year_stats, axis = 1))
    return pd.concat(dfs, keys = valid_years.keys())

def get_superbowl_winners(valid_years: dict, NFL_teams: dict) -> pd.DataFrame:
    dfs = []
    for year, winner in valid_years.items():
        year_df = pd.DataFrame({'SB Winner': 0}, index=pd.Index(NFL_teams.keys(), name='Team'))
        year_df.loc[winner, 'SB Winner'] = 1
        dfs.append(year_df)
    return pd.concat(dfs, keys = valid_years.keys())

superbowl_winners = get_superbowl_winners(years, teams)

win_loss_tie = pd.concat(dfs_win_loss_tie, keys = years.keys())
offensive_stats = get_stats('offense', years, teams, reverse_items)
defensive_stats = get_stats('defense', years, teams, reverse_items)

offensive_data = pd.concat([win_loss_tie, superbowl_winners, offensive_stats], axis = 1)
defensive_data = pd.concat([win_loss_tie, superbowl_winners, offensive_stats], axis = 1)

#Uncomment each file to save it to directory
offensive_data.to_csv('offensive_data.csv')
defensive_data.to_csv('defensive_data.csv')

print(f"{(time.time() - start_time):3f} seconds")