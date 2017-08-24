import sys
import MySQLdb
import math
import json_wrapper
import numpy as np
import pandas as pd

terms = [
    # java
    # '102.1x-2T2015',
    # '102.1x-2T2016',
    # '102.1x-3T2016',
    '102.1x-4T2015',
    # '102.2x-1T2016',
    # '102.2x-2T2016',
    # '102.2x-3T2016',
    # '102.2x-4T2015',
    # '102x-2T2014',
    ]


def get_attempts(json):
    json = json.replace('\\\\', '\\')
    try:
        temp = json_wrapper.loads(json)
    except Exception:
        print json
        raise
    if 'attempts' in temp:
        return temp['attempts']
    else:
        return 0


def get_video_duration(conn):
    table_name = 'Video_Basic_Info'
    sql = 'select video_id, duration from ' + table_name + ' where term_id = \'COMP102_1x\';'
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    dt = [('vid', 'S64'), ('video_duration', np.float32)]
    video_info = np.array(list(result), dtype=dt)
    video_info_df = pd.DataFrame(video_info)
    all_features = pd.read_csv('weekly_quantities.csv')
    new_features = all_features.join(video_info_df.set_index('vid'), on='vid')
    new_features.to_csv('new_weekly_quantities.csv')


def get_users(conn, term):
    table_name1 = (term + '_courseware_studentmodule').replace('-', '_').replace('.', '_')
    sql = 'select distinct student_id from ' + table_name1 + ';'
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return map(lambda x: x[0], result)


def mean(play_piece):
    total = sum(map(lambda x: x[0] * x[1], play_piece))
    length = sum(map(lambda x: x[0], play_piece))
    if total == 0:
        return 0
    return length / total


def std(play_piece):
    m = mean(play_piece)
    if m == 0:
        return 0
    length = sum(map(lambda x: x[0], play_piece))
    return math.sqrt(sum(map(lambda x: (x[1] - m) * (x[1] - m) * x[0], play_piece)) / length)


def get_weekly_grades(cursor, term, uid):
    table_name1 = (term + '_courseware_studentmodule').replace('-', '_').replace('.', '_')
    table_name2 = ('HKUSTx-COMP' + term + '_problem_set').replace('-', '_').replace('.', '_')
    sql = 'select state, grade, max_grade, module_id from ' + table_name1 + ' where student_id = ' + str(
        uid) + ' and module_type = \'problem\' and grade is not NULL;'
    cursor.execute(sql)
    temp = cursor.fetchall()
    result = []
    for row in temp:
        xml_id = row[3].split('@')[-1]
        cursor.execute('select aggregated_category from ' + table_name2 + ' where xml_id=\'' + xml_id + '\';')
        temp1 = cursor.fetchall()
        if len(temp1) > 0:
            result.append([row[0], float(row[1]), float(row[2]), row[3], temp1[0][0]])
    return result


