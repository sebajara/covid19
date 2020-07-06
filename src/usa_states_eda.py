import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from localutils.dataload import covidtracking_ustates
from localutils.plotutils import local_axes_formatting
from localutils.plotutils import figsaveandclose
from localutils.plotutils import get_list_colors

# ===== Get covidtracking data for the us states
(states_df, states_info) = covidtracking_ustates()
states_df['total_test'] = states_df['positive']+states_df['negative']
max_test = states_df['total_test'].max()
max_death = states_df['death'].max()
max_pop = states_info['POPESTIMATE2019'].max()
dates = np.sort(states_df['date'].unique())
min_date = dates.min()
max_date = dates.max()
states = states_df['state'].unique()

window = 7
topn = 20
maxx = np.max(states_df['date'].unique()-min_date)/np.timedelta64(1, 'D')
colors = get_list_colors('rainbow', len(states))

maxy = 1e07
miny = 10
hlstates = states_df.groupby('state')['positive'].max().sort_values(ascending=True).index[-topn:].values
legendys = np.logspace(np.log10(miny), np.log10(maxy), len(hlstates)+2)
fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(11, 10))
for (i, state) in enumerate(states):
    sdf = states_df[states_df['state'] == state].sort_values('date', ascending=True)
    days = pd.Series((sdf['date'] - min_date).values/np.timedelta64(1, 'D'))
    yval = sdf['positive']
    if(state in hlstates):
        color = colors[i]
        ind = np.where(hlstates == state)[0][0]
        axes.text(1.1*maxx, legendys[ind+1], str(topn-ind)+'. '+state,
                  horizontalalignment='left', verticalalignment='center', fontsize=14)
        plt.arrow(maxx, yval.iloc[-1],
                  0.04*maxx, legendys[ind+1]-yval.iloc[-1],
                  clip_on=False, shape='right', color=color)
        path = 'state-svg-defs/SVG/'+ state +'.png'
        zoom = 0.3
        #path = 'flags/svg/us/' + state.lower() + '.png'
        #zoom = 0.1
        if(not os.path.isfile(path)):
            print(path)
        img = mpimg.imread(path)
        im = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(im, (1.06*maxx, legendys[ind+1]), xycoords='data',
                            frameon=False, annotation_clip=False)
        axes.add_artist(ab)
    else:
        color = (0.8, 0.8, 0.8, 0.3)
    sizes = 2
    axes.plot(days, yval, 'o-', c=color, markersize=sizes, markeredgecolor=color)
local_axes_formatting(axes, "Days since 2020-MAR-06", "Total Positive Cases", xlim1=30, xlim2=maxx, ylim1=miny, ylim2=maxy, logx=False, fs=20)
axes.set_title('Top 20 states in total positive cases', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
figsaveandclose(fig, output="../figures/eda_covidtracking_states_total_cases.png")

maxy = 1.5*max_death
miny = 1
hlstates = states_df.groupby('state')['death'].max().sort_values(ascending=True).index[-topn:].values
legendys = np.logspace(np.log10(miny), np.log10(maxy), len(hlstates)+2)
fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(11, 10))
for (i, state) in enumerate(states):
    sdf = states_df[states_df['state'] == state].sort_values('date', ascending=True)
    days = pd.Series((sdf['date'] - min_date).values/np.timedelta64(1, 'D'))
    yval = sdf['death']
    if(state in hlstates):
        color = colors[i]
        ind = np.where(hlstates == state)[0][0]
        axes.text(1.1*maxx, legendys[ind+1], str(topn-ind)+'. '+state,
                  horizontalalignment='left', verticalalignment='center', fontsize=14)
        plt.arrow(maxx, yval.iloc[-1],
                  0.04*maxx, legendys[ind+1]-yval.iloc[-1],
                  clip_on=False, shape='right', color=color)
        path = 'state-svg-defs/SVG/'+ state +'.png'
        zoom = 0.3
        #path = 'flags/svg/us/' + state.lower() + '.png'
        #zoom = 0.1
        if(not os.path.isfile(path)):
            print(path)
        img = mpimg.imread(path)
        im = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(im, (1.06*maxx, legendys[ind+1]), xycoords='data',
                            frameon=False, annotation_clip=False)
        axes.add_artist(ab)
    else:
        color = (0.8, 0.8, 0.8, 0.3)
    sizes = 2
    axes.plot(days, yval, 'o-', c=color, markersize=sizes, markeredgecolor=color)
