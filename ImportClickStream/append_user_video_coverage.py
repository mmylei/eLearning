from warnings import filterwarnings
import MySQLdb


def coverage(duration, watchs):
    if len(watchs) == 0:
        return 0.0
    for watch in watchs:
        if watch[0] < 0:
            watch[0] = 0
        if watch[1] > duration:
            watch[1] = duration
    watchs.sort(key=lambda x: x[0])
    start = watchs[0][0]
    end = watchs[0][1]
    total = 0.0
    for watch in watchs:
        if watch[0] > end:
            total += end - start
            start = watch[0]
            end = watch[1]
        elif watch[1] > end:
            end = watch[1]
    total += end - start
    return total / duration

if __name__ == '__main__':
    terms = [
            'COMP102.1x-2T2015',
            'COMP102.1x-2T2016',
            'COMP102.1x-3T2016',
            'COMP102.1x-4T2015',
            'COMP102.2x-1T2016',
            'COMP102.2x-2T2016',
            'COMP102.2x-3T2016',
            'COMP102.2x-4T2015',
        ]
    filterwarnings('ignore', category=MySQLdb.Warning)
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
    for term in terms:
        print('start calc term ' + term)
        table_name1 = ('HKUSTx-' + term + '-user_video').replace('-', '_').replace('.', '_')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, video_id FROM ' + table_name1 + ';')
        user_video_pair = cursor.fetchall()
        table_name2 = ('HKUSTx-' + term + '-video_play_piece').replace('-', '_').replace('.', '_')
        for row in user_video_pair:
            if row[1] is None:
                continue
            user_id = str(row[0])
            video_id = row[1]
            cursor.execute('SELECT video_time_start, video_time_end'
                           ' FROM ' + table_name2 +
                           ' WHERE video_id=\'' + video_id + '\' AND user_id=' + user_id + ';')
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
            cov = coverage(duration, watch_times)
            covered = 0
            if cov > 0.8:
                covered = 1
            cursor.execute('UPDATE ' + table_name1 +
                           ' SET coverage=' + str(cov) + ', is_covered=' + str(covered) +
                           ' WHERE video_id=\'' + video_id + '\' AND user_id=' + user_id + ';')
    conn.commit()
    conn.close()
