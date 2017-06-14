import math
import MySQLdb
import json_wrapper

event_types = ['pause_video', 'play_video', 'seek_video', 'speed_change_video']
total_type = 6


def make_array(duration):
    return [0] * ((int(duration / 5) + 1) * total_type)


def get_index(time, event_type, direction=1):
    index = (int(time / 5) * total_type) + event_types.index(event_type)
    if event_type in ['seek_video', 'speed_change_video'] and direction < 0:
        index += 1
    return index
sql_good = 'select user_id from 102_1x_4T2015_certificates_generatedcertificate where grade >= 0.80;'
sql_medium = 'select user_id from 102_1x_4T2015_certificates_generatedcertificate where grade >= 0.60 and grade <0.80;'
sql_poor = 'select user_id from 102_1x_4T2015_certificates_generatedcertificate where grade < 0.60;'
conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
cursor = conn.cursor()
cursor.execute(sql_good)
good_uid = []
very_poor_uid = []
poor_uid = []
good_result = cursor.fetchall()
for i in good_result:
    good_uid.append(i[0])
cursor.execute(sql_poor)
very_poor_result = cursor.fetchall()
for i in very_poor_result:
    very_poor_uid.append(i[0])
cursor.execute(sql_medium)
poor_result = cursor.fetchall()
for i in poor_result:
    poor_uid.append(i[0])

all_uid = []
all_uid.extend(good_uid)
all_uid.extend(poor_uid)
all_uid.extend(very_poor_uid)

sql2 = 'select video_id, sequence, duration from Video_Basic_Info where module_number < 6 order by sequence;'
cursor.execute(sql2)
result2 = cursor.fetchall()
features = []
labels = []
test_index = []
test_index.extend(range(1, 601))
test_index.extend(range(900, 1201))
test_index.extend(range(1240, 1300))
train_index = filter(lambda x: x not in test_index, range(len(all_uid)))
for uid in all_uid:
    result_user = []
    for row in result2:
        video_id = row[0]
        duration = math.ceil(float(row[2]))
        partial_array = make_array(duration)
        sql1 = 'select event_type, event_time, `current_time`, slide_type, old_time, new_time, old_speed, new_speed' \
               ' from clickstream.HKUSTx_COMP102_1x_4T2015_clickstream' \
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
            elif row1[0] == 'speed_change_video' and row1[2] is not None and row1[6] is not None and row1[7] is not None:
                index = get_index(row1[2], row1[0], row1[7] - row1[6])
                partial_array[index] += 1
                index = get_index(row1[2], row1[0], row1[6] - row1[7])
                partial_array[index] += 1
        result_user.extend(partial_array)
        sql3 = 'select coverage from clickstream.HKUSTx_COMP102_1x_4T2015_user_video ' \
               ' where  user_id = ' + str(uid) + ' and video_id=\'' + video_id + ';\''
        cursor.execute(sql3)
        result3 = cursor.fetchall()
        result_user.append(result3[0][0])
        sql4 = 'select sum(video_time_end - video_time_start) as watched_duration ' \
               'from clickstream.HKUSTx_COMP102_1x_4T2015_video_play_piece ' \
               ' where user_id = ' + str(uid) + ' and video_id=\'' + video_id + ';\''
        cursor.execute(sql4)
        result4 = cursor.fetchall()
        result_user.append(result4[0][0]/duration)
    features.append(result_user)
    if uid in good_uid:
        labels.append(1)
    elif uid in poor_uid:
        labels.append(0)
    else:
        labels.append(-1)

with open('data.json', 'w') as f:
    f.write(json_wrapper.dumps({'features': features, 'labels': labels, 'test_index': test_index, 'train_index': train_index}))
