import read_file
import json_wrapper
import MySQLdb
import sys


def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(user_name varchar(64), user_id int, event_source varchar(32), event_type varchar(256),"
              "event_time datetime, course_id varchar(128), `session` varchar(64), `current_time` decimal(10, 5),"
              "slide_type varchar(16), old_time decimal(10, 5), new_time decimal(10, 5), old_speed decimal(4, 2),"
              "new_speed decimal(4, 2));")
    conn.commit()


def insert_table(conn, fields, p, table):
    c = conn.cursor()
    c.execute("INSERT INTO " + table + "(" + ','.join(fields) + ")" + " VALUES(" + ','.join(['%s']*len(p)) + ");", p)
    conn.commit()


def truncate(date_time):
    return date_time[:date_time.find('.')]

if __name__ == '__main__':
    dir = sys.argv[1]
    if not dir.endswith('/'):
        dir += '/'
    terms = [
        'COMP102.1x-2T2015',
        'COMP102.1x-2T2016',
        'COMP102.1x-3T2016',
        'COMP102.1x-4T2015',
        'COMP102.2x-1T2016',
        'COMP102.2x-2T2016',
        'COMP102.2x-3T2016',
        'COMP102.2x-4T2015',
        'COMP102x-2T2014'
    ]
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
    for term in terms:
        table_name = ('HKUSTx-' + term + '-clickstream').replace('-', '_').replace('.', '_')
        file_name = dir + 'HKUSTx-' + term + '-clickstream.log'
        create_table(conn, table_name)
        for row in read_file.read(file_name):
            row['time'] = truncate(row['time'])
            if row['event_type'] == 'load_video':
                try:
                    insert_table(conn,
                                 ['user_name', 'user_id', 'event_source', 'event_type',
                                  'event_time', 'course_id', '`session`'],
                                 [row['username'], row['context']['user_id'], row['event_source'], row['event_type'],
                                  row['time'], row['context']['course_id'], row['session']],
                                 table_name)
                except Exception:
                    print(row['time'])
                    raise
            elif row['event_type'] in ['play_video', 'pause_video', 'stop_video']:
                event = row['event']
                if isinstance(event, str):
                    event = json_wrapper.loads(event)
                if 'currentTime' not in event:
                    event['currentTime'] = None
                try:
                    insert_table(conn,
                                 ['user_name', 'user_id', 'event_source', 'event_type',
                                  'event_time', 'course_id', '`session`', '`current_time`'],
                                 [row['username'], row['context']['user_id'], row['event_source'], row['event_type'],
                                  row['time'], row['context']['course_id'], row['session'], event['currentTime']],
                                 table_name)
                except Exception:
                    print(row['time'])
                    raise
            elif row['event_type'] == 'seek_video':
                event = row['event']
                if isinstance(event, str):
                    event = json_wrapper.loads(event)
                try:
                    if 'old_time' not in event:
                        event['old_time'] = None
                    insert_table(conn,
                                 ['user_name', 'user_id', 'event_source', 'event_type',
                                  'event_time', 'course_id', '`session`', 'slide_type', 'old_time', 'new_time'],
                                 [row['username'], row['context']['user_id'], row['event_source'], row['event_type'],
                                  row['time'], row['context']['course_id'], row['session'], event['type'], event['old_time'], event['new_time']],
                                 table_name)
                except Exception:
                    print(row['time'])
                    raise
            elif row['event_type'] == 'speed_change_video':
                event = row['event']
                if isinstance(event, str):
                    event = json_wrapper.loads(event)
                try:
                    insert_table(conn,
                                 ['user_name', 'user_id', 'event_source', 'event_type',
                                  'event_time', 'course_id', '`session`', 'old_speed', 'new_speed'],
                                 [row['username'], row['context']['user_id'], row['event_source'], row['event_type'],
                                  row['time'], row['context']['course_id'], row['session'], event['old_speed'],
                                  event['new_speed']],
                                 table_name)
                except Exception:
                    print(row['time'])
                    raise
