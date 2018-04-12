import json_wrapper
import MySQLdb
import sys


def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + "(user_id varchar(32), user_name varchar(64),"
                                        "session_id varchar(64), event_type varchar(128),"
                                        "name varchar(128), event_source varchar(16), emitted_time datetime);")
    conn.commit()


def insert_table(conn, p, table):
    c = conn.cursor()
    c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s, %s, %s);", p)
    conn.commit()


def process(file_name, conn, term):
    f = open(file_name)
    line = f.readline()
    term = term.replace('.', '_').replace('-', '_')
    create_table(conn, term + '_clickstream_events')
    while line:
        obj = json_wrapper.loads(line)
        text = [obj['context']['user_id'], obj['username'], obj['session'] if 'session' in obj else None, obj['event_type'],
                              obj['name']if 'name' in obj else None, obj['event_source'],
                              obj['time']]
        insert_table(conn, text, term + '_clickstream_events')
        line = f.readline()
    f.close()

if __name__ == '__main__':
    old_terms = ['102.1x-2T2015', '102.1x-2T2016', '102.1x-4T2015', '102.2x-1T2016', '102.2x-2T2016', '102.2x-4T2015',
             '102x-2T2014', '102.1x-3T2016', '102.2x-3T2016']
    # terms = ['102.1x-2T2015']

    java_terms = ['COMP102.1x-2T2015', 'COMP102.1x-2T2016', 'COMP102.1x-4T2015', 'COMP102.2x-1T2016', 'COMP102.2x-2T2016', 'COMP102.2x-4T2015',
                  'COMP102x-2T2014', 'COMP102.1x-3T2016', 'COMP102.2x-3T2016']
    # java_table_prefix = [x.replace('.', '_').replace('-', '_') for x in java_terms]

    android_terms = ['COMP107x-3T2016', 'COMP107x-2016_T1', 'COMP107x-1T2016']
    # android_table_prefix = [x.replace('.', '_').replace('-', '_') for x in android_terms]

    speaking_terms = ['EBA101x-3T2016', 'EBA101x-3T2014', 'EBA101x-1T2016']
    # speaking_table_prefix = [x.replace('.', '_').replace('-', '_') for x in speaking_terms]

    writing_terms = ['EBA102x-4Q2015', 'EBA102x-3T2016', 'EBA102x-1T2016']
    # writing_table_prefix = [x.replace('.', '_').replace('-', '_') for x in writing_terms]

    dir = sys.argv[1]
    if not dir.endswith('/'):
        dir += '/'
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
    terms = java_terms
    for term in terms:
        file_name = dir + "HKUSTx-" + term + "-clickstream.log"
        process(file_name, conn, term)
    conn.close()
