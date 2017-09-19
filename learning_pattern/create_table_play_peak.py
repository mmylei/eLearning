import MySQLdb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import json_wrapper

width = 1024
height = 256
my_dpi = 256
dir = "./"


def play_times(duration, watchs):
    seconds = int(duration)
    count_repeat = np.zeros(seconds, dtype=float)
    for time in watchs:
        point = int(time)
        # drop 0 second data
        if 0 < point < seconds:
            count_repeat[point] += 1
    return count_repeat


def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + "(module_number int, video_id varchar(32), sequence int, peak varchar(4096));")
    conn.commit()


def insert_table(conn, p, table):
    c = conn.cursor()
    c.execute("INSERT INTO " + table + " VALUES(" + ','.join(['%s']*len(p)) + ");", p)
    conn.commit()


if __name__ == '__main__':
    terms = [
            'COMP102.1x-4T2015',
            # 'COMP107x-2016_T1'
        ]

    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
    for term in terms:
        print('start draw term ' + term)
        if not os.path.exists('./play/'):
            os.mkdir('./play/')
        dir = './play/' + term + '/'
        if not os.path.exists(dir):
            os.mkdir(dir)

        table_name = ('HKUSTx-' + term + '_clickstream').replace('-', '_').replace('.', '_')
        cursor = conn.cursor()
        cursor.execute('SELECT distinct(video_id) FROM ' + table_name + ';')
        result = cursor.fetchall()
        table_name2 = ('HKUSTx_' + term + '_play_peak').replace('-', '_').replace('.', '_')
        create_table(conn, table_name2)
        module_count = {}
        for row in result:
            if row[0] is None:
                continue
            video_id = row[0]
            # print('start draw video ' + video_id)
            cursor.execute('SELECT `current_time`'
                           ' FROM ' + table_name +
                           ' WHERE video_id=\'' + video_id + '\' ' + 'and event_type = \'play_video\' and `current_time` is not NULL;')
            play_records = [x[0] for x in cursor.fetchall()]
            cursor.execute('SELECT duration, module_number'
                           ' FROM eLearning.Video_Basic_Info'
                           ' WHERE video_id=\'' + video_id + '\';')
            d_result = cursor.fetchall()
            if len(d_result) == 0:
                print 'cannot find video info:', video_id
                continue
            duration = float(d_result[0][0])
            module_number = int(d_result[0][1])

            sequence = 0
            if str(module_number) in module_count:
                sequence = module_count[str(module_number)] + 1
            module_count[str(module_number)] = sequence

            play_count = play_times(duration, play_records)
            threshold = 0.3 * max(play_count)
            peak = map(lambda x: 1 if x >= threshold else 0, play_count)
            insert_table(conn, [module_number, video_id, sequence, json_wrapper.dumps(peak)], table_name2)
