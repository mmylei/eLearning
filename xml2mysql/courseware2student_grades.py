import MySQLdb


def create_grades_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(`student_id` int, `course_id` varchar(20), `term_id` varchar(20), `xml_id` varchar(50), "
                "grade decimal(10,5), max_grade decimal(10,5));")
    conn.commit()

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
create_grades_table(conn, "all_students_grades")
terms = [
        # java
        '102.1x-2T2015',
        '102.1x-2T2016',
        '102.1x-3T2016',
        '102.1x-4T2015',
        '102.2x-1T2016',
        '102.2x-2T2016',
        '102.2x-3T2016',
        '102.2x-4T2015',
        '102x-2T2014',
        # android
        '107x-3T2016',
        '107x-2016_T1',
        '107x-1T2016',
        # speaking
        '101x-3T2016',
        '101x-3T2014',
        '101x-1T2016',
        # writing
        '102x-4Q2015',
        '102x-3T2016',
        '102x-1T2016'
    ]
for term in terms:
    term = term.replace('.', '_').replace('-', '_')
    cursor = conn.cursor()
    cursor.execute("SELECT module_id, student_id, grade, max_grade, course_id FROM "
                   + term + "_courseware_studentmodule" + " WHERE module_type = \"problem\" and grade is not NULL;")
    result = cursor.fetchall()
    for row in result:
        student_id = row[1]
        grade = row[2]
        max_grade = row[3]
        if '+' in row[4]:
            course_id = row[4].split('+')[1]
            term_id = row[4].split('+')[-1]
        else:
            course_id = row[4].split('/')[1]
            term_id = row[4].split('/')[-1]
        if '+' in row[0]:
            xml_id = row[0].split('+')[-1]
        else:
            xml_id = row[0].split('/')[-1]
        cursor.execute("INSERT INTO all_students_grades VALUES(%s, %s, %s, %s, %s, %s)", [student_id, course_id, term_id, xml_id, grade, max_grade])
        conn.commit()

conn.close()
