import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from localutils.dataload import covidtracking_ustates
#import fitderivpackage.gaussianprocess as gp
from fitderivpackage.fitderiv import fitderiv
import pickle

# ===== Get covidtracking data for the us states
(states_df, states_info) = covidtracking_ustates()

# Let's handle each state as an individual df and save them in a dict
state_ids = states_df.state.unique()
dfs = {}
for state in state_ids:
    df = states_df[states_df['state'] == state].sort_values('date', ascending=True)
    df['tests'] = df['positive'] + df['negative']
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
    dfs[state] = df

states_df_rates = pd.concat(dfs.values())
    
with open("analyzed_data/covidtracking_states_df_rates.pickle", "wb") as file:
    pickle.dump(states_df_rates, file)

