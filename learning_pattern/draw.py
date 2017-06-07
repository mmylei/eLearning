import matplotlib
matplotlib.use('agg')
from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import os
from os import listdir, path, mkdir
import sys


# keep your data file as the following format, you can check the .ld file as an example
# then you can use this script to draw pictures using `python draw.py {file_name}`
#
# x\t{x_axis_name}\t{x_axis_labels}
# y\t{y_axis_name}\t{y_axis_labels}
# xtick\t{x_axis_ticks}
# ytick\t{y_axis_ticks}
# data\t{line_name}\t{line_data}
# data\t{line_name}\t{line_data}
# ...

# support latex rendering
# os.environ["PATH"] += os.pathsep + '/usr/local/texlive/2016/bin/x86_64-darwin'
# rc('text', usetex=True)
# plt.rc('font', family='serif')


def read_file(file_path):
    with open(file_path, 'r') as infile:
        line = infile.readline().strip()
        data = {
            'lines': {},
            'file_name': file_path.split('/')[-1].split('.')[0],
            'order': []
        }
        while line != '':
            params = line.split('\t')
            if params[0] == 'x':
                data['x_label'] = params[1]
                data['x_series'] = params[2:]
            elif params[0] == 'y':
                data['y_label'] = params[1]
                data['y_series'] = params[2:]
            elif params[0] == 'ytick':
                data['y_tick'] = [float(x) for x in params[1:]]
            elif params[0] == 'xtick':
                data['x_tick'] = [float(x) for x in params[1:]]
            elif params[0] == 'data':
                data['lines'][params[1]] = [float(x) for x in params[2:]]
                while len(data['lines'][params[1]]) < len(data['x_series']):
                    data['lines'][params[1]].append(float('NaN'))
                data['order'].append(params[1])
            line = infile.readline().strip()
        if 'x_tick' not in data:
            data['x_tick'] = range(len(data['x_series']))
    return data


def draw_line(data, suffix):
    line_width = 2
    markers = [
        {
            'marker': 's',
            'mew': 1,
            'markerSize': 14
        }, {
            'marker': '^',
            'mew': 1,
            'markerSize': 14
        }, {
            'marker': 'd',
            'mew': 1,
            'markerSize': 14
        }, {
            'marker': '*',
            'mew': 1,
            'markerSize': 16
        }, {
            'marker': '.',
            'mew': 1,
            'markerSize': 16
        }, {
            'marker': '+',
            'mew': 2,
            'markerSize': 14
        }, {
            'marker': 'x',
            'mew': 2,
            'markerSize': 14
        }]
    legend_text_size = 20
    label_text_size = 30
    tick_text_size = 24
    plots = []
    marker = 0
    plt.figure(figsize=(9.1, 6.7))
    for label in data['order']:
        # print data['x_tick'], data['lines'][label]
        p, = plt.plot(data['x_tick'], data['lines'][label], color='k', label=label,
                      markerfacecolor='w', lineWidth=line_width, **markers[marker])
        plots.append(p)
        marker += 1
    # plt.xticks(range(len(data['x_series'])), data['x_series'], fontsize=tick_text_size)
    plt.xticks(data['x_tick'], data['x_series'], fontsize=tick_text_size)
    plt.yticks(data['y_tick'], data['y_series'], fontsize=tick_text_size)
    plt.xlabel(data['x_label'], fontsize=label_text_size)
    plt.ylabel(data['y_label'], fontsize=label_text_size)
    lgd = plt.legend(handles=plots, fontsize=legend_text_size, labelspacing=0.08,
               bbox_to_anchor=(0., 1.02, 1., 0.102), loc=3, ncol=3, mode='expand', borderaxespad=0.)
    # print data
    plt.grid(which='major', axis='y', linestyle='dashed', linewidth=1)
    plt.tight_layout()

    # save picture into 'pics' directory
    if not path.isdir('./pics'):
        mkdir('./pics')
    savefig('./pics/' + data['file_name'] + '.' + suffix, bbox_extra_artists=(lgd,), bbox_inches='tight')


def draw_bar(data, suffix):
    legend_text_size = 20
    label_text_size = 30
    tick_text_size = 24
    total_width = 0.8
    patterns = ["+", "\\", ".", "x", "//", " ", "o", "O", "*", "-"]

    center = data['x_tick']
    start = [x - total_width / 2 for x in center]
    offset = total_width / len(data['lines'])
    plots = []
    plt.figure(figsize=(9.1, 6.7))
    hatch = 0
    for label in data['order']:
        # print data['x_tick'], data['lines'][label]
        p = plt.bar(start, data['lines'][label], width=offset, label=label,
                    hatch=patterns[hatch], color='None', edgecolor='black')
        hatch += 1
        plots.append(p)
        start = [x + offset for x in start]
    # plt.xticks(range(len(data['x_series'])), data['x_series'], fontsize=tick_text_size)
    plt.xticks(data['x_tick'], data['x_series'], fontsize=tick_text_size)
    plt.yticks(data['y_tick'], data['y_series'], fontsize=tick_text_size)
    plt.xlabel(data['x_label'], fontsize=label_text_size)
    plt.ylabel(data['y_label'], fontsize=label_text_size)
    lgd = plt.legend(handles=plots, fontsize=legend_text_size, labelspacing=0.08,
                     bbox_to_anchor=(0., 1.02, 1., 0.102), loc=3, ncol=3, mode='expand', borderaxespad=0.)
    # for hdler in lgd.legendHandles:
    #     hdler._sizes = [1]
    # print data
    plt.grid(which='major', axis='y', linestyle='dashed', linewidth=1)
    plt.yscale('log')
    plt.tight_layout()
    # plt.show()
    # save picture into 'pics' directory
    if not path.isdir('./pics'):
        mkdir('./pics')
    savefig('./pics/' + data['file_name'] + '.' + suffix, bbox_extra_artists=(lgd,), bbox_inches='tight')


def main():
    files = listdir('./figure_data')
    for file_name in files:
        if '.ld' in file_name:
            data = read_file('./figure_data/' + file_name)
            print file_name
            draw_line(data, 'png')
        elif '.bd' in file_name:
            data = read_file('./figure_data/' + file_name)
            print file_name
            draw_bar(data, 'png')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    main()
