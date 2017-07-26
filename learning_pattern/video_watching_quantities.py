import MySQLdb
import math


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


def make_array(duration):
    return [0] * total_type


def get_features(conn, term, users):
    sql1 = 'select B.video_id, B.sequence, B.duration from Video_Basic_Info as B, clickstream.Video_Stats_Info as S where B.video_id = S.video_id and S.flag = 1 and B.term_id = \'COMP102_1x\' and B.module_number < 6 order by B.sequence;'
    cursor = conn.cursor()
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    features = []
    table_name5 = ('HKUSTx-COMP' + term + '_clickstream').replace('-', '_').replace('.', '_')
    table_name3 = ('HKUSTx-COMP' + term + '-user_video').replace('-', '_').replace('.', '_')
    table_name2 = ('HKUSTx-COMP' + term + '_video_play_piece').replace('-', '_').replace('.', '_')
    #table_name5 = (term + '_auth_userprofile').replace('-', '_').replace('.', '_')
    table_name6 = (term + '_comment').replace('-', '_').replace('.', '_')
    table_name7 = (term + '_commentthread').replace('-', '_').replace('.', '_')
    table_name8 = (term + '_courseware_studentmodule').replace('-', '_').replace('.', '_')
    for uid in users:
        result_user = []
        for row in result1:
            video_id = row[0]
            duration = math.ceil(float(row[2]))
            partial_array = make_array(duration)

            sql2 = 'select sum(TIMESTAMPDIFF(SECOND, real_time_start, real_time_end)) as real_watched_duration ' \
               ' from clickstream.' + table_name2 + \
               ' where user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\'' \
               ' and real_time_start >= 0 and real_time_end > real_time_start;'
            cursor.execute(sql2)
            result2 = cursor.fetchall()
            if result2[0][0] is not None:
                result_user.append(float(result2[0][0]) / duration)
                if result_user[-1] < 0:
                    print uid
            else:
                result_user.append(0)

            sql3 = 'select coverage from clickstream.' + table_name3 + \
                   ' where  user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\' and coverage > 0;'
            cursor.execute(sql3)
            result3 = cursor.fetchall()
            if len(result3) > 0:
                result_user.append(float(result3[0][0]))
                if result_user[-1] < 0:
                    print uid
            else:
                result_user.append(0)

            sql4 = 'select sum(video_time_end - video_time_start) as watched_duration ' \
                   ' from clickstream.' + table_name2 + \
                   ' where user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\'' \
                   ' and video_time_start >= 0 and video_time_end > video_time_start and video_time_end <= ' + str(duration) + ';'
            cursor.execute(sql4)
            result4 = cursor.fetchall()
            if result4[0][0] is not None:
                result_user.append(float(result4[0][0]) / duration)
                if result_user[-1] < 0:
                    print uid
            else:
                result_user.append(0)

            sql5 = 'select count(event_type) from clickstream.' + table_name5 + \
                   ' where user_id = ' + str(uid) + ' and video_id=\'' + video_id + '\' and event_type = \'pause_video\';'
            cursor.execute(sql5)
            result5 = cursor.fetchall()
            if result5[0][0] is not None:
                result_user.append(result5[0][0])

            sql6 = ''
