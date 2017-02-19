def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(id int, user_id int, download_url varchar(100), grade decimal(3,2), course_id varchar(100), `key` varchar(100),"
              "distinction int, status varchar(100), verity_uuid varchar(100), download_uuid varchar(100), name varchar(100), "
              "created_date datetime, modified_date datetime, error_reason varchar(100), mode varchar(100));")
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
        p[3] = float(p[3])
        p[6] = int(p[6])
        c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", p)
        line = f.readline()
    conn.commit()
