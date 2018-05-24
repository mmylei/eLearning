import numpy as np
from sklearn.cluster import KMeans
import MySQLdb
import os
import csv
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import StandardScaler, MinMaxScaler

conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="clickstream")

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

video_basic_info_term_name_table = {
    '102.1x-4T2015': 'COMP102_1x',
    '107x-2016_T1': 'COMP107x_2016T1',
    '101x-3T2014': '101x-3T2014',
    '101x-1T2016': '101x-1T2016',
    '102x-4Q2015': '102x-4Q2015',
    '102x-1T2016': '102x-1T2016'
}

# user_id module_id avg_watch_time avg_solve_time avg_watch_num complete_time avg_replay_times avg_submit_times grades correct_num forum_activity


def get_avg_watch_time(cursor, user_id, module_number, term_key):
    cursor.execute("select P.video_id, sum(TIMESTAMPDIFF(SECOND,P.real_time_start, P.real_time_end)) from HKUSTx_" + terms[term_key]
                   + term_key.replace('.', '_').replace('-', '_') + "_video_play_piece as P, eLearning.Video_Basic_Info as V"
                                              " where P.video_id = V.video_id and V.term_id = %s"
                    + " and P.user_id = %s and V.module_number = %s group by P.video_id;", [video_basic_info_term_name_table[term_key], user_id, module_number])
    video_count = 0
    time = 0.0
    for row in cursor.fetchall():
        video_count += 1
        time += float(row[1])
    avg_watch_time = (time / video_count) if video_count > 0 else 0.0
    return avg_watch_time


def get_avg_solve_time(cursor, user_id, module_id, term, module_name):
    cursor.execute("select avg_solve_time from eLearning." + term + "_assignment_stats where student_id = %s"
                   + " and module_id = %s and module_name = %s;", [user_id, module_id, module_name])
    return cursor.fetchall()[0][0]


# avg watch num for each day
def get_avg_watch_num(cursor, user_id, module_number, term_key):
    cursor.execute("select P.video_id, P.real_time_start, P.real_time_end from HKUSTx_" + terms[term_key]
                   + term_key.replace('.', '_').replace('-', '_') + "_video_play_piece as P, eLearning.Video_Basic_Info as V"
                   + " where P.video_id = V.video_id and V.term_id = %s"
                   + " and P.user_id = %s and V.module_number = %s;", [video_basic_info_term_name_table[term_key], user_id, module_number])
    video_list = []
    time_list = []
    for row in cursor.fetchall():
        if row[0] not in video_list:
            video_list.append(row[0])
        if str(row[1]).split(' ')[0] not in time_list:
            time_list.append(str(row[1]).split(' ')[0])
        if str(row[2]).split(' ')[0] not in time_list:
            time_list.append(str(row[2]).split(' ')[0])
    avg_watch_num = (1.0 * len(video_list) / len(time_list)) if len(time_list) > 0 else 0.0
    return avg_watch_num


def get_complete_time(cursor, user_id, module_id, module_number, term_key):
    cursor.execute("select min(P.real_time_start), max(P.real_time_end) from HKUSTx_" + terms[term_key]
                   + term_key.replace('.', '_').replace('-', '_') + "_video_play_piece as P, eLearning.Video_Basic_Info as V"
                   + " where P.video_id = V.video_id and V.term_id = %s"
                   + " and P.user_id = %s and V.module_number = %s;", [video_basic_info_term_name_table[term_key], user_id, module_number])
    result1 = cursor.fetchall()
    cursor.execute("select min(start), max(end) from eLearning." + term_key.replace('.', '_').replace('-', '_') +
                   "_assignment_stats where student_id = %s and module_id = %s;", [user_id, module_id])
    result2 = cursor.fetchall()
    min_time = result1[0][0]
    max_time = result1[0][1]
    if result1[0][0] is None or result1[0][1] is None or result2[0][0] is None or result2[0][1] is None:
        return 0
    if min_time > result2[0][0]:
        min_time = result2[0][0]
    if max_time < result2[0][1]:
        max_time = result2[0][1]
    return (max_time - min_time).seconds


def get_avg_replay_times(user_id, module_name, replay):
    return float(replay[user_id][module_name])


def get_avg_submit_times(cursor, user_id, module_id, term, module_name):
    cursor.execute("select distinct_problem_attempt, submission from eLearning." + term +
                   "_assignment_stats where student_id = %s and module_id = %s and module_name = %s;",
                   [user_id, module_id, module_name])
    num, submission = cursor.fetchall()[0]
    return (1.0 * submission / num) if num > 0 else 0.0


def get_grades(cursor, user_id, term, module_name, term_key):
    cursor.execute("select G.grade, A.max_grade from eLearning.HKUSTx_" + terms[term_key] + term +
                   "_student_grade as G, eLearning.all_max_grade as A where G.student_id = %s"
                   + " and G.aggregated_category = A.problem_type and A.problem_type = %s;", [user_id, module_name])
    grade, max_grade = cursor.fetchall()[0]
    return float(grade) / float(max_grade)


