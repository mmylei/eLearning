import MySQLdb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np
import os

width = 1024
height = 256
my_dpi = 256
# max_watching = 26665.0
dir = "./"


def draw(video_id, duration, watchs):
    seconds = int(duration)
    data = np.zeros((1, seconds), dtype=float)
    for watch in watchs:
        x1 = int(watch[0] / duration * seconds)
        x2 = int(watch[1] / duration * seconds)
        if x1 < 0:
            x1 = 0
        if x2 >= seconds:
            x2 = seconds - 1
        for i in range(x1, x2):
            try:
                data[0][i] += 1.0
            except Exception:
                print watch[0], watch[1], duration, x2
                raise
    max_watching = max(data[0])
    min_watching = np.percentile(data[0], 3)
    # print min(data[0]), min_watching, np.percentile(data[0], 20), np.percentile(data[0], 30), max_watching
    for i in range(seconds):
        data[0][i] = (data[0][i] - min_watching) / (max_watching - min_watching)
        if data[0][i] < 0:
            data[0][i] = 0

    plt.figure(figsize=(width / my_dpi, height / my_dpi), dpi=my_dpi)
    fig = plt.imshow(data, extent=(0, seconds, 0, seconds * height / width), cmap=cm.plasma)
    # plt.axis('off')
    # fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.xticks(range(0, seconds, 50), fontsize=5)
    plt.xlabel('Video Time (second)', fontsize=5)
    plt.savefig(dir + video_id + '.png', format='png', bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    terms = [
            'COMP102.1x-4T2015',
            'COMP107x-2016_T1'
        ]

    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
    for term in terms:
        print('start draw term ' + term)
        if not os.path.exists('./area/'):
            os.mkdir('./area/')
        dir = './area/' + term + '/'
        if not os.path.exists(dir):
            os.mkdir(dir)
        table_name = ('HKUSTx-' + term + '-video_play_piece').replace('-', '_').replace('.', '_')
        cursor = conn.cursor()
        cursor.execute('SELECT distinct(video_id) FROM ' + table_name + ';')
        result = cursor.fetchall()
        for row in result:
            if row[0] is None:
                continue
            video_id = row[0]
            print('start draw video ' + video_id)
            cursor.execute('SELECT video_time_start, video_time_end'
                           ' FROM ' + table_name +
                           ' WHERE video_id=\'' + video_id + '\';')
            result_video = cursor.fetchall()
            watch_times = []
            for time in result_video:
                if time[0] is not None and time[1] is not None:
                    if float(time[0]) < float(time[1]):
                        watch_times.append((float(time[0]), float(time[1])))
            cursor.execute('SELECT duration'
                           ' FROM eLearning.Video_Basic_Info'
                           ' WHERE video_id=\'' + video_id + '\';')
            d_result = cursor.fetchall()
            if len(d_result) == 0:
                print 'cannot find video info:', video_id
                continue
            duration = float(d_result[0][0])
            draw(video_id, duration, watch_times)

    # print(max_watching)
