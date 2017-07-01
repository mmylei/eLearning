import os
import numpy as np
from sklearn.model_selection import ShuffleSplit, StratifiedShuffleSplit
from sklearn.feature_selection import RFECV, VarianceThreshold
from sklearn.decomposition import PCA, KernelPCA
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier, Lasso
from sklearn import tree
from sklearn import svm
from sklearn.metrics import mean_squared_error, zero_one_loss
from sklearn.preprocessing import StandardScaler
import logging
import json_wrapper

FORMAT = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)


def grades_to_labels(grades):
    good_normal = np.percentile(grades, 75)
    normal_poor = np.percentile(grades, 25)
    return np.array(map(lambda x: 1 if x >= good_normal else (-1 if x < normal_poor else 0), grades), dtype=np.intp)


def load_data():
    if 'data.npz' in os.listdir('.'):
        logger.info('loading saved features')
        return np.load('data.npz')
    else:
        result = {}
        logger.info('loading json')
        f = open('data.json', 'r')
        data = json_wrapper.loads(f.read())
        f.close()
        logger.info('json loaded')
        X = np.array(data['features'], np.float16)
        Y = grades_to_labels(np.array(data['grades'], np.float16))
        logger.info('feature selection')
        X = feature_selection(X, Y)
        logger.info('writing npz data')
        result['X'] = X
        result['Y'] = Y
        np.savez('data', **result)
        return result


def feature_selection(X, Y):
    # return SelectKBest(mutual_info_classif, 50).fit_transform(X, Y)
    # return PCA(n_components=50).fit_transform(X)
    # return KernelPCA(n_components=50, kernel='rbf').fit_transform(X)
    X = VarianceThreshold(threshold=(.9 * (1 - .9))).fit_transform(X)
    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)
    return RFECV(svm.SVR(kernel="linear"), cv=5, step=0.05).fit_transform(X)


def split_train_test(data):
    train_index = np.array([], dtype=np.int32)
    test_index = np.array([], dtype=np.int32)
    for label in [-1, 0, 1]:
        indices = np.where(data['Y_' + str(label)] == 1)[0]
        # print indices
        for train_part, test_part in ShuffleSplit(n_splits=1, test_size=0.2, train_size=0.8).split(indices):
            # print train_part
            # print test_part
            # print indices[train_part]
            train_index = np.concatenate((train_index, indices[train_part]))
            test_index = np.concatenate((test_index, indices[test_part]))
    return train_index, test_index


def train(X, Y, model=SGDClassifier(penalty='l1', alpha=0.01)):
    test_error = 0
    train_error = 0
    for train_index, test_index in StratifiedShuffleSplit(n_splits=5, test_size=0.2).split(X, Y):
        # logger.info('train index: ' + str(train_index))
        # logger.info('test index: ' + str(test_index))
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        # model = tree.DecisionTreeClassifier()
        model.fit(X_train, Y_train)
        Y_predict = model.predict(X_test)
        error = zero_one_loss(Y_test, Y_predict)
        test_error += error
        Y_predict = model.predict(X_train)
        error = zero_one_loss(Y_train, Y_predict)
        train_error += error
    real_test_error = test_error / 5
    real_train_error = train_error / 5

    logger.info('train_error: ' + str(real_train_error))
    logger.info('test_error: ' + str(real_test_error))
    return model


if __name__ == '__main__':
    data = load_data()
    # train_index, test_index = split_train_test(data)
    # combined_Y = data['Y_1'] - data['Y_-1']
    # models = []
    # for label in [-1, 0, 1]:
    #     logger.info('train for label ' + str(label))
        # print train_index
        # print data['Y_' + str(label)]
        # Y_one = data['Y_' + str(label)][train_index]
        # X_one = data['X_' + str(label)][train_index]
    logger.info('cross validation')
    train(data['X'], data['Y'], OneVsRestClassifier(svm.SVC(kernel='linear')))

    # logger.info('test combined classifier')
    # Y_predict = []
    # for label in [-1, 0, 1]:
    #     Y_predict.append(models[label + 1].predict(data['X_' + str(label)]))
    # correct = [0.0, 0.0, 0.0]
    # combined_predict = []
    # total_correct = 0.0
    # total = len(Y_predict[0])
    # for i in range(len(Y_predict[0])):
    #     final_label = -1
    #     if Y_predict[1][i] > Y_predict[0][i]:
    #         final_label = 0
    #     if Y_predict[2][i] > Y_predict[final_label + 1][i]:
    #         final_label = 1
    #     if data['Y_' + str(final_label)][i] == 1:
    #         total_correct += 1.0
    #         correct[final_label + 1] += 1.0
    #     combined_predict.append(final_label)
    # combined_predict = np.array(combined_predict)
    # logger.info("total train error: " + str(zero_one_loss(combined_Y[train_index], combined_predict[train_index])))
    # logger.info("total test error: " + str(zero_one_loss(combined_Y[test_index], combined_predict[test_index])))
    # logger.info("-1 output sum: " + str(combined_predict[0]))
    # logger.info("0 output sum: " + str(combined_predict[1]))
    # logger.info("1 output sum: " + str(combined_predict[2]))
    # logger.info("-1 precision: " + str(correct[0]) + ' / ' + str(combined_predict[0]))
    # logger.info("-1 recall: " + str(correct[0]) + ' / ' + str(sum(data['Y_-1'])))
    # logger.info("0 precision: " + str(correct[1]) + ' / ' + str(combined_predict[1]))
    # logger.info("0 recall: " + str(correct[1]) + ' / ' + str(sum(data['Y_0'])))
    # logger.info("1 precision: " + str(correct[2]) + ' / ' + str(combined_predict[2]))
    # logger.info("1 recall: " + str(correct[2]) + ' / ' + str(sum(data['Y_1'])))
    # logger.info("final precision: " + str(total_correct / total))
    # logger.info("final recall: " + str(total_correct / total))
