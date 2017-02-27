import MySQLdb
import json_wrapper

def create_relation_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(`student_id` int, xml_id varchar(50), survey_type varchar(30), question_id int, answer int, `term_id` varchar(50));")
    conn.commit()

terms = ['102.1x-2T2015', '102.1x-2T2016', '102.1x-4T2015', '102.2x-1T2016', '102.2x-2T2016', '102.2x-4T2015',
         '102x-2T2014', '102.1x-3T2016', '102.2x-3T2016']
table_prefix = [x.replace('.', '_').replace('-', '_') for x in terms]


conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
# conn = MySQLdb.connect(host="10.89.54.131", user="mmy", passwd="123", db="eLearning_Java")
create_relation_table(conn, "Java_survey_answers")
cursor = conn.cursor()
cursor.execute("SELECT xml_id, survey_type FROM Java_survey_questions;")
result = cursor.fetchall()
survey_map = {}
for row in result:
    survey_map[row[0]] = row[1]

# cursor = conn.cursor()
for table in table_prefix:
    cursor.execute("SELECT module_type, module_id, student_id, state FROM " + table + "_courseware_studentmodule;")
    result = cursor.fetchall()
    term_id = table
    for row in result:
        if row[0] == 'problem':
            xml_id = row[1].split('@')[-1]
            student_id = int(row[2])
            if xml_id in survey_map:
                survey_type = survey_map[xml_id]
                try:
                    state = json_wrapper.loads(row[3].replace('\\\\', '\\'))
                except Exception:
                    print(row[3])
                    raise
                if 'student_answers' in state:
                    for key in state['student_answers']:
                        question_id = int(key.split('_')[1]) - 1
                        if question_id < 15:
                            answer = int(state['student_answers'][key].split('_')[1])
                            cursor.execute("INSERT INTO Java_survey_answers VALUES(%s, %s, %s, %s, %s, %s)", [student_id, xml_id, survey_type, question_id, answer, term_id])
conn.commit()
conn.close()
