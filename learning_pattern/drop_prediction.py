import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import sys
import MySQLdb
import numpy as np
import pandas as pd
from sklearn.model_selection import ShuffleSplit, StratifiedShuffleSplit
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier, Lasso
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn import svm
from sklearn import neighbors
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import mean_squared_error, zero_one_loss
from sklearn.preprocessing import MinMaxScaler
import logging

FORMAT = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

week_df = None


def append_drop_feature():
    data = pd.read_csv('weekly_quantities_with_no_flag.csv')
    data.assign(drop_kind1=pd.Series(np.zeros((data.shape[0]), dtype=np.int8)))
    data.assign(drop_kind2=pd.Series(np.zeros((data.shape[0]), dtype=np.int8)))
    data.assign(drop_kind3=pd.Series(np.zeros((data.shape[0]), dtype=np.int8)))
    data.assign(drop_kind4=pd.Series(np.zeros((data.shape[0]), dtype=np.int8)))
    conn = MySQLdb.connect(host="localhost", user="eLearning", passwd="Mdb4Learn", db="eLearning")
    cursor = conn.cursor()
    cursor.execute(
        'select user_id, drop_week1, drop_week2, drop_week3, drop_week4 from weekly_participate_features;')
    result = cursor.fetchall()
    n = len(result)
    i = 0
    for row in result:
        i += 1
        print 'insert row', i, '/', n
        uid = row[0]
        data.loc[data.uid == uid, 'drop_kind1'] = row[1]
        data.loc[data.uid == uid, 'drop_kind2'] = row[2]
        data.loc[data.uid == uid, 'drop_kind3'] = row[3]
        data.loc[data.uid == uid, 'drop_kind4'] = row[4]
    data.to_csv('weekly_quantities_with_drop.csv')


def load_data():
    logger.info('loading csv data')
    data = pd.read_csv('weekly_quantities_with_drop.csv')
    return data


def non_0_row_index(df):
    return (df.T > 0.0001).any()


def drop_long_real_spent_row(df):
    week_df = df[df.real_spent <= 10]
    return week_df


def classification(X, Y, model):
    test_error = 0
    train_error = 0
    fold = 0
    for train_index, test_index in ShuffleSplit(n_splits=5, test_size=0.2).split(X, Y):
        fold += 1
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        model.fit(X_train, Y_train)

        Y_predict = model.predict(X_train)
        error = mean_squared_error(Y_train, Y_predict)
        logger.info('fold: ' + str(fold) + ', training error: ' + str(error))
        train_error += error

        Y_predict = model.predict(X_test)
        error = mean_squared_error(Y_test, Y_predict)
        logger.info('fold: ' + str(fold) + ', test error: ' + str(error))

        test_error += error

    real_test_error = test_error / 5.0
    real_train_error = train_error / 5.0

    logger.info('train_error: ' + str(real_train_error))
    logger.info('test_error: ' + str(real_test_error))
    return model


if __name__ == '__main__':
    if 'append_feature' in sys.argv:
        append_drop_feature()
        exit()

    df = load_data()
    drop_kind = 'drop_kind1'
    # group by uid and module_number
    df = week_df.groupby(['uid', 'module_number']) \
        .agg({'real_spent': 'mean', 'coverage': 'mean', 'watched': 'mean', 'pauses': 'mean',
              'pause_length': 'mean', 'avg_speed': 'mean', 'std_speed': 'mean',
              'seek_backward': 'mean', 'seek_forward': 'mean', 'attempts': 'max', drop_kind: 'max'}) \
        .reset_index(drop=True)
    # features after dropping are not useful
    df = df[df['module_number'] < df[drop_kind]].reset_index(drop=True)
    # clean data
    df = drop_long_real_spent_row(df).reset_index(drop=True)
    idx = non_0_row_index(df[['real_spent', 'coverage', 'watched', 'pauses', 'pause_length', 'avg_speed', 'std_speed',
                              'seek_backward', 'seek_forward']])
    df = df[idx].reset_index(drop=True)
    # get Y, default class 0
    Y = np.zeros((df.shape[0]), dtype=np.int8)
    # class 1: drop in the next week
    Y[df['module_number'] == df[drop_kind] - 1] = 1
    # get X
    X = week_df[['real_spent', 'coverage', 'watched', 'pauses', 'pause_length', 'avg_speed', 'std_speed', 'seek_backward', 'seek_forward']].values
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    # classification
    classification(X, Y, RandomForestClassifier())
