import MySQLdb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

width = 1024
height = 256
my_dpi = 256
dir = "./"


def play_times(duration, watchs):
    seconds = int(duration)
    count_repeat = np.zeros(seconds, dtype=float)
    for time in watchs:
        point = int(time)
        if 0 <= point < seconds:
            count_repeat[point] += 1
    return count_repeat


def draw(video_id, duration, watchs):
    data = play_times(duration, watchs)
    seconds = int(duration)
    plt.figure(figsize=(width / my_dpi, height / my_dpi), dpi=my_dpi)
    # plt.plot(range(width), count_repeat)
    # plt.plot(range(width), count_distinct)
    plt.plot(range(seconds), data)
    plt.xlabel('Video Time (second)', fontsize=5)
    plt.xticks(range(0, seconds, 50), fontsize=5)
    plt.ylabel('Play Count', fontsize=5)
    # plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5], ['1', '1.1', '1.2', '1.3', '1.4', '1.5'], fontsize=5)
    plt.savefig(dir + video_id + '.png', format='png', bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    terms = [
            'COMP102.1x-4T2015',
            'COMP107x-2016_T1'
        ]

    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
    for term in terms:
        print('start draw term ' + term)
        if not os.path.exists('./play/'):
            os.mkdir('./play/')
        dir = './play/' + term + '/'
        if not os.path.exists(dir):
            os.mkdir(dir)

        table_name = ('HKUSTx-' + term + '_clickstream').replace('-', '_').replace('.', '_')
        cursor = conn.cursor()
        cursor.execute('SELECT distinct(video_id) FROM ' + table_name + ';')
        result = cursor.fetchall()
        for row in result:
            if row[0] is None:
                continue
            video_id = row[0]
            print('start draw video ' + video_id)
            cursor.execute('SELECT `current_time`'
                           ' FROM ' + table_name +
                           ' WHERE video_id=\'' + video_id + '\' ' + 'and event_type = \'play_video\' and `current_time` is not NULL;')
            play_records = [x[0] for x in cursor.fetchall()]
            cursor.execute('SELECT duration'
                           ' FROM eLearning.Video_Basic_Info'
                           ' WHERE video_id=\'' + video_id + '\';')
            d_result = cursor.fetchall()
            if len(d_result) == 0:
                print 'cannot find video info:', video_id
                continue
            duration = float(d_result[0][0])
            draw(video_id, duration, play_records)

