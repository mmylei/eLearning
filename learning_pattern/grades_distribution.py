import numpy as np
import MySQLdb
import random
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
# sql = 'select user_id, grade from 102_1x_4T2015_certificates_generatedcertificate;'
sql = 'select student_id, sum(grade) from HKUSTx_COMP102_1x_4T2015_student_grade where aggregated_category like \'%04\' group by student_id;'
cursor = conn.cursor()
cursor.execute(sql)
data = cursor.fetchall()
grade = map(lambda x: float(x[1]), data)
plt.hist(grade, bins=range(0, 20))
plt.title("grades distribution")
# plt.show()
plt.savefig('week04_grades_distribution.png', dpi=120)
