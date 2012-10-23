#!/usr/bin/env python
""" Cocosci scientific Python course, Week 3: Part 2 - Advanced pyplot."""

# plotting interface for matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

# A few notes:
# 1) You may need to call "plt.show()" after each plot command in order to see
#    the plot!
# 2) I am wrapping a lot of these demos in functions, to make it easy to create
#    the whole graph at once.  It will be more obvious later when I introduce
#    saving figures.


# Random number generator
seed = 9
rand = np.random.RandomState(seed)


## Customizing 1D plots

# Create some noisy data from n trials
n = 10    # number of trials
s = 50    # number of samples from each trial

# Trial ids
X = np.arange(1, n+1)
# Target data point for each trial
Y = 5 * rand.randn(n)
# s noisy samples for each trial
Yn = Y[:, None] + rand.randn(n, s)
# Mean and standard deviation of each trial's samples
Ymean = np.mean(Yn, axis=-1)
Ystd = np.std(Yn, axis=-1, ddof=1)

# Various plotting constants
axis2d = [0.5, n+0.5, -10, 10]
titlesize = 20

def formatting_demo():
    """Customize the formatting of a simple 1D plot.

    """

    # Plot the targets and raw samples
    plt.figure()
    plt.plot(X, Y, 'k-')
    plt.plot(X[:, None], Yn, 'r.')

    # We can choose from among several different common line styles:
    #   solid : '-'
    #   dashed: '--'
    #   dash-dot: '-.'
    #   dotted: ':'
    # And common marker styles:
    #   circle: 'o'
    #   cross: 'x'
    #   plus: '+'
    #   point: '.'
    #   pixel: ','
    # See the pyplot documentation for plt.plot() for more line and marker
    # options.
    
    # Set the axis labels and title
    plt.xlabel("Trial")
    plt.ylabel("Sample")
    plt.title("Formatting Demo", fontsize=titlesize)

    # The tick labels for the x-axis as [2, 4, 6, 8, 10].  This seems
    # undesirable -- we want them to be 1 through 10.  How do we fix this?
    plt.xticks(X, X) # (tick values, tick labels)

    # How do you set the axis limits? (This can also be done using plt.xlim ad
    # plt.ylim)
    plt.axis(axis2d)

    # If you want finer resolution for where your points lie, you can turn on
    # grid lines (see docs for more options here)
    plt.grid(True)
    # Turn off grid lines
    plt.grid(False)

    # We can also turn on and off the box surrounding the axes.  Let's turn them
    # off and enable grid lines:
    plt.box(on=False)
    plt.grid(True)
    # And turn the box on again:
    plt.box(on=True)
    plt.grid(False)

def latex_demo():
    """If you're creating a figure for a LaTeX document, you can make it render
    all the text with LaTeX so it matches the style better.  You usually would
    call this command at the top of your file, with the rest of your import
    statements.  It's not strictly necessary, but if you want the full suite of
    LaTeX symbols and math, you'll need to specify this.

    """
    
    from matplotlib import rc
    # Use a serif font like LaTeX does for text that isn't rendered by LaTeX
    rc('font', family='serif')
    # Use LaTeX to render text
    rc('text', usetex=True)

    # use the formatting demo to show the LaTeX
    formatting_demo()
    plt.title(r"\LaTeX{} Demo", fontsize=titlesize)


## Other forms of 1D plotting

def boxplot_demo():
    """Create a box-and-whiskers plot for each trial.

    """

    plt.figure()
    # Why is Yn transposed? Because plt.boxplot expects the columns to be
    # vectors and rows to be individual data points, but the shape of Yn is the
    # reverse of that.
    plt.boxplot(Yn.T)
    plt.xlabel("Trial")
    plt.ylabel("Sample")
    plt.title("Box-and-whiskers Demo", fontsize=titlesize)
    plt.xticks(X, [r"$%s$" % x for x in X])
    plt.axis(axis2d)

def errorbar_demo():
    """Plot the mean of the data, with error bars for the standard deviation.
    
    """

    plt.figure()
    plt.errorbar(X, Ymean, Ystd)
    plt.xlabel("Trial")
    plt.ylabel("Sample")
    plt.title("Errorbar Demo", fontsize=titlesize)
    plt.xticks(X, [r"$%s$" % x for x in X])
    plt.axis(axis2d)

def fill_between_demo():
    """Plot the mean of the data, with a lighter color band around the mean to
    denote standard deviation.  

    """

    plt.figure()
    # How do we know what a lighter red is?  We could just unifomly increase the
    # blue and green channels, but it's easier to just change the alpha value,
    # which governs the color's opacity (0 is completely transparent, 1 is
    # completely opaque).
    plt.fill_between(X, Ymean-Ystd, Ymean+Ystd, color='r', alpha=0.2)
    plt.plot(X, Ymean, 'r-')
    plt.xlabel("Trial")
    plt.ylabel("Sample")
    plt.title("Fill-Between Demo", fontsize=titlesize)
    plt.xticks(X, [r"$%s$" % x for x in X])
    plt.axis(axis2d)

