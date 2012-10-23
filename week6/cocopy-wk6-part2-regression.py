#!/usr/bin/env python
""" Cocosci scientific Python course, Week 6: Part 2 - Regression with
sklearn"""

import numpy as np
from sklearn import datasets
from sklearn import cross_validation
from sklearn import neighbors
from sklearn import linear_model
from sklearn import svm
from sklearn import gaussian_process

RSO = np.random.RandomState(0)

def f(x):
    return 0.2*x**3 - 0.05*x**2 + 3

X = np.linspace(-10, 10, 10)[:, None]
tY = f(X)[:, 0]
Y = tY + RSO.normal(0, 20, size=tY.shape)
plt.clf()
plt.plot(X, tY)
plt.plot(X, Y, 'bo')

def regression(data, target, regr, label):
    regr.fit(data.copy(), target.copy())
    pred = regr.predict(data.copy())
    mse = np.mean((pred - tY)**2)
    print "%s MSE: %s" % (label, mse)
    plt.plot(data, pred, label=label)

## Linear regression
regr = linear_model.LinearRegression()
regression(X, Y, regr, "Linear")

## Ridge regression -- this "shrinks" the coefficients of the
## regression towards zero.  The classifier takes an 'alpha' parameter
## -- higher values of alpha mean higher bias towards zero, but less
## variance.  How do we pick an optimal alpha?  Luckily, scikit-learn
## has the answer again: RidgeRegressionCV uses cross-validation to
## automatically pick an alpha parameter.
regr = linear_model.RidgeCV()
regression(X, Y, regr, "RidgeCV")

## Lasso regression (sparsity) -- this forces small coefficients to be
## zero, enforcing sparsity
regr = linear_model.LassoCV()
regression(X, Y, regr, "LassoCV")


# Of course, neither of those helped because our data is polynomial,
# not linear.  Obviously, the polynomial kernel is best:
regr = svm.SVR(kernel='poly')
regression(X, Y, regr, "SVM poly")
regr = svm.SVR(kernel='sigmoid')
regression(X, Y, regr, "SVM sigmoid")
regr = svm.SVR(kernel='rbf')
regression(X, Y, regr, "SVM rbf")

# Gaussian processes do the best:
regr = gaussian_process.GaussianProcess()
regression(X, Y, regr, "Gaussian Process")

plt.legend()