def get_correct_num(cursor, user_id, term, module_id, module_name, term_key):
    cursor.execute("select count(*) from eLearning.HKUSTx_" + terms[term_key] + term +
                   "_problem_set where aggregated_category = %s;", [module_name])
    problem_num = cursor.fetchall()[0][0]
    cursor.execute("select distinct_correct from eLearning." + term +
                   "_assignment_stats where student_id = %s and module_id = %s and module_name = %s;",
                   [user_id, module_id, module_name])
    correct_num = cursor.fetchall()[0][0]
    return (1.0 * correct_num / problem_num) if problem_num > 0 else 0.0


def get_forum_activity(cursor, user_id, term, module_name):
    cursor.execute("select response_num from eLearning." + term +
                   "_forum_stats where author_id = %s and module_id = %s;", [user_id, module_name])
    result = cursor.fetchall()
    if len(result) > 0:
        respond = result[0][0]
    else:
        respond = 0
    cursor.execute("select sum(response_num) from eLearning." + term +
                   "_forum_stats where module_id = %s;", [module_name])
    all_respond = cursor.fetchall()[0][0]
    return (1.0 * respond / float(all_respond)) if all_respond > 0 else 0.0


def get_replay():
    with open('graded_modules_w_p.txt', 'r') as r:
        result = r.read()
        replay = {}
        for line in result:
            if len(line) > 1:
                line = line.split(',')
                if line[0] not in replay:
                    replay[line[0]] = {}
                replay[line[0]][line[1]] = line[2].strip()
    return replay


def prepare_features():
    for term_key in terms:
        if os.path.exists(term_key + '_assignment_stats_features.csv'):
            continue
        term = term_key.replace('.', '_').replace('-', '_')
        cursor = conn.cursor()
        cursor.execute("select A.student_id, A.module_id, A.module_name from eLearning." + term +
                       "_assignment_stats as A, eLearning." + term +
                       "_django_comment_client_role_users as R, HKUSTx_" + terms[term_key]
                   + term_key.replace('.', '_').replace('-', '_') + "_video_play_piece as P where A.student_id = R.user_id and A.student_id = P.user_id and A.student_id <> 0 "
                       "and R.name = 'Student';")
        features = []
        replay = get_replay()
        for row in cursor.fetchall():
            user_id = str(row[0])
            module_id = row[1]
            module_name = row[2]
            module_number = int(row[2].split('0')[-1]) if '0' in row[2] else -10
            avg_watch_time = get_avg_watch_time(cursor, user_id, module_number, term_key)
            avg_solve_time = get_avg_solve_time(cursor, user_id, module_id, term, module_name)
            avg_watch_num = get_avg_watch_num(cursor, user_id, module_number, term_key)
            complete_time = get_complete_time(cursor, user_id, module_id, module_number, term_key)
            avg_replay_times = get_avg_replay_times(user_id, module_name, replay)
            avg_submit_times = get_avg_submit_times(cursor, user_id, module_id, term, module_name)
            grades = get_grades(cursor, user_id, term, module_name, term_key)
            correct_num = get_correct_num(cursor, user_id, term, module_id, module_name, term_key)
            forum_activity = get_forum_activity(cursor, user_id, term, module_name)
            one_feature = [user_id, module_id, module_name, avg_watch_time, avg_solve_time, avg_watch_num, complete_time,
                           avg_replay_times, avg_submit_times, grades, correct_num, forum_activity]
            features.append(one_feature)
        with open(term_key + '_assignment_stats_features.csv', 'wb') as f:
            writer = csv.writer(f)
            for feature in features:
                writer.writerow(feature)


def clustering():
    for term_key in terms:
        scaler = MinMaxScaler()
        features = []
        with open(term_key + '_assignment_stats_features.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                features.append(row[3:])
        np_features = np.array(features, dtype=np.float32)
        np_features = scaler.fit_transform(np_features)
        model = KMeans(n_clusters=4)
        model.fit(np_features)
        with open(term_key + '_assignment_stats_KMeans.csv', 'wb') as f:
            writer = csv.writer(f)
            for label in model.labels_:
                writer.writerow(label)


def get_correlation():
    for term_key in terms:
        print term_key
        features = []
        labels = []
        scaler = MinMaxScaler()
        with open(term_key + '_assignment_stats_features.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                features.append(row[3:])
        np_features = np.array(features, dtype=np.float32)
        np_features = scaler.fit_transform(np_features)
        with open(term_key + '_assignment_stats_KMeans.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                labels.append(row[0])
        np_labels = np.array(labels, dtype=np.float32)
        correlation = SelectKBest(k='all')
        correlation.fit(np_features, np_labels)
        scores = correlation.scores_
        print scores

if __name__ == '__main__':
    prepare_features()
    conn.close()
    clustering()
    get_correlation()
