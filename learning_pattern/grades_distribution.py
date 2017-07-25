import numpy as np
import MySQLdb
import random
from matplotlib import pyplot as plt

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
sql = 'select user_id, grade from 102_1x_4T2015_certificates_generatedcertificate;'
cursor = conn.cursor()
cursor.execute(sql)
data = cursor.fetchall()
grade = map(lambda x: x[1], data)
plt.hist(grade, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
plt.title("grades distribution")
plt.show()
plt.savefig('grades_distribution.png', dpi=120)
