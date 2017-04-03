import MySQLdb
from draw_video_repeat import repeat_ratio

threshold = 1.35


def watch_area(repeat_array):
    result = []
    start = None
    for i in range(len(repeat_array)):
        if repeat_array[i] >= threshold and start is None:
            start = i
        if repeat_array[i] < threshold and start is not None:
            end = i
            result.append((start, end))
            start = None
    return result


if __name__ == '__main__':
    terms = [
            'COMP102.1x-4T2015',
            'COMP107x-2016_T1'
        ]

    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
    for term in terms:
        print('start calc term ' + term)
        table_name = ('HKUSTx-' + term + '-video_play_piece').replace('-', '_').replace('.', '_')
        table_name2 = ('HKUSTx-' + term + '-user_video').replace('-', '_').replace('.', '_')
        cursor = conn.cursor()
        cursor.execute('SELECT distinct(video_id) FROM ' + table_name + ';')
        result = cursor.fetchall()
        repeat_table = {}
        durations = {}
        total_repeat_ratio = 0.0
        total_time_slots = 0
        for row in result:
            if row[0] is None:
                continue
            video_id = row[0]
            cursor.execute('SELECT video_time_start, video_time_end, user_id'
                           ' FROM ' + table_name +
                           ' WHERE video_id=\'' + video_id + '\';')
            result_video = cursor.fetchall()
            watch_times = []
            for time in result_video:
                if time[0] is not None and time[1] is not None:
                    if float(time[0]) < float(time[1]):
                        watch_times.append([float(time[0]), float(time[1]), str(time[2])])
            cursor.execute('SELECT duration'
                           ' FROM eLearning.Video_Basic_Info'
                           ' WHERE video_id=\'' + video_id + '\';')
            d_result = cursor.fetchall()
            if len(d_result) == 0:
                print 'cannot find video info:', video_id
                continue
            duration = float(d_result[0][0])
            durations[video_id] = duration
            repeat_table[video_id] = repeat_ratio(duration, watch_times)
            total_repeat_ratio += sum(repeat_table[video_id])
            total_time_slots += len(repeat_table[video_id])
        threshold = total_repeat_ratio / total_time_slots
        print('threshold of term ' + term + 'is ' + str(threshold))
        for row in result:
            if row[0] is None:
                continue
            video_id = row[0]
            cursor.execute('SELECT count(*)'
                           ' FROM ' + table_name2 +
                           ' WHERE video_id=\'' + video_id + '\' AND is_covered=1;')
            watched_num = str(cursor.fetchall()[0][0])
            areas = watch_area(repeat_table[video_id])
            repeat_area_portion = sum(x[1] - x[0] for x in areas) / durations[video_id]
            cursor.execute('UPDATE Video_Stats_Info' +
                           ' SET watched_area1=\'' + str(areas) + '\', num_watched_all=' + watched_num +
                           ', time_spent_ratio=' + str(repeat_area_portion) +
                           ' WHERE video_id=\'' + video_id + '\';')
    conn.commit()
    conn.close()
