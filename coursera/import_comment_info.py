import MySQLdb
import json_wrapper

courses = {
    'html': 'LgWwihnoEeWDtQoum3sFeQ',
    'front': 'ycQnChn3EeWDtQoum3sFeQ',
    'server': 'ngZrURn5EeWwrBKfKrqlSQ',
    'angularJS': '52blABnqEeW9dA4X94-nLQ',
    'mobile': '-gcU5xn4EeWwrBKfKrqlSQ',
    'web': 'DzdXURoCEeWg_RJGAuFGjw'
}


def create_comment_info_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(`course_id` varchar(50), user_id varchar(16), `comment` text, rating float(3,2), `timestamp` varchar(16), completed tinyint(1));")
    conn.commit()


def insert_comment_info_table(conn, file):
    f = open(file)
    content = f.read()
    obj = json_wrapper.loads(content)
    for element in obj['elements']:
        course_id = element['context']['definition']['courseId']
        user_id = element['userId']
        comment = element['comments']['generic']['definition']['value']
        rating = float(element['rating']['value'].split(' ')[0])
        timestamp = element['timestamp']
        if 'completed' in file:
            completed = 1
        else:
            completed = 0
        c = conn.cursor()
        c.execute("INSERT INTO coursera_comment_info VALUES(%s, %s, %s, %s, %s, %s);",
                  [course_id, user_id, comment, rating, timestamp, completed])
        conn.commit()

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
create_comment_info_table(conn, "coursera_comment_info")
for course in courses:
    insert_comment_info_table(conn, 'coursera_comment_info_' + course + '_all.json')
    insert_comment_info_table(conn, 'coursera_comment_info_' + course + '_completed.json')

conn.close()