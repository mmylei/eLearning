import read_file
import json_wrapper
import re
import MySQLdb
import sys

reg = re.compile(r'[0-9a-z]{32}')


def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(user_name varchar(64), user_id int, event_source varchar(32), event_type varchar(256),"
              "event_time datetime, course_id varchar(128), `session` varchar(64), `current_time` decimal(15, 5),"
              "slide_type varchar(16), old_time decimal(10, 5), new_time decimal(10, 5), old_speed decimal(4, 2),"
              "new_speed decimal(4, 2), saved_video_position int, video_id varchar(64));")
    conn.commit()


def insert_table(conn, fields, p, table):
    c = conn.cursor()
    c.execute("INSERT INTO " + table + "(" + ','.join(fields) + ")" + " VALUES(" + ','.join(['%s']*len(p)) + ");", p)
    conn.commit()


def truncate(date_time):
    return date_time[:date_time.find('.')]


def extract_video_id(event_type):
    for x in event_type.split('/'):
        if '@' in x:
            return x.split('@')[-1]
    return reg.search(event_type).group()


def video_position_to_decimal(position):
    parts = position.split(':')
    try:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except:
        #print(position)
        return -1

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(extract_video_id('/courses/course-v1:HKUSTx+COMP102.1x+3T2016/xblock/block-v1:HKUSTx+COMP102.1x+3T2016+type@video+block@dfe488d381a542dfa8557bd069421e4a/handler/xmodule_handler/save_user_state'))
        exit()
    dir = sys.argv[1]
    if not dir.endswith('/'):
        dir += '/'
    java_terms = [
        #'COMP102.1x-2T2015',
        #'COMP102.1x-2T2016',
        #'COMP102.1x-3T2016',
        #'COMP102.1x-4T2015',
        #'COMP102.2x-1T2016',
        #'COMP102.2x-2T2016',
        #'COMP102.2x-3T2016',
        #'COMP102.2x-4T2015',
        'COMP102x-2T2014'
    ]

    android_terms = ['COMP107x-3T2016', 'COMP107x-2016_T1', 'COMP107x-1T2016']
    speaking_terms = ['EBA101x-3T2016', 'EBA101x-3T2014', 'EBA101x-1T2016']
    writing_terms = ['EBA102x-4Q2015', 'EBA102x-3T2016', 'EBA102x-1T2016']
    terms = android_terms
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
    for term in terms:
        table_name = ('HKUSTx-' + term + '-clickstream').replace('-', '_').replace('.', '_')
        file_name = dir + 'HKUSTx-' + term + '-clickstream.log'
        create_table(conn, table_name)
        for row in read_file.read(file_name):
            row['time'] = truncate(row['time'])
            if row['event_type'] == 'load_video':
                event = row['event']
                if isinstance(event, str):
                    event = json_wrapper.loads(event)
                if 'currentTime' not in event:
                    event['currentTime'] = None
                try:
                    insert_table(conn,
                                 ['user_name', 'user_id', 'event_source', 'event_type',
                                  'event_time', 'course_id', '`session`', 'video_id'],
                                 [row['username'], row['context']['user_id'], row['event_source'], row['event_type'],
                                  row['time'], row['context']['course_id'], row['session'], event['id']],
                                 table_name)
                except KeyError:
                    print("exception found in term " + term)
                    print(row['time'])

            elif row['event_type'] in ['play_video', 'pause_video', 'stop_video']:
                event = row['event']
                if isinstance(event, str):
                    event = json_wrapper.loads(event)
                if 'currentTime' not in event:
                    event['currentTime'] = None
                try:
                    insert_table(conn,
                                 ['user_name', 'user_id', 'event_source', 'event_type',
                                  'event_time', 'course_id', '`session`', 'video_id', '`current_time`'],
                                 [row['username'], row['context']['user_id'], row['event_source'], row['event_type'],
                                  row['time'], row['context']['course_id'], row['session'], event['id'], event['currentTime']],
                                 table_name)
                except Exception:
                    print("exception found in term " + term)
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
                                  'event_time', 'course_id', '`session`', 'video_id', 'slide_type', 'old_time', 'new_time'],
                                 [row['username'], row['context']['user_id'], row['event_source'], row['event_type'],
                                  row['time'], row['context']['course_id'], row['session'], event['id'], event['type'], event['old_time'], event['new_time']],
                                 table_name)
                except Exception:
                    print("exception found in term " + term)
                    print(row['time'])
                    raise
            elif row['event_type'] == 'speed_change_video':
                event = row['event']
                if isinstance(event, str):
                    event = json_wrapper.loads(event)
                try:
                    insert_table(conn,
                                 ['user_name', 'user_id', 'event_source', 'event_type',
                                  'event_time', 'course_id', '`session`', 'video_id', 'old_speed', 'new_speed'],
                                 [row['username'], row['context']['user_id'], row['event_source'], row['event_type'],
                                  row['time'], row['context']['course_id'], row['session'], event['id'], event['old_speed'],
                                  event['new_speed']],
                                 table_name)
                except Exception:
                    print("exception found in term " + term)
                    print(row['time'])
                    raise
            elif row['event_type'].endswith("save_user_state"):
                event = row['event']
                if isinstance(event, str):
                    event = json_wrapper.loads(event)
                if 'saved_video_position' not in event['POST']:
                    continue
                video_position = video_position_to_decimal(event['POST']['saved_video_position'][0])
                if video_position == -1:
                    continue
                try:
                    insert_table(conn,
                                 ['user_name', 'user_id', 'event_source', 'event_type',
                                  'event_time', 'course_id', 'video_id', 'saved_video_position'],
                                 [row['username'], row['context']['user_id'], row['event_source'], 'save_user_state',
                                  row['time'], row['context']['course_id'], extract_video_id(row['event_type']),
                                  video_position],
                                 table_name)
                except Exception:
                    print("exception found in term " + term)
                    print(row['time'])
                    raise
