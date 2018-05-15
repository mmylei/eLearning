import json_wrapper
import MySQLdb
import Queue
import sys


def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(course_id varchar(16), term_id varchar(16), set_name varchar(64), set_category varchar(16),"
              "aggregated_category varchar(16), xml_id varchar(128), category varchar(16));")
    conn.commit()

dir = sys.argv[1]
if not dir.endswith('/'):
    dir += '/'
terms = [
         # 'COMP102.1x-2T2015',
         # 'COMP102.1x-2T2016',
         # 'COMP102.1x-3T2016',
         # 'COMP102.1x-4T2015',
         # 'COMP102.2x-1T2016',
         # 'COMP102.2x-2T2016',
         # 'COMP102.2x-3T2016',
         # 'COMP102.2x-4T2015',
         # 'COMP102x-2T2014',
         # android
         # 'COMP107x-3T2016',
         # 'COMP107x-2016_T1',
         # 'COMP107x-1T2016',
         # speaking
         # 'EBA101x-3T2016',
         # 'EBA101x-3T2014',
         # 'EBA101x-1T2016',
         # writing
         'EBA102x-4Q2015',
         'EBA102x-3T2016',
         'EBA102x-1T2016'
         ]
conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
for term in terms:
    term_id = term.split('-')[1]
    course_id = term.split('-')[0]
    table_name = ('HKUSTx-' + term + '-problem_set').replace('.', '_').replace('-', '_')
    create_table(conn, table_name)
    cursor = conn.cursor()
    data = None
    problem_sets = {}
    with open(dir + 'HKUSTx-' + term + '-course_structure-prod-analytics.json', 'r') as infile:
        data = json_wrapper.loads(infile.read())
    for key in data:
        if 'graded' in data[key]['metadata'] and data[key]['metadata']['graded']:
            # xml_id = key.split('@')[-1]
            set_category = data[key]['metadata']['format']
            set_name = data[key]['metadata']['display_name']
            queue = Queue.Queue()
            for child in data[key]['children']:
                queue.put_nowait(child)
            while not queue.empty():
                id = queue.get_nowait()
                category = data[id]['category']
                if category in ['problem', 'openassessment']:
                    xml_id = id.split('@')[-1]
                    aggregated_category = 'Exam'
                    if set_category.startswith('Module'):
                        aggregated_category = 'M' + set_category.split(' ')[1]
                    elif set_category.startswith('Week'):
                        aggregated_category = 'M' + set_category.split(' ')[1]
                    elif set_category.startswith('Participation'):
                        aggregated_category = 'M' + set_name.split(' ')[0][:-1]
                    elif set_category.startswith('Quiz'):
                        aggregated_category = 'Q0' + set_name.split(' ')[1]
                    elif set_category.startswith('Task'):
                        aggregated_category = 'T0' + set_name.split(' ')[1]
                    elif set_category == 'Labs':
                        aggregated_category = 'L' + set_name.split(' ')[1]
                    elif set_category == 'Final Exam':
                        aggregated_category = 'Exam'
                    elif set_category != 'Exam':
                        print 'unhandled category:'
                        print course_id, ',', term_id, ',', set_name, ',', set_category, ',', xml_id, ',', category
                    try:
                        cursor.execute('INSERT INTO ' + table_name + ' values(%s, %s, %s, %s, %s, %s, %s);',
                                   [course_id, term_id, set_name, set_category, aggregated_category, xml_id, category])
                    except Exception:
                        print course_id, term_id, set_name, set_category, xml_id, category
                        raise
                else:
                    for child in data[id]['children']:
                        queue.put_nowait(child)
    conn.commit()
