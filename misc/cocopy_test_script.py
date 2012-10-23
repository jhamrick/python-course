#!/usr/bin/env python

""" Test script to make sure you have Python and Numpy/Scipy properly
installed."""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import scipy as sp
import scipy.stats as stats

# RandomState object ('RSO') that provides a stream of pseudo-random
# numbers, seeded with 1.
seed = 1
RSO = np.random.RandomState(seed=seed)
# Dimensions of array
m, n = 20, 20
# x,y coordinates
x, y = np.arange(m), np.arange(n)
# Make 2D arrays over the x,y coordinates (which can be used for plotting 3D)
X, Y = np.meshgrid(x, y)
# Generate array of normally distributed random numbers using the
# random stream, 'RSO', instantiated above.
A = RSO.randn(m, n)
# Compute the log-probability of each element
L = stats.norm.logpdf(A)
# Compute the sum of the log-probabilities across axis=1
lp1 = np.sum(L, axis=1)
# Find the index of the maximum value of lp1 (along axis=1)
max_idx = np.argmax(lp1)
# Get the value of that max
max_lp1 = lp1[max_idx]
# Get its x-coordinate
max_x = x[max_idx]

## Save the data to disk
# Create the filename of where the data will be saved
data_filename = "test_script_data.npy"
# Save the A array
np.save(data_filename, A)
# Try loading it back as a new variable, A2
A2 = np.load(data_filename)
# Perform an element-wise test on A and A2, checking whether the
# corresponding elements of A and A2 are equal or not, and create a
# boolean indicator array with the results.
equal_ind = A == A2
# Check whether all boolean indicators are True, which will mean that
# the test was passed. Store as a boolean flag variable (True/False).
f_all_equal = np.all(equal_ind)
# Handle different outcomes of the f_all_equal test:
if f_all_equal:
    # If the test passed (f_all_equal == True), then print an "OK"
    # message to the user.
    print "Array A was saved and loaded OK."
else:
    # If the test failed (f_all_equal == False), then count the number
    # of elements that were not equal ('~' means 'not' in numpy) and
    # store them in 'n_mismatches'.
    n_mismatches = np.sum(~equal_ind)
    # Create an error message that gives some details about the problem.
    error_msg = ("Array 'A' was NOT saved and/or loaded properly, "
                 "because %i elements were mismatched." % n_mismatches)
    # Raise an 'Exception', which tells Python to immediately stop
    # executing the program, and which can print information about the
    # error.
    raise RuntimeError(error_msg)
# Remove the test file that we just created.
os.remove(data_filename)

## Make some plots
# Set the figure number that you want to use
ifig = 4
# Make the figure and return a handle to it
fig = plt.figure(ifig)
# Clear it, in case it already has stuff in it
fig.clear()
# Adjust the figure's size to fit the plots (this might take some
# tweaking)
fig.set_figwidth(6.)
fig.set_figheight(12.)

## Subplot 1
# Make a subplot of fig (which has 3 rows and 1 column total), make
# the 1st subplot active, and return a handle to it
ax1 = fig.add_subplot(3, 1, 1)
# Make a 2D heatmap of the A array, using the "gray" colormap (cmap)
plt.imshow(A, interpolation="nearest", cmap="gray")
# Add x- and y-labels to the plot
# (within strings, $...$ notation means "use LaTeX math here")
ax1.set_xlabel("$axis_1$") 
ax1.set_ylabel("$axis_0$")
# Make a title for the plot
ax1.set_title("A values")

## Subplot 2
# Make a second subplot in fig, make it 3d, and activate it
ax2 = fig.add_subplot(3, 1, 2, projection='3d')
# Plot the L array in 3D, along the coordinates x and y
ax2.plot_surface(X, Y, L, rstride=1, cstride=1, cmap="jet")
ax2.set_xlabel("$axis_1$")
ax2.set_ylabel("$axis_0$")
ax2.set_zlabel("$\log(p)$")
ax2.set_title("log-probabilities of A (under normal dist.)")

## Subplot 3
# Make a third subplot in fig and activate it
ax3 = fig.add_subplot(3, 1, 3)
# Plot lp1 as a red line ("r-"), with width 2.
plt.plot(x, lp1, "r-", linewidth=2.)
# Plot a red circle at (max_x, max_lp1) to indicate the peak, and make it size=10
plt.plot(max_x, max_lp1, "ro", markersize=10.)
# Write some text into the plot, near the red circle, to label it
plt.text(max_x + 0.6, max_lp1, "$\max_j \sum_i L_{i,j}$")
# Set the x- and y-axes' limits in proportion to the scale of the data
ax3.set_xlim(np.min(x) - 1., np.max(x) + 1.)
ax3.set_ylim(np.min(lp1) - 2., np.max(lp1) + 2.)
ax3.set_xlabel("$axis_1$")
ax3.set_ylabel("$\log(p)$")
ax3.set_title("log-probabilities summed across $axis_0$")

## Save the figure to disk
# Create the figure's filename
figure_filename = "test_script_figure.png"
# Save the figure
fig.savefig(figure_filename)

# Displays the figure and makes it interactive. This means that Python
# will wait until you close the figure to resume execution, and thus
# any commands that follow plt.show() will not be executed until then.
plt.show()

# This text demonstrates that plt.show() waited until you closed the figure.
print ("You should see this text after you have closed the figure "
       "(unless you're using IPython -pylab).")


## A few notes:

# 1. When you use numpy.random, it is a good habit to always
# explicitly set your random seed ahead of time, which means passing
# the pseudo-random number generator an integer that controls the
# specific sequence of random numbers that will be returned from that
# object. E.g. at the top of this script:
# RSO = np.random.RandomState(seed=seed)
# That way, no matter what, you can re-create, exactly, any
# computation you have done, regardless of whether it had random
# choices or not. Also, it allows you to easily "re-shuffle" the deck
# of random numbers, to see how your results differ due to the
# specific random numbers that were chosen.

# 2. When using Pyplot, many commands operate on the active figure or
# axes, so instead of explicitly telling Pyplot which figure or axes
# you mean, e.g. "fig.savefig" or "ax1.set_xlabel", you can instead
# use "plt.savefig" or "plt.xlabel" to default to the currently active
# ones. However, sometimes you'll want specific control over which
# axes or elements you're modifying, so then the "fig.<command>"
# syntax is what you'll want to use.

# 3. When writing text in Pyplot (and elsewhere in Python), sometimes
# you'll need to put an 'r' before your string, like this,
# r"$\log(p)$", which tells Python "use the exact string I specified,
# and don't do any format-parsing on it" (r"" notation is called a
# 'string literal'). So, if your LaTeX text isn't showing up properly,
# or Python returns an error on one of those lines, trying prepending
# the string with 'r'.

# 4. When using plt.show(), one caveat is that when you're using
# IPython in "pylab interactive mode" (by running the script with:
# "ipython -pylab my_script.py"), plt.show() does not suspend
# execution, but instead continues executing.


