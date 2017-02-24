import MySQLdb
import os

import sys

import user_id_map, auth_user, auth_userprofile, certificates_generatedcertificate, courseware_studentmodule,\
    student_anonymoususerid, student_courseenrollment, student_languageproficiency, django_comment_client_role_users

terms = ['102.1x-2T2015', '102.1x-2T2016', '102.1x-4T2015', '102.2x-1T2016', '102.2x-2T2016', '102.2x-4T2015',
         '102x-2T2014', '102.1x-3T2016', '102.2x-3T2016']
table_prefix = [x.replace('.', '_').replace('-', '_') for x in terms]
dir = sys.argv[1]
if not dir.endswith('/'):
    dir += '/'

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
for i in range(len(terms)):
    auth_user.create_table(conn, table_prefix[i] + '_auth_user')
    auth_user.insert_table(conn, dir + "HKUSTx-COMP" + terms[i] + "-auth_user-prod-analytics.sql", table_prefix[i] + '_auth_user')
    auth_userprofile.create_table(conn, table_prefix[i] + '_auth_userprofile')
    auth_userprofile.insert_table(conn, dir + "HKUSTx-COMP" + terms[i] + "-auth_userprofile-prod-analytics.sql", table_prefix[i] + '_auth_userprofile')
    certificates_generatedcertificate.create_table(conn, table_prefix[i] + '_certificates_generatedcertificate')
    certificates_generatedcertificate.insert_table(conn, dir + "HKUSTx-COMP" + terms[i] + "-certificates_generatedcertificate-prod-analytics.sql",
                                                    table_prefix[i] + '_certificates_generatedcertificate')
    courseware_studentmodule.create_table(conn, table_prefix[i] + '_courseware_studentmodule')
    courseware_studentmodule.insert_table(conn, dir + "HKUSTx-COMP" + terms[i] + "-courseware_studentmodule-prod-analytics.sql",
                           table_prefix[i] + '_courseware_studentmodule')
    student_anonymoususerid.create_table(conn, table_prefix[i] + '_student_anonymoususerid')
    student_anonymoususerid.insert_table(conn, dir + "HKUSTx-COMP" + terms[i] + "-student_anonymoususerid-prod-analytics.sql",
                                          table_prefix[i] + '_student_anonymoususerid')
    student_courseenrollment.create_table(conn, table_prefix[i] + '_student_courseenrollment')
    student_courseenrollment.insert_table(conn, dir + "HKUSTx-COMP" + terms[i] + "-student_courseenrollment-prod-analytics.sql",
                                         table_prefix[i] + '_student_courseenrollment')
    student_languageproficiency.create_table(conn, table_prefix[i] + '_student_languageproficiency')
    student_languageproficiency.insert_table(conn, dir + "HKUSTx-COMP" + terms[i] + "-student_languageproficiency-prod-analytics.sql",
                                          table_prefix[i] + '_student_languageproficiency')
    user_id_map.create_table(conn, table_prefix[i] + '_user_id_map')
    user_id_map.insert_table(conn, dir + "HKUSTx-COMP" + terms[i] + "-user_id_map-prod-analytics.sql", table_prefix[i] + '_user_id_map')
    django_comment_client_role_users.create_table(conn, table_prefix[i] + '_django_comment_client_role_users')
    django_comment_client_role_users.insert_table(conn, dir + "HKUSTx-COMP" + terms[i] + "-django_comment_client_role_users-prod-analytics.sql", table_prefix[i] + '_django_comment_client_role_users')

conn.close()
