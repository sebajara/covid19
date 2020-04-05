import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
#from matplotlib.animation import FuncAnimation
#import seaborn as sns
import pickle
from us import states
import os
#import imageio

## ========== Import
# import nytimes data
# see: data/nytimes_updatedata.py
with open("data/nytimes_covid19/nytimes_dfs.pickle", "rb") as file:
    nytimes_dfs = pickle.load(file)
# import covidtracking data
# see: data/covidtracking_update.py
with open("data/covidtracking/covidtracking_dfs.pickle", "rb") as file:
    covidtracking_dfs = pickle.load(file)
state_census = pd.read_csv('data/usa_census/SCPRC-EST2019-18+POP-RES.csv')

## ========== Cleaning
# Let's use covidtracking for now, as it has the number of tests done. 
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
#states_info['clabel'] = np.array(list(range(0, states_info.shape[0])))
#states_info.loc[states_info['POPESTIMATE2019'].isnull(), 'clabel'] = 0
max_death = states_df['death'].max()
max_pop = states_info['POPESTIMATE2019'].max()
# get the set of dates
dates = np.sort(states_df['date'].unique())

# =========== Animation plot over time
# Before then, let's sort out the color map and some functions to help
# us out
N = 100 # color bins
#cmap = plt.cm.Greys
cmap = plt.cm.YlOrRd
# extract all colors from the .jet map
cmaplist = [cmap(i) for i in range(cmap.N)]
# create the new map
cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
# Define color bins for death counts and normalize. Notice we are using
# log-scale
bounds = np.logspace(1, np.log10(max_death), N+1)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
# Just a scale transformation, that will be used to getting the size of
# the points for the scatter plots
def get_point_sizes(values, maxval, maxs=500, mins=5, log=False):
    values[values.isnull()] = 0
    if(log):
        temp = mins+(maxs-mins)*np.log(values)/np.log(maxval)
        temp[temp < mins] = mins  # To avoid -Inf
        return temp
    else:
        return mins+(maxs-mins)*values/maxval
# some common axes settings
def local_axes_formatting(ax, xlabel, ylabel, xlim2, ylim2, xlim1=1, ylim1=1, fs=18, logx=True, logy=True):
    if(logx):
        ax.set_xscale('log')
    if(logy):
        ax.set_yscale('log')
    ax.set_xlabel(xlabel, fontsize=fs)
    ax.set_ylabel(ylabel, fontsize=fs)
    ax.set_xlim(xlim1, xlim2)
    ax.set_ylim(ylim1, ylim2)
# this will help us put the name of the states on the plot
def add_text_fig1(ax, xs, ys, txts, xlims, ylims, yoffset=0, xoffset=0, qtile=0.9):
    locs = ys[ys >= ys.quantile(qtile)].index
    for (x, y, txt) in zip(xs.loc[locs].values, ys.loc[locs].values, txts.loc[locs].values):
        if(not (np.isnan(x) or np.isnan(y) or (x < xlims[0]) or (x > xlims[1]) or (y < ylims[0]) or (y > ylims[1]))):
            ax.text(x+xoffset, y+yoffset, txt, horizontalalignment='left',
                    verticalalignment='bottom', color='k', fontsize=12)

# TODO: get a better way to organize the data frame. Right now the
# solution is very inefficient. Perhaps multi-indexing?
def make_eda_fig1(date, positives_low_min=1):
    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(14, 5))
    # get the data pertaining the date
    sdf = states_df[states_df['date'] == date].fillna(0)
    sdf = sdf.merge(states_info.loc[:, ['abbreviation', 'POPESTIMATE2019']], right_on='abbreviation', left_on='state', how='left')
    # prefer to use named variables
    labels = sdf['abbreviation']
    deaths = sdf['death']
    total_test = (sdf['positive']+sdf['negative'])
    positives = (sdf['positive'])
    population = (sdf['POPESTIMATE2019'])    
    sizes = get_point_sizes(population.copy(), max_pop)
    # population v/s positives
    axes[0].scatter(population, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[0], "Population", "Total Positives", 1e08, 1e06, xlim1=5e05, ylim1=positives_low_min)
    # total_test v/s positives
    axes[1].scatter(total_test, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[1], "Total tests", "Total Positives", 1e06, 1e06, xlim1=positives_low_min, ylim1=positives_low_min)
    axes[1].set_title(np.datetime_as_string(date, unit='D'), fontsize=20)  # put the date as title
    # deaths v/s positives
    axes[2].scatter(deaths, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[2], "Total Deaths", "Total Positives", 1e04, 1e06, ylim1=positives_low_min)
    plt.tight_layout()
    # Add the labels for the top states. Note: it is better to add
    # labels after plt.tight_layout()
    add_text_fig1(axes[0], population, positives, labels, (5e05, 1e08), (positives_low_min, 1e06), qtile=0.9)
    add_text_fig1(axes[1], total_test, positives, labels, (positives_low_min, 1e06), (positives_low_min, 1e06), qtile=0.9)
    add_text_fig1(axes[2], deaths, positives, labels, (1, 1e04), (positives_low_min, 1e06), qtile=0.9)
    return fig

