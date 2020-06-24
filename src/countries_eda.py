import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from localutils.plotutils import local_axes_formatting
from localutils.plotutils import figsaveandclose
from localutils.plotutils import get_list_colors
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

world_df = pd.read_csv('../data/ecdc/ecdc_data.csv')
world_df['dateRep'] = pd.to_datetime(world_df['dateRep'], format="%d/%m/%Y")
world_df.drop(columns=['day', 'month', 'year'], inplace=True)

# Calculate cumulatives
world_df['total_cases'] = np.nan
world_df['total_deaths'] = np.nan
names = world_df['countriesAndTerritories'].unique()
for name in names:
    sdf = world_df[world_df['countriesAndTerritories'] == name].sort_values('dateRep', ascending=True)
    ind = sdf.index
    csum_cases = np.cumsum(sdf['cases'])
    csum_deaths = np.cumsum(sdf['deaths'])
    per_per_cap = 100*csum_cases/sdf['popData2019'].iloc[0]
    per_per_cap2 = 100*csum_deaths/sdf['popData2019'].iloc[0]
    world_df.loc[ind, 'total_cases'] = csum_cases
    world_df.loc[ind, 'total_deaths'] = csum_deaths
    world_df.loc[ind, 'cases_per_cap'] = per_per_cap
    world_df.loc[ind, 'deaths_per_cap'] = per_per_cap2

max_death = world_df['total_deaths'].max()
max_pop = world_df['popData2019'].max()
max_cases = world_df['total_cases'].max()
dates = np.sort(world_df['dateRep'].unique())
min_date = dates.min()
max_date = dates.max()

#countries = world_df[world_df['total_cases']>1e04]['countriesAndTerritories'].unique()

countries = world_df['countriesAndTerritories'].unique()
colors = get_list_colors('rainbow', len(countries))

countries2id = pd.DataFrame(world_df.groupby('countriesAndTerritories')['geoId'].max())
countries2abr = pd.DataFrame(world_df.groupby('countriesAndTerritories')['countryterritoryCode'].max())

topn = 20
maxx = np.max(world_df['dateRep'].unique()-min_date)/np.timedelta64(1, 'D')

maxy = 1e07
miny = 100
hlcountries = world_df.groupby('countriesAndTerritories')['total_cases'].max().sort_values(ascending=True).index[-topn:].values
legendys = np.logspace(np.log10(miny), np.log10(maxy), len(hlcountries)+2)
fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(11, 10))
for (i, country) in enumerate(countries):
    sdf = world_df[world_df['countriesAndTerritories'] == country].sort_values('dateRep', ascending=True)
    days = pd.Series((sdf['dateRep'] - min_date).values/np.timedelta64(1, 'D'))
    yval = sdf['total_cases']
    if(country in hlcountries):
        color = colors[i]
        abr = countries2abr.loc[country, 'countryterritoryCode']
        ind = np.where(hlcountries == country)[0][0]
        axes.text(1.1*maxx, legendys[ind+1], str(topn-ind)+'. '+abr,
                  horizontalalignment='left', verticalalignment='center', fontsize=14)
        plt.arrow(maxx, sdf['total_cases'].iloc[-1],
                  0.04*maxx, legendys[ind+1]-sdf['total_cases'].iloc[-1],
                  clip_on=False, shape='right', color=color)
        geoid = countries2id.loc[country, 'geoId'].lower()
        if(geoid == 'uk'):
            geoid = 'gb'
        flagpath = 'circle-flags/flags/'+ geoid +'.png'
        if(not os.path.isfile(flagpath)):
            print(flagpath)
        flagimg = mpimg.imread(flagpath)
        zoom = 0.05
        im = OffsetImage(flagimg, zoom=zoom)
        ab = AnnotationBbox(im, (1.06*maxx, legendys[ind+1]), xycoords='data',
                            frameon=False, annotation_clip=False)
        axes.add_artist(ab)
    else:
        color = (0.8, 0.8, 0.8, 0.3)
    sizes = 2
    axes.plot(days, sdf['total_cases'], 'o-', c=color, markersize=sizes, markeredgecolor=color)
local_axes_formatting(axes, "Days since 2020", "Total Positive Cases", xlim1=50, xlim2=maxx, ylim1=miny, ylim2=maxy, logx=False, fs=20)
axes.set_title('Top 20 countries in total positive cases', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
figsaveandclose(fig, output="../figures/eda_ecdc_countries_total_cases.png")

hlcountries = world_df.groupby('countriesAndTerritories')['total_deaths'].max().sort_values(ascending=True).index[-topn:].values
maxy = 1e06
miny = 10
legendys = np.logspace(np.log10(miny), np.log10(maxy), len(hlcountries)+2)
fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(11, 10))
for (i, country) in enumerate(countries):
    sdf = world_df[world_df['countriesAndTerritories'] == country].sort_values('dateRep', ascending=True)
    days = pd.Series((sdf['dateRep'] - min_date).values/np.timedelta64(1, 'D'))
    yval = sdf['total_deaths']
    if(country in hlcountries):
        color = colors[i]
        abr = countries2abr.loc[country, 'countryterritoryCode']
        ind = np.where(hlcountries == country)[0][0]
        axes.text(1.1*maxx, legendys[ind+1], str(topn-ind)+'. '+abr,
                  horizontalalignment='left', verticalalignment='center', fontsize=14)
        plt.arrow(maxx, yval.iloc[-1],
                  0.04*maxx, legendys[ind+1]-yval.iloc[-1],
                  clip_on=False, shape='right', color=color)
        geoid = countries2id.loc[country, 'geoId'].lower()
        if(geoid == 'uk'):
            geoid = 'gb'
        flagpath = 'circle-flags/flags/'+ geoid +'.png'
        if(not os.path.isfile(flagpath)):
            print(flagpath)
        flagimg = mpimg.imread(flagpath)
        zoom = 0.05
        im = OffsetImage(flagimg, zoom=zoom)
        ab = AnnotationBbox(im, (1.06*maxx, legendys[ind+1]), xycoords='data',
                            frameon=False, annotation_clip=False)
        axes.add_artist(ab)
    else:
        color = (0.8, 0.8, 0.8, 0.3)
    sizes = 2
    axes.plot(days, yval, 'o-', c=color, markersize=sizes, markeredgecolor=color)
local_axes_formatting(axes, "Days since 2020", "Total Reported Deaths", xlim1=50, xlim2=maxx, ylim1=miny, ylim2=maxy, logx=False, fs=20)
axes.set_title('Top 20 countries in total reported deaths', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
figsaveandclose(fig, output="../figures/eda_ecdc_countries_total_deaths.png")


