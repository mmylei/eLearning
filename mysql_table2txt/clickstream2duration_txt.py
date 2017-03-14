import MySQLdb


conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
cursor = conn.cursor()
sql1 = """select user_id, video_id, sum(real_time_end-real_time_start) from HKUSTx_COMP102_1x_4T2015_video_play_piece group by user_id, video_id"""
text1 = open("/disk02/data/eLearning/xylei/102_1x_4T2015_video_play_time.txt", "w")
cursor.execute(sql1)
result1 = cursor.fetchall()
for row in result1:
    print>>text1, str(row[0])+'\t'+str(row[1])+'\t'+str(row[2])
text1.close()

conn.close()
