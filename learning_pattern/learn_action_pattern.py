import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import SGDClassifier
from sklearn import tree
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

import json_wrapper

f = open('data.json', 'r')
data = json_wrapper.loads(f.read())
f.close()
test_error = 0
train_error = 0
X = np.array(data['features'], np.intp)
Y = np.array(data['labels'], np.intp)
for train_index, test_index in KFold(n_splits=5).split(X):
    X_train, X_test = X[train_index], X[test_index]
    Y_train, Y_test = Y[train_index], Y[test_index]
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
# train_x = features[data['train_index'], :]
# train_y = labels[data['train_index']]
# test_x = features[data['test_index'], :]
# test_y = labels[data['test_index']]

    model = SGDClassifier(penalty='l1', l1_ratio=0.5)
    #model = tree.DecisionTreeClassifier()
    model.fit(X_train, Y_train)
    Y_predict = model.predict(X_test)
    error = mean_squared_error(Y_test, Y_predict)
    test_error += error
    Y_predict = model.predict(X_train)
    error = mean_squared_error(Y_train, Y_predict)
    train_error += error
real_test_error = test_error/5
real_train_error = train_error/5

print 'train_error=', real_train_error
print 'test_error=', real_test_error

