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


def repeat_ratio(duration, watchs):
    seconds = int(duration)
    count_repeat = np.zeros(seconds, dtype=float)
    count_distinct = np.zeros(seconds, dtype=float)
    entries = []
    for watch in watchs:
        x1 = int(watch[0] / duration * seconds)
        x2 = int(watch[1] / duration * seconds)
        if x1 < 0:
            x1 = 0
        if x2 >= seconds:
            x2 = seconds - 1
        # 1 means start, -1 means end
        if x1 < x2:
            entries.append((x1, watch[2], 1))
            entries.append((x2, watch[2], -1))

    entries.sort(key=lambda x: x[0])
    l = len(entries)
    # count for each user
    count = {}
    entry_ptr = 0
    for point in range(seconds):
        while entry_ptr < l and entries[entry_ptr][0] <= point:
            if entries[entry_ptr][2] == 1:
                if entries[entry_ptr][1] not in count:
                    count[entries[entry_ptr][1]] = 1
                else:
                    count[entries[entry_ptr][1]] += 1
            else:
                if count[entries[entry_ptr][1]] > 1:
                    count[entries[entry_ptr][1]] -= 1
                else:
                    del count[entries[entry_ptr][1]]
            entry_ptr += 1
        count_distinct[point] = len(count)
        count_repeat[point] = float(sum(count.itervalues()))

    return [count_repeat[i] / count_distinct[i] - 1 if count_distinct[i] > 0 else 0 for i in range(seconds)]


def draw(video_id, duration, watchs):
    data = repeat_ratio(duration, watchs)
    seconds = int(duration)
    plt.figure(figsize=(width / my_dpi, height / my_dpi), dpi=my_dpi)
    # plt.plot(range(width), count_repeat)
    # plt.plot(range(width), count_distinct)
    plt.plot(range(seconds), data)
    plt.xlabel('Video Time (second)', fontsize=5)
    plt.xticks(range(0, seconds, 50), fontsize=5)
    plt.ylabel('Repeat Ratio', fontsize=5)
    plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5], ['1', '1.1', '1.2', '1.3', '1.4', '1.5'], fontsize=5)
    plt.savefig(dir + video_id + '.png', format='png', bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    terms = [
            'COMP102.1x-4T2015',
            'COMP107x-2016_T1'
        ]

    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
    for term in terms:
        print('start draw term ' + term)
        if not os.path.exists('./repeat/'):
            os.mkdir('./repeat/')
        dir = './repeat/' + term + '/'
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
            cursor.execute('SELECT video_time_start, video_time_end, user_id'
                           ' FROM ' + table_name +
                           ' WHERE video_id=\'' + video_id + '\';')
            result_video = cursor.fetchall()
            watch_times = []
            for time in result_video:
                if time[0] is not None and time[1] is not None:
                    if float(time[0]) < float(time[1]):
                        watch_times.append((float(time[0]), float(time[1]), str(time[2])))
            cursor.execute('SELECT duration'
                           ' FROM eLearning.Video_Basic_Info'
                           ' WHERE video_id=\'' + video_id + '\';')
            d_result = cursor.fetchall()
            if len(d_result) == 0:
                print 'cannot find video info:', video_id
                continue
            duration = float(d_result[0][0])
            draw(video_id, duration, watch_times)

