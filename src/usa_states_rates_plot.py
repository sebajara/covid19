import numpy as np
import matplotlib.pyplot as plt
from localutils.dataload import covidtracking_ustates
from localutils.plotutils import getcolormapandnorm
#from localutils.plotutils import get_point_sizes
from localutils.plotutils import local_axes_formatting
from localutils.plotutils import addtexts2axes
from localutils.plotutils import figsaveandclose
from localutils.plotutils import figs2gif
import pickle

# ===== Get covidtracking data 
(states_df, states_info) = covidtracking_ustates()
# ===== Get covidtracking data rate estimates
with open("analyzed_data/covidtracking_states_df_rates.pickle", "rb") as file:
    states_df_rates = pickle.load(file)

max_death = states_df_rates['death'].max()
max_pop = states_info['POPESTIMATE2019'].max()
dates = np.sort(states_df_rates['date'].unique())

# ===== Some descriptive plots and annimations
# NOTE: overall the implementation is a bit inefficient, but works for now.
# Define color bins based on death counts
(cmap, norm) = getcolormapandnorm(1, max_death, log=True, cmapstr='YlOrRd', N=100)

def make_fig1(date, positives_low_min=1):
    # get the data pertaining the date
    sdf = states_df_rates[states_df_rates['date'] == date].fillna(0)
    sdf = sdf.merge(states_info.loc[:, ['abbreviation', 'POPESTIMATE2019']], right_on='abbreviation', left_on='state', how='left')
    # named variables
    labels = sdf['abbreviation']
    deaths = sdf['death']
    total_test = sdf['positive']+sdf['negative']
    positives = sdf['positive']
    population = sdf['POPESTIMATE2019']
    gr_total_test = 100*sdf['gr_tests']
    gr_positives = 100*sdf['gr_positive']
    gr_deaths = 100*sdf['gr_death']
    sizes = 100#get_point_sizes(population.copy(), max_pop)
    # acutal plotting
    fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(11.5, 6.5))
    # population v/s positives
    axes[0, 0].scatter(population, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[0, 0], "Population", "Total Positives", xlim2=1e08, ylim2=5e05, xlim1=5e05, ylim1=positives_low_min, fs=12)
    # total_test v/s positives
    axes[0, 1].scatter(total_test, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[0, 1], "Total tests", "Total Positives", xlim2=1e06, ylim2=5e05, xlim1=positives_low_min, ylim1=positives_low_min, fs=12)
    axes[0, 1].set_title(np.datetime_as_string(date, unit='D'), fontsize=20)  # put the date as title
    # deaths v/s positives
    axes[0, 2].scatter(deaths, positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[0, 2], "Total Deaths", "Total Positives", xlim2=1e04, ylim2=5e05, ylim1=positives_low_min, fs=12)
    # population v/s positives_rate
    axes[1, 0].scatter(population, gr_positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[1, 0], "Population", "Positives gr-rate [%/day]", xlim2=1e08, ylim2=125, xlim1=5e05, ylim1=0, logy=False, fs=12)
    # gr_total_test v/s positives_rate
    axes[1, 1].scatter(gr_total_test, gr_positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[1, 1], "Tests gr-rate [%/day]", "Positives gr-rate [%/day]", xlim2=100, ylim2=125, xlim1=0, ylim1=0, logy=False, logx=False, fs=12)
    # gr_deaths v/s positives_rate
    axes[1, 2].scatter(gr_deaths, gr_positives, c=deaths, cmap=cmap, norm=norm, edgecolors='k', alpha=0.75, s=sizes)
    local_axes_formatting(axes[1, 2], "Deaths gr-rate [%/day]", "Positives gr-rate [%/day]", xlim2=100, ylim2=125, xlim1=0, ylim1=0, logy=False, logx=False, fs=12)
    plt.tight_layout()
    # Add the labels for the top states. Note: it is better to add
    # labels after plt.tight_layout()
    addtexts2axes(axes[0, 0], population, positives, labels, (5e05, 1e08), (positives_low_min, 5e05), qtile=0.9, fs=10)
    addtexts2axes(axes[0, 1], total_test, positives, labels, (positives_low_min, 5e05), (positives_low_min, 1e06), qtile=0.9, fs=10, yqtile=False)
    addtexts2axes(axes[0, 2], deaths, positives, labels, (1, 1e04), (positives_low_min, 5e05), qtile=0.9, fs=10, yqtile=False)
    addtexts2axes(axes[1, 0], population, gr_positives, labels, (5e05, 1e08), (0, 125), qtile=0.9, fs=10)
    addtexts2axes(axes[1, 1], gr_total_test, gr_positives, labels, (0, 100), (0, 125), qtile=0.9, fs=10, yqtile=False)
    addtexts2axes(axes[1, 2], gr_deaths, gr_positives, labels, (0, 100), (0, 125), qtile=0.9, fs=10, yqtile=False)
    return fig

def get_list_colors(cmapstr, N):
    cmap = plt.cm.get_cmap(name=cmapstr)
    return [cmap(int(i)) for i in np.linspace(0, cmap.N, N)]

