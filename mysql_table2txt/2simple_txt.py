import MySQLdb
import re

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
cursor = conn.cursor()
sql3 = """SELECT commentable_id, title, body FROM 102_1x_4T2015_commentthread"""
text3_module = open("/disk02/data/eLearning/xylei/102_1x_4T2015_module_simplified.txt", "w")
text3_others = open("/disk02/data/eLearning/xylei/102_1x_4T2015_others_simplified.txt", "w")
cursor.execute(sql3)
result3 = cursor.fetchall()
for row in result3:
    if re.match('m', row[0]) is not None:
        print>>text3_module, row[1], '\n', row[2].replace('\n', '\\n')
    else:
        print>> text3_others, row[2].replace('\n', '\\n')
text3_module.close()
text3_others.close()

conn.close()