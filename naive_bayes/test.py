__author__ = 'ercanc'

import numpy as np
import urllib
from sklearn import preprocessing
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB

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
print(model)
# make predictions
expected = y
predicted = model.predict(X)
# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))

# model.fit(X, y)
# print(model)
# # make predictions
# expected = y
# print X[0]
# predicted = model.predict(X[0])
# print y
# print "*" * 40
# print predicted
