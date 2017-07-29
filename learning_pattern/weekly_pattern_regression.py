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
from sklearn.ensemble import RandomForestClassifier
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

if __name__ == '__main__':
    X, columns = load_data()
    feature_length = len(columns)
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
