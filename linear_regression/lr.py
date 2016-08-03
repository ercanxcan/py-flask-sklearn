import numpy as np
from sklearn.linear_model import LinearRegression

def get_lr(x_):
    train_data = np.matrix([[82.583220,134.907414],[73.922466,134.085180],[61.839983,114.530638]])
    x, y = train_data[:,0], train_data[:,1]
    linear_reg = LinearRegression().fit(x,y)
    m = linear_reg.coef_[0]
    b = linear_reg.intercept_

    predict = m*x_+b

    return predict