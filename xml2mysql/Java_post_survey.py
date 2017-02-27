import MySQLdb

def create_relation_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(`student_id` int, xml_id varchar(50), survey_type varchar(30), question_id int, answer int, `term_id` varchar(50));")
    conn.commit()

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
# conn = MySQLdb.connect(host="10.89.54.131", user="mmy", passwd="123", db="eLearning_Java")
create_relation_table(conn, "Java_post_survey_answers")
cursor = conn.cursor()
cursor.execute("SELECT * FROM Java_survey_answers WHERE survey_type = \"Post-course Survey\";")
result = cursor.fetchall()
for row in result:
    cursor.execute("INSERT INTO Java_post_survey_answers VALUES(%s, %s, %s, %s, %s, %s)",row)
conn.commit()
conn.close()