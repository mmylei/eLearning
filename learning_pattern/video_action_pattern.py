import math
import numpy as np
import MySQLdb
import json_wrapper

event_types = ['pause_video', 'play_video', 'seek_video', 'speed_change_video']
total_type = 6

terms = [
    # java
    '102.1x-2T2015',
    '102.1x-2T2016',
    '102.1x-3T2016',
    '102.1x-4T2015',
    # '102.2x-1T2016',
    # '102.2x-2T2016',
    # '102.2x-3T2016',
    # '102.2x-4T2015',
    # '102x-2T2014',
    ]


def make_array(duration):
    return [0] * ((int(duration / 5) + 1) * total_type)


def get_index(time, event_type, direction=1):
    index = (int(time / 5) * total_type) + event_types.index(event_type)
    if event_type in ['seek_video', 'speed_change_video'] and direction < 0:
        index += 1
    return index


def get_users(conn, term):
    table_name1 = (term + '_certificates_generatedcertificate').replace('-', '_').replace('.', '_')
    sql = 'select user_id, grade from ' + table_name1 + ';'
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    grades = np.array(map(lambda x: x[1], result), dtype=np.float32)
    good_normal = np.percentile(grades, 75)
    normal_poor = np.percentile(grades, 25)
    labels = map(lambda x: 1 if x >= good_normal else (-1 if x < normal_poor else 0), grades)
    return map(lambda x: x[0], result), labels


def get_features(conn, term, users):
    sql2 = 'select B.video_id, B.sequence, B.duration from Video_Basic_Info as B, clickstream.Video_Stats_Info as S where B.video_id = S.video_id and S.flag = 1 and B.module_number < 6 order by B.sequence;'
    cursor = conn.cursor()
    cursor.execute(sql2)
    result2 = cursor.fetchall()
    features = []
    table_name2 = ('HKUSTx-COMP' + term + '_clickstream').replace('-', '_').replace('.', '_')
    table_name3 = ('HKUSTx-COMP' + term + '-user_video').replace('-', '_').replace('.', '_')
    table_name4 = ('HKUSTx-COMP' + term + '_video_play_piece').replace('-', '_').replace('.', '_')
    for uid in users:
        result_user = []
        for row in result2:
            video_id = row[0]
            duration = math.ceil(float(row[2]))
            partial_array = make_array(duration)
            sql1 = 'select event_type, event_time, `current_time`, slide_type, old_time, new_time, old_speed, new_speed' \
                   ' from clickstream.' + table_name2 + \
                   ' where user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\'' \
                                                                                    ' order by event_time;'
            cursor.execute(sql1)
            result1 = cursor.fetchall()
            for row1 in result1:
                if row1[0] in ['play_video', 'pause_video'] and row1[2] is not None:
                    index = get_index(row1[2], row1[0])
                    # print row1[0], row1[2], duration
                    if index >= len(partial_array):
                        index = len(partial_array) - 1
                    partial_array[index] += 1
                elif row1[0] == 'seek_video' and row1[4] is not None and row1[5] is not None:
                    index = get_index(row1[4], row1[0], row1[5] - row1[4])
                    if index >= len(partial_array):
                        # print row1[0], row1[4], row1[5], duration
                        index = len(partial_array) - 1
                    partial_array[index] += 1
                    index = get_index(row1[5], row1[0], row1[4] - row1[5])
                    if index >= len(partial_array):
                        index = len(partial_array) - 1
                    partial_array[index] += 1
                elif row1[0] == 'speed_change_video' and row1[2] is not None and row1[6] is not None and row1[
                    7] is not None:
                    index = get_index(row1[2], row1[0], row1[7] - row1[6])
                    partial_array[index] += 1
                    index = get_index(row1[2], row1[0], row1[6] - row1[7])
                    partial_array[index] += 1
            result_user.extend(partial_array)
            sql3 = 'select coverage from clickstream.' + table_name3 + \
                   ' where  user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\';'
            cursor.execute(sql3)
            result3 = cursor.fetchall()
            if len(result3) > 0:
                result_user.append(result3[0][0])
            else:
                result_user.append(0)
            sql4 = 'select sum(video_time_end - video_time_start) as watched_duration ' \
                   ' from clickstream.' + table_name4 + \
                   ' where user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\';'
            cursor.execute(sql4)
            result4 = cursor.fetchall()
            if result4[0][0] is not None:
                result_user.append(float(result4[0][0]) / duration)
            else:
                result_user.append(0)
        features.append(result_user)
    return features

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
all_users = []
all_features = []
all_labels = []
for term in terms:
    users, labels = get_users(conn, term)
    features = get_features(conn, term, users)
    all_users.extend(users)
    all_labels.extend(labels)
    all_features.extend(features)

with open('data.json', 'w') as f:
    f.write(json_wrapper.dumps({'features': all_features, 'labels': all_labels}))
