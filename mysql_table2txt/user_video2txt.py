import MySQLdb


conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")
cursor = conn.cursor()
sql1 = """select * from HKUSTx_COMP102_1x_4T2015_user_video"""
text1 = open("/disk02/data/eLearning/xylei/102_1x_4T2015_user_video.txt", "w")
cursor.execute(sql1)
result1 = cursor.fetchall()
for row in result1:
    print>>text1, row[0]+'\t'+row[1]+'\t'+row[2]
text1.close()

conn.close()
