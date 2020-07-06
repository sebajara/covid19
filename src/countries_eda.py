import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from localutils.plotutils import local_axes_formatting
from localutils.plotutils import figsaveandclose
from localutils.plotutils import get_list_colors
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from scipy import stats

world_df = pd.read_csv('../data/ecdc/ecdc_data.csv')
world_df['dateRep'] = pd.to_datetime(world_df['dateRep'], format="%d/%m/%Y")
world_df.drop(columns=['day', 'month', 'year'], inplace=True)

# Calculate cumulatives
window = 7
world_df['total_cases'] = np.nan
world_df['total_deaths'] = np.nan
world_df['cases_rolling'] = np.nan
world_df['deaths_rolling'] = np.nan
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
    world_df.loc[ind, 'cases_rolling'] = sdf['cases'].rolling(window=window).mean()
    world_df.loc[ind, 'deaths_rolling'] = sdf['deaths'].rolling(window=window).mean()

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
    if((sdf['total_cases'] > 100).sum() > 0):
        zeroday = (sdf[sdf['total_cases'] > 100]['dateRep'].iloc[0]-min_date)/np.timedelta64(1, 'D')
    else:
        zeroday = days.max()
    yval = sdf['total_cases']
    deltadays = days-zeroday
    if(country in hlcountries):
        color = colors[i]
        abr = countries2abr.loc[country, 'countryterritoryCode']
        ind = np.where(hlcountries == country)[0][0]
        axes.text(1.1*maxx, legendys[ind+1], str(topn-ind)+'. '+abr,
                  horizontalalignment='left', verticalalignment='center', fontsize=14)
        plt.arrow(deltadays.max(), sdf['total_cases'].iloc[-1],
                  1.04*maxx-deltadays.max(), legendys[ind+1]-sdf['total_cases'].iloc[-1],
                  clip_on=False, shape='right', ls=':', color=color, alpha=0.75)
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
        color = (0.8, 0.8, 0.8, 0.5)
    sizes = 2
    axes.plot(deltadays, yval, 'o-', c=color, markersize=sizes, markeredgecolor=color)
local_axes_formatting(axes, "Days since reaching 100 cases", "Total Positive Cases", xlim1=0, xlim2=maxx, ylim1=miny, ylim2=maxy, logx=False, fs=20)
axes.set_title('Top 20 countries in total positive cases', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
#plt.show()
figsaveandclose(fig, output="../figures/eda_ecdc_countries_total_cases.png")

maxy = 1e05
miny = 10
hlcountries = world_df.sort_values('dateRep', ascending=True).groupby('countriesAndTerritories')['cases_rolling'].last().sort_values(ascending=True).index[-topn:].values
legendys = np.logspace(np.log10(miny), np.log10(maxy), len(hlcountries)+2)
fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(11, 10))
for (i, country) in enumerate(countries):
    sdf = world_df[world_df['countriesAndTerritories'] == country].sort_values('dateRep', ascending=True)
    days = pd.Series((sdf['dateRep'] - min_date).values/np.timedelta64(1, 'D'))
    if((sdf['total_cases'] > 100).sum() > 0):
        zeroday = (sdf[sdf['total_cases'] > 100]['dateRep'].iloc[0]-min_date)/np.timedelta64(1, 'D')
    else:
        zeroday = days.max()
    yval = sdf['cases_rolling']
    deltadays = days-zeroday
    if(country in hlcountries):
        color = colors[i]
        abr = countries2abr.loc[country, 'countryterritoryCode']
        ind = np.where(hlcountries == country)[0][0]
        axes.text(1.1*maxx, legendys[ind+1], str(topn-ind)+'. '+abr,
                  horizontalalignment='left', verticalalignment='center', fontsize=14)
        plt.arrow(deltadays.max(), yval.iloc[-1],
                  1.04*maxx-deltadays.max(), legendys[ind+1]-yval.iloc[-1],
                  clip_on=False, shape='right', ls=':', color=color, alpha=0.75)
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
        color = (0.8, 0.8, 0.8, 0.5)
    sizes = 2
    axes.plot(deltadays, yval, 'o-', c=color, markersize=sizes, markeredgecolor=color)
local_axes_formatting(axes, "Days since reaching 100 cases", "New cases per day (7 days rolling average)", xlim1=0, xlim2=maxx, ylim1=miny, ylim2=maxy, logx=False, fs=20)
axes.set_title('Top 20 countries in positive cases per day', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
#plt.show()
figsaveandclose(fig, output="../figures/eda_ecdc_countries_new_cases.png")

hlcountries = world_df.groupby('countriesAndTerritories')['total_deaths'].max().sort_values(ascending=True).index[-topn:].values
maxy = 1e06
miny = 10
legendys = np.logspace(np.log10(miny), np.log10(maxy), len(hlcountries)+2)
fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(11, 10))
for (i, country) in enumerate(countries):
    sdf = world_df[world_df['countriesAndTerritories'] == country].sort_values('dateRep', ascending=True)
    days = pd.Series((sdf['dateRep'] - min_date).values/np.timedelta64(1, 'D'))
    days = pd.Series((sdf['dateRep'] - min_date).values/np.timedelta64(1, 'D'))
    if((sdf['total_deaths'] > 10).sum() > 0):
        zeroday = (sdf[sdf['total_deaths'] > 10]['dateRep'].iloc[0]-min_date)/np.timedelta64(1, 'D')
    else:
        zeroday = days.max()
    yval = sdf['total_deaths']
    deltadays = days-zeroday
    if(country in hlcountries):
        color = colors[i]
        abr = countries2abr.loc[country, 'countryterritoryCode']
        ind = np.where(hlcountries == country)[0][0]
        axes.text(1.1*maxx, legendys[ind+1], str(topn-ind)+'. '+abr,
                  horizontalalignment='left', verticalalignment='center', fontsize=14)
        plt.arrow(deltadays.max(), yval.iloc[-1],
                  1.04*maxx-deltadays.max(), legendys[ind+1]-yval.iloc[-1],
                  clip_on=False, shape='right', ls=':', color=color, alpha=0.75)
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
        color = (0.8, 0.8, 0.8, 0.5)
    sizes = 2
    axes.plot(deltadays, yval, 'o-', c=color, markersize=sizes, markeredgecolor=color)
