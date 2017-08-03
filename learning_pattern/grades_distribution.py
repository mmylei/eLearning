import numpy as np
import MySQLdb
import random
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
# sql = 'select user_id, grade from 102_1x_4T2015_certificates_generatedcertificate;'
sql = 'select student_id, sum(grade), sum(max_grade) from HKUSTx_COMP102_1x_4T2015_student_grade where aggregated_category like \'%05\' group by student_id;'
cursor = conn.cursor()
cursor.execute(sql)
data = cursor.fetchall()
grade_ratio = map(lambda x: float(x[1]/x[2]), data)
plt.hist(grade_ratio, bins=range(0, 20))
plt.title("grades ratio distribution")
# plt.show()
plt.savefig('week05_grades_ratio_distribution.png', dpi=120)
