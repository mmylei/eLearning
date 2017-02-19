def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(comment_thread_id varchar(100), votes_up int, votes_down int, votes_count int, votes_point int,"
              "body text, updated_at datetime,"
              "created_at datetime, author_id int, author_username varchar(50));")
    conn.commit()


def insert_table(conn, p, table):
    c = conn.cursor()
    # p[1] = int(p[1])
    # p[2] = int(p[2])
    # p[3] = int(p[3])
    # p[4] = int(p[4])
    p[6] = truncate(p[6])
    p[7] = truncate(p[7])
    c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", p)
    conn.commit()


def truncate(date_time):
    return date_time[:date_time.find('.')]
