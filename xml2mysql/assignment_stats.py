import MySQLdb
import json_wrapper


def create_grades_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table +
              "(`student_id` int, `module_id` varchar(64), `page_view` int,"
              " distinct_attempt int, `submission` int, distinct_correct int, avg_solve_time decimal(10, 5),"
              " `start` datetime, `end` datetime);")
    conn.commit()

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
# create_grades_table(conn, "all_students_grades")
terms = {
        # java
        # '102.1x-2T2015': 'COMP',
        # '102.1x-2T2016': 'COMP',
        # '102.1x-3T2016': 'COMP',
        '102.1x-4T2015': 'COMP',
        # '102.2x-1T2016': 'COMP',
        # '102.2x-2T2016': 'COMP',
        # '102.2x-3T2016': 'COMP',
        # '102.2x-4T2015': 'COMP',
        # '102x-2T2014': 'COMP',
        # android
        # '107x-3T2016': 'COMP',
        # '107x-2016_T1': 'COMP',
        # '107x-1T2016': 'COMP',
        # speaking
        # '101x-3T2016': 'EBA',
        # '101x-3T2014': 'EBA',
        # '101x-1T2016': 'EBA',
        # writing
        # '102x-4Q2015': 'EBA',
        # '102x-3T2016': 'EBA',
        # '102x-1T2016': 'EBA'
        }
modules = ['pre@ae687c1204b84885a4797f517715722a', 'M01@1ee4603833d742e698d27695d2aa25b5',
             'M02@db78e7f298c345f3af42589e06c470a2', 'M03@b57525ba4b974719b9ce4eca914e1c39',
             'M04@668fb99bb9684644822889e460197fe9', 'M05@3f0585f6e4574bac95384a227d50ef5f',
             'Exam@1020d90b174142239fcdefc2f8555d55', 'post@fd8a124c47d940dfa7d88a8ac37a7cc5']
for term_key in terms:
    term = term_key.replace('.', '_').replace('-', '_')
    create_grades_table(conn, term + "_assignment_stats")
    cursor = conn.cursor()
    # get page views of each student
    page_views = {}
    cursor.execute("SELECT user_id, event_type FROM " + terms[term_key] + term + "_clickstream_events"
                   " WHERE user_id <> '' and user_id is not NULL and event_type like %s;", ['%problem_get'])
    for row in cursor.fetchall():
        student_id = int(row[0])
        xml_id = row[1].split('/')[-4].split('@')[-1]
        if student_id not in page_views:
            page_views[student_id] = {}
        if xml_id not in page_views[student_id]:
            page_views[student_id][xml_id] = 1
        else:
            page_views[student_id][xml_id] += 1
    print('page view counted')
    for module in modules:
        module_id = module.split('@')[-1]
        # get all problems under this module
        cursor.execute("SELECT element_id from " + terms[term_key] + term + "_element where module_id=%s and element_type=\"problem\"",
                       [module_id])
        problems = [row[0] for row in cursor.fetchall()]
        # calc values of each column
        cursor.execute("SELECT student_id, count(distinct xml_id), sum(attempts), sum(grade=max_grade),"
                       " sum(TIMESTAMPDIFF(SECOND, created, modified)), min(created), max(end) FROM "
                       + term + "_student_grades" + " WHERE attempts > 0 and xml_id in %s group by student_id;", [problems])
        result = cursor.fetchall()
        for row in result:
            student_id = row[0]
            if student_id in page_views:
                page_view = sum(page_views[student_id][problem_id] if problem_id in page_views[student_id] else 0
                                for problem_id in problems)
            else:
                page_view = 0
            distinct_attempt = row[1]
            submission = row[2]
            distinct_correct = row[3]
            avg_solve_time = row[4] * 1.0 / distinct_attempt
            start = row[5]
            end = row[6]
            cursor.execute("INSERT INTO " + term + "_assignment_stats VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           [student_id, module_id, page_view, distinct_attempt, submission, distinct_correct,
                            avg_solve_time, start, end])
        conn.commit()
        print('module ' + module_id + ' inserted')

conn.close()
