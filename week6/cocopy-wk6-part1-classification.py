#!/usr/bin/env python
""" Cocosci scientific Python course, Week 6: Part 1 - Classification
with sklearn"""

import numpy as np
from sklearn import datasets
from sklearn import cross_validation
from sklearn import neighbors
from sklearn import linear_model
from sklearn import svm
from sklearn import mixture

# random number generator
RSO = np.random.RandomState(0)

# Load the digits data set
digits = datasets.load_digits()

# First, let's take a look at our data to get a sense of what we're
# working with:
#
# Add a buffer around images to make them easier to see
nimg = digits.images.shape[0]
images = np.concatenate([
    np.zeros((nimg, 12, 2)),
    np.concatenate([
        np.zeros((nimg, 2, 8)),
        digits.images,
        np.zeros((nimg, 2, 8))], axis=-2),
    np.zeros((nimg, 12, 2))], axis=-1)
# Use plt.imshow to view the data set
n = int(np.sqrt(nimg))
img = images[:n**2].reshape(
    (n, n, 12, 12)
    ).transpose((0, 2, 1, 3)
                ).reshape((n*12, n*12))
plt.imshow(img, interpolation='nearest', cmap='gray')
plt.xticks([], [])
plt.yticks([], [])

## sklearn provides many supervised as well as unsupervised
## classification algorithms (including GMM and DPGMM!).  I'm just
## going to focus on supervised learning -- the unsupervised
## algorithms are analogous in syntax.

# To be sure we aren't overfitting when we try a regression or
# classification, we need to split the data set up into testing and
# training sets.  scikit-learn makes this really easy with KFold,
# which produces testing and training indices for your data.

def FoldCV(data, target, classifier, k=3):
    """Make indices for testing and training.  n is the number of
    total data points, and k is the number of folds.  Each fold is
    used once as testing while the other folds are training.

    """
    RSO.seed(0)
    kf = cross_validation.KFold(
        n=data.shape[0], k=3,
        indices=True,
        random_state=RSO,
        shuffle=True)
    scores = []
    for idx, (train_idx, test_idx) in enumerate(kf):
        # Extract training and testing data
        X_train = data[train_idx]
        y_train = target[train_idx]
        X_test = data[test_idx]
        y_test = target[test_idx]
        # Fit the classifier
        classifier.fit(X_train.copy(), y_train.copy())
        # Score predictions
        score = classifier.score(X_test.copy(), y_test.copy())
        print "Fold %d score: %s" % (idx, score)
        scores.append(score)
    mean = np.mean(scores)
    std = np.std(scores, ddof=1)
    print "Mean scores: %.4f +/- %.4f" % (mean, std)
    print

def classify(data, target, classifier, n=20):
    """Helper function to fit, predict, and score some subset (n) of
    the data.

    """
    print "-"*70
    print classifier
    print
    # Reseed the random state
    RSO.seed(0)
    # Generate indices and training/testing sets
    idx = RSO.permutation(data.shape[0])
    X_train = data[idx[:-n]]
    y_train = target[idx[:-n]]
    X_test = data[idx[-n:]]
    y_test = target[idx[-n:]]
    # Fit the classifier
    classifier.fit(X_train.copy(), y_train.copy())
    # Generate predictions
    pred = classifier.predict(X_test.copy())
    # Score predictions
    score = classifier.score(X_test.copy(), y_test.copy())
    print "Score: %s" % score
    return pred, idx[-n:], score

def examine_results(y_pred, y_target, images, plot=True):
    """Helper function to determine which images were incorrectly
    classified.  It optionally plots the images which were incorrect.

    """
    # Determine the indices of the wrong answers
    wrong = np.nonzero(y_pred != y_target)
    # Get the image data
    imgs = images[wrong]
    for widx in wrong[0]:
        img = images[widx]
        # Plot the image
        if plot:
            plt.figure()
            plt.imshow(img, interpolation='nearest', cmap='gray')
        # Print what it was classified as and what it is labeled as
        print "Classified as %d, truth is %d" % (
            y_pred[widx], y_target[widx])
    print

## Logistic regression
logistic = linear_model.LogisticRegression(C=1e4)
y_pred, idx, score = classify(digits.data, digits.target, logistic)
examine_results(y_pred, digits.target[idx], digits.images[idx])
FoldCV(digits.data, digits.target, logistic)

## k-Nearest Neighbors Classifier
knn = neighbors.KNeighborsClassifier(algorithm='kd_tree')
y_pred, idx, score = classify(digits.data, digits.target, knn)
examine_results(y_pred, digits.target[idx], digits.images[idx])
FoldCV(digits.data, digits.target, knn)

## Support vector machines
svc = svm.SVC(kernel='linear')
y_pred, idx, score = classify(digits.data, digits.target, svc)
examine_results(y_pred, digits.target[idx], digits.images[idx], plot=False)
FoldCV(digits.data, digits.target, svc)

svc = svm.SVC(kernel='poly', degree=3)
y_pred, idx, score = classify(digits.data, digits.target, svc)
examine_results(y_pred, digits.target[idx], digits.images[idx], plot=False)
FoldCV(digits.data, digits.target, svc)

svc = svm.SVC(kernel='rbf', gamma=0.001)
y_pred, idx, score = classify(digits.data, digits.target, svc)
examine_results(y_pred, digits.target[idx], digits.images[idx], plot=False)
FoldCV(digits.data, digits.target, svc)

