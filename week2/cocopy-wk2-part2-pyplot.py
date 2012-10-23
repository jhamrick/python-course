#!/usr/bin/env python
""" Cocosci scientific Python course, Week 2: Part 2 - pyplot."""

# plotting interface for matplotlib
import matplotlib.pyplot as plt
import numpy as np

## Pyplot is numpy's main plotting module
# NOTE: You may need to call "plt.show()" after each plot command in
# order to see it!


## Plotting 1D data

# make X values from -10 to 10, and calculate their sine:
n = 50
seed = 9
X = np.linspace(-10, 10, n)
Y = np.sin(X)
# plot it
plt.plot(Y)
# Notice, the X values are wrong -- we didn't tell plot which X values
# to use, so it defaulted to 0 -> (n-1). To specify them:
plt.clf() # (clear the current figure)
plt.plot(X, Y)
# You can also specify color and line style, similar to Matlab's syntax:
plt.clf()
plt.plot(X, Y, "r--o")
# And, if you want to plot more data at the same time:
Z = 0.5 * np.cos(X)
plt.clf()
plt.plot(X, Y, "r--o", X, Z, "bs")
# That's fine, but you'll often need more control over the details:
plt.clf()
plt.plot(X, Y, color=(1., 0.7, 0.2), label="cos",
         linestyle="--", linewidth=3, marker="o", markersize=8)
plt.plot(X, Z, color=(0., 0.7, 0.9), label="sin",
         linestyle="None", linewidth=2, marker="s", markersize=10)
# You can also create a legend automatically from the labels:
plt.legend(("sin", "cos"), loc="upper left")
# ... or define the labels explicitly
plt.legend(loc="upper left")
plt.legend(("np.cos", "np.sin"), loc="upper left")
# Give your plot a title:
plt.title("My trigonometry plots")
# Set the axis boundaries:
plt.axis([-11., 11, -1.5, 3])
# Label the axes:
plt.xlabel("Angle (radians)")
plt.ylabel("Y, Z")
# Add some text to the plot:
plt.text(0., 2, "Yellow is higher than blue")
# Use latex (put the letter 'r' before your string to instruct Python
# to use the raw string, instead of interpreting the escape '\'
# backslash)
plt.xlabel(r"$\alpha (radians)$")
plt.text(0., -1, r"$angle = \alpha$")


# Bar graphs + histograms
# make some random data
n = 500
seed = 5
RSO = np.random.RandomState(seed=seed)
R = 2 * RSO.randn(n)
# compute its histogram
H, bins = np.histogram(R)
# plot the histogram as a bar graph
plt.clf()
plt.bar(bins[:-1], H)
# or
plt.clf()
plt.barh(bins[:-1], H)
# Getting the bins and bar widths set properly can be time-consuming,
# so if you just want to see a quick histogram, you can use:
plt.clf()
plt.hist(R)



## Plotting 2D data

# Make an array of random numbers to play with
# array dimensions
m, n = 48, 64
seed = 2
RSO = np.random.RandomState(seed=seed)
R = RSO.randn(m, n)
# Make arrays that contain the domain and range of some 2D polynomial
# you can easily make the domain using meshgrid
X, Y = np.meshgrid(np.linspace(-10, 10, n), np.linspace(-10, 10, m))
Z = (X - 2.) ** 2 + X * Y - (Y + 1.) ** 2
# quickly show the arrays
plt.matshow(R)
plt.matshow(Z)

# For more control, use "imshow", which plots a 2D array, or 3D with
# dim=2 of length 3 (RGB) or 4 (RGBA)
plt.clf()
plt.imshow(Z)
# Here are some common options
plt.clf()
plt.imshow(Z, interpolation="nearest", cmap="gray",
           vmin=Z.min() - 10., vmax=Z.max() + 10.)
# add a colorbar
plt.colorbar(shrink=0.75, ticks=np.linspace(Z.min(), Z.max(), 5).astype(np.int))

# Another colormap
plt.clf()
plt.imshow(Z, interpolation="nearest", cmap="bwr",
           vmin=Z.min() - 10., vmax=Z.max() + 10.)
# add a colorbar
plt.colorbar(shrink=0.75, ticks=np.linspace(Z.min(), Z.max(), 5).astype(np.int))

# If you have too many plots hanging around, use:
plt.close("all")



# When using Pyplot, many commands operate on the active figure or
# axes, so instead of explicitly telling Pyplot which figure or axes
# you mean, e.g. "fig.clf()" or "ax.set_xlabel(...)", you can instead
# use "plt.clf()" or "plt.xlabel(...)", which default to the currently
# active ones. However, sometimes you'll want specific control over
# which axes or elements you're modifying, so then the "fig.<command>"
# / "ax.<command>" syntax is what you'll want.
#
# This will be covered in greater depth next time.

