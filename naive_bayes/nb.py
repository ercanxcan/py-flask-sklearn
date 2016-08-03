__author__ = 'ercanc'

import numpy as np
import urllib
from sklearn import preprocessing
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB

def get_nb(x1,x2,x3,x4,x5,x6,x7,x8):
    # url dataset
    url = "http://localhost:8080/dashboard/data/pima-indians-diabetes.data"
    # get dataset from url and download
    raw_data = urllib.urlopen(url)
    # load the csv file as a numpy matrix
    dataset = np.loadtxt(raw_data, delimiter=",")

    # separate the data from the target attributes
    X = dataset[:, 0:8]
    y = dataset[:, 8]

    # normalize the data attributes
    normalized_X = preprocessing.normalize(X)
    # standardize the data attributes
    standardized_X = preprocessing.scale(X)

    model = GaussianNB()
    model.fit(X, y)
    # make predictions
    expected = y
    # print X
    input = np.matrix([[x1,x2,x3,x4,x5,x6,x7,x8]])
    predicted = model.predict(input)
    return predicted


# input =  np.matrix([[x1,x2,x3,x4,x5,x6,x7,x8]])
# print get_nb(6. ,148.   ,   72.   ,   35.   ,    0.    ,  33.6    ,  0.627  , 50.)
