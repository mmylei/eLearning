import numpy as np
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.linear_model import SGDClassifier
from sklearn import tree
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

import json_wrapper


def feature_selection(X, Y):
    return SelectKBest(mutual_info_classif, 20).fit_transform(X, Y)


def train(X, Y, model=SGDClassifier(penalty='l1', alpha=0.1)):
    test_error = 0
    train_error = 0
    for train_index, test_index in KFold(n_splits=5).split(X):
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

    print 'train_error:', real_train_error
    print 'test_error:', real_test_error
    return model

if __name__ == '__main__':
    f = open('data.json', 'r')
    data = json_wrapper.loads(f.read())
    f.close()
    X = np.array(data['features'], np.intp)
    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)
    Y = np.array(data['labels'], np.intp)
    models = []
    for label in [-1, 0, 1]:
        print 'train for label', label
        Y_one = map(lambda x: 1 if x == label else 0, Y)
        X_one = feature_selection(X, Y_one)
        models.append(train(X_one, Y_one))