local_axes_formatting(axes, "Days since reaching 10 deaths", "Total Reported Deaths", xlim1=0, xlim2=maxx, ylim1=miny, ylim2=maxy, logx=False, fs=20)
axes.set_title('Top 20 countries in total reported deaths', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
figsaveandclose(fig, output="../figures/eda_ecdc_countries_total_deaths.png")

maxy = 5e03
miny = 1
hlcountries = world_df.sort_values('dateRep', ascending=True).groupby('countriesAndTerritories')['deaths_rolling'].last().sort_values(ascending=True).index[-topn:].values
legendys = np.logspace(np.log10(miny), np.log10(maxy), len(hlcountries)+2)
fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(11, 10))
for (i, country) in enumerate(countries):
    sdf = world_df[world_df['countriesAndTerritories'] == country].sort_values('dateRep', ascending=True)
    days = pd.Series((sdf['dateRep'] - min_date).values/np.timedelta64(1, 'D'))
    days = pd.Series((sdf['dateRep'] - min_date).values/np.timedelta64(1, 'D'))
    if((sdf['total_deaths'] > 10).sum() > 0):
        zeroday = (sdf[sdf['total_deaths'] > 10]['dateRep'].iloc[0]-min_date)/np.timedelta64(1, 'D')
    else:
        zeroday = days.max()
    yval = sdf['deaths_rolling']
    deltadays = days-zeroday
    if(country in hlcountries):
        color = colors[i]
        abr = countries2abr.loc[country, 'countryterritoryCode']
        ind = np.where(hlcountries == country)[0][0]
        axes.text(1.1*maxx, legendys[ind+1], str(topn-ind)+'. '+abr,
                  horizontalalignment='left', verticalalignment='center', fontsize=14)
        plt.arrow(deltadays.max(), yval.iloc[-1],
                  1.04*maxx-deltadays.max(), legendys[ind+1]-yval.iloc[-1],
                  clip_on=False, shape='right', ls=':', color=color, alpha=0.75)
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
        color = (0.8, 0.8, 0.8, 0.5)
    sizes = 2
    axes.plot(deltadays, yval, 'o-', c=color, markersize=sizes, markeredgecolor=color)
local_axes_formatting(axes, "Days since reaching 10 deaths", "Deaths per day (7 days rolling average)", xlim1=0, xlim2=maxx, ylim1=miny, ylim2=maxy, logx=False, fs=20)
axes.set_title('Top 20 countries in reported deaths per day', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
figsaveandclose(fig, output="../figures/eda_ecdc_countries_new_deaths.png")

# x = total cases, y = deaths
maxx = 1e07
minx = 10
maxy = 1e06
miny = 1
xvals = []
yvals = []
ids = []
for (i, country) in enumerate(countries):
    sdf = world_df[world_df['countriesAndTerritories'] == country].sort_values('dateRep', ascending=True)
    id = countries2id.loc[country, 'geoId']
    if(isinstance(id, str)):
        xvals.append(sdf['total_cases'].iloc[-1])
        yvals.append(sdf['total_deaths'].iloc[-1])
        ids.append(id.lower())
xvals = np.array(xvals)
yvals = np.array(yvals)
slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(xvals[yvals>0]), np.log(yvals[yvals>0]))
#label = 'Deaths = '+str(round(slope, 2))+'*Cases + '+str(int(round(intercept,0)))+' (R='+str(round(r_value,2))+')'
fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(10.5, 10))
#vec = np.linspace(minx, maxx, 10)
#axes.plot(vec, np.exp(slope*np.log(vec)+intercept), ':', color=(0.3,0.3,0.3,0.5), linewidth=2, label=label)
for i in range(0, len(ids)):
    x = xvals[i]
    y = yvals[i]
    if((x > minx) and (y > miny)):
        id = ids[i]
        if(id == 'uk'):
            id = 'gb'
        flagpath = 'circle-flags/flags/'+ id +'.png'
        if(os.path.isfile(flagpath)):
            axes.plot(x, y, 'o', markersize=16, markeredgecolor='black', markerfacecolor=(1,1,1,0))
            flagimg = mpimg.imread(flagpath)
            zoom = 0.025
            im = OffsetImage(flagimg, zoom=zoom)
            ab = AnnotationBbox(im, (x, y), xycoords='data',
                                frameon=False, annotation_clip=False)
            axes.add_artist(ab)
        else:
            print('Warning: flag '+flagpath+' not found')
local_axes_formatting(axes, "Total Positive Cases", "Total Reported Deaths", xlim1=minx, xlim2=maxx, ylim1=miny, ylim2=maxy, fs=20)
axes.set_title('Countries total cases v/s total deaths', fontsize=24)
#axes.legend()
axes.grid(True)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
figsaveandclose(fig, output="../figures/eda_ecdc_countries_scatter_total_cases_vs_deaths.png")
