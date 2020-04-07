import pandas as pd
import numpy as np
import pickle
from us import states


def covidtracking_ustates():
    ## ========== Import
    # import covidtracking data
    # see: data/covidtracking_update.py
    with open("../data/covidtracking/covidtracking_dfs.pickle", "rb") as file:
        covidtracking_dfs = pickle.load(file)
    state_census = pd.read_csv('../data/usa_census/SCPRC-EST2019-18+POP-RES.csv')
    ## ========== Cleaning
    # convert date to datetime 
    tables = ['states_daily']  # see covidtracking_dfs.keys()
    for table in tables:
        covidtracking_dfs[table]['date'] = pd.to_datetime(covidtracking_dfs[table]['date'], format="%Y%m%d")
    # we are goint to use for now just a few columns
    columns = ['state', 'date', 'negative', 'positive', 'death']
    states_df = covidtracking_dfs['states_daily'].loc[:, columns]
    # Let's get the estimated 2019 population for each state 
    state_abrs = states_df['state'].unique()
    state_names = [states.lookup(abr).name for abr in list(state_abrs)]
    states_info = pd.DataFrame(dict(abbreviation=state_abrs, name=state_names))
    states_info = states_info.merge(state_census.loc[:, ['NAME', 'POPESTIMATE2019']], right_on='NAME', left_on='name',how='left').sort_values('POPESTIMATE2019')
    states_info.drop(columns=['NAME'], inplace=True)
    return(states_df, states_info)