def make_fig2(states):
    fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(11.5, 6.5))
    local_axes_formatting(axes[0, 0], "Days since 2020-03-06", "Total tests", xlim2=35, ylim2=1e06, xlim1=0, ylim1=1, fs=12, logx=False)
    local_axes_formatting(axes[0, 1], "Days since 2020-03-06", "Total Positives", xlim2=35, ylim2=1e06, xlim1=0, ylim1=1, fs=12, logx=False)
    local_axes_formatting(axes[0, 2], "Days since 2020-03-06", "Total Deaths", xlim2=35, ylim2=1e04, xlim1=0, ylim1=1, fs=12, logx=False)
    local_axes_formatting(axes[1, 0], "Days since 2020-03-06", "Tests gr-rate [%/day]", xlim2=35, ylim2=100, xlim1=0, ylim1=0, fs=12, logx=False, logy=False)
    local_axes_formatting(axes[1, 1], "Days since 2020-03-06", "Positives gr-rate [%/day]", xlim2=35, ylim2=100, xlim1=0, ylim1=0, fs=12, logx=False, logy=False)
    local_axes_formatting(axes[1, 2], "Days since 2020-03-06", "Deaths gr-rate [%/day]", xlim2=35, ylim2=100, xlim1=0, ylim1=0, fs=12, logx=False, logy=False)
    sizes = 5#get_point_sizes(population.copy(), max_pop)
    min_date = states_df_rates['date'].min()
    #colors = plt.cm.get_cmap('jet', len(states))
    colors = get_list_colors('rainbow', len(states))
    plt.tight_layout()
    for (i, state) in enumerate(states):
        # get the data pertaining the date
        sdf = states_df_rates[states_df_rates['state'] == state].sort_values('date', ascending=True)
        deaths = sdf['death']
        total_test = sdf['positive']+sdf['negative']
        positives = sdf['positive']
        gr_total_test = 100*sdf['gr_tests']
        gr_positives = 100*sdf['gr_positive']
        gr_deaths = 100*sdf['gr_death']
        gr_total_test_err = 100*sdf['gr_tests_err']
        gr_positives_err = 100*sdf['gr_positive_err']
        gr_deaths_err = 100*sdf['gr_death_err']
        days = (sdf['date'] - min_date).values/np.timedelta64(1, 'D')
        color = colors[i]
        # acutal plotting
        axes[0, 0].plot(days, total_test, 'o:', c=color, alpha=0.9, markersize=sizes, markeredgecolor=(0.4,0.4,0.4))
        axes[0, 1].plot(days, positives, 'o:', c=color, alpha=0.9, markersize=sizes, markeredgecolor=(0.4,0.4,0.4))
        axes[0, 2].plot(days, deaths, 'o:', c=color, alpha=0.9, markersize=sizes, markeredgecolor=(0.4,0.4,0.4))
        axes[1, 0].plot(days, gr_total_test, 'o:', c=color, alpha=0.9, markersize=sizes, markeredgecolor=(0.4,0.4,0.4))
        axes[1, 1].plot(days, gr_positives, 'o:', c=color, alpha=0.9, markersize=sizes, markeredgecolor=(0.4,0.4,0.4))
        axes[1, 2].plot(days, gr_deaths, 'o:', c=color, alpha=0.9, markersize=sizes, markeredgecolor=(0.4,0.4,0.4))
        axes[1, 0].fill_between(days, gr_total_test-gr_total_test_err, gr_total_test+gr_total_test_err, color=color, alpha=0.3)
        axes[1, 1].fill_between(days, gr_positives-gr_positives_err, gr_positives+gr_positives_err, color=color, alpha=0.3)
        axes[1, 2].fill_between(days, gr_deaths-gr_deaths_err, gr_deaths+gr_deaths_err, color=color, alpha=0.3)
    # Add the labels for the top states. Note: it is better to add
    # labels after plt.tight_layout()
    axes[0, 0].legend(states)
    axes[0, 1].legend(states)
    axes[0, 2].legend(states)
    return fig

#fig = make_fig1(dates[2], positives_low_min=100)
#plt.show()

figsaveandclose(fig=make_fig1(dates[-1]), output="../figures/covidtracking_states_rates_latest.png")
figs2gif(dates, make_fig1, '../figures/covidtracking_states_rates.gif', 60, positives_low_min=100)

#fig = make_fig2(['CA', 'NY', 'FL', 'TX', 'OH'])
#plt.show()

sets = [['CA', 'TX', 'FL', 'NY', 'PA'],
        ['IL', 'OH', 'GA', 'NC', 'MI'],
        ['NJ', 'VA', 'WA', 'AZ', 'MA'],
        ['TN', 'IN', 'MO', 'MD', 'WI'],
        ['CO', 'MN', 'SC', 'AL', 'LA'],
        ['KY', 'OR', 'OK', 'CT', 'UT'],
        ['IA', 'NV', 'AR', 'MS', 'KS'],
        ['NM', 'NE', 'WV', 'ID', 'HI'],
        ['NH', 'ME', 'MT', 'RI', 'DE'],
        ['SD', 'ND', 'AK', 'DC', 'VT', 'WY'],
        ['AS', 'GU', 'MP', 'PR', 'VI']]

#fig = make_fig2(sets[10])
#plt.show()

for (i, set) in enumerate(sets):
    figsaveandclose(fig=make_fig2(set), output="../figures/covidtracking_states_rates_byset_{}.png".format(i))
    

