import MySQLdb
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] (%(name)s: %(lineno)d) %(message)s')


def create_grades_table(conn, table):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + table + ";")
    conn.commit()
    c.execute("CREATE TABLE " + table +
              "(`student_id` int, `module_id` varchar(64), module_name char(16), `page_view` int, "
              "distinct_problem_view int,"
              " distinct_problem_attempt int, `submission` int, distinct_correct int, avg_solve_time double,"
              " `start` datetime, `end` datetime, grades decimal(10, 5), PRIMARY KEY (student_id, module_id, module_name));")
    conn.commit()


conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
# create_grades_table(conn, "all_students_grades")
terms = {
    # java
    # '102.1x-2T2015': 'COMP',
    # '102.1x-2T2016': 'COMP',
    # '102.1x-3T2016': 'COMP',
    # '102.1x-4T2015': 'COMP',
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
    '101x-1T2016': 'EBA',
    # writing
    # '102x-4Q2015': 'EBA',
    # '102x-3T2016': 'EBA',
    # '102x-1T2016': 'EBA'
}

get_problem_id = {
    # java
    '102.1x-2T2015': lambda x: x.split('@')[-1].split('/')[0],
    '102.1x-2T2016': lambda x: x.split('@')[-1].split('/')[0],
    '102.1x-3T2016': lambda x: x.split('@')[-1].split('/')[0],
    '102.1x-4T2015': lambda x: x.split('@')[-1].split('/')[0],
    '102.2x-1T2016': lambda x: x.split('@')[-1].split('/')[0],
    '102.2x-2T2016': lambda x: x.split('@')[-1].split('/')[0],
    '102.2x-3T2016': lambda x: x.split('@')[-1].split('/')[0],
    '102.2x-4T2015': lambda x: x.split('@')[-1].split('/')[0],
    '102x-2T2014': lambda x: x.split('@')[-1].split('/')[0],
    # android
    '107x-3T2016': lambda x: x.split('@')[-1].split('/')[0],
    '107x-2016_T1': lambda x: x.split('@')[-1].split('/')[0],
    '107x-1T2016': lambda x: x.split('@')[-1].split('/')[0],
    # speaking
    '101x-3T2016': lambda x: x.split('@')[-1].split('/')[0],
    '101x-3T2014': lambda x: x.split('/')[-4].split('_')[-1],
    '101x-1T2016': lambda x: x.split('@')[-1].split('/')[0],
    # writing
    '102x-4Q2015': lambda x: x.split('/')[-4].split('_')[-1],
    '102x-3T2016': lambda x: x.split('@')[-1].split('/')[0],
    '102x-1T2016': lambda x: x.split('@')[-1].split('/')[0]
}

