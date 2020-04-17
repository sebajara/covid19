import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from localutils.plotutils import getcolormapandnorm
from localutils.plotutils import get_point_sizes
from localutils.plotutils import local_axes_formatting
from localutils.plotutils import addtexts2axes
from localutils.plotutils import figsaveandclose
from localutils.plotutils import figs2gif

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
    world_df.loc[ind, 'total_cases'] = csum_cases
    world_df.loc[ind, 'total_deaths'] = csum_deaths

max_death = world_df['total_deaths'].max()
max_pop = world_df['popData2018'].max()
max_cases = world_df['total_cases'].max()
dates = np.sort(world_df['dateRep'].unique())

(cmap, norm) = getcolormapandnorm(1, max_death, log=True, cmapstr='YlOrRd', N=100)

def make_eda_fig1(date, positives_low_min=1):
    # get the data pertaining the date
    sdf = world_df[world_df['dateRep'] == date].fillna(0)
    # named variables
    labels = sdf['geoId']
    deaths = sdf['total_deaths']
    positives = (sdf['total_cases'])
    population = (sdf['popData2018'])
    sizes = get_point_sizes(population.copy(), max_pop)
    # acutal plotting
    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(9.3, 5))
    # population v/s positives
    axes[0].scatter(population, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[0], "Population", "Total Cases", xlim1=1e04, xlim2=3e09, ylim1=positives_low_min, ylim2=1e06)
    # deaths v/s positives
    axes[1].scatter(positives, deaths, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[1], "Total Cases", "Total Deaths", xlim1=positives_low_min, xlim2=1e06, ylim2=5e04)
    axes[0].set_title(np.datetime_as_string(date, unit='D'), fontsize=20)  # put the date as title
    axes[1].set_title(np.datetime_as_string(date, unit='D'), fontsize=20)  # put the date as title
    plt.tight_layout()
    # Add the labels for the top states. Note: it is better to add
    # labels after plt.tight_layout()
    addtexts2axes(axes[0], population, positives, labels, (1e04, 3e09), (positives_low_min, 1e06), qtile=0.96)
    addtexts2axes(axes[1], positives, deaths, labels, (positives_low_min, 1e06), (1, 5e04), qtile=0.96)
    return fig

#fig = make_eda_fig1(dates[0], positives_low_min=10)
#plt.show()

#fig = make_eda_fig1(dates[-1])
#plt.show()

figsaveandclose(fig=make_eda_fig1(dates[-1]), output="../figures/ecdc_countries_eda1_latest.png")
figsaveandclose(fig=make_eda_fig1(dates[-1], positives_low_min=10), output="../figures/ecdc_countries_eda1_latest_zoom.png")
figs2gif(dates, make_eda_fig1, '../figures/ecdc_countries_eda1_zoom.gif', 60, positives_low_min=10)
