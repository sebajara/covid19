import numpy as np
import matplotlib.pyplot as plt
from localutils.dataload import covidtracking_ustates
from localutils.plotutils import getcolormapandnorm
from localutils.plotutils import get_point_sizes
from localutils.plotutils import local_axes_formatting
from localutils.plotutils import addtexts2axes
from localutils.plotutils import figsaveandclose
from localutils.plotutils import figs2gif

# NOTE: would be nice instead of using scatter circles, use the shape of each state instead
# https://github.com/coryetzkorn/state-svg-defs
# We could also use countries flags
# https://github.com/HatScripts/circle-flags?files=1

#from importlib import reload

# ===== Get covidtracking data for the us states
(states_df, states_info) = covidtracking_ustates()
max_death = states_df['death'].max()
max_pop = states_info['POPESTIMATE2019'].max()
dates = np.sort(states_df['date'].unique())

# ===== Some descriptive plots and annimations
# NOTE: overall the implementation is a bit inefficient, but works for now.
# Define color bins based on death counts
(cmap, norm) = getcolormapandnorm(1, max_death, log=True, cmapstr='YlOrRd', N=100)


def make_eda_fig1(date, positives_low_min=1):
    # get the data pertaining the date
    sdf = states_df[states_df['date'] == date].fillna(0)
    sdf = sdf.merge(states_info.loc[:, ['abbreviation', 'POPESTIMATE2019']], right_on='abbreviation', left_on='state', how='left')
    # named variables
    labels = sdf['abbreviation']
    deaths = sdf['death']
    total_test = (sdf['positive']+sdf['negative'])
    positives = (sdf['positive'])
    population = (sdf['POPESTIMATE2019'])    
    sizes = get_point_sizes(population.copy(), max_pop)
    # acutal plotting
    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(14, 5))
    # population v/s positives
    axes[0].scatter(population, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[0], "Population", "Total Positives", xlim2=1e08, ylim2=1e06, xlim1=5e05, ylim1=positives_low_min)
    # total_test v/s positives
    axes[1].scatter(total_test, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[1], "Total tests", "Total Positives", xlim2=1e06, ylim2=1e06, xlim1=positives_low_min, ylim1=positives_low_min)
    axes[1].set_title(np.datetime_as_string(date, unit='D'), fontsize=20)  # put the date as title
    # deaths v/s positives
    axes[2].scatter(deaths, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[2], "Total Deaths", "Total Positives", xlim2=1e04, ylim2=1e06, ylim1=positives_low_min)
    plt.tight_layout()
    # Add the labels for the top states. Note: it is better to add
    # labels after plt.tight_layout()
    addtexts2axes(axes[0], population, positives, labels, (5e05, 1e08), (positives_low_min, 1e06), qtile=0.9)
    addtexts2axes(axes[1], total_test, positives, labels, (positives_low_min, 1e06), (positives_low_min, 1e06), qtile=0.9)
    addtexts2axes(axes[2], deaths, positives, labels, (1, 1e04), (positives_low_min, 1e06), qtile=0.9)
    return fig


def make_eda_fig2(date, positives_low_min=1):
    # get the data pertaining the date
    sdf = states_df[states_df['date'] == date].fillna(0)
    sdf = sdf.merge(states_info.loc[:, ['abbreviation', 'POPESTIMATE2019']], right_on='abbreviation', left_on='state', how='left')
    # named variables
    labels = sdf['abbreviation']
    population = (sdf['POPESTIMATE2019'])
    positives = (sdf['positive'])
    deaths = sdf['death']
    tests = (sdf['positive']+sdf['negative'])
    positives_ratio = 100*sdf['positive']/(sdf['positive']+sdf['negative'])
    death_ratio = 100*sdf['death']/sdf['positive']
    sizes = get_point_sizes(population.copy(), max_pop)
    # acutal plotting
    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(14, 5))
    # population v/s positives
    axes[0].scatter(population, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[0], "Population", "Total Positives",
                          xlim2=1e08, ylim2=1e06, xlim1=5e05, ylim1=positives_low_min)
    # total_test v/s positives
    axes[1].scatter(tests, positives_ratio, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[1], "Total Tests", "Positives / Tests [%]",
                          xlim2=1e06, ylim2=100, xlim1=positives_low_min, ylim1=0, logy=False)
    axes[1].set_title(np.datetime_as_string(date, unit='D'), fontsize=20)  # put the date as title
    # deaths v/s positives
    axes[2].scatter(positives, death_ratio, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[2], "Total Positives", "Deaths / Positives [%]",
                          xlim2=1e06, ylim2=8, xlim1=positives_low_min, ylim1=0, logy=False)
    plt.tight_layout()
    # Add the labels for the top states. Note: it is better to add
    # labels after plt.tight_layout()
    addtexts2axes(axes[0], population, positives, labels, (5e05, 1e08), (positives_low_min, 1e06), qtile=0.85)
    addtexts2axes(axes[1], tests, positives_ratio, labels, (positives_low_min, 1e06), (0, 100), qtile=0.85)
    addtexts2axes(axes[2], positives, death_ratio, labels, (positives_low_min, 1e06), (0, 8), qtile=0.85)
    return fig


#fig = make_eda_fig2(dates[-1])
#plt.show()

# save figures for the last date individually
figsaveandclose(fig=make_eda_fig1(dates[-1]), output="../figures/covidtracking_states_eda1_latest.png")
figsaveandclose(fig=make_eda_fig1(dates[-1], positives_low_min=100), output="../figures/covidtracking_states_eda1_latest_zoom.png")
figsaveandclose(fig=make_eda_fig2(dates[-1], positives_low_min=100), output="../figures/covidtracking_states_eda2_latest_zoom.png")

# Make an animation with the plots for each date.
# NOTE: I tried doing gif via matplotlib, but got tired. Doing regular
# convert instead, it requires saving individual figures into a temp/ folder.
#figs2gif(dates, make_eda_fig1, '../figures/covidtracking_states_eda1.gif', 60)
figs2gif(dates, make_eda_fig1, '../figures/covidtracking_states_eda1_zoom.gif', 60, positives_low_min=100)
#figs2gif(dates, make_eda_fig2, '../figures/covidtracking_states_eda2_zoom.gif', 60, positives_low_min=100)