modules = {
    '102.1x-4T2015': [
        'M01@1ee4603833d742e698d27695d2aa25b5',
        'M02@db78e7f298c345f3af42589e06c470a2',
        'M03@b57525ba4b974719b9ce4eca914e1c39',
        'M04@668fb99bb9684644822889e460197fe9',
        'M05@3f0585f6e4574bac95384a227d50ef5f',
        'Exam@1020d90b174142239fcdefc2f8555d55'
    ],
    '107x-2016_T1': [
        'M01@234fa80753b1476592ae17d37b17bb9e',
        'M02@9fd029452bf2495f819dd083fe769a5d',
        'M03@b254be2e401a44a794c1a6961adffcc5',
        'M04@4f6e3c6c28564d2f84289d7eaceebcb1',
        'M05@93ca675ee54240d79cddc6219556011f'
    ],
    '101x-3T2014': [
        'M01@786a1e9b72a4426aa0faae7ea8dfd458',
        'M02@9f97ebac81584d4d82c2278c04466f72',
        'M03@0347ec2e8ed84434a3ffdd0aeb9b29ca',
        'M04@8dfb41aede1b4adc98354c5ff05335d8',
        'M05@d49f74961ee74674950be979f2365f82',
        'M06@d0f02e09d13c41d1a1e1135ecb54cbe9',
        'M07@c588e52413634310b2fd1aa257f840e3',
    ],
    '101x-1T2016': [
        'M01@786a1e9b72a4426aa0faae7ea8dfd458',
        'M02@9f97ebac81584d4d82c2278c04466f72',
        'M03@0347ec2e8ed84434a3ffdd0aeb9b29ca',
        'M04@8dfb41aede1b4adc98354c5ff05335d8',
        'M05@d49f74961ee74674950be979f2365f82',
        'M06@d0f02e09d13c41d1a1e1135ecb54cbe9',
        'M07@c588e52413634310b2fd1aa257f840e3',
    ],
    '102x-4Q2015': [
        'M01@df20fa07b6ae4e84bd0d51cd7c407e56',
        'M02@174183c4cc9844508e4a98556614b7f0',
        'M03@16b9fe2877fc413d88e2a0008a85b36e',
        'M04@81f50f96e4c44d87ae19452270f1aa6d',
        'M05@d2e89afb6cd743218d80f92272c98bff',
        'M06@60ffad0df6d94b8f8016ede87ebca6bd',
        'M07@2406dcc97b9c4aa1a2b8fd8ebd38d7b7',
    ],
    '102x-1T2016': [
        'M01@df20fa07b6ae4e84bd0d51cd7c407e56',
        'M02@174183c4cc9844508e4a98556614b7f0',
        'M03@16b9fe2877fc413d88e2a0008a85b36e',
        'M04@81f50f96e4c44d87ae19452270f1aa6d',
        'M05@d2e89afb6cd743218d80f92272c98bff',
        'M06@60ffad0df6d94b8f8016ede87ebca6bd',
        'M07@2406dcc97b9c4aa1a2b8fd8ebd38d7b7',
    ]
}
# 10214T2015
# modules = ['M01@1ee4603833d742e698d27695d2aa25b5',
#              'M02@db78e7f298c345f3af42589e06c470a2', 'M03@b57525ba4b974719b9ce4eca914e1c39',
#              'M04@668fb99bb9684644822889e460197fe9', 'M05@3f0585f6e4574bac95384a227d50ef5f',
#              'Exam@1020d90b174142239fcdefc2f8555d55']

# 1072016T1
# modules = ['M01@234fa80753b1476592ae17d37b17bb9e',
#                  'M02@9fd029452bf2495f819dd083fe769a5d', 'M03@b254be2e401a44a794c1a6961adffcc5',
#                  'M04@4f6e3c6c28564d2f84289d7eaceebcb1', 'M05@93ca675ee54240d79cddc6219556011f']

# 1013T2014 1011T2016
# modules = ['M01@786a1e9b72a4426aa0faae7ea8dfd458',
#            'M02@9f97ebac81584d4d82c2278c04466f72', 'M03@0347ec2e8ed84434a3ffdd0aeb9b29ca',
#            'M04@8dfb41aede1b4adc98354c5ff05335d8', 'M05@d49f74961ee74674950be979f2365f82',
#            'M06@d0f02e09d13c41d1a1e1135ecb54cbe9', 'M07@c588e52413634310b2fd1aa257f840e3',
#            ]


# 1024Q2015 1021T2016
# modules = ['M01@df20fa07b6ae4e84bd0d51cd7c407e56',
#              'M02@174183c4cc9844508e4a98556614b7f0', 'M03@16b9fe2877fc413d88e2a0008a85b36e',
#              'M04@81f50f96e4c44d87ae19452270f1aa6d', 'M05@d2e89afb6cd743218d80f92272c98bff',
#              'M06@60ffad0df6d94b8f8016ede87ebca6bd', 'M07@2406dcc97b9c4aa1a2b8fd8ebd38d7b7',
#               ]
# #

def solve_time_table(cursor, student_id, table):
    cursor.execute("SELECT event_type, referer, emitted_time FROM " + table +
                   " WHERE user_id = %s AND (event_type in %s OR event_type like %s) ORDER BY emitted_time;",
                   [str(student_id), ['problem_graded', 'page_close'], '%problem_get'])
    time_table = {}
    current_referer = None
    current_problem = None
    current_time = None
    for row in cursor.fetchall():
        if row[0].endswith('problem_get'):
            current_problem = get_problem_id[term_key](row[0])
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


