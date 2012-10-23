#!/usr/bin/env python
""" Cocosci scientific Python course, Week 3: Part 2 - Scipy"""

### Scipy
# 
# Scipy is a companion library to numpy that requires a Fortran
# compiler to be built. It has many more functions than numpy, as well
# as some identical functions that are optimized for speed. The way I
# think about the distinction between numpy and scipy is that numpy
# provides an efficient implementation of arrays and some basic means
# to operate on them, and scipy provides a suite of scientific tools
# that can exploit arrays.

import matplotlib.pyplot as plt
import numpy as np
## By convention, the scipy module is referenced by 'sp'
import scipy as sp

# Quick note about sub-module importing: in Python, sub-modules are
# not automatically imported, so you usually need to manually import
# them. However, the rules for defining modules includes a special
# technique for automatically importing sub-modules, so sometimes it
# will appear as if a sub-module was automatically imported because
# the developer made it that way. For instance, scipy doesn't
# automatically import its 'linalg' sub-module, but 'numpy' does:

print "Did 'numpy' import the 'linalg' sub-module?", hasattr(np, "linalg")
#
print "Did 'scipy' import the 'linalg' sub-module?", hasattr(sp, "linalg")
import scipy.linalg as linalg
print "How about now?", hasattr(sp, "linalg")
# Let's call it 'la' for short (or, we could have done):
# import scipy.linalg as la
la = linalg

## scipy.linalg - linear algebra functions
#
# There is some overlap between numpy's and scipy's linalg functions,
# but scipy's is more extensive and should be faster in many cases
# because it is compiled against highly optimized C and Fortran
# libraries.

# Let's make a few example arrays and do some linear algebra

seed = 4
RSO = np.random.RandomState(seed)

# Size of the arrays, 3x3 and 3x2 will be good for now
m, n = 3, 2
# I3 is the 3x3 identity matrix, I2 is the 2x2 identity matrix
I3 = np.eye(m)
I2 = np.eye(n)
# A is a square matrix with random, normally distributed elements
A = RSO.randn(m, m)
# Make a symmetric matrix by taking the dot product of A with its
# transpose
B = np.dot(A.T, A)
# C is a diagonal matrix made with diagonal elements in 'c'
c = RSO.randn(m)
C = np.diag(c)
# (np.diag can also be used to extract an array's diagonal)
print "Is the diagonal of C equal to c?", np.all(c == np.diag(C))
# D is a lower triangular version of A (0's in upper right half)
D = la.tril(A) # optional argument 'k' lets you specify the k-th diagonal

## Basic linear algebra functions
# E is the inverse of A
E = la.inv(A)
# verify that E is the inverse by checking whether the dot product of
# E and A equals the identity matrix (use 'np.allclose' instead of
# 'np.all' because of the imprecision of floating point values)
print "Is E the inverse of A?", np.allclose(np.dot(E, A), I3)
# Matrix inverse is not defined for non-square matrices, so use the
# pseudo-inverse:
# X is a non-square matrix
X = RSO.randn(m, n)
# There are two pseudo-inverse calculation functions:
# scipy.linalg.pinv uses least-squares
Y1 = la.pinv(X)
# scipy.linalg.pinv2 uses singular value decomposition (SVD)
Y2 = la.pinv2(X)
print "Is Y1 the pseudo-inverse of X?", np.allclose(np.dot(Y1, X), I2)
print "Is Y2 the pseudo-inverse of X?", np.allclose(np.dot(Y2, X), I2)
# pinv/pinv2 can generally be used instead of inv
E1 = la.pinv(A)
# scipy.linalg.pinv2 uses singular value decomposition (SVD)
E2 = la.pinv2(A)
print "Is E1 the pseudo-inverse of A?", np.allclose(np.dot(E1, A), I3)
print "Is E2 the pseudo-inverse of A?", np.allclose(np.dot(E2, A), I3)

# Compute the determinant
print "The determinants of A and B are:", la.det(A), la.det(B)

# Matrix decompositions
#
# scipy.linalg has many standard matrix decomposition techniques. Most
# take optional arguments that control the output (e.g. right v. left
# eigenvectors).
# Eigen-decomposition
eval, evec_right = la.eig(A)
# Singular value decomposition (SVD)
u, s, v = la.svd(A)
# Cholesky decomposition (requires a positive definite matrix -- i.e. B)
c = la.cholesky(B)

