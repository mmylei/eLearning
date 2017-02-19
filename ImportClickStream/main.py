import read_file
import json_wrapper
import coursera
import MySQLdb
import sys

if __name__ == '__main__':
    file_name = sys.argv[1]
    table_name = sys.argv[2]
    conn = MySQLdb.connect(host="localhost", user="mmy", passwd="123", db="test")
    coursera.create_table(conn, table_name)
    m = {}
    for row in read_file.read(file_name):
        # if row['key'] == 'user.video.lecture.action':
        #     value = json_wrapper.loads(row['value'])
        #     if value['type'] not in m:
        #         m[value['type']] = ''
        #         print(row)
        # continue
        if row['key'] == 'pageview':
            try:
                coursera.insert_table(conn,
                                  ['user_name', 'page_url', '`timestamp`', '`key`', '`session`'],
                                  [row['username'], row['page_url'], row['timestamp'], row['key'], row['session']],
                                  table_name)
            except Exception:
                print(row['timestamp'])
                raise
        elif row['key'] == 'user.video.lecture.action':
            value = json_wrapper.loads(row['value'])
            try:
                coursera.insert_table(conn,
                                  ['user_name', 'page_url', '`timestamp`', '`key`', '`session`', 'action_type',
                                   'prev_time', 'cur_time', 'playback_rate'],
                                  [row['username'], row['page_url'], row['timestamp'], row['key'], row['session'],
                                   value['type'], value['prevTime'], value['currentTime'], value['playbackRate']],
                                  table_name)
            except Exception:
                print(row['timestamp'])
                raise
