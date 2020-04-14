import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from localutils.dataload import covidtracking_ustates
#import fitderivpackage.gaussianprocess as gp
from fitderivpackage.fitderiv import fitderiv
import pickle

# ===== Get covidtracking data for the us states
(states_df, states_info) = covidtracking_ustates()
states_info.set_index('abbreviation',inplace=True)

# Let's handle each state as an individual df and save them in a dict
state_ids = states_df.state.unique()
dfs = {}
for state in state_ids:
    df = states_df[states_df['state'] == state].sort_values('date', ascending=True)
    df['tests'] = df['positive'] + df['negative']
    population = states_info.loc[state, 'POPESTIMATE2019']
    df['posperpop'] = 1e06*df['positive']/population
    #df.set_index('date', inplace=True)
    #df.drop(columns=['state'], inplace=True)
    dates = df['date'].values
    t = (dates - dates[0])/np.timedelta64(1, 'D')
    for col in df.columns:
        if((col == 'date') | (col == 'state')):
            continue
        y = df[col].values
        pos = y>0  # to avoid nan and 0 values
        # NOTE: for now looks ok. Fine tuning? How should approach it? 
        df['log_'+col] = np.nan
        df['log_'+col+'_err'] = np.nan
        df['gr_'+col] = np.nan
        df['gr_'+col+'_err'] = np.nan
        if(np.sum(y[pos]) > 0): 
            q = fitderiv(t[pos], y[pos], cvfn='sqexp', stats=False, esterrs=False)
            df.loc[pos, 'log_'+col] = q.f
            df.loc[pos, 'log_'+col+'_err'] = np.sqrt(q.fvar)
            df.loc[pos, 'gr_'+col] = np.sqrt(q.df)
            df.loc[pos, 'gr_'+col+'_err'] = np.sqrt(q.dfvar)    
    # rate of positive v/s tests
    y = df['positive'].values
    x = df['tests'].values
    pos = (y>0) & (x>0)  # to avoid nan and 0 values
    col = 'positive_tests'
    df['gr_'+col] = np.nan
    df['gr_'+col+'_err'] = np.nan
    if(np.sum(y[pos]) > 0):
        norm = np.mean(y[pos])  # given the way the parameters are designed it is
        # easier to scale them. I believe should not matter as
        # we are not taking the log, just the relative variation.
        q = fitderiv(x[pos]/norm, y[pos]/norm,
                     cvfn='sqexp',
                     stats=False, esterrs=False, logs=False)  # 
        df.loc[pos, 'gr_'+col] = np.sqrt(q.df)
        df.loc[pos, 'gr_'+col+'_err'] = np.sqrt(q.dfvar)
    y = df['death'].values
    x = df['positive'].values
    pos = (y>0) & (x>0)  # to avoid nan and 0 values
    col = 'death_positive'
    df['gr_'+col] = np.nan
    df['gr_'+col+'_err'] = np.nan
    if(np.sum(y[pos]) > 0):
        norm = np.mean(y[pos])  # given the way the parameters are designed it is
        # easier to scale them. I believe should not matter as
        # we are not taking the log, just the relative variation.
        q = fitderiv(x[pos]/norm, y[pos]/norm,
                     cvfn='sqexp',
                     stats=False, esterrs=False, logs=False)  # 
        df.loc[pos, 'gr_'+col] = np.sqrt(q.df)
        df.loc[pos, 'gr_'+col+'_err'] = np.sqrt(q.dfvar)
    dfs[state] = df

states_df_rates = pd.concat(dfs.values())
    
with open("analyzed_data/covidtracking_states_df_rates.pickle", "wb") as file:
    pickle.dump(states_df_rates, file)

