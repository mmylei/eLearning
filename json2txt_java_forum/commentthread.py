def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(id varchar(100), votes_up int, votes_down int, votes_count int, votes_point int,"
              "thread_type varchar(50),comment_count int, title text, body text, updated_at datetime,"
              "created_at datetime, last_activity_at datetime, commentable_id varchar(50), author_id int, author_username varchar(50);")
    conn.commit()


def insert_table(conn, p, table):
    c = conn.cursor()
    # p[1] = int(p[1])
    # p[2] = int(p[2])
    # p[3] = int(p[3])
    # p[4] = int(p[4])
    # p[6] = int(p[6])
    p[9] = truncate(p[9])
    p[10] = truncate(p[10])
    p[11] = truncate(p[11])
    c.execute("INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", p)
    conn.commit()


def truncate(date_time):
    return date_time[:date_time.find('.')]

if __name__ == '__main__':
    print(truncate('2015-08-25T19:57:55.210Z'))