def get_grades(cursor, student_id, aggregated_category, table):
    cursor.execute("select grade from " + table + " where student_id = %s and aggregated_category = %s;", [student_id, aggregated_category])
    return cursor.fetchall()[0][0]


for term_key in terms:
    logger.info("start term " + term_key)
    term = term_key.replace('.', '_').replace('-', '_')
    create_grades_table(conn, term + "_assignment_stats")
    cursor = conn.cursor()
    # get page views of each student
    page_views = {}
    cursor.execute("SELECT user_id, event_type FROM " + terms[term_key] + term + "_clickstream_events"
                                                                                 " WHERE user_id <> '' AND user_id IS NOT NULL AND event_type LIKE %s;",
                   ['%problem_get'])
    for row in cursor.fetchall():
        student_id = int(row[0])
        xml_id = get_problem_id[term_key](row[1])
        if student_id not in page_views:
            page_views[student_id] = {}
        if xml_id not in page_views[student_id]:
            page_views[student_id][xml_id] = 1
        else:
            page_views[student_id][xml_id] += 1
    logger.info('page view counted')
    for module in modules[term_key]:
        logger.info("start module " + module)
        module_id = module.split('@')[-1]
        module_name = module.split('@')[0]
        if module_name == 'Exam':
            problem_types = ['Exam']
        elif module_name[0] == 'M':
            problem_types = [module_name, module_name.replace('M', 'L'), module_name.replace('M', 'Q'),
                             module_name.replace('M', 'T')]
        else:
            problem_types = [module_name]
        logger.info("problem_types: " + str(problem_types))
        for problem_type in problem_types:
            logger.info("problem type: " + problem_type)
            # get all problems under this module
            cursor.execute("SELECT element_id from " + terms[term_key] + term + "_element, HKUSTx_"
                           + terms[term_key] + term + "_problem_set as P where element_id = xml_id and P.aggregated_category = \""
                           + problem_type + "\" and module_id=%s and (element_type=\"problem\" or element_type=\"openassessment\")",
                           [module_id])
            result = cursor.fetchall()
            problems = []
            for row in result:
                problems.append(row[0])
            if len(problems) == 0:
                logger.info("no problems of type " + problem_type)
                continue
            # calc values of each column
            cursor.execute("SELECT student_id, count(distinct xml_id), sum(attempts), sum(grade=max_grade),"
                           " 0, min(created), max(modified) FROM "
                           + term + "_students_grades" + " WHERE attempts > 0 and xml_id in %s GROUP BY student_id;",
                           [problems])
            result = cursor.fetchall()
            logger.info("student num: " + str(len(result)))
            for row in result:
                student_id = row[0]
                # logger.info("start student id " + str(student_id))
                problem_solve_time_table = solve_time_table(cursor, student_id,
                                                            terms[term_key] + term + "_clickstream_events")
                if student_id in page_views:
                    page_view = sum(page_views[student_id][problem_id] if problem_id in page_views[student_id] else 0
                                    for problem_id in problems)
                else:
                    page_view = 0
                if student_id in page_views:
                    distinct_problem_view = sum(1 if problem_id in page_views[student_id] else 0 for problem_id in problems)
                else:
                    distinct_problem_view = 0
                distinct_problem_attempt = row[1]
                submission = row[2]
                distinct_correct = row[3]
                total_solve_time = sum(
                    problem_solve_time_table[problem_id] if problem_id in problem_solve_time_table else 0
                    for problem_id in problems)
                avg_solve_time = float(total_solve_time) / distinct_problem_attempt
                start = row[5]
                end = row[6]
                grades = get_grades(cursor, student_id, problem_type, "HKUSTx_" + terms[term_key] + term + "_student_grade")
                cursor.execute(
                    "INSERT INTO " + term + "_assignment_stats VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    [student_id, module_id, problem_type, page_view, distinct_problem_view, distinct_problem_attempt,
                     submission, distinct_correct, avg_solve_time, start, end, grades])
                # logger.info("finished student " + str(student_id))
            logger.info("finished problem type " + problem_type)
            conn.commit()
        logger.info('module ' + module_id + ' inserted')

conn.close()
