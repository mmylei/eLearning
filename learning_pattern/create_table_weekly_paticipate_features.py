import MySQLdb


def get_users(conn, term):
    table_name1 = (term + '_auth_user').replace('-', '_').replace('.', '_')
    sql = 'select distinct `id` from ' + table_name1 + ';'
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return map(lambda x: x[0], result)


def insert_table(conn, p, table):
    c = conn.cursor()
    c.execute("INSERT INTO " + table + " VALUES(" + ','.join(['%s']*len(p)) + ");", p)
    conn.commit()


def get_weekly_participate(conn, term, users):
    table_name2 = ('HKUSTx-COMP' + term + '_clickstream').replace('-', '_').replace('.', '_')
    table_name3 = ('HKUSTx-COMP' + term + '-user_video').replace('-', '_').replace('.', '_')
    table_name4 = ('HKUSTx-COMP' + term + '_student_grade').replace('-', '_').replace('.', '_')
    table_name5 = (term + '_certificates_generatedcertificate').replace('-', '_').replace('.', '_')
    table_name6 = (term + '_commentthread').replace('-', '_').replace('.', '_')
    table_name7 = (term + '_comment').replace('-', '_').replace('.', '_')
    sql1 = 'select B.video_id, B.module_number, S.flag from Video_Basic_Info as B, clickstream.Video_Stats_Info as S where B.video_id = S.video_id and B.term_id = \'COMP102_1x\' and B.module_number < 6;'
    cursor = conn.cursor()
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    for uid in users:
        m_video = [0] * 5
        finished = [0] * 5
        finished_flag1 = [0] * 5
        flag1 = [0] * 5
        video = [0] * 5
        m_assignment = [0] * 5
        l_assignment = [0] * 5
        comment_thread = [0] * 5
        comment = [0] * 5
        watched = [''] * 5
        for row in result1:
            for module_num in range(1, 6):
                if row[1] == module_num:
                    sql2 = 'select coverage, is_finished, is_covered from clickstream.' + table_name3 + ' where user_id = ' + str(uid) + ' and video_id= \'' + row[0] + '\';'
                    cursor.execute(sql2)
                    result2 = cursor.fetchall()
                    if len(result2) > 0:
                        video[module_num-1] += 1
                        if result2[0][0] > 0:
                            m_video[module_num-1] += 1
                        if row[2] == 1:
                            flag1[module_num-1] += 1
                            if result2[0][1] == 1 or result2[0][2] == 1:
                                finished_flag1[module_num-1] += 1
                                finished[module_num-1] += 1
                        else:
                            if result2[0][1] == 1 or result2[0][2] == 1:
                                finished[module_num-1] += 1
                    sql3 = 'select student_id, aggregated_category, grade from ' + table_name4 + ' where student_id = ' + str(uid) + ' and aggregated_category = \'M0' + str(module_num) + '\';'
                    cursor.execute(sql3)
                    result3 = cursor.fetchall()
                    if len(result3) > 0:
                        m_assignment[module_num-1] = result3[0][2]
                    else:
                        m_assignment[module_num-1] = -1
                    sql4 = 'select student_id, aggregated_category, grade from ' + table_name4 + ' where student_id = ' + str(uid) + ' and aggregated_category = \'L0' + str(module_num) + '\';'
                    cursor.execute(sql4)
                    result4 = cursor.fetchall()
                    if len(result4) > 0:
                        l_assignment[module_num-1] = result4[0][2]
                    else:
                        l_assignment[module_num-1] = -1
                    sql7 = 'select count(*) from ' + table_name6 + ' where author_id = ' + str(uid) + ' and commentable_id like \'m' + str(module_num) + '%\';'
                    cursor.execute(sql7)
                    result7 = cursor.fetchall()
                    comment_thread[module_num-1] = result7[0][0]
                    sql8 = 'select distinct(`id`) from ' + table_name6 + ' where commentable_id like \'m' + str(module_num) + '%\';'
                    cursor.execute(sql8)
                    result8 = cursor.fetchall()
                    for row8 in result8:
                        sql9 = 'select count(*) from ' + table_name7 + ' where author_id = ' + str(uid) + ' and comment_thread_id = \'' + row8[0] + '\';'
                        cursor.execute(sql9)
                        result9 = cursor.fetchall()
                        comment[module_num-1] += result9[0][0]
                watched[module_num-1] = str(finished_flag1[module_num-1]) + '/' + str(flag1[module_num-1]) + '/' + str(finished[module_num-1]) + '/' + str(video[module_num-1])
        sql5 = 'select student_id, aggregated_category, grade from ' + table_name4 + ' where student_id = ' + str(uid) + ' and aggregated_category = \'Exam\';'
        cursor.execute(sql5)
        result5 = cursor.fetchall()
        if len(result5) > 0:
            final = result5[0][2]
        else:
            final = -1
        sql6 = 'select user_id, status from ' + table_name5 + ' where user_id = ' + str(uid) + ';'
        cursor.execute(sql6)
        result6 = cursor.fetchall()
        if len(result6) == 0:
            passed = -1
        elif result6[0][1] == 'downloadable':
            passed = 1
        else:
            passed = 0
        values = [uid]
        for module_num in range(0, 5):
            values.append(m_video[module_num])
            values.append(m_assignment[module_num])
            values.append(l_assignment[module_num])
            values.append(comment[module_num])
            values.append(comment_thread[module_num])
        values.append(final)
        values.append(passed)
        values.extend(watched)
        insert_table(conn, values, 'weekly_participate_features')


def create_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table + " "
              "(user_id int, m01_video int, m01_assignment decimal(6,3), m01_lab decimal(6,3), m01_comment int, m01_commentthread int,"
              "m02_video int, m02_assignment decimal(6,3), m02_lab decimal(6,3), m02_comment int, m02_commentthread int,"
              "m03_video int, m03_assignment decimal(6,3), m03_lab decimal(6,3), m03_comment int, m03_commentthread int,"
              "m04_video int, m04_assignment decimal(6,3), m04_lab decimal(6,3), m04_comment int, m04_commentthread int,"
              "m05_video int, m05_assignment decimal(6,3), m05_lab decimal(6,3), m05_comment int, m05_commentthread int,"
              "final decimal(32,5), passed tinyint(2), m01_watched varchar(16), m02_watched varchar(16),"
              "m03_watched varchar(16), m04_watched varchar(16), m05_watched varchar(16));")
    conn.commit()

if __name__ == '__main__':

    terms = [
        # java
        # 'COMP102.1x-2T2015',
        # 'COMP102.1x-2T2016',
        # 'COMP102.1x-3T2016',
        '102.1x-4T2015',
        # 'COMP102.2x-1T2016',
        # 'COMP102.2x-2T2016',
        # 'COMP102.2x-3T2016',
        # 'COMP102.2x-4T2015',
        # 'COMP102x-2T2014',
    ]
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
    for term in terms:
        create_table(conn, 'weekly_participate_features')
        users = get_users(conn, term)
        get_weekly_participate(conn, term, users)