def get_features(conn, term, users):
    sql1 = 'select B.video_id, B.sequence, B.duration, B.module_number from Video_Basic_Info as B, clickstream.Video_Stats_Info as S where B.video_id = S.video_id and S.flag = 1 and B.term_id = \'COMP102_1x\' and B.module_number < 6 order by B.sequence;'
    cursor = conn.cursor()
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    features = []
    table_name5 = ('HKUSTx-COMP' + term + '_clickstream').replace('-', '_').replace('.', '_')
    table_name3 = ('HKUSTx-COMP' + term + '-user_video').replace('-', '_').replace('.', '_')
    table_name2 = ('HKUSTx-COMP' + term + '_video_play_piece').replace('-', '_').replace('.', '_')
    # table_name5 = (term + '_auth_userprofile').replace('-', '_').replace('.', '_')
    # table_name6 = ('HKUSTx-COMP' + term + '_problem_set').replace('-', '_').replace('.', '_')
    # table_name7 = (term + '_commentthread').replace('-', '_').replace('.', '_')
    # table_name11 = (term + '_courseware_studentmodule').replace('-', '_').replace('.', '_')
    print 'num of users:', len(users)
    print 'num of videos:', len(result1)
    total_pairs = len(users) * len(result1)
    processed_count = 0
    for uid in users:
        weekly_grades = get_weekly_grades(cursor, term, uid)
        for row in result1:
            processed_count += 1
            if processed_count == total_pairs or processed_count % 1000 == 0:
                print 'progress:', processed_count, '/', total_pairs
            video_id = row[0]
            duration = math.ceil(float(row[2]))
            module_number = row[3]
            result_user_video = [uid, video_id, module_number]

            cursor.execute('select count(distinct `session`) from clickstream.' + table_name5 +
                           ' where user_id=' + str(uid) + ' and video_id=\'' + video_id + '\' and event_type=\'play_video\';')
            watched_times = int(cursor.fetchall()[0][0])

            sql2 = 'select sum(TIMESTAMPDIFF(SECOND, real_time_start, real_time_end)) as real_watched_duration ' \
               ' from clickstream.' + table_name2 + \
               ' where user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\'' \
               ' and real_time_start >= 0 and real_time_end > real_time_start;'
            cursor.execute(sql2)
            result2 = cursor.fetchall()
            if result2[0][0] is not None:
                result_user_video.append(float(result2[0][0]) / duration)
                if result_user_video[-1] < 0:
                    print uid
            else:
                result_user_video.append(0)

            sql3 = 'select coverage from clickstream.' + table_name3 + \
                   ' where  user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\' and coverage > 0;'
            cursor.execute(sql3)
            result3 = cursor.fetchall()
            if len(result3) > 0:
                result_user_video.append(float(result3[0][0]))
                if result_user_video[-1] < 0:
                    print uid
            else:
                result_user_video.append(0)

            sql4 = 'select sum(video_time_end - video_time_start) as watched_duration ' \
                   ' from clickstream.' + table_name2 + \
                   ' where user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\'' \
                   ' and video_time_start >= 0 and video_time_end > video_time_start and video_time_end <= ' + str(duration) + ';'
            cursor.execute(sql4)
            result4 = cursor.fetchall()
            if result4[0][0] is not None:
                result_user_video.append(float(result4[0][0]) / duration)
                if result_user_video[-1] < 0:
                    print uid
            else:
                result_user_video.append(0)

            sql5 = 'select count(*) from clickstream.' + table_name5 + \
                   ' where user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\' and event_type = \'pause_video\';'
            cursor.execute(sql5)
            result5 = cursor.fetchall()
            if watched_times > 1:
                result_user_video.append(result5[0][0] / watched_times)
            else:
                result_user_video.append(result5[0][0])

            cursor.execute(
                'SELECT event_type, `current_time`, old_time, new_time, saved_video_position, `session`, UNIX_TIMESTAMP(event_time)'
                ' FROM clickstream.' + table_name5 +
                ' WHERE user_id=' + str(uid) + ' and video_id=\'' + video_id + '\' order by event_time;')
            result6 = cursor.fetchall()
            pause_length = 0
            pause_time = None
            current_session = '1234567890'
            for row_user in result6:
                event_type = row_user[0]
                if event_type in ['pause_video', 'play_video']:
                    session = row_user[5]
                    if session is not None and session != current_session:
                        current_session = session
                        pause_time = None
                    if session is not None:
                        if event_type == 'pause_video':
                            pause_time = float(row_user[6])
                        if event_type == 'play_video' and pause_time is not None:
                            pause_length += float(row_user[6]) - pause_time
                            pause_time = None
            if watched_times > 1:
                result_user_video.append(pause_length / duration / watched_times)
            else:
                result_user_video.append(pause_length / duration)

            # get play speed
            cursor.execute(
                'SELECT video_id, event_type, `current_time`, old_time, new_time, saved_video_position, `session`, event_time, new_speed'
                ' FROM clickstream.' + table_name5 +
                ' WHERE user_id=' + str(uid) + ' and video_id=\'' + video_id + '\' order by event_time;')
            result7 = cursor.fetchall()
            playing = {}
            current_session = None
            current_speed = 1
            play_piece = []
            for row_user in result7:
                event_type = row_user[1]
                session = row_user[6]
                if session is not None and session != current_session:
                    playing = {}
                    current_session = session
                    current_speed = 1
                if row_user[2] is not None:
                    current_time = float(row_user[2])
                else:
                    current_time = None
                if event_type == 'play_video' and current_time is not None:
                    playing[video_id] = current_time
                elif event_type in ['stop_video', 'pause_video'] and current_time is not None:
                    if video_id in playing:
                        play_piece.append((playing[video_id], current_time, current_speed))
                        del playing[video_id]
                elif event_type == 'seek_video':
                    if video_id in playing and row_user[3] is not None:
                        old_time = float(row_user[3])
                        play_piece.append((playing[video_id], old_time, current_speed))
                    elif video_id in playing:
                        del playing[video_id]
                    if row_user[4] is not None:
                        new_time = float(row_user[4])
                        playing[video_id] = new_time
                elif event_type == 'speed_change_video' and row_user[8] is not None:
                    # todo no current_time
                    current_speed = float(row_user[8])
            play_piece = map(lambda x: (x[1]-x[0], x[2]), filter(lambda x: x[1] > x[0] > 0, play_piece))

            result_user_video.append(mean(play_piece))
            result_user_video.append(std(play_piece))

            sql9 = 'select count(*) from clickstream.' + table_name5 + \
                   ' where user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\' and event_type = \'seek_video\' and old_time > new_time and new_time >= 0 ;'
            cursor.execute(sql9)
            result9 = cursor.fetchall()
            if watched_times > 1:
                result_user_video.append(result9[0][0] / watched_times)
            else:
                result_user_video.append(result9[0][0])

            sql10 = 'select count(*) from clickstream.' + table_name5 + \
                   ' where user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\' and event_type = \'seek_video\' and old_time < new_time and old_time >= 0 ;'
            cursor.execute(sql10)
            result10 = cursor.fetchall()
            if watched_times > 1:
                result_user_video.append(result10[0][0] / watched_times)
            else:
                result_user_video.append(result10[0][0])

            current_week_grades = filter(lambda x: x[4].endswith(str(module_number)), weekly_grades)
            attempts = sum(map(lambda x: get_attempts(x[0]), current_week_grades))
            result_user_video.append(attempts)

            grade = sum(map(lambda x: x[1], current_week_grades))
            max_grade = sum(map(lambda x: x[2], current_week_grades))
            result_user_video.append(grade)
            result_user_video.append(max_grade)
            if max_grade == 0:
                result_user_video.append(0)
            else:
                result_user_video.append(grade / max_grade)
            result_user_video.append(duration)
            features.append(tuple(result_user_video))
    return features


