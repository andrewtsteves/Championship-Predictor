import numpy as np
import pandas as pd

offensive_data = pd.read_csv('offensive_data.csv')
defensive_data = pd.read_csv('defensive_data.csv')

def stats(side: pd.DataFrame, outcome: str, stat: str):
    return [side[outcome].to_list(), side[stat].to_list()]

attempts = stats(offensive_data, 'W', 'Att')
cmp = stats(offensive_data, 'W', 'Cmp')
passyds = stats(offensive_data, 'W', 'Pass Yds')