def polar_demo():
    """Make a polar plot of some random angles.

    """

    # Sample a bunch of random angles
    A = rand.randint(0, 360, 100)
    # Plot each angle as a point with radius 1
    plt.figure()
    plt.polar(A, np.ones_like(A), 'ko')
    # Disable y-ticks, because they are distracting
    plt.yticks([], [])
    plt.title("Polar Demo", fontsize=titlesize)

## More advanced control: axes objects

def axes_demo():
    """We don't always have to use 'plt.' to do plotting commands.  In
    particular, we can often use the same (or similar commands) on specific sets
    of axes, which is really useful when you're dealing with multiple figures
    and/or subplots.

    """

    # Create two figures and get the axis objects associated with them
    fig1 = plt.figure()
    fig2 = plt.figure()
    ax1 = fig1.gca()
    ax2 = fig2.gca()

    # Plot raw trial samples on one figure. Note how we need to use set_xlabel,
    # set_ylabel, set_xticks, and set_xticklabels instead of xlabel, ylabel, and
    # xticks (in particular, plt.xticks becomes BOTH ax1.set_xticks and
    # ax1.set_xticklabels).
    ax1.plot(X, Y, 'k-')
    ax1.plot(X[:, None], Yn, 'r.')
    ax1.set_xlabel("Trial")
    ax1.set_ylabel("Sample")
    ax1.set_xticks(X)
    ax1.set_xticklabels([r"$%s$" % x for x in X])
    ax1.axis(axis2d)

    # Plot trial means and errors on the other figure
    ax2.errorbar(X, Ymean, Ystd)
    ax2.set_xlabel("Trial")
    ax2.set_ylabel("Sample")
    ax2.set_xticks(X)
    ax2.set_xticklabels([r"$%s$" % x for x in X])
    ax2.axis(axis2d)

    # Draw both figures.  We use plt.figure to switch the active figure, so we
    # can tell pyplot to draw both figures
    plt.figure(fig1.number)
    plt.draw()
    plt.figure(fig2.number)
    plt.draw()


## Creating subplots

def subplots_demo():
    """We don't always want separate figures -- just multiple plots in the same
    figure.  To do this, we use the subplot command, which takes the following
    arguments:

        (number of rows, number of columns, subplot #)

   """

    # Create the subplots. You can alternately use fig.add_subplot, which is
    # mostly the same as plt.subplot except it operates directly on the figure.
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)
    
    # Plot raw trial samples on one figure.
    ax1.plot(X, Y, 'k-')
    ax1.plot(X[:, None], Yn, 'r.')
    ax1.set_xlabel("Trial")
    ax1.set_ylabel("Sample")
    ax1.set_xticks(X)
    ax1.set_xticklabels([r"$%s$" % x for x in X])
    ax1.set_title("Raw Data")
    ax1.axis(axis2d)

    # Plot trial means and errors on the other figure.  We won't use y-ticks
    # here because they take up space and it's obvious from the first subplot
    # what they are.
    ax2.errorbar(X, Ymean, Ystd)
    ax2.set_xlabel("Trial")
    ax2.set_xticks(X)
    ax2.set_xticklabels([r"$%s$" % x for x in X])
    ax2.set_yticks([])
    ax2.set_title("Means and Errors")
    ax2.axis(axis2d)

    # Often, the spacing between subplots is less than desirable.  We can change
    # it using subplots_adjust:
    plt.subplots_adjust(
        left=0.1,
        right=0.95,
        bottom=0.1,
        top=0.9,
        hspace=0.1,
        wspace=0.1)

    # We can also add a title for the whole figure.  I usually feel like pyplot
    # makes the suptitle too small, so let's include a font size keyword, too.
    plt.suptitle("Subplots Demo", fontsize=titlesize)


def gridspec_demo():
    """If you need even more flexibility with subplots (for example, a 2x2
    figure with only 3 subplots, where one subplot spans two rows), use
    GridSpec.  We won't go into a lot of details here, but it will allow you to
    create plots like the one produced by this function.

    For more details and documentation, see:
    http://matplotlib.sourceforge.net/users/gridspec.html

    """

    # Import GridSpec
    from matplotlib.gridspec import GridSpec

    # Create a new figure
    fig = plt.figure()

    # First grid specification -- a 3x3 plot with only three subplots
    gs1 = GridSpec(3, 3)
    gs1.update(left=0.05, right=0.48, wspace=0.05)
    ax1 = plt.subplot(gs1[:-1, :])
    ax2 = plt.subplot(gs1[-1, :-1])
    ax3 = plt.subplot(gs1[-1, -1])

    # A different grid specification on the same figure.  This essentially
    # expands the figure to be 6x3 by explicitly setting the location of the
    # GridSpec (with gs2.update).
    gs2 = GridSpec(3, 3)
    gs2.update(left=0.55, right=0.98, hspace=0.05)
    ax4 = plt.subplot(gs2[:, :-1])
    ax5 = plt.subplot(gs2[:-1, -1])
    ax6 = plt.subplot(gs2[-1, -1])

    # Remove tick labels and print the name of the axes for each set of axes
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        for tl in ax.get_xticklabels() + ax.get_yticklabels():
            tl.set_visible(False)

    # Set overall plot title
    plt.suptitle("GridSpec w/ different subplotpars", fontsize=titlesize)


## Plotting with 3D axes

def axes3d_demo():
    """We can plot three-dimensional data using the mplot3d module.

    More 3D plotting functions can be found in the pyplot documentation:
    http://matplotlib.sourceforge.net/mpl_toolkits/mplot3d/tutorial.html

    """

    # First, we need to import pyplot's 3D capabilities.  Even though we're not
    # explicitly using Axes3D, we must make this call or the subplot commands
    # below will not recognize the '3d' projection.
    from mpl_toolkits.mplot3d import Axes3D

    # Axis limits
    lim = [-20, 20]

    # Create a random point cloud
    n1 = 1000
    Px = rand.randn(n1) * 5
    Py = rand.randn(n1) * 2
    Pz = rand.randn(n1)
    # Calculate points for a parabolic function
    n2 = 20
    Sx, Sy = np.meshgrid(
        np.linspace(lim[0], lim[1], n2),
        np.linspace(lim[0], lim[1], n2))
    Sz = -(Sx**2 + Sy**2)

    # Add a few 3d subplots
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(1, 3, 1, projection='3d')
    ax2 = fig.add_subplot(1, 3, 2, projection='3d')
    ax3 = fig.add_subplot(1, 3, 3, projection='3d')

    # Plot the point cloud as a scatter plot
    ax1.plot3D(Px, Py, Pz, 'k.')
    # Several of the basic adjustment functions, like set_xlim, have a 3d
    # counterpart, so we need to use those.
    ax1.set_xlim3d(lim)
    ax1.set_ylim3d(lim)
    ax1.set_zlim3d(lim)
    # Some of these functions are the same, too.
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("z")

    # Plot the function as a wireframe surface
    ax2.plot_wireframe(Sx, Sy, Sz)
    ax2.set_xlim3d(lim)
    ax2.set_ylim3d(lim)
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_zlabel("z")

    # Plot the function as a surface
    surf = ax3.plot_surface(
        Sx, Sy, Sz,
        rstride=1,   # array row step size
        cstride=1,   # array column step size
        cmap='jet',  # colormap for the surface patches
        linewidth=0, # disable grid lines
        )
    ax3.set_xlim3d(lim)
    ax3.set_ylim3d(lim)
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    ax3.set_zlabel("z")
    # Show a color bar describing how the colors map to vales
    fig.colorbar(surf, shrink=0.5, aspect=6)

    # Adjust the spacing between subplots
    fig.subplots_adjust(
        left=0.05,
        right=0.85,
        bottom=0.1,
        top=0.9,
        hspace=0.1,
        wspace=0.2)

    plt.suptitle("3D Demo", fontsize=titlesize)

## Saving figures to disk

# Pyplot allows you to save figures through the UI, which is nice, but sometimes
# we want to just generate and save a lot of figures programmatically.  Because
# we might want to do a lot of saving, this is a great example of something to
# wrap inside a function.  This is my 'save' function which I use constantly for
# saving figures:

def save(path, ext='png', close=True):
    """Save a figure from pyplot.

    """
    
    # Extract the directory and filename from the given path
    directory = os.path.split(path)[0]
    filename = "%s.%s" % (os.path.split(path)[1], ext)
    if directory == '':
        directory = '.'
    # If the directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Actually save the figure
    print "Saving figure to '" + os.path.join(directory, filename) + "'...", 
    plt.savefig(os.path.join(directory, filename))
    # Close it
    if close:
        plt.close()        
    print "Done"

# Now let's use the save function to save all the plots we've created thus far:
latex_demo()
save("1_latex_demo")
boxplot_demo()
save("2_boxplot_demo")
errorbar_demo()
save("3_errorbar_demo")
fill_between_demo()
save("4_fill_between_demo")
polar_demo()
save("5_polar_demo")
subplots_demo()
save("6_subplots_demo")
gridspec_demo()
save("7_gridspec_demo")
axes3d_demo()
save("8_axes3d_demo")


## Miscellaneous Notes

# Many of the formatting and style adjustments can be set in matplotlib's
# configuration file.  If you find you set certain formatting options (e.g.,
# font size) over and over, look into customizing the configuration file so that
# pyplot will default to using the format you prefer.  See:
# http://matplotlib.sourceforge.net/users/customizing.html

# This is a great colormap reference:
# http://matplotlib.sourceforge.net/examples/pylab_examples/show_colormaps.html
