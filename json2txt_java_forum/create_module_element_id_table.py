import json_wrapper
import MySQLdb
import sys


def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + "(module_id varchar(32), module_name varchar(64),"
                                        "element_type varchar(64), element_id varchar(64));")
    conn.commit()


def insert_table(conn, p, table):
    c = conn.cursor()
    c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s);", p)
    conn.commit()


def process(file_name, conn, term, module_id):
    f = open(file_name)
    term = term.replace('.', '_').replace('-', '_')
    create_table(conn, term + '_element')
    element = {}
    obj = json_wrapper.loads(f.read())
    for key in obj:
        child = []
        if key.split('@')[-2].split('+')[0] == 'course':
            continue
        else:
            for children in obj[key]['children']:
                child.append(children.split('@')[-2].split('+')[0] + '@' + children.split('@')[-1])
            element[key.split('@')[-2].split('+')[0] + '@' + key.split('@')[-1]] = child
    for mid in module_id:
        name = mid.split('@')[0]
        num = mid.split('@')[-1]
        sequential = element['chapter@' + num]
        for sqt in sequential:
            vertical = element[sqt]
            for vert in vertical:
                eid = vert.split('@')[-1]
                etype = vert.split('@')[0]
                text = [num, name, etype, eid]
                insert_table(conn, text, term + '_element')
    f.close()

if __name__ == '__main__':
    old_terms = ['102.1x-2T2015', '102.1x-2T2016', '102.1x-4T2015', '102.2x-1T2016', '102.2x-2T2016', '102.2x-4T2015',
             '102x-2T2014', '102.1x-3T2016', '102.2x-3T2016']
    # terms = ['102.1x-2T2015']

    java_terms = ['COMP102.1x-2T2015', 'COMP102.1x-2T2016', 'COMP102.1x-4T2015', 'COMP102.2x-1T2016', 'COMP102.2x-2T2016', 'COMP102.2x-4T2015',
                  'COMP102x-2T2014', 'COMP102.1x-3T2016', 'COMP102.2x-3T2016']
    # java_table_prefix = [x.replace('.', '_').replace('-', '_') for x in java_terms]
    java_4T2015 = ['COMP102.1x-4T2015']

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
    terms = java_4T2015
    module_id = ['pre@ae687c1204b84885a4797f517715722a', 'M01@1ee4603833d742e698d27695d2aa25b5',
                 'M02@db78e7f298c345f3af42589e06c470a2', 'M03@b57525ba4b974719b9ce4eca914e1c39',
                 'M04@668fb99bb9684644822889e460197fe9', 'M05@3f0585f6e4574bac95384a227d50ef5f',
                 'Exam@1020d90b174142239fcdefc2f8555d55', 'post@fd8a124c47d940dfa7d88a8ac37a7cc5']
    for term in terms:
        file_name = dir + "HKUSTx-" + term + "-course_structure-prod-analytics.json"
        process(file_name, conn, term, module_id)
    conn.close()
