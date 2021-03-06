import MySQLdb


def get_users(conn, term):
    table_name1 = (term.replace('COMP', '').replace('EBA', '') + '_auth_user').replace('-', '_').replace('.', '_')
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
    table_name2 = ('HKUSTx-' + term + '_clickstream').replace('-', '_').replace('.', '_')
    table_name3 = ('HKUSTx-' + term + '-user_video').replace('-', '_').replace('.', '_')
    table_name4 = ('HKUSTx-' + term + '_student_grade').replace('-', '_').replace('.', '_')
    table_name5 = (term.replace('COMP', '').replace('EBA', '') + '_certificates_generatedcertificate').replace('-', '_').replace('.', '_')
    table_name6 = (term.replace('COMP', '').replace('EBA', '') + '_commentthread').replace('-', '_').replace('.', '_')
    table_name7 = (term.replace('COMP', '').replace('EBA', '') + '_comment').replace('-', '_').replace('.', '_')
    sql1 = 'select B.video_id, B.module_number, S.flag from Video_Basic_Info as B, clickstream.Video_Stats_Info as S where B.video_id = S.video_id and B.term_id = \''+ convert_term_id(term) + '\' and B.module_number < 6;'
    cursor = conn.cursor()
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    flag1 = [0] * 5
    video = [0] * 5
    sql10 = 'select module_number, count(B.video_id) from Video_Basic_Info as B, clickstream.Video_Stats_Info as S where B.video_id = S.video_id and B.term_id = \''+ convert_term_id(term) + '\' and B.module_number < 6 group by B.module_number;'
    cursor.execute(sql10)
    result10 = cursor.fetchall()
    for module_num in range(1,6):
        video[module_num-1] = result10[module_num-1][1]
    sql11 = 'select module_number, count(B.video_id) from Video_Basic_Info as B, clickstream.Video_Stats_Info as S where B.video_id = S.video_id and B.term_id = \''+ convert_term_id(term) + '\' and B.module_number < 6 and S.flag = 1 group by B.module_number;'
    cursor.execute(sql11)
    result11 = cursor.fetchall()
    for module_num in range(1, 6):
        flag1[module_num - 1] = result11[module_num - 1][1]
    for uid in users:
        m_video = [0] * 5
        finished = [0] * 5
        finished_flag1 = [0] * 5
        m_assignment = [0] * 5
        l_assignment = [0] * 5
        comment_thread = [0] * 5
        comment = [0] * 5
        watched = [''] * 5
        for row in result1:
            module_num = row[1]
            sql2 = 'select coverage, is_finished, is_covered from clickstream.' + table_name3 + ' where user_id = ' + str(uid) + ' and video_id= \'' + row[0] + '\';'
            cursor.execute(sql2)
            result2 = cursor.fetchall()
            if len(result2) > 0:
                # video[module_num-1] += 1
                if result2[0][0] > 0:
                    m_video[module_num-1] += 1
                if row[2] == 1:
                    # flag1[module_num-1] += 1
                    if result2[0][1] == 1 or result2[0][2] == 1:
                        finished_flag1[module_num-1] += 1
                        finished[module_num-1] += 1
                else:
                    if result2[0][1] == 1 or result2[0][2] == 1:
                        finished[module_num-1] += 1

        for module_num in xrange(1, 6):
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
            sql8 = 'select comment_thread_id, count(*) from ' + table_name7 + ' where author_id = ' + str(uid) + ' group by comment_thread_id;'
            cursor.execute(sql8)
            result8 = cursor.fetchall()
            for row8 in result8:
                comment_thread_id = row8[0]
                sql9 = 'select count(*) from ' + table_name6 + ' where `id`=\'' + comment_thread_id + '\' and commentable_id like \'m' + str(
                    module_num) + '%\';'
                cursor.execute(sql9)
                result9 = cursor.fetchall()
                if len(result9) > 0:
                    comment[module_num-1] += row8[1]

        for module_num in range(1, 6):
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
        values.append(term)
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


def convert_term_id(term):
    if term in ['COMP102.1x-2T2015',
        'COMP102.1x-2T2016',
        'COMP102.1x-3T2016',
        # '102.1x-4T2015',
        'COMP102.2x-1T2016',
        'COMP102.2x-2T2016',
        'COMP102.2x-3T2016',
        'COMP102.2x-4T2015']:
        return 'COMP102_1x'
    if term in ['COMP107x-3T2016',
        'COMP107x-2016_T1',
        'COMP107x-1T2016']:
        return 'COMP107x_2016T1'
    if term in ['EBA101x-3T2016',
        'EBA101x-3T2014',
        'EBA101x-1T2016']:
        return 'EBA101x'
    if term in [
        'EBA102x-4Q2015',
        'EBA102x-3T2016',
        'EBA102x-1T2016']:
        return 'EBA102x'


if __name__ == '__main__':

    terms = [
        # java
        'COMP102.1x-2T2015',
        'COMP102.1x-2T2016',
        'COMP102.1x-3T2016',
        # '102.1x-4T2015',
        'COMP102.2x-1T2016',
        'COMP102.2x-2T2016',
        'COMP102.2x-3T2016',
        'COMP102.2x-4T2015',
        # 'COMP102x-2T2014',
        # android
        'COMP107x-3T2016',
        'COMP107x-2016_T1',
        'COMP107x-1T2016',
        # speaking
        'EBA101x-3T2016',
        'EBA101x-3T2014',
        'EBA101x-1T2016',
        # writing
        'EBA102x-4Q2015',
        'EBA102x-3T2016',
        'EBA102x-1T2016'
    ]
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
    for term in terms:
        # create_table(conn, 'weekly_participate_features')
        users = get_users(conn, term)
        get_weekly_participate(conn, term, users)
