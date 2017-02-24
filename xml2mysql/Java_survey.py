import xml.etree.ElementTree as ET
import MySQLdb

def create_question_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(`id` int, xml_id varchar(50), survey_type varchar(30), body varchar(1000), choice_num int);")
    conn.commit()


def create_choice_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(question_id int, xml_id varchar(50), survey_type varchar(30), body varchar(100), "
                                        "choice_id int);")
    conn.commit()

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
create_question_table(conn, "Java_survey_questions")
create_choice_table(conn, "Java_survey_choices")
file = ["4b9026e2ae434af79e436a5161145b43", "642a6320ec6646539a5c4796291d4e39"]
for file_id in file:
    tree = ET.parse('/disk02/data/eLearning/data/Java/DB Snapshots/xml/HKUSTx-COMP102.1x-2T2016-course-prod-analytics/HKUSTx-COMP102.1x-2T2016/problem/' + file_id + '.xml')
    root = tree.getroot()
    xml_id = file_id
    survey_type = root.get('display_name')
    question_body = []
    question_id = []
    choice_num = 0
    choice_body = []
    choice_id = []
    for multiplechoiceresponse in root.iter('multiplechoiceresponse'):
        choice_num = 0
        group = multiplechoiceresponse.find('choicegroup')
        question_id = int(group.get('label').split(' ')[0][1:])
        question_body = ' '.join(group.get('label').split(' ')[1:])
        for choice in group.iter('choice'):
            choice_num += 1
            choice_body = choice.text
            choice_id = choice_num
            c = conn.cursor()
            c.execute("INSERT INTO Java_survey_choices VALUES(%s, %s, %s, %s, %s);",
                      [question_id, xml_id, survey_type, choice_body, choice_id])
            conn.commit()
        c = conn.cursor()
        c.execute("INSERT INTO Java_survey_questions VALUES(%s, %s, %s, %s, %s);",
                  [question_id, xml_id, survey_type, question_body, choice_num])
        conn.commit()
