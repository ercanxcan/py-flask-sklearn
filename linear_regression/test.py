import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

train_data = np.matrix([[80.583220,124.907414],[82.583220,134.907414],[73.922466,134.085180],[61.839983,114.530638]])
x, y = train_data[:,0], train_data[:,1]
linear_reg = LinearRegression().fit(x,y)
m = linear_reg.coef_[0]
b = linear_reg.intercept_
print "formula: y = {0}x + {1}".format(m, b)

plt.scatter(x,y, color='blue')
plt.plot([0,100],[b,m*100+b],'r')
plt.title('Linear Regression', fontsize = 20)
plt.xlabel('x', fontsize = 15)
plt.ylabel('y', fontsize = 15)
plt.show()