local_axes_formatting(axes, "Days since 2020-MAR-06", "Total reported deaths", xlim1=30, xlim2=maxx, ylim1=miny, ylim2=maxy, logx=False, fs=20)
axes.set_title('Top 20 states in total reported deaths', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
figsaveandclose(fig, output="../figures/eda_covidtracking_states_total_deaths.png")

maxy = 1e07
miny = 10
hlstates = states_df.groupby('state')['positive'].max().sort_values(ascending=True).index[-topn:].values
legendys = np.logspace(np.log10(miny), np.log10(maxy), len(hlstates)+2)
fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(11, 10))
for (i, state) in enumerate(states):
    sdf = states_df[states_df['state'] == state].sort_values('date', ascending=True)
    days = pd.Series((sdf['date'] - min_date).values/np.timedelta64(1, 'D'))
    yval = sdf['total_test']
    if(state in hlstates):
        color = colors[i]
        ind = np.where(hlstates == state)[0][0]
        axes.text(1.1*maxx, legendys[ind+1], str(topn-ind)+'. '+state,
                  horizontalalignment='left', verticalalignment='center', fontsize=14)
        plt.arrow(maxx, yval.iloc[-1],
                  0.04*maxx, legendys[ind+1]-yval.iloc[-1],
                  clip_on=False, shape='right', color=color)
        path = 'state-svg-defs/SVG/'+ state +'.png'
        zoom = 0.3
        #path = 'flags/svg/us/' + state.lower() + '.png'
        #zoom = 0.1
        if(not os.path.isfile(path)):
            print(path)
        img = mpimg.imread(path)
        im = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(im, (1.06*maxx, legendys[ind+1]), xycoords='data',
                            frameon=False, annotation_clip=False)
        axes.add_artist(ab)
    else:
        color = (0.8, 0.8, 0.8, 0.3)
    sizes = 2
    axes.plot(days, yval, 'o-', c=color, markersize=sizes, markeredgecolor=color)
local_axes_formatting(axes, "Days since 2020-MAR-06", "Total tests", xlim1=30, xlim2=maxx, ylim1=miny, ylim2=maxy, logx=False, fs=20)
axes.set_title('Top 20 states in testing', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
figsaveandclose(fig, output="../figures/eda_covidtracking_states_total_tests.png")

maxy = 100
miny = 0
tempdic = {}
for (i, state) in enumerate(states):
    sdf = states_df[states_df['state'] == state].sort_values('date', ascending=True)
    days = pd.Series((sdf['date'] - min_date).values/np.timedelta64(1, 'D')).values
    val1 = sdf['positive'].rolling(window=window).mean().values
    val2 = sdf['total_test'].rolling(window=window).mean().values
    ratio = val1[-1]/val2[-1]
    if(ratio >= 0):
        tempdic[state] = ratio
hlstates = np.array([k for (k,v) in sorted(tempdic.items(), key=lambda item: item[1])][-topn:])
legendys = np.linspace(miny, maxy, len(hlstates)+2)
fig, axes = plt.subplots(ncols=1, nrows=1, figsize=(11, 10))
for (i, state) in enumerate(states):
    sdf = states_df[states_df['state'] == state].sort_values('date', ascending=True)
    days = pd.Series((sdf['date'] - min_date).values/np.timedelta64(1, 'D')).values
    val1 = sdf['positive'].rolling(window=window).mean().values
    val2 = sdf['total_test'].rolling(window=window).mean().values
    #val1 = smooth(sdf['positive'].values)
    #val2 = smooth(sdf['total_test'].values)
    yval = 100*val1/val2
    sizes = 2
    if(state in hlstates):
        color = colors[i]
        ind = np.where(hlstates == state)[0][0]
        axes.text(1.1*maxx, legendys[ind+1], str(topn-ind)+'. '+state,
                  horizontalalignment='left', verticalalignment='center', fontsize=14)
        plt.arrow(maxx, yval[-1],
                  0.04*maxx, legendys[ind+1]-yval[-1],
                  clip_on=False, shape='right', color=color)
        path = 'state-svg-defs/SVG/'+ state +'.png'
        zoom = 0.3
        #path = 'flags/svg/us/' + state.lower() + '.png'
        #zoom = 0.1
        if(os.path.isfile(path)):
            img = mpimg.imread(path)
            im = OffsetImage(img, zoom=zoom)
            ab = AnnotationBbox(im, (1.06*maxx, legendys[ind+1]), xycoords='data',
                                frameon=False, annotation_clip=False)
            axes.add_artist(ab)
        else:
            print(path)
    else:
        color = (0.8, 0.8, 0.8, 0.3)
    axes.plot(days[yval >= 0], yval[yval >= 0], 'o-', c=color, markersize=sizes, markeredgecolor=color)
local_axes_formatting(axes, "Days since 2020-MAR-06", "Positives/Tests Fraction [%]", xlim1=30, xlim2=maxx, ylim1=miny, ylim2=maxy, logy=False, logx=False, fs=20)
axes.set_title('Top 20 states in positives per testing', fontsize=24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
figsaveandclose(fig, output="../figures/eda_covidtracking_states_positive_totals_ratio.png")

