import numpy as np
import pandas as pd

offensive_data = pd.read_csv('offensive_data.csv')
defensive_data = pd.read_csv('defensive_data.csv')

'''
Stats() provides a quick way to get the outcomes of each team's seasons (x) and the desired stat for 
comparison (y) in a comma-separated list.
'''

def stats(side: pd.DataFrame, outcome: str, stat: str) -> np.array:
    '''
    :param side: 'offense' or 'defense'
    :param outcome: 'W' or 'L'
    :param stat: Any statistical category (reference scraped_dats for all stat abbreviations)
    :return: 2xN dimensional array
    '''
    return np.array([side[outcome], side[stat]])