def make_eda_fig2(date, positives_low_min=1):
    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(14, 5))
    # get the data pertaining the date
    sdf = states_df[states_df['date'] == date].fillna(0)
    sdf = sdf.merge(states_info.loc[:, ['abbreviation', 'POPESTIMATE2019']], right_on='abbreviation', left_on='state', how='left')
    # prefer to use named variables
    labels = sdf['abbreviation']
    population = (sdf['POPESTIMATE2019'])
    positives = (sdf['positive'])
    deaths = sdf['death']
    tests = (sdf['positive']+sdf['negative'])
    positives_ratio = 100*sdf['positive']/(sdf['positive']+sdf['negative'])
    death_ratio = 100*sdf['death']/sdf['positive']
    sizes = get_point_sizes(population.copy(), max_pop)
    # population v/s positives
    axes[0].scatter(population, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[0], "Population", "Total Positives", 1e08, 1e06, xlim1=5e05, ylim1=positives_low_min)
    # total_test v/s positives
    axes[1].scatter(tests, positives_ratio, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[1], "Total Tests", "Positives / Tests [%]", 1e06, 100, xlim1=positives_low_min, ylim1=0, logy=False)
    axes[1].set_title(np.datetime_as_string(date, unit='D'), fontsize=20)  # put the date as title
    # deaths v/s positives
    axes[2].scatter(positives, death_ratio, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[2], "Total Positives", "Deaths / Positives [%]", 1e06, 8, xlim1=positives_low_min, ylim1=0, logy=False)
    plt.tight_layout()
    # Add the labels for the top states. Note: it is better to add
    # labels after plt.tight_layout()
    add_text_fig1(axes[0], population, positives, labels, (5e05, 1e08), (positives_low_min, 1e06), qtile=0.85)
    add_text_fig1(axes[1], tests, positives_ratio, labels, (positives_low_min, 1e06), (0, 100), qtile=0.85)
    add_text_fig1(axes[2], positives, death_ratio, labels, (positives_low_min, 1e06), (0, 8), qtile=0.85)
    return fig

#fig = make_eda_fig2(dates[-1])
#plt.show()

# save the last date individually
fig = make_eda_fig1(dates[-1])
plt.savefig("figures/covidtracking_states_eda1_latest.png")
plt.close(fig)
fig = make_eda_fig1(dates[-1], positives_low_min=100)
plt.savefig("figures/covidtracking_states_eda1_latest_zoom.png")
plt.close(fig)
fig = make_eda_fig2(dates[-1], positives_low_min=100)
plt.savefig("figures/covidtracking_states_eda2_latest_zoom.png")
plt.close(fig)

# Make an animation with the plots for each date. NOTE: I tried doing
# gif via matplotlib, but got tired. Doing regular convert instead
for i, date in enumerate(dates):
    fig = make_eda_fig1(date)
    plt.savefig("temp/fig{}.png".format(str(i).zfill(3)))
    plt.close(fig)
os.system('convert -delay 60 temp/*.png figures/covidtracking_states_eda1.gif')
os.system('rm temp/*')
for i, date in enumerate(dates):
    fig = make_eda_fig1(date, positives_low_min=100)
    plt.savefig("temp/fig{}.png".format(str(i).zfill(3)))
    plt.close(fig)
os.system('convert -delay 60 temp/*.png figures/covidtracking_states_eda1_zoom.gif')
os.system('rm temp/*')

for i, date in enumerate(dates):
    fig = make_eda_fig2(date, positives_low_min=100)
    plt.savefig("temp/fig{}.png".format(str(i).zfill(3)))
    plt.close(fig)
os.system('convert -delay 60 temp/*.png figures/covidtracking_states_eda2_zoom.gif')
os.system('rm temp/*')
