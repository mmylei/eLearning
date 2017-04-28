import MySQLdb
import os

import sys

import user_id_map, auth_user, auth_userprofile, certificates_generatedcertificate, courseware_studentmodule,\
    student_anonymoususerid, student_courseenrollment, student_languageproficiency, django_comment_client_role_users, student_courseaccessrole

java_terms = ['102.1x-2T2015', '102.1x-2T2016', '102.1x-4T2015', '102.2x-1T2016', '102.2x-2T2016', '102.2x-4T2015',
         '102x-2T2014', '102.1x-3T2016', '102.2x-3T2016']
java_table_prefix = [x.replace('.', '_').replace('-', '_') for x in java_terms]

android_terms = ['107x-3T2016', '107x-2016_T1', '107x-1T2016']
android_table_prefix = [x.replace('.', '_').replace('-', '_') for x in android_terms]

speaking_terms = ['101x-3T2016', '101x-3T2014', '101x-1T2016']
speaking_table_prefix = [x.replace('.', '_').replace('-', '_') for x in speaking_terms]

writing_terms = ['102x-4Q2015', '102x-3T2016', '102x-1T2016']
writing_table_prefix = [x.replace('.', '_').replace('-', '_') for x in writing_terms]

dir = sys.argv[1]
if not dir.endswith('/'):
    dir += '/'

terms = java_terms
table_prefix = java_table_prefix
conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
for i in range(len(terms)):
    # auth_user.create_table(conn, table_prefix[i] + '_auth_user')
    # auth_user.insert_table(conn, dir + "HKUSTx-EBA" + terms[i] + "-auth_user-prod-analytics.sql", table_prefix[i] + '_auth_user')
    # auth_userprofile.create_table(conn, table_prefix[i] + '_auth_userprofile')
    # auth_userprofile.insert_table(conn, dir + "HKUSTx-EBA" + terms[i] + "-auth_userprofile-prod-analytics.sql", table_prefix[i] + '_auth_userprofile')
    # certificates_generatedcertificate.create_table(conn, table_prefix[i] + '_certificates_generatedcertificate')
    # certificates_generatedcertificate.insert_table(conn, dir + "HKUSTx-EBA" + terms[i] + "-certificates_generatedcertificate-prod-analytics.sql",
    #                                                 table_prefix[i] + '_certificates_generatedcertificate')
    # courseware_studentmodule.create_table(conn, table_prefix[i] + '_courseware_studentmodule')
    # courseware_studentmodule.insert_table(conn, dir + "HKUSTx-EBA" + terms[i] + "-courseware_studentmodule-prod-analytics.sql",
    #                        table_prefix[i] + '_courseware_studentmodule')
    # student_anonymoususerid.create_table(conn, table_prefix[i] + '_student_anonymoususerid')
    # student_anonymoususerid.insert_table(conn, dir + "HKUSTx-EBA" + terms[i] + "-student_anonymoususerid-prod-analytics.sql",
    #                                       table_prefix[i] + '_student_anonymoususerid')
    # student_courseenrollment.create_table(conn, table_prefix[i] + '_student_courseenrollment')
    # student_courseenrollment.insert_table(conn, dir + "HKUSTx-EBA" + terms[i] + "-student_courseenrollment-prod-analytics.sql",
    #                                      table_prefix[i] + '_student_courseenrollment')
    # student_languageproficiency.create_table(conn, table_prefix[i] + '_student_languageproficiency')
    # student_languageproficiency.insert_table(conn, dir + "HKUSTx-EBA" + terms[i] + "-student_languageproficiency-prod-analytics.sql",
    #                                       table_prefix[i] + '_student_languageproficiency')
    # user_id_map.create_table(conn, table_prefix[i] + '_user_id_map')
    # user_id_map.insert_table(conn, dir + "HKUSTx-EBA" + terms[i] + "-user_id_map-prod-analytics.sql", table_prefix[i] + '_user_id_map')
    # django_comment_client_role_users.create_table(conn, table_prefix[i] + '_django_comment_client_role_users')
    # django_comment_client_role_users.insert_table(conn, dir + "HKUSTx-EBA" + terms[i] + "-django_comment_client_role_users-prod-analytics.sql", table_prefix[i] + '_django_comment_client_role_users')

    student_courseaccessrole.create_table(conn, table_prefix[i] + '_student_courseacessrole')
    student_courseaccessrole.insert_table(conn, dir + "HKUSTx-COMP" + terms[i] + "-student_courseaccessrole-prod-analytics.sql",
                           table_prefix[i] + '_student_courseaccessrole')

conn.close()
