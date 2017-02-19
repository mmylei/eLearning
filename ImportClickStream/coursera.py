def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS `" + table + "`;")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(user_name varchar(64), page_url varchar(1024), `timestamp` bigint, `key` varchar(128),"
              "`session` varchar(64), action_type varchar(16), prev_time decimal(10, 5), cur_time decimal(10, 5),"
              " playback_rate int);")
    conn.commit()


def insert_table(conn, fields, p, table):
    c = conn.cursor()
    c.execute("INSERT INTO " + table + "(" + ','.join(fields) + ")" + " VALUES(" + ','.join(['%s']*len(p)) + ");", p)
    conn.commit()


def truncate(date_time):
    return date_time[:date_time.find('.')]
