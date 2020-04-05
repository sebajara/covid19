import wget
import pandas as pd
import pickle

# From:
# https://github.com/nytimes/covid-19-data/
wget.download('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv',
              'nytimes_covid19/us-states.csv')
wget.download('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv',
              'nytimes_covid19/us-counties.csv')

nytimes_dfs = {}
nytimes_dfs['states'] = pd.read_csv('nytimes_covid19/us-states.csv')
nytimes_dfs['counties'] = pd.read_csv('nytimes_covid19/us-counties.csv')

with open("nytimes_covid19/nytimes_dfs.pickle", "wb") as file:
    pickle.dump(nytimes_dfs, file)
