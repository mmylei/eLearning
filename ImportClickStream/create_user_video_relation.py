import MySQLdb
import sys


def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(user_id int, video_id varchar(64), is_finished tinyint(1) default 0,"
              "last_progress decimal(15, 5));")
    conn.commit()


def insert_table(conn, fields, p, table):
    c = conn.cursor()
    c.execute("INSERT INTO " + table + "(" + ','.join(fields) + ")" + " VALUES(" + ','.join(['%s']*len(p)) + ");", p)
    conn.commit()


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
        table_name2 = ('HKUSTx-' + term + '-user_video').replace('-', '_').replace('.', '_')
        create_table(conn, table_name2)
        cursor.execute('SELECT distinct(user_id) FROM ' + table_name1 + ';')
        result = cursor.fetchall()
        for row in result:
            user_id = int(row[0])
            cursor.execute('SELECT video_id, event_type, `current_time`, old_time, new_time, saved_video_position'
                           ' FROM ' + table_name1 +
                           ' WHERE user_id=' + str(user_id) + ';')
            result_user = cursor.fetchall()
            finished = {}
            last_progress = {}
            for row_user in result_user:
                video_id = row_user[0]
                if video_id not in last_progress:
                    last_progress[video_id] = 0
                event_type = row_user[1]
                if event_type == 'stop_video':
                    finished[video_id] = 1
                elif event_type == 'seek_video':
                    if row_user[4] is not None:
                        last_progress[video_id] = max(last_progress[video_id], float(row_user[4]))
                    if row_user[3] is not None:
                        last_progress[video_id] = max(last_progress[video_id], float(row_user[3]))
                elif event_type == 'save_user_state' and row_user[5] is not None:
                    last_progress[video_id] = max(last_progress[video_id], float(row_user[5]))
                elif event_type in ['play_video', 'pause_video'] and row_user[2] is not None:
                    last_progress[video_id] = max(last_progress[video_id], float(row_user[2]))

            for video_id in last_progress:
                if video_id in finished:
                    cursor.execute('INSERT INTO ' + table_name2 + ' VALUES(%s, %s, %s, %s);', [user_id, video_id, 1, None])
                else:
                    cursor.execute('INSERT INTO ' + table_name2 + ' VALUES(%s, %s, %s, %s);', [user_id, video_id, 0, last_progress[video_id]])

            conn.commit()
