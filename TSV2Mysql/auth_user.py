def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(id int, username varchar(100), first_name varchar(100), last_name varchar(100), email varchar(100),"
              "password varchar(20), is_staff int, is_active int, is_superuser int, last_login datetime,"
              "date_joined datetime);")
    conn.commit()


def insert_table(conn, file, table):
    c = conn.cursor()
    f = open(file)
    line = f.readline()
    line = f.readline()
    while line:
        p = line.strip().split('\t')
        p = p[0:11]
        p[0] = int(p[0])
        p[6] = int(p[6])
        p[7] = int(p[7])
        p[8] = int(p[8])
        c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", p)
        line = f.readline()
    conn.commit()
