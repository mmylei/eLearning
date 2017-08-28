from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import pandas as pd

pd.set_option('display.width', 180)
pd.set_option('display.max_rows', 1000)


def non_0_row_index(df):
    return (df.T > 0.0001).any()


def drop_long_real_spent_row(df):
    week_df = df[df.real_spent <= 10]
    return week_df

df = pd.read_csv('weekly_quantities_with_no_flag.csv')
# bins = [np.array([0, 1.2, 3.2, 4], dtype=np.float32),
#         np.array([0, 5.2, 10.4, 13], dtype=np.float32),
#         np.array([0, 4.5, 8.1, 9], dtype=np.float32),
#         np.array([0, 4, 8], dtype=np.float32),
#         np.array([0, 4.8, 10.8, 12], dtype=np.float32)]
scaler = StandardScaler()
for week_number in range(1, 6):
    print '-------------- week', week_number, '--------------'
    # indices = np.where(features[:, 0] == week_number)[0]  # only keep week 1 data
    # Y = features[indices, :][:, len(columns)-3]  # grade (last column)
    # X = features[indices, :][:, range(1, len(columns)-3)]  # except module_number (first column) and grade (last column)
    week_df = df[df.module_number == week_number]
    week_df = week_df.groupby('uid') \
        .agg({'real_spent': 'mean', 'coverage': 'mean', 'watched': 'mean', 'pauses': 'mean',
              'pause_length': 'mean', 'avg_speed': 'mean', 'std_speed': 'mean',
              'seek_backward': 'mean', 'seek_forward': 'mean', 'attempts': 'max', 'grade': 'max'}) \
        .reset_index()
    # week_df = drop_all_0_row(week_df)
    week_df = drop_long_real_spent_row(week_df).reset_index()
    X = week_df[
        ['real_spent', 'coverage', 'watched', 'pauses', 'pause_length', 'avg_speed', 'std_speed', 'seek_backward',
         'seek_forward']]
    idx = non_0_row_index(X)
    X = X[idx].values
    X = scaler.fit_transform(X)
    week_df = week_df[idx].reset_index()
    if week_number == 1:
        inlier_uid = [96243, 126901, 171082, 283682, 200160, 79486, 83536]
        inlier = week_df[week_df['uid'].isin(inlier_uid)][['real_spent', 'coverage', 'watched', 'pauses', 'pause_length', 'avg_speed', 'std_speed', 'seek_backward',
         'seek_forward']].values
        clf = IsolationForest()
        clf.fit(inlier)
        Y = clf.predict(X)
        print 'outliers:'
        print week_df[Y == -1]
    # md = DBSCAN(eps=1.5, min_samples=10)
    # md.fit(X)
    # print 'noisy samples:'
    # print week_df[md.labels_ == -1]
