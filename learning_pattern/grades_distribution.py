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
mean = 0
sigma = 1
x = grade
fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(9, 6))
ax0.hist(x, 40, normed=1, histtype='bar', facecolor='yellowgreen', alpha=0.75)
ax0.set_title('pdf')
ax1.hist(x, 20, normed=1, histtype='bar', facecolor='pink', alpha=0.75, cumulative=True, rwidth=0.8)
ax1.set_title("cdf")
fig.subplots_adjust(hspace=0.4)
plt.savefig('grades_distribution.png', dpi=120)
