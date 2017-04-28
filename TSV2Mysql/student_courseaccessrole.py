def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(org varchar(8), course_id varchar(50), user_id varchar(10), role varchar(16));")
    conn.commit()


def insert_table(conn, file, table):
    c = conn.cursor()
    f = open(file)
    line = f.readline()
    line = f.readline()
    while line:
        p = line.strip().split('\t')
        # p = p[0:11]
        # p[0] = int(p[0])
        # p[1] = int(p[1])
        c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s);", p)
        line = f.readline()
    conn.commit()
