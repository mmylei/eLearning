import numpy as np
from sklearn.model_selection import ShuffleSplit
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.linear_model import SGDClassifier
from sklearn import tree
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import logging
import json_wrapper

FORMAT = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)


def feature_selection(X, Y):
    return SelectKBest(mutual_info_classif, 20).fit_transform(X, Y)


def train(X, Y, model=SGDClassifier(penalty='l1', alpha=0.01)):
    test_error = 0
    train_error = 0
    for train_index, test_index in ShuffleSplit(n_splits=5, test_size=0.2, train_size=0.8).split(X):
        logger.info('train index: ' + str(train_index))
        logger.info('test index: ' + str(test_index))
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        # model = tree.DecisionTreeClassifier()
        model.fit(X_train, Y_train)
        Y_predict = model.predict(X_test)
        error = mean_squared_error(Y_test, Y_predict)
        test_error += error
        Y_predict = model.predict(X_train)
        error = mean_squared_error(Y_train, Y_predict)
        train_error += error
    real_test_error = test_error / 5
    real_train_error = train_error / 5

    logger.info('train_error: ' + str(real_train_error))
    logger.info('test_error: ' + str(real_test_error))
    return model

if __name__ == '__main__':
    logger.info('reading file')
    f = open('data.json', 'r')
    data = json_wrapper.loads(f.read())
    f.close()
    X = np.array(data['features'], np.intp)
    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)
    Y = np.array(data['labels'], np.intp)
    # X = np.array([range(0, 40), range(1, 41), range(2, 42), range(3, 43), range(4, 44)])
    # Y = np.array([0, 1, 2, 3, 4])
    models = []
    for label in [-1, 0, 1]:
        logger.info('train for label ' + str(label))
        Y_one = np.array(map(lambda x: 1 if x == label else 0, Y))
        logger.info('feature selection')
        X_one = feature_selection(X, Y_one)
        logger.info('training')
        models.append(train(X_one, Y_one))