## Least-squares and linear systems
# scipy can solve least squares problems in matrix form:
# x values
x = np.linspace(-1, 1, 15)
# y values
y = y = x ** 3. + 4.
# noisy data
z = y + RSO.randn(y.size) * 0.3
# Plot truth and data
plt.figure(1)
plt.clf()
plt.plot(x, y, "k--", x, z, "ro", linewidth=2)
plt.xlabel("x-values")
plt.ylabel("y-values")
plt.legend(("true function", "noisy data"), loc="upper left")

# Fit a line to the data using least squares
M = np.hstack((np.ones((x.size, 1)), x[:, None]))
coef, residuals, rank, sv = la.lstsq(M, z)
# compute the fitted lien
y_fit = np.dot(M, coef)

# Plot it
plt.plot(x, y_fit, "g-", linewidth=2)
plt.legend(("true function", "noisy data", "linear fit"), loc="upper left")



## scipy.stats
import scipy.stats as stats

# scipy.stats has many distributions, from which you can draw random
# samples, compute PDFs, CDFs, etc, and fit parameters.
# It also has a variety of data analysis/statistics functions

# Each distribution can be accessed via:
print stats.norm
print stats.gamma

# Make some x-values
n = 100
mu = 1.5
sigma = 2.
x = np.linspace(-10, 10, n)
# Compute the PDF
y = stats.norm.pdf(x, mu, sigma)
# Plot it
plt.figure(10)
plt.clf()
plt.plot(x, y, "r")
# Compute the CDF
z = stats.norm.cdf(x, mu, sigma)
# Plot it
plt.plot(x, z, "k")
# Generate some random variables
r = stats.norm.rvs(mu, sigma, size=100)
# Plot them all (and increase y and z to match size of r)
plt.figure(10)
plt.clf()
plt.hist(r)
plt.plot(x, y * 100, "r", linewidth=3)
plt.plot(x, z * 20, "b", linewidth=3)

# You can also "freeze" distribution objects with the parameters you like:
norm1 = stats.norm(mu, sigma)
norm2 = stats.norm(mu - 4., sigma * 0.7)
# Plot
plt.figure(11)
plt.clf()
plt.plot(x, norm1.pdf(x), "r", linewidth=3)
plt.plot(x, norm2.pdf(x), "k", linewidth=3)

# There are many more distributions, just type 'stats?' in your
# IPython prompt

# scipy.stats also contains basic statistical functions

# Create some sample data from normal dists
norm3 = stats.norm(mu - 1., 4)
N = 20
r1 = norm1.rvs(size=N)
r2 = norm2.rvs(size=N)
r3 = norm3.rvs(size=N)
plt.figure(12)
plt.clf()
plt.hist(np.vstack((r1, r2, r3)).T)
plt.plot(x, norm1.pdf(x) * N, "b", linewidth=3)
plt.plot(x, norm2.pdf(x) * N, "g", linewidth=3)
plt.plot(x, norm3.pdf(x) * N, "r", linewidth=3)

# t-tests
t12, p12 = stats.ttest_ind(r1, r2)
t13, p13 = stats.ttest_ind(r1, r3)
t23, p23 = stats.ttest_ind(r2, r3)
print "sample 1 v 2 T- and p-values", t12, p12
print "sample 1 v 3 T- and p-values", t13, p13
print "sample 2 v 3 T- and p-values", t23, p23
# ANOVA
f123, p123 = stats.f_oneway(r1, r2, r3)
print "sample 1 v 2 v 3 T- and p-values", f123, p123




## scipy.ndimage
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage as ndim

# Load the image from disk
img = mpimg.imread("tree.jpg")

# Filter it
# make a blur kernel
x = np.arange(-16, 17)
sigma = 4.
k = stats.norm.pdf(x, 0, sigma)
kernel = np.dot(k[:, None], k[None, :])
kernel /= kernel.sum()
# Convolve it with the image
img_lo = ndim.convolve(img, np.expand_dims(kernel, axis=2))
plt.subplot(2, 3, 2)
plt.imshow(img_lo[::-1])
# That convolution was slow because it did not exploit the
# separability of the filter.
#
# However, scipy.ndimage contains many packaged filtering operations
# that are efficient.
#
# high-pass, laplace filter
img_hi = ndim.laplace(img)

