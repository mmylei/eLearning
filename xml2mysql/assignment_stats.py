import MySQLdb
import json_wrapper


def create_grades_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table +
              "(`student_id` int, `module_id` varchar(64), module_name char(16), `page_view` int, "
              "distinct_problem_view int,"
              " distinct_problem_attempt int, `submission` int, distinct_correct int, avg_solve_time double,"
              " `start` datetime, `end` datetime, PRIMARY KEY (student_id, module_id, module_name));")
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

#10214T2015
modules = ['pre@ae687c1204b84885a4797f517715722a', 'M01@1ee4603833d742e698d27695d2aa25b5',
             'M02@db78e7f298c345f3af42589e06c470a2', 'M03@b57525ba4b974719b9ce4eca914e1c39',
             'M04@668fb99bb9684644822889e460197fe9', 'M05@3f0585f6e4574bac95384a227d50ef5f',
             'Exam@1020d90b174142239fcdefc2f8555d55', 'post@fd8a124c47d940dfa7d88a8ac37a7cc5']

#1072016T1
# modules = ['pre@72365fc2f807409582f1db38f3ac6879', 'M01@234fa80753b1476592ae17d37b17bb9e',
#                  'M02@9fd029452bf2495f819dd083fe769a5d', 'M03@b254be2e401a44a794c1a6961adffcc5',
#                  'M04@4f6e3c6c28564d2f84289d7eaceebcb1', 'M05@93ca675ee54240d79cddc6219556011f']

#1013T2014 1011T2016
# modules = ['pre@7bb6213618344dd9a3d6eed0679cd1da', 'M01@786a1e9b72a4426aa0faae7ea8dfd458',
#              'M02@9f97ebac81584d4d82c2278c04466f72', 'M03@0347ec2e8ed84434a3ffdd0aeb9b29ca',
#              'M04@8dfb41aede1b4adc98354c5ff05335d8', 'M05@d49f74961ee74674950be979f2365f82',
#              'M06@d0f02e09d13c41d1a1e1135ecb54cbe9', 'M07@c588e52413634310b2fd1aa257f840e3',
#              'post@428e6b7750e54d92a2c5bae1561a3b62']

#1024Q2015 1021T2016
# modules = ['pre@4efc576a67bc4d3f97c9e5826cc1af83', 'M01@df20fa07b6ae4e84bd0d51cd7c407e56',
#              'M02@174183c4cc9844508e4a98556614b7f0', 'M03@16b9fe2877fc413d88e2a0008a85b36e',
#              'M04@81f50f96e4c44d87ae19452270f1aa6d', 'M05@d2e89afb6cd743218d80f92272c98bff',
#              'M06@60ffad0df6d94b8f8016ede87ebca6bd', 'M07@2406dcc97b9c4aa1a2b8fd8ebd38d7b7',
#              'post@7bcb47d024034947b7db98ebc1a0d8b5']
#

def solve_time_table(cursor, student_id, table):
    cursor.execute("SELECT event_type, referer, emitted_time FROM " + table +
                   " WHERE user_id = %s AND (event_type in %s OR event_type like %s) SORT BY emitted_time;",
                   [student_id, ['problem_graded', 'page_close'], '%problem_get'])
    time_table = {}
    current_referer = None
    current_problem = None
    current_time = None
    for row in cursor.fetchall():
        if row[0].endswith('problem_get'):
            current_problem = row[0].split('@')[-1].split('/')[0]
            current_referer = row[1]
            current_time = row[2]
        if current_problem is not None and current_referer == row[1]:
            solve_time = (row[2] - current_time).total_seconds()
            if current_problem not in time_table:
                time_table[current_problem] = solve_time
            else:
                time_table[current_problem] += solve_time
            current_time = row[2]
    return time_table


for term_key in terms:
    term = term_key.replace('.', '_').replace('-', '_')
    create_grades_table(conn, term + "_assignment_stats")
    cursor = conn.cursor()
    # get page views of each student
    page_views = {}
    cursor.execute("SELECT user_id, event_type FROM " + terms[term_key] + term + "_clickstream_events"
                   " WHERE user_id <> '' AND user_id IS NOT NULL AND event_type LIKE %s;", ['%problem_get'])
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
        module_name = module.split('@')[0]
        if module_name == 'Exam':
            problem_types = ['Exam']
        elif module_name[0] == 'M':
            problem_types = [module_name, module_name.replace('M', 'L')]
        else:
            problem_types = [module_name]
        for problem_type in problem_types:
            # get all problems under this module
            cursor.execute("SELECT element_id from " + terms[term_key] + term + "_element, HKUSTx_"
                           + terms[term_key] + term + "_problem_set where element_id = xml_id and aggregated_category = \""
                           + problem_type + "\" and module_id=%s and element_type=\"problem\"",
                           [module_id])
            result = cursor.fetchall()
            problems = []
            for row in result:
                problems.append(row[0])
            if len(problems) == 0:
                continue
            # calc values of each column
            cursor.execute("SELECT student_id, count(distinct xml_id), sum(attempts), sum(grade=max_grade),"
                           " 0, min(created), max(modified) FROM "
                           + term + "_students_grades" + " WHERE attempts > 0 and xml_id in %s GROUP BY student_id;", [problems])
            result = cursor.fetchall()
            for row in result:
                student_id = row[0]
                problem_solve_time_table = solve_time_table(cursor, student_id, terms[term_key] + term + "_clickstream_events")
                if student_id in page_views:
                    page_view = sum(page_views[student_id][problem_id] if problem_id in page_views[student_id] else 0
                                    for problem_id in problems)
                else:
                    page_view = 0
                distinct_problem_view = len(page_view[student_id])
                distinct_problem_attempt = row[1]
                submission = row[2]
                distinct_correct = row[3]
                total_solve_time = sum(problem_solve_time_table[problem_id] if problem_id in problem_solve_time_table else 0
                                       for problem_id in problems)
                avg_solve_time = float(total_solve_time) / distinct_problem_attempt
                start = row[5]
                end = row[6]
                cursor.execute("INSERT INTO " + term + "_assignment_stats VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                               [student_id, module_id, problem_type, page_view, distinct_problem_view, distinct_problem_attempt,
                                submission, distinct_correct, avg_solve_time, start, end])
            conn.commit()
        print('module ' + module_id + ' inserted')

conn.close()
