import MySQLdb
import re

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
cursor = conn.cursor()
sql1 = """SELECT commentable_id, title, body FROM 102_1x_2T2016_commentthread"""
sql2 = """SELECT commentable_id, title, body FROM 102_1x_3T2016_commentthread"""
sql3 = """SELECT commentable_id, title, body FROM 102_1x_4T2015_commentthread"""
text1_module = open("/disk02/data/eLearning/xylei/102_1x_2T2016_module.txt", "w")
text1_others = open("/disk02/data/eLearning/xylei/102_1x_2T2016_others.txt", "w")
text2_module = open("/disk02/data/eLearning/xylei/102_1x_3T2016_module.txt", "w")
text2_others = open("/disk02/data/eLearning/xylei/102_1x_3T2016_others.txt", "w")
text3_module = open("/disk02/data/eLearning/xylei/102_1x_4T2015_module.txt", "w")
text3_others = open("/disk02/data/eLearning/xylei/102_1x_4T2015_others.txt", "w")
cursor.execute(sql1)
result1 = cursor.fetchall()
for row in result1:
    if re.match('m', row[0]) is not None:
        print>>text1_module, row[0], '\n', row[1], '\n', row[2].replace('\n', '\\n')
    else:
        print>> text1_others, row[0], '\n', row[1], '\n', row[2].replace('\n', '\\n')
text1_module.close()
text1_others.close()

cursor.execute(sql2)
result2 = cursor.fetchall()
for row in result2:
    if re.match('m', row[0]) is not None:
        print>>text2_module, row[0], '\n', row[1], '\n', row[2].replace('\n', '\\n')
    else:
        print>> text2_others, row[0], '\n', row[1], '\n', row[2].replace('\n', '\\n')
text2_module.close()
text2_others.close()

cursor.execute(sql3)
result3 = cursor.fetchall()
for row in result3:
    if re.match('m', row[0]) is not None:
        print>>text3_module, row[0], '\n', row[1], '\n', row[2].replace('\n', '\\n')
    else:
        print>> text3_others, row[0], '\n', row[1], '\n', row[2].replace('\n', '\\n')
text3_module.close()
text3_others.close()

conn.close()