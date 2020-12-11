"""
File: plot_log.py
Author: Felix Steinmetz
Email: fsteinme@rhrk.uni-kl.de
Github: https://github.com/FeStein
Description: Collects Marvelmind Plots and prints out 3 plots (one for each
axis). Each plot contains a dot per value. Detected transmission errors are
marked as red bar.
"""
###Parameter
filename = 'Log.csv'
hedgehog_id = 6             

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({'font.size': 12})

df = pd.read_csv('Log.csv',delimiter=';',header=None)

#clean data 
df =df.replace(',','.',regex = True)
df[0] = df[0].astype(float).astype(int)
for i in [4,5,6]: df[i] = df[i].astype(float)

wdf = df[df[3] != hedgehog_id] #wrong entrys -> necessary to plot mistakes
df = df[df[3] == hedgehog_id] #filter wrong entry


def custom_plot(ndf,edf,i,label):
    """Creates a custom plot interface for each axis

    :ndf: DataFrame part of the correctly transmitted positioning values
    :edf: DataFrame part of the wrongly transmitted position values
    :i: index of the Position row (4,5,6 possible for the three axis) if i is a
    list, it will plot all indices in one plot
    :label: Title of the plot
    :returns: Shows the plot and saves it as pdf and png 
    """
    #plot values
    if type(i) == list:
        for j in i: plt.plot(ndf.index,ndf[i],'.-')
    else:
        plt.plot(ndf.index,ndf[i],'.-')

    pos_min = ndf[i].min()
    pos_max = ndf[i].max()
    interval = abs(abs(pos_max) - abs(pos_min))
    mini = pos_min - (interval*0.1)
    maxi = pos_max + (interval * 0.1)

    #plot errors
    for j in edf.index: plt.plot([j,j],[mini,maxi],c = 'r',alpha=0.7,linewidth=1)

    plt.ylim(mini,maxi)
    plt.xlim(0,ndf.index[-1])

    plt.grid(True)
    plt.ylabel('Position in m')
    plt.xlabel('Zeitschritt')
    plt.title(label)

    plt.savefig(label + '_plot.pdf')
    plt.savefig(label + '_plot.png')
    plt.show()

custom_plot(df,wdf,4,'x-Achse')
custom_plot(df,wdf,5,'y-Achse')
custom_plot(df,wdf,6,'z-Achse')
