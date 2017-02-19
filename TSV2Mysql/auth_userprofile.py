def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(id int, user_id int, name varchar(100), language varchar(300), location varchar(300), meta varchar(5000),"
              "courseware varchar(100), gender varchar(10), mailing_address varchar(1000), year_of_birth int,"
              "level_of_education varchar(30), goals varchar(5000),allow_certificate int, country varchar(50),"
              "city varchar(50), bio varchar(5000), profile_image_uploaded_at datetime);")
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
        if p[9] == "NULL":
            p[9] = None
        else:
            p[9] = int(p[9])
        p[12] = int(p[12])
        if p[16] == "NULL":
            p[16] = None
        try:
            c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", p)
        except:
            print(p)
            raise
        line = f.readline()
    conn.commit()