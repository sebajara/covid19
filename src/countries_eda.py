import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from localutils.plotutils import getcolormapandnorm
from localutils.plotutils import get_point_sizes
from localutils.plotutils import local_axes_formatting
from localutils.plotutils import addtexts2axes
from localutils.plotutils import figsaveandclose
from localutils.plotutils import get_list_colors

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
    per_per_cap = 100*csum_cases/sdf['popData2018'].iloc[0]
    per_per_cap2 = 100*csum_deaths/sdf['popData2018'].iloc[0]
    world_df.loc[ind, 'total_cases'] = csum_cases
    world_df.loc[ind, 'total_deaths'] = csum_deaths
    world_df.loc[ind, 'cases_per_cap'] = per_per_cap
    world_df.loc[ind, 'deaths_per_cap'] = per_per_cap2

max_death = world_df['total_deaths'].max()
max_pop = world_df['popData2018'].max()
max_cases = world_df['total_cases'].max()
dates = np.sort(world_df['dateRep'].unique())
min_date = dates.min()
max_date = dates.max()
countries = world_df[world_df['total_cases']>1e04]['countriesAndTerritories'].unique()

# (cmap, norm) = getcolormapandnorm(1, max_death, log=True, cmapstr='YlOrRd', N=100)

fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(11.5, 6.5))
colors = get_list_colors('rainbow', len(countries))
for (i, country) in enumerate(countries):
    sizes = 1
    edgecolor = (0.4, 0.4, 0.4)
    color = colors[i]
    sdf = world_df[world_df['countriesAndTerritories'] == country].sort_values('dateRep', ascending=True)
    days = pd.Series((sdf['dateRep'] - min_date).values/np.timedelta64(1, 'D'))
    axes[0, 0].plot(days, sdf['total_cases'], 'o:', c=color, alpha=0.5, markersize=sizes, markeredgecolor=color)
    local_axes_formatting(axes[0, 0], "Days since 2020", "Total Positives", xlim2=150, ylim2=1e07, xlim1=1, ylim1=10, logx=False, fs=12)
    axes[0, 1].plot(days, sdf['total_deaths'], 'o:', c=color, alpha=0.5, markersize=sizes, markeredgecolor=color)
    local_axes_formatting(axes[0, 1], "Days since 2020", "Total Deaths", xlim2=150, ylim2=2e05, xlim1=1, ylim1=10, logx=False, fs=12)
    axes[1, 0].plot(days, sdf['cases_per_cap'], 'o:', c=color, alpha=0.5, markersize=sizes, markeredgecolor=color)
    local_axes_formatting(axes[1, 0], "Days since 2020", "Positives/Population [%]", xlim2=150, ylim2=5, xlim1=1, ylim1=0.001, logx=False, fs=12)
    axes[1, 1].plot(days, sdf['deaths_per_cap'], 'o:', c=color, alpha=0.5, markersize=sizes, markeredgecolor=color)
    local_axes_formatting(axes[1, 1], "Days since 2020", "Deaths/Population [%]", xlim2=150, ylim2=0.3, xlim1=1, ylim1=0.00001, logx=False, fs=12)
    size = 200*sdf['popData2018'].iloc[0]/max_pop
    axes[0, 2].scatter(sdf['total_cases'].iloc[-1], sdf['total_deaths'].iloc[-1], color=color, edgecolors='k', alpha=0.75, s=size)
    if(sdf['total_deaths'].iloc[-1] > 2e04):
        f1 = np.random.choice([0.7, 1.2])
        f2 = np.random.choice([0.7, 1.2])
        axes[0, 2].text(f1*sdf['total_cases'].iloc[-1], f1*sdf['total_deaths'].iloc[-1],
                        sdf['countryterritoryCode'].iloc[-1], horizontalalignment='left',
                        verticalalignment='bottom', color='k', fontsize=10)
    local_axes_formatting(axes[0, 2], "Total Positives", "Total deaths", xlim2=1e07, xlim1=1e04, ylim2=2e05, ylim1=100, fs=12)
    axes[1, 2].scatter(sdf['cases_per_cap'].iloc[-1], sdf['deaths_per_cap'].iloc[-1], color=color, edgecolors='k', alpha=0.75, s=size)
    local_axes_formatting(axes[1, 2], "Positives/Population", "Deaths/Population", xlim2=5, xlim1=0.001, ylim2=0.3, ylim1=0.0001, fs=12)
    if(sdf['deaths_per_cap'].iloc[-1] > 0.05):
        f1 = np.random.choice([0.7, 1.2])
        f2 = np.random.choice([0.7, 1.2])
        axes[1, 2].text(f1*sdf['cases_per_cap'].iloc[-1], f1*sdf['deaths_per_cap'].iloc[-1],
                        sdf['countryterritoryCode'].iloc[-1], horizontalalignment='left',
                        verticalalignment='bottom', color='k', fontsize=10)
    plt.tight_layout()
figsaveandclose(fig, output="../figures/ecdc_countries_eda.png")
