import numpy as np
import MySQLdb
import random
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt


terms = [
    # java
    # '102.1x-2T2015',
    # '102.1x-2T2016',
    # '102.1x-3T2016',
    '102.1x-4T2015',
    # '102.2x-1T2016',
    # '102.2x-2T2016',
    # '102.2x-3T2016',
    # '102.2x-4T2015',
    # '102x-2T2014',
    ]


def get_weekly_grades(cursor, term):
    table_name1 = (term + '_courseware_studentmodule').replace('-', '_').replace('.', '_')
    table_name2 = ('HKUSTx-COMP' + term + '_problem_set').replace('-', '_').replace('.', '_')
    sql = 'select grade, max_grade, module_id, student_id from ' + table_name1 + \
          ' where module_type = \'problem\' and grade is not NULL;'
    cursor.execute(sql)
    temp = cursor.fetchall()
    result = []
    for row in temp:
        xml_id = row[2].split('@')[-1]
        cursor.execute('select aggregated_category from ' + table_name2 + ' where xml_id=\'' + xml_id + '\';')
        temp1 = cursor.fetchall()
        if len(temp1) > 0:
            result.append([float(row[0]), float(row[1]), row[2], row[3], temp1[0][0]])
    return result


def grades_by_week(weekly_grades, week_number):
    return filter(lambda x: x[4].endswith(str(week_number)), weekly_grades)


def sum_by_user(grades):
    grade = {}
    for row in grades:
        uid = row[3]
        if uid not in grade:
            grade[uid] = [0, 0]
        grade[uid][0] += row[0]
        grade[uid][1] += row[1]
    return [grade[x][0] for x in grade]


def draw(grades, week_number):
    plt.figure()
    plt.hist(grades, bins=10, normed=True)
    plt.title("grades distribution")
    # plt.show()
    plt.savefig('week' + str(week_number) + '_normalized_grades_distribution.png', dpi=120)


if __name__ == '__main__':
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
    # sql = 'select user_id, grade from 102_1x_4T2015_certificates_generatedcertificate;'
    # sql = 'select student_id, sum(grade) from HKUSTx_COMP102_1x_4T2015_student_grade where aggregated_category like \'%05\' group by student_id;'
    # cursor = conn.cursor()
    # cursor.execute(sql)
    # data = cursor.fetchall()
    # grade = map(lambda x: float(x[1]), data)
    # plt.hist(grade, bins=range(0, 20))
    # plt.title("grades distribution")
    # # plt.show()
    # plt.savefig('week05_grades_distribution.png', dpi=120)
    for term in terms:
        # table_name1 = (term + '_courseware_studentmodule').replace('-', '_').replace('.', '_')
        # table_name2 = ('HKUSTx-COMP' + term + '_problem_set').replace('-', '_').replace('.', '_')
        # table_name3 = ('HKUSTx-COMP' + term + '_student_grade').replace('-', '_').replace('.', '_')
        # sql = 'select max_grade from ' + table_name3 + ' where student_id = ' + str(uid) + ' and module_type = \'problem\' and grade is not NULL;'
        cursor = conn.cursor()
        weekly_grades = get_weekly_grades(cursor, term)
        for week_number in range(1, 6):
            current_week_grades = grades_by_week(weekly_grades, week_number)
            user_week_grades = sum_by_user(current_week_grades)
            draw(user_week_grades, week_number)
        # cursor.execute(sql)