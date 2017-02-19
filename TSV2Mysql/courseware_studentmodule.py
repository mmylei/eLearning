def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(id int, module_type varchar(100), module_id varchar(100), student_id int, state text,"
              "grade decimal(30,25), created datetime, modified datetime, max_grade decimal(30,25), done varchar(100),"
              "course_id varchar(100));")
    conn.commit()


def insert_table(conn, file, table):
    c = conn.cursor()
    f = open(file)
    line = f.readline()
    line = f.readline()
    while line:
        p = line.strip().split('\t')
        # p = p[0:11]
        p[0] = int(p[0])
        p[3] = int(p[3])
        if p[5] == "NULL":
            p[5] = None
        else:
            p[5] = float(p[5])
        if p[8] == "NULL":
            p[8] = None
        else:
            p[8] = float(p[8])
        c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", p)
        line = f.readline()
    conn.commit()
