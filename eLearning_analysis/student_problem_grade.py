import MySQLdb

sql_template = 'create table $term$_student_grade as ' \
      'select G.student_id as student_id, aggregated_category, sum(grade) as grade' \
      ' from all_students_grades as G, $term$_problem_set as P' \
      ' where G.course_id = P.course_id and G.term_id = P.term_id and G.xml_id = P.xml_id' \
      ' group by student_id, aggregated_category;'

terms = [
         'HKUSTx_COMP102_1x_2T2015',
         'HKUSTx_COMP102_1x_2T2016',
         'HKUSTx_COMP102_1x_3T2016',
         # 'HKUSTx_102_1x_4T2015',
         'HKUSTx_COMP102_2x_1T2016',
         'HKUSTx_COMP102_2x_2T2016',
         'HKUSTx_COMP102_2x_3T2016',
         'HKUSTx_COMP102_2x_4T2015',
         # 'COMP102x-2T2014',
         # android
         'HKUSTx_COMP107x_3T2016',
         'HKUSTx_COMP107x_2016_T1',
         'HKUSTx_COMP107x_1T2016',
         # speaking
         'HKUSTx_EBA101x_3T2016',
         'HKUSTx_EBA101x_3T2014',
         'HKUSTx_EBA101x_1T2016',
         # writing
         'HKUSTx_EBA102x_4Q2015',
         'HKUSTx_EBA102x_3T2016',
         'HKUSTx_EBA102x_1T2016'
         ]
conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
for term in terms:
    sql = sql_template.replace('$term$', term)
    cursor = conn.cursor()
    cursor.execute(sql)
conn.commit()
