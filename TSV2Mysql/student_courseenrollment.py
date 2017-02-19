def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(id int, user_id int, course_id varchar(100), created datetime, is_active int, mode varchar(100));")
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
        p[1] = int(p[1])
        p[4] = int(p[4])
        c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s, %s);", p)
        line = f.readline()
    conn.commit()
