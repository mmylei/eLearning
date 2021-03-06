import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import numpy as np
import pandas as pd
from sklearn.model_selection import ShuffleSplit, StratifiedShuffleSplit
from sklearn.feature_selection import RFECV, VarianceThreshold, SelectKBest, chi2
from sklearn.decomposition import PCA, KernelPCA
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn import tree
from sklearn import svm
from sklearn import neighbors
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import mean_squared_error, zero_one_loss, mean_absolute_error
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import logging

FORMAT = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

week_df = None


def load_data():
    logger.info('loading csv data')
    # data = np.load('weekly_quantities_data.npz')
    data = pd.read_csv('weekly_quantities_with_no_flag.csv')
    # X = data['features']
    # column_names = data['columns']
    # return X, column_names
    return data


def non_0_row_index(df):
    return (df.T > 0.0001).any()


def drop_long_real_spent_row(df):
    week_df = df[df.real_spent <= 10]
    return week_df


def draw_correlation_figure(df):
    # df = pd.DataFrame(data=X, columns=columns)
    correlations = df.corr()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlations, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, len(df.columns), 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(list(df.columns))
    ax.set_yticklabels(list(df.columns))
    savefig('./correlation.png', bbox_inches='tight')


def baseline(Y):
    average = np.mean(Y)
    bl = 0
    for grade in Y:
        bl += abs(grade - average)
    bl = bl / len(Y)
    return bl


def regression(X, Y, model=RandomForestRegressor()):
    test_error = 0
    train_error = 0
    fold = 0
    for train_index, test_index in ShuffleSplit(n_splits=5, test_size=0.2).split(X, Y):
        fold += 1
        # logger.info('train index: ' + str(train_index))
        # logger.info('test index: ' + str(test_index))
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        # model = tree.DecisionTreeClassifier()
        # logger.info('fold: ' + str(fold) + ', good students in training: ' + str(sum(map(lambda x: 1 if x == 1 else 0, Y_train))))
        # logger.info('fold: ' + str(fold) + ', normal students in training: ' + str(sum(map(lambda x: 1 if x == 0 else 0, Y_train))))
        # logger.info('fold: ' + str(fold) + ', poor students in training: ' + str(sum(map(lambda x: 1 if x == -1 else 0, Y_train))))
        # logger.info('fold: ' + str(fold) + ', good students in test: ' + str(
        #     sum(map(lambda x: 1 if x == 1 else 0, Y_test))))
        # logger.info('fold: ' + str(fold) + ', normal students in test: ' + str(
        #     sum(map(lambda x: 1 if x == 0 else 0, Y_test))))
        # logger.info('fold: ' + str(fold) + ', poor students in test: ' + str(
        #     sum(map(lambda x: 1 if x == -1 else 0, Y_test))))
        model.fit(X_train, Y_train)

        Y_predict = model.predict(X_train)
        error = mean_absolute_error(Y_train, Y_predict)
        logger.info('fold: ' + str(fold) + ', training error: ' + str(error))
        train_error += error

        Y_predict = model.predict(X_test)
        error = mean_absolute_error(Y_test, Y_predict)
        logger.info('fold: ' + str(fold) + ', test error: ' + str(error))

        uids = week_df['uid'].values[test_index]
        full_info = np.dstack([uids, Y_test, Y_predict, np.fabs(Y_predict-Y_test)])[0]
        order = full_info[:, 3].argsort()
        full_info = full_info[order][[1, 2, 3, 4, 5, -5, -4, -3, -2, -1]]
        #print 'absolute error:', full_info
        # for x in full_info:
        #     print int(x[0]), x[1], x[2], x[3]
        #     print 'features: ', week_df[week_df.uid == int(x[0])]

        test_error += error

    real_test_error = test_error / 5.0
    real_train_error = train_error / 5.0

    logger.info('train_error: ' + str(real_train_error))
    logger.info('test_error: ' + str(real_test_error))
    bl = baseline(Y)
    logger.info('baseline: ' + str(bl))
    return model


# def sum_feature_by_user(features):


if __name__ == '__main__':
    df = load_data()
    # feature_length = len(columns)
    # columns = ['uid', 'vid', 'module_number', 'real_spent', 'coverage', 'watched', 'pauses', 'pause_length', 'avg_speed', 'std_speed', 'seek_backward', 'seek_forward', 'attempts', 'grade', 'max_grade', 'normalized_grade']
    draw_correlation_figure(df[['real_spent', 'coverage', 'watched', 'pauses', 'pause_length', 'avg_speed', 'std_speed', 'seek_backward', 'seek_forward', 'grade']])
    for week_number in range(1, 6):
        print '-------------- week', week_number, '--------------'
        # indices = np.where(features[:, 0] == week_number)[0]  # only keep week 1 data
        # Y = features[indices, :][:, len(columns)-3]  # grade (last column)
        # X = features[indices, :][:, range(1, len(columns)-3)]  # except module_number (first column) and grade (last column)
        week_df = df[df.module_number == week_number]
        week_df = drop_long_real_spent_row(week_df).reset_index(drop=True)
        idx = non_0_row_index(week_df[['real_spent', 'coverage', 'watched', 'pauses', 'pause_length', 'avg_speed', 'std_speed', 'seek_backward', 'seek_forward']])
        week_df = week_df[idx].reset_index(drop=True)

        week_df = week_df.groupby('uid', as_index=False)\
            .agg({'real_spent': 'mean', 'coverage': 'mean', 'watched': 'mean', 'pauses': 'mean',
                                        'pause_length': 'mean', 'avg_speed': 'mean', 'std_speed': 'mean',
                                        'seek_backward': 'mean', 'seek_forward': 'mean', 'attempts': 'max', 'grade': 'max'})\
            .reset_index(drop=True)
        # week_df = drop_all_0_row(week_df)

        X = week_df[['real_spent', 'coverage', 'watched', 'pauses', 'pause_length', 'avg_speed', 'std_speed', 'seek_backward', 'seek_forward']].values
        scaler = MinMaxScaler()
        X = scaler.fit_transform(X)
        # X = X[idx].values
        # week_df = week_df[idx].reset_index()
        Y = week_df['grade'].values
        regression(X, Y, RandomForestRegressor())
