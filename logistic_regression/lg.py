import numpy as np
from sklearn import linear_model, preprocessing

def get_lg(x1,x2,x3,x4,x5):
    # train_data = np.random.randn(3,5)
    train_data = np.matrix([[-0.76868572,  3.16466081,  1.30319059,  0.45436659,  0.61572467],
                            [-0.29511482, -0.00899264,  0.72071203, -0.03181753, -0.82713265],
                            [-0.35625049,  1.11800786,  0.46191793,  0.75260939, -0.64071133]])
    y = [2,1,1]
    lr = linear_model.LogisticRegression()
    lr.fit(train_data,y)
    input =  np.matrix([[x1,x2,x3,x4,x5]])

    return lr.predict_proba(input)

# print np.array_str(get_lg(-0.76868572,  3.16466081,  1.30319059,  0.45436659,  0.61572467))