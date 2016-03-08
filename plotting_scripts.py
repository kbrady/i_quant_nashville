# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 14:44:23 2016
A set of functions to plot things

@author: kate
"""

# to plot histograms
import matplotlib.pyplot as plt
# to interpret times correctly
from matplotlib import dates
# to fix the plot axes
from mpl_toolkits.axes_grid.axislines import Subplot
# to read times like a human
import time
# to view images
import matplotlib.image as mpimg
# to calculate statistics
import numpy as np
# to see dates in plt
from matplotlib import dates

# build a histogram
def get_histogram_lists(value_list, bins=10, threshold=2, percentage=False):
    combined = [v for vlist in value_list for v in vlist]
    hist, bin_dividers = get_histogram(combined, bins, threshold)
    hist_list = [[] for i in range(len(value_list))]
    for i in range(bins):
        for j in range(len(value_list)):
            if i == 0:
                raw_num = len([v for v in value_list[j] if v >= bin_dividers[i] and v <= bin_dividers[i+1]])
            else:
                raw_num = len([v for v in value_list[j] if v > bin_dividers[i] and v <= bin_dividers[i+1]])
            if percentage:
                hist_list[j].append(float(raw_num)/len(value_list[j]))
            else:
                hist_list[j].append(raw_num)
    return hist_list, bin_dividers

# build a cumulative histogram
def get_cummulative_histogram_lists(value_list, bins=10, threshold=2, percentage=False):
    combined = [v for vlist in value_list for v in vlist]
    hist, bin_dividers = get_histogram(combined, bins, threshold)
    hist_list = [[] for i in range(len(value_list))]
    for i in range(bins):
        for j in range(len(value_list)):
            raw_num = len([v for v in value_list[j] if v <= bin_dividers[i+1]])
            if percentage:
                hist_list[j].append(float(raw_num)/len(value_list[j]))
            else:
                hist_list[j].append(raw_num)
    return hist_list, bin_dividers

def get_histogram(values, bins=10, threshold=2, counter=0):
    min_value = min(values)
    max_value = max(values)
    diff = max_value - min_value
    bin_dividers = [min_value]
    for i in range(bins):
        bin_dividers.append(bin_dividers[-1]+(diff/bins))
    bin_dividers[-1] = max_value
    hist = []
    for i in range(bins):
        if i == 0:
            hist.append(len([v for v in values if v >= bin_dividers[i] and v <= bin_dividers[i+1]]))
        else:
            hist.append(len([v for v in values if v > bin_dividers[i] and v <= bin_dividers[i+1]]))
    # get rid of outliers
    if counter < 3:        
        if hist[0] < threshold:
            if hist[-1] < threshold:
                return get_histogram([v for v in values if v > bin_dividers[1] and v <= bin_dividers[-2]], bins, threshold, counter+1)
            else:
                return get_histogram([v for v in values if v > bin_dividers[1]], bins, threshold, counter+1)
        if hist[-1] < threshold:
            return get_histogram([v for v in values if v <= bin_dividers[-2]], bins, threshold, counter+1)
    # return values
    return hist, bin_dividers

def plot_frame_attr(frame, attr, y_label='', title='', to_100=False):
    tick_labels = list(frame['text'])
    relevant_columns = [c for c in frame.columns if c.find(attr) > -1]
    bar_list = [list(frame[c]) for c in relevant_columns]
    legend_names = [c[c.find(attr)+len(attr)+1:].strip() for c in relevant_columns]
    plot_bars(bar_list, tick_labels, x_label='Token', y_label=y_label, title=title, legend_names=legend_names)
    if to_100:
        plt.ylim([0,100])
    plt.show()

def plot_bars(bar_list, tick_labels, tick_positions=None, x_label='', y_label='', title='', legend_names=[], loc=2):
    # plot values
    fig = plt.figure()
    fig.suptitle(title)
    ax = Subplot(fig, 111)
    ax = fig.add_subplot(ax)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    # plot each dataset
    width = .9/len(bar_list)                      # the width of the bars
    ind = np.array(range(len(bar_list[0])))
    color_list = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928']
    recs = []
    for i in range(len(bar_list)):
        recs.append(ax.bar(ind + (width * i), bar_list[i], width, color=color_list[i], linewidth=0))
    # calculate where the labels should go
    if tick_positions is not None:
        ax.set_xticks(np.array(tick_positions) + .5)
    else:
        ax.set_xticks(ind + .5)
    xtickNames = ax.set_xticklabels(tick_labels)
    # adjust how the axis shows
    ax.axis["bottom"].major_ticklabels.set_pad(30)
    ax.axis["bottom"].label.set_pad(20)
    ax.axis["bottom"].major_ticklabels.set_rotation(30)
    ax.axis["bottom"].major_ticks.set_visible(False)
    ax.axis["top"].set_visible(False)
    # add a legend
    if len(legend_names) == len(recs):
        legend_names = tuple([ln.title() for ln in legend_names])
        legend_colors = tuple(r[0] for r in recs)
        ax.legend( legend_colors, legend_names, frameon=False, loc=loc )
    
    plt.gcf().subplots_adjust(bottom=0.19)    # adjust the bottom of the plot
    plt.show()

def plot_histogram(value_list, bins=10, cummulative=False, threshold=2, is_time=False, is_log=False, x_label='', y_label='', title='', most_labels=15, legend_names=[], loc=2, percentage=False):
    if is_log:
        # allow log scales
        value_list = [[np.log10(v) for v in vl] for vl in value_list]
    if cummulative:
        hist_list, bin_dividers = get_cummulative_histogram_lists(value_list, bins=bins, threshold=threshold, percentage=percentage)
    else:
        hist_list, bin_dividers = get_histogram_lists(value_list, bins=bins, threshold=threshold, percentage=percentage)
    if is_log:
        # allow log scales
        bin_dividers = [10 ** b for b in bin_dividers]
    if is_time:
        bin_labels = [time.strftime("%m/%d/%y", time.localtime((bin_dividers[i-1]+bin_dividers[i])/2)) for i in range(1,len(bin_dividers))]
        x_label = 'Time'
    else:
        bin_labels = ["%.2f" % ((bin_dividers[i-1]+bin_dividers[i])/2) for i in range(1,len(bin_dividers))]
    # calculate where the labels should go
    if len(bin_labels) > most_labels:
        tick_positions = [int(i * (float(len(bin_labels))/most_labels)) for i in range(most_labels)]
        tick_labels = []
        for i in tick_positions:
            tick_labels.append(bin_labels[i])
    else:
        tick_positions = None
        tick_labels = bin_labels
    # plot values
    plot_bars(hist_list, tick_labels, tick_positions=tick_positions, x_label=x_label, y_label=y_label, title=title, legend_names=legend_names, loc=loc)

def scatter(x_values, y_values, labels=[], kargs={}):
    fig = plt.figure()
    fig.suptitle(kargs.get('title',''))
    ax = plt.axes()
    plt.xlabel(kargs.get('x_label',''))
    plt.ylabel(kargs.get('y_label',''))
    dots = ax.scatter(x_values, y_values)
    if len(labels) == len(x_values):
        cursor = datacursor(dots, point_labels=labels, bbox=dict(fc='white', alpha=1), formatter=lambda **kwargs: ', '.join(kwargs['point_label']))
    if kargs.get('trendline', False):
        # calc the trendline
        z = np.polyfit(x_values, y_values, 1)
        p = np.poly1d(z)
        ax.plot(x_values,p(x_values),"r-")
        #squared error
        error = np.mean((np.array(y_values) - p(x_values)) ** 2) ** .5
        # the line equation:
        if z[1] < 0:
            plt.title("y=%.8fx%.8f error:%.3f" % (z[0],z[1],error))
        else:
            plt.title("y=%.8fx+%.8f error:%.3f" % (z[0],z[1],error))
    plt.show()
