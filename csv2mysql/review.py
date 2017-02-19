import MySQLdb


def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(username varchar(100), in_dex int, helpful int, course_name varchar(100), rank varchar(50),"
              "comments text, stage varchar(50));")
    conn.commit()


conn = MySQLdb.connect(host="localhost", user="mmy", passwd="123", db="test")
create_table(conn, 'review')
c = conn.cursor()
c.execute("LOAD DATA LOCAL INFILE '~/Downloads/e-learning/review.csv' INTO TABLE review "
          "FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n'"
          "IGNORE 1 LINES (username, in_dex, helpful, course_name, rank, comments, stage);")
conn.commit()
