import xml.etree.ElementTree as ET
import MySQLdb
import json_wrapper
import sys


def create_problem_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(`course_id` varchar(20), term_id varchar(20) xml_id varchar(50), "
                "display_name varchar(100), problem_type varchar(50);")
    conn.commit()


def process(file_name, conn):
    f = open(file_name)
    content = f.read()
    obj = json_wrapper.loads(content)
    for name in obj:
        if obj[name]['category'] == "problem" and 'display_name' in obj[name]['metadata']:
            course_id = name.split('\+')[1]
            term_id = name.split('\+')[2]
            xml_id = name.split('\+')[-1].split('@')[-1]
            display_name = obj[name]['metadata']['display_name']
            problem_type =' '.join(display_name.split(' ')[0:2])
            c = conn.cursor()
            c.execute("INSERT INTO all_courses_problems VALUES(%s, %s, %s, %s, %s);",
                      [course_id, term_id, xml_id, display_name, problem_type])
            conn.commit()


conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
create_problem_table(conn, "all_courses_problems")
dir = sys.argv[1]
if not dir.endswith('/'):
    dir += '/'

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

for term in terms:
    file_name = dir + "HKUSTx-" + term + "-course_structure-prod-analytics.json"
    process(file_name, conn)
conn.close()
