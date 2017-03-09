import MySQLdb
import time


def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(`session` varchar(64), user_id int, video_id varchar(64), "
              "video_time_start decimal(10, 5) not null, video_time_end decimal(10, 5) not null, "
              "real_time_start datetime, real_time_end datetime);")
    conn.commit()


def insert_table(conn, fields, p, table):
    c = conn.cursor()
    c.execute("INSERT INTO " + table + "(" + ','.join(fields) + ")" + " VALUES(" + ','.join(['%s']*len(p)) + ");", p)
    conn.commit()


def transform_time(time_str):
    return time.mktime(time.strptime(time_str))


if __name__ == '__main__':

    terms = [
        # java
        'COMP102.1x-2T2015',
        'COMP102.1x-2T2016',
        'COMP102.1x-3T2016',
        'COMP102.1x-4T2015',
        'COMP102.2x-1T2016',
        'COMP102.2x-2T2016',
        'COMP102.2x-3T2016',
        'COMP102.2x-4T2015',
        'COMP102x-2T2014',
        # android
        'COMP107x-3T2016',
        'COMP107x-2016_T1',
        'COMP107x-1T2016',
        # speaking
        'EBA101x-3T2016',
        'EBA101x-3T2014',
        'EBA101x-1T2016',
        # writing
        'EBA102x-4Q2015',
        'EBA102x-3T2016',
        'EBA102x-1T2016'
    ]
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
    for term in terms:
        print('start convert term ' + term)
        table_name1 = ('HKUSTx-' + term + '-clickstream').replace('-', '_').replace('.', '_')
        # check if the table exists
        cursor = conn.cursor()
        cursor.execute('SHOW TABLES LIKE \'' + table_name1 + '\';')
        tables = cursor.fetchall()
        if len(tables) == 0:
            continue
        table_name2 = ('HKUSTx-' + term + '-video_play_piece').replace('-', '_').replace('.', '_')
        create_table(conn, table_name2)
        cursor.execute('SELECT distinct(user_id) FROM ' + table_name1 + ';')
        result = cursor.fetchall()
        for row in result:
            if row[0] is None:
                continue
            user_id = int(row[0])
            cursor.execute('SELECT video_id, event_type, `current_time`, old_time, new_time, saved_video_position, `session`, event_time'
                           ' FROM ' + table_name1 +
                           ' WHERE user_id=' + str(user_id) + ' order by event_time;')
            result_user = cursor.fetchall()
            playing = {}
            event_start = {}
            temporary = {}
            temporary_time = {}
            current_session = None
            for row_user in result_user:
                video_id = row_user[0]
                # if video_id not in last_progress:
                #     last_progress[video_id] = 0
                event_type = row_user[1]
                session = row_user[6]
                if session != current_session:
                    playing = {}
                    event_start = {}
                    temporary = {}
                    temporary_time = {}
                    current_session = session
                event_time = row_user[7]
                if row_user[2] is not None:
                    current_time = float(row_user[2])
                else:
                    current_time = None
                if event_type == 'play_video' and current_time is not None:
                    if video_id not in playing:
                        playing[video_id] = current_time
                        event_start[video_id] = event_time
                    else:
                        temporary[video_id] = current_time
                        temporary_time[video_id] = event_time
                elif event_type in ['stop_video', 'pause_video']:
                    if video_id in playing:
                        cursor.execute('INSERT INTO ' + table_name2 + ' VALUES(%s, %s, %s, %s, %s, %s, %s);',
                                       [session, user_id, video_id, playing[video_id], current_time, event_start[video_id], event_time])
                        del playing[video_id]
                        del event_start[video_id]
                        if video_id in temporary:
                            del temporary[video_id]
                elif event_type == 'seek_video':
                    if video_id in playing and row_user[3] is not None:
                        old_time = float(row_user[3])
                        cursor.execute('INSERT INTO ' + table_name2 + ' VALUES(%s, %s, %s, %s, %s, %s, %s);',
                                       [session, user_id, video_id, playing[video_id], old_time, event_start[video_id], event_time])
                        if video_id in temporary:
                            del temporary[video_id]
                            del playing[video_id]
                    elif video_id in playing and video_id in temporary:
                        cursor.execute('INSERT INTO ' + table_name2 + ' VALUES(%s, %s, %s, %s, %s, %s, %s);',
                                       [current_session, user_id, video_id, playing[video_id], temporary[video_id], event_start[video_id],
                                        temporary_time[video_id]])
                        del temporary[video_id]
                        del playing[video_id]
                    elif video_id in playing:
                        del playing[video_id]

                    if row_user[4] is not None:
                        new_time = float(row_user[4])
                        playing[video_id] = new_time
                        event_start[video_id] = event_time
                elif event_type == 'save_user_state' and row_user[5] is not None:
                    if video_id not in playing:
                        playing[video_id] = float(row_user[5])
                        event_start[video_id] = event_time
                    elif playing[video_id] != row_user[5]:
                        temporary[video_id] = float(row_user[5])
                        temporary_time[video_id] = event_time

            # make up plays without `stop` or `pause` event
            for video_id in temporary:
                cursor.execute('INSERT INTO ' + table_name2 + ' VALUES(%s, %s, %s, %s, %s, %s, %s);',
                               [current_session, user_id, video_id, playing[video_id], temporary[video_id], event_start[video_id],
                                temporary_time[video_id]])

            conn.commit()
