import MySQLdb

threshold = 1.3


def watch_area(duration, watchs, watched_num):
    result = []
    start = None
    count = 0
    count_threshold = threshold * watched_num
    entries = []
    for watch in watchs:
        if watch[0] < 0:
            watch[0] = 0
        entries.append((watch[0], 1))
        if watch[1] >= duration:
            watch[1] = duration
        entries.append((watch[1], -1))
    entries.sort(key=lambda x: x[0])
    for entry in entries:
        count += entry[1]
        if count >= count_threshold and start is None:
            start = entry[0]
        if count < count_threshold and start is not None:
            end = entry[0]
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
        for row in result:
            if row[0] is None:
                continue
            video_id = row[0]
            cursor.execute('SELECT video_time_start, video_time_end'
                           ' FROM ' + table_name +
                           ' WHERE video_id=\'' + video_id + '\';')
            result_video = cursor.fetchall()
            watch_times = []
            for time in result_video:
                if time[0] is not None and time[1] is not None:
                    if float(time[0]) < float(time[1]):
                        watch_times.append([float(time[0]), float(time[1])])
            cursor.execute('SELECT duration'
                           ' FROM eLearning.Video_Basic_Info'
                           ' WHERE video_id=\'' + video_id + '\';')
            d_result = cursor.fetchall()
            if len(d_result) == 0:
                print 'cannot find video info:', video_id
                continue
            duration = float(d_result[0][0])
            cursor.execute('SELECT count(*)'
                           ' FROM ' + table_name2 +
                           ' WHERE video_id=\'' + video_id + '\' AND is_covered=1;')
            watched_num = str(cursor.fetchall()[0][0])
            areas = watch_area(duration, watch_times, float(watched_num))
            cursor.execute('UPDATE Video_Stats_Info' +
                           ' SET watched_area2=\'' + str(areas) + '\', num_watched_all=' + watched_num +
                           ' WHERE video_id=\'' + video_id + '\';')
    conn.commit()
    conn.close()