# grayscale versions of the images
img_gray = np.mean(img, axis=2)
img_gray_lo = ndim.convolve(img_gray, kernel)
img_gray_hi = ndim.laplace(img_gray)

def plot_image(ax, img, title="", gray=False):
    if gray:
        ax.imshow(img[::-1], cmap='gray')
    else:
        ax.imshow(img[::-1])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    plt.draw()

def plot_contour(ax, img, title=""):
    mean = np.mean(img, axis=-1)
    x, y = np.meshgrid(
        np.arange(mean.shape[1]),
        np.arange(mean.shape[0]))
    ax.plot_surface(x, y, mean, rstride=10, cstride=10,
                    linewidth=0, cmap='jet')
    ax.set_zlim3d(0, 255)
    # for tl in ax.get_xticklabels() + ax.get_yticklabels():
    #     tl.set_visible(False)
    ax.set_title(title)
    plt.draw()

def plot_histogram(ax, img, title=""):
    kwargs = {
        'histtype': 'stepfilled',
        'bins': 256,
        'range': (0, 256),
        'normed': True,
        'alpha': 0.5,
        }
    ax.hist(np.mean(img, axis=-1).ravel(), color='gray', **kwargs)
    ax.hist(img[..., 0].ravel(), color='r', **kwargs)
    ax.hist(img[..., 1].ravel(), color='g', **kwargs)
    ax.hist(img[..., 2].ravel(), color='b', **kwargs)
    ax.set_title(title)
    ax.set_xlim(0, 255)
    ax.set_xticks([])
    plt.draw()
    
# 3x3 subplots
plt.close('all')
fig1 = plt.figure(1, figsize=(12, 8))
fig1.clf()
ax1 = fig1.add_subplot(3, 3, 1)
ax2 = fig1.add_subplot(3, 3, 2)
ax3 = fig1.add_subplot(3, 3, 3)
ax4 = fig1.add_subplot(3, 3, 4)
ax5 = fig1.add_subplot(3, 3, 5)
ax6 = fig1.add_subplot(3, 3, 6)
ax7 = fig1.add_subplot(3, 3, 7, projection='3d')
ax8 = fig1.add_subplot(3, 3, 8, projection='3d')
ax9 = fig1.add_subplot(3, 3, 9, projection='3d')

# 1. raw image
plot_image(ax1, img, "Original")
# 2. low pass filtered image
plot_image(ax2, img_lo, "Low Pass")
# 3. high pass filtered image
plot_image(ax3, img_hi, "High Pass")
# 4-6. grayscale, low, high
plot_image(ax4, img_gray, "Grayscale", gray=True)
plot_image(ax5, img_gray_lo, "Low Pass Grayscale", gray=True)
plot_image(ax6, img_gray_hi, "High Pass Grayscale", gray=True)
# 7-9. contour plot of each image
plot_contour(ax7, img, "Original")
plot_contour(ax8, img_lo, "Low Pass")
plot_contour(ax9, img_hi, "High Pass")

fig1.suptitle("Image Filters", fontsize=20)
plt.draw()

# hist of each color channel, plus gray (mean), for each img
fig2 = plt.figure(2, figsize=(12, 8))
fig2.clf()
ax1 = fig2.add_subplot(1, 3, 1)
ax2 = fig2.add_subplot(1, 3, 2)
ax3 = fig2.add_subplot(1, 3, 3)

plot_histogram(ax1, img, "Original")
plot_histogram(ax2, img_lo, "Low Pass")
plot_histogram(ax3, img_hi, "High Pass")

ax1.set_ylim(0, .12)
ax2.set_ylim(0, .12)
ax2.set_yticks([])
ax3.set_ylim(0, .12)
ax3.set_yticks([])
fig2.suptitle("Image Histograms", fontsize=20)
plt.draw()





## scipy.special
#
# Contains a number of fancy functions like:
# gamma, bessel, hypergeometric, and many others
