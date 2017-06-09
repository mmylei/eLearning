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

good_uid = [524811, 2135908, 2314026, 2454324, 2546039]
very_poor_uid = [386558, 696595, 1102783, 3240464, 3821755]
poor_uid = [4026932, 2639832, 7768096, 8730616, 7186222]

all_uid = []
all_uid.extend(good_uid)
all_uid.extend(poor_uid)
all_uid.extend(very_poor_uid)

sql2 = 'select video_id, sequence, duration from Video_Basic_Info where module_number < 6 order by sequence;'
conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
cursor = conn.cursor()
cursor.execute(sql2)
result2 = cursor.fetchall()
features = []
labels = []
for uid in all_uid:
    result_user = []
    for row in result2:
        video_id = row[0]
        duration = float(row[2])
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
                partial_array[index] += 1
            elif row1[0] == 'seek_video' and row1[4] is not None and row1[5] is not None:
                index = get_index(row1[4], row1[0], row1[5] - row1[4])
                partial_array[index] += 1
                index = get_index(row1[5], row1[0], row1[4] - row1[5])
                partial_array[index] += 1
            elif row1[0] == 'speed_change_video' and row1[2] is not None and row1[6] is not None and row1[7] is not None:
                index = get_index(row1[2], row1[0], row1[7] - row1[6])
                partial_array[index] += 1
                index = get_index(row1[2], row1[0], row1[6] - row1[7])
                partial_array[index] += 1
        result_user.extend(partial_array)
    features.append(result_user)
    if uid in good_uid:
        features.append(1)
    elif uid in poor_uid:
        features.append(0)
    else:
        features.append(-1)

with open('data.json', 'w') as f:
    f.write(json_wrapper.dumps({'features': features, 'labels': labels}))
