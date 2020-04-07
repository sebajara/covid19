import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

def getcolormapandnorm(minv, maxv, log=False, cmapstr='Greys', N=50):
    cmap = plt.cm.get_cmap(name=cmapstr)
    # extract all colors from the map
    cmaplist = [cmap(i) for i in range(cmap.N)]
    # create the new map
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    # Define color bins and normalize.
    if(log):
        bounds = np.logspace(np.log10(minv), np.log10(maxv), N+1)
    else:
        bounds = np.linspace(minv, maxv, N+1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    return(cmap, norm)


def get_point_sizes(values, maxval, maxs=500, mins=5, log=False):
    values[values.isnull()] = 0
    if(log):
        temp = mins+(maxs-mins)*np.log(values)/np.log(maxval)
        temp[temp < mins] = mins  # To avoid -Inf
        return temp
    else:
        return mins+(maxs-mins)*values/maxval


def local_axes_formatting(ax, xlabel, ylabel, fs=18,
                          xlim1=1, xlim2=10, ylim1=1, ylim2=10,
                          logx=True, logy=True):
    if(logx):
        ax.set_xscale('log')
    if(logy):
        ax.set_yscale('log')
    ax.set_xlabel(xlabel, fontsize=fs)
    ax.set_ylabel(ylabel, fontsize=fs)
    ax.set_xlim(xlim1, xlim2)
    ax.set_ylim(ylim1, ylim2)


def addtexts2axes(ax, xs, ys, txts, xlims, ylims,
                  c='k', fs=12, yoffset=0, xoffset=0,
                  yqtile=True, qtile=0.9):
    if(yqtile):
        locs = ys[ys >= ys.quantile(qtile)].index
    else:
        locs = xs[xs >= xs.quantile(qtile)].index
    for (x, y, txt) in zip(xs.loc[locs].values,
                           ys.loc[locs].values,
                           txts.loc[locs].values):
        if(not (np.isnan(x) or np.isnan(y)
                or (x < xlims[0]) or (x > xlims[1])
                or (y < ylims[0]) or (y > ylims[1]))):
            ax.text(x+xoffset, y+yoffset, txt, horizontalalignment='left',
                    verticalalignment='bottom', color=c, fontsize=fs)
    

def figsaveandclose(fig, output):
    plt.savefig(output)
    plt.close(fig)


def figs2gif(iterable, figfunction, output, delay, **kwargs):
    for i, value in enumerate(iterable):
        fig = figfunction(value, **kwargs)
        plt.savefig("temp/fig{}.png".format(str(i).zfill(3)))
        plt.close(fig)
    os.system('convert -delay {} temp/*.png {}'.format(delay, output))
    os.system('rm temp/*')


