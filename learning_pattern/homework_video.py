import MySQLdb
import json_wrapper

sql = "select student_id, created, modified" \
      " from 102_2x_4T2015_courseware_studentmodule" \
      " where module_type='problem' and grade is not NULL"
sql2 = "select count(*)" \
       " from clickstream.HKUSTx_COMP102_1x_4T2015_clickstream" \
       " where user_id = %s and event_type = 'play_video' and event_time >= %s and event_time <= %s;"
conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
c = conn.cursor()
c.execute(sql)
homeworks = c.fetchall()

result = {}
for row in homeworks:
    student_id = row[0]
    if str(student_id) not in result:
        result[str(student_id)] = 0
    c.execute(sql2, (student_id, row[1], row[2]))
    if c.fetchall()[0][0] > 0:
        result[str(student_id)] += 1

with open('homework_video.json', 'w') as f:
    f.write(json_wrapper.dumps(result) + '\n')
