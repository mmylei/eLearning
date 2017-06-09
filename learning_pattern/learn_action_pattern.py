import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import mean_squared_error
import json_wrapper

f = open('data.json', 'r')
data = json_wrapper.loads(f.read())
f.close()

features = np.array(data['features'], np.intp)
labels = np.array(data['labels'], np.intp)
train_x = features[data['train_index'], :]
train_y = labels[data['train_index']]
test_x = features[data['test_index'], :]
test_y = labels[data['test_index']]

model = SGDClassifier()
model.fit(train_x, train_y)
predict_y = model.predict(test_x)
error = mean_squared_error(test_y, predict_y)
print 'error=', error