def reset_feature_column():
    data = np.load('weekly_quantities_data.npz')
    columns = np.array(['module_number', 'real_spent', 'coverage', 'watched', 'pauses', 'pause_length', 'avg_speed', 'std_speed', 'seek_backward', 'seek_forward', 'attempts', 'grade', 'max_grade', 'normalized_grade'], dtype=np.str)
    np.savez('weekly_quantities_data', **{'features': data['features'], 'columns': columns})

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'setcolumn':
        reset_feature_column()
        exit()
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
    if len(sys.argv) == 2 and sys.argv[1] == 'setduration':
        get_video_duration(conn)
        exit()
    all_users = []
    all_features = []
    all_grades = []
    for term in terms:
        users = get_users(conn, term)
        features = get_features(conn, term, users)
        all_users.extend(users)
        all_features.extend(features)
    dt = [('uid', np.int32), ('vid', 'S64'), ('module_number', np.int32), ('real_spent', np.float32),
          ('coverage', np.float32), ('watched', np.float32), ('pauses', np.float32), ('pause_length', np.float32),
          ('avg_speed', np.float32), ('std_speed', np.float32), ('seek_backward', np.float32),
          ('seek_forward', np.float32), ('attempts', np.float32), ('grade', np.float32), ('max_grade', np.float32),
          ('normalized_grade', np.float32), ('video_duration', np.float32)]
    all_features = np.array(all_features, dtype=dt)
    feature_df = pd.DataFrame(all_features)
    feature_df.to_csv('weekly_quantities.csv')
    #columns = np.array(['module_number', 'real_spent', 'coverage', 'watched', 'pauses', 'pause_length', 'avg_speed', 'std_speed', 'seek_backward', 'seek_forward', 'attempts', 'grade', 'max_grade', 'normalized_grade'], dtype=np.str)
    #np.savez('weekly_quantities_data', **{'features': all_features, 'columns': columns})
