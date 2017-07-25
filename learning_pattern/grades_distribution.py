import numpy as np
import MySQLdb
import random
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
sql = 'select user_id, grade from 102_1x_4T2015_certificates_generatedcertificate;'
cursor = conn.cursor()
cursor.execute(sql)
data = cursor.fetchall()
grade = map(lambda x: float(x[1]*100), data)
plt.hist(grade, bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
plt.title("grades distribution")
# plt.show()
plt.savefig('grades_distribution.png', dpi=120)
