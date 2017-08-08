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
from sklearn.metrics import mean_squared_error, zero_one_loss
from sklearn.preprocessing import StandardScaler
import logging

FORMAT = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)


def load_data():
    logger.info('loading npz data')
    data = np.load('weekly_quantities_data.npz')
    X = data['features']
    column_names = data['columns']
    return X, column_names


def draw_correlation_figure(X, columns):
    df = pd.DataFrame(data=X, columns=columns)
    correlations = df.corr()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlations, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, feature_length, 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(columns)
    ax.set_yticklabels(columns)
    savefig('./correlation.png', bbox_inches='tight')


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
    X, columns = load_data()
    feature_length = len(columns)
    draw_correlation_figure(X, columns)
    indices = np.where(X[:, 0] == 5)[0]  # only keep week 1 data
    Y = X[indices, :][:, len(columns)-3]  # grade (last column)
    X = X[indices, :][:, range(1, len(columns)-4)]  # except module_number (first column) and grade (last column)
    regression(X, Y, RandomForestRegressor())
