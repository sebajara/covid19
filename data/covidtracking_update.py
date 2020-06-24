import requests
import pandas as pd
import pickle

# Check the website for more information
covidtracking_api = 'https://covidtracking.com/api/v1/'
covidtracking_json_urls = dict(states='states',
                               states_daily='states/daily',
                               states_info='states/info',
                               us='us',
                               us_daily='us/daily')
# NOTE JUN/24/2020: Seems like counties and urls datasets are no longer
# part of the api
#counties='counties',
#urls='urls'

dataframes = {}
for id, url in covidtracking_json_urls.items():
    data = requests.get(covidtracking_api+url+'.json').json()
    dataframes[id] = pd.DataFrame(data)
covidtracking_dfs = dataframes

with open("covidtracking/covidtracking_dfs.pickle", "wb") as file:
    pickle.dump(covidtracking_dfs, file)
