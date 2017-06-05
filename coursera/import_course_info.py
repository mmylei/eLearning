import MySQLdb
import json_wrapper


def create_course_info_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(`course_id` varchar(50), course_name varchar(128), instructor varchar(30), rating float(3,2), level varchar(20));")
    conn.commit()


def insert_course_info_table(conn, file, table):
    c = conn.cursor()
    f = open(file)
    content = json_wrapper.loads(f.read())
    for item in content:
        p = []
        for column in ['course_id', 'course_name', 'instructor', 'rating', 'level']:
            if column not in item:
                p.append(None)
            elif column == 'rating':
                p.append(float(item[column].split(' ')[0]))
            else:
                p.append(item[column])
        try:
            c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s);", p)
        except:
            print(p)
            raise
    conn.commit()

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
create_course_info_table(conn, "coursera_course_info")
insert_course_info_table(conn, "courses.json", "coursera_course_info")

conn.close()