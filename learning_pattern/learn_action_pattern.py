import os
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


def load_data():
    if 'data.npz' in os.listdir('.'):
        logger.info('loading saved features')
        return np.load('data.npz')
    else:
        result = {}
        logger.info('building from original json')
        f = open('data.json', 'r')
        data = json_wrapper.loads(f.read())
        f.close()
        X = np.array(data['features'], np.intp)
        scaler = StandardScaler().fit(X)
        X = scaler.transform(X)
        Y = np.array(data['labels'], np.intp)
        for label in [-1, 0, 1]:
            Y_one = np.array(map(lambda x: 1 if x == label else 0, Y))
            logger.info('feature selection')
            X_one = feature_selection(X, Y_one)
            result['X_' + str(label)] = X_one
            result['Y_' + str(label)] = Y_one
        np.savez('data', **result)
        return result


def feature_selection(X, Y):
    return SelectKBest(mutual_info_classif, 20).fit_transform(X, Y)


def train(X, Y, model=SGDClassifier(penalty='l1', alpha=0.01)):
    test_error = 0
    train_error = 0
    for train_index, test_index in ShuffleSplit(n_splits=5, test_size=0.1, train_size=0.9).split(X):
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
    data = load_data()
    models = []
    for label in [-1, 0, 1]:
        logger.info('train for label ' + str(label))
        Y_one = data['Y_' + str(label)]
        X_one = data['X_' + str(label)]
        logger.info('training')
        models.append(train(X_one, Y_one))

    logger.info('test combined classifier')
    Y_predict = []
    correct = [0.0, 0.0, 0.0]
    total_correct = 0.0
    total = len(Y_predict[0])
    for label in [-1, 0, 1]:
        Y_predict[label + 1] = models[label + 1].predict(data['X_' + str(label)])
    for i in range(len(Y_predict[0])):
        final_label = 0
        if Y_predict[1][i] > Y_predict[0][i]:
            final_label = 1
        if Y_predict[2][i] > Y_predict[final_label][i]:
            final_label = 2
        if data['Y_' + str(final_label - 1)][i] == 1:
            total_correct += 1.0
            correct[final_label] += 1.0
    logger.info("final precision: " + str(total_correct / total))
    logger.info("-1 precision: " + str(correct[0] / sum(data['Y_-1'])))
    logger.info("0 precision: " + str(correct[1] / sum(data['Y_0'])))
    logger.info("1 precision: " + str(correct[2] / sum(data['Y_1'])))
