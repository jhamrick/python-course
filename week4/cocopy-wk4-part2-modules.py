#!/usr/bin/env python
""" Cocosci scientific Python course, Week 4: Part 2 - Modules"""

# IMPORTANT: make sure you are running python/ipython from the
# directory where you saved all of this week's files -- otherwise the
# import statements might not work!

# Another note: some of the functions in this tutorial are actually
# really useful!  Peter and I use similar circular statistics
# functions all the time, and I also frequently use the normalize
# function.



## Basic modules

# If your project has a lot of code, you may want to organize it into
# modules and packages.

# Fist, let's take a second look at the import statement.  Open up
# module.py and note the if statement at the bottom.

# 'if __name__ == "__main__"' is a way of determining whether or not
# the python file is being imported as a module or if it's being
# executed directly.  Because we're importing it, we shouldn't see the
# output of 'print hello("Alice")'.

import module

# And in fact, we don't.  If we were to run this from the command
# line, however, we would see both calls.  This is an important point:
# when you import a module, ALL the code will be run, unless it is in
# that special if statement.

# Like other things that we've imported, we can import functions and
# classes from modules, or just access them using the '.'.  This
# includes imports done in the module as well (this wlil become even
# more relevant in just a bit).

# running 'hello' without using an import
print module.hello("world")

# running 'hello' using an import
from module import hello
print hello("world")

# running 'pickled_hello' from the module
print module.pickled_hello("world")
# using the pickle module, as imported from the module
print module.pickle.dumps(hello("world"))


## Basic packages

# What if we want multiple modules?  For example, let's say we wanted
# to put together a statistics package.  We could put all of our
# statistics code in one directory, 'stats'.

# Looking inside 'stats', we see that it has four things:
#   - a file called circ.py
#   - a file called __init__.py
#   - a file called misc.py
#   - a folder called rvs

# What's that "__init__.py" file?  Similar to how classes have an
# __init__ method, packages have an __init__ file which can be used to
# specify what is in the package.  The file doesn't necessarily have
# to contain anything, but it /must/ be present, or Python won't
# recognize the directory as a package.

# Look inside the __init__.py file, and you'll see that it imports a
# few things and then creates a variable called '__all__'.  As you
# might have guessed, this is another special variable.  It's just a
# list with the names of all of the modules, functions, and variables
# that are included in the package.

# Important note: if you want "from package import *" to work
# correctly, you need to include __all__.  We strongly discourage the
# use of "import *", but it's still good practice to properly specify
# __all__ -- it makes it more explicit what the module is supposed to
# include.  You can also put __all__ in a file module (for example,
# look in circ.py).

import stats
print "The stats package is:", stats

# Why does python say that 'stats' is a module, when we thought we
# were creating a package?  It's sort of a terminology mixup --
# "package" really refers to the organization of files and directories
# on disk in a way that Python can interpret, where "module" is the
# in-memory object that provides access to the
# modules/classes/variables/functions in packages or files.

print "stats contains:", stats.__all__

# Ok, going back to our stats module. What are all of these things in
# stats?
print "stats.circ is a", type(stats.circ).__name__
print "stats.rvs is a", type(stats.rvs).__name__
print "stats.normalize is a", type(stats.normalize).__name__
print "stats.rand is a", type(stats.rand).__name__

# What do all these modules and functions do?  Let's look at the
# docstrings:
print "stats.circ:", stats.circ.__doc__
print "stats.rvs:", stats.rvs.__doc__
print "stats.normalize:", stats.normalize.__doc__

# (Side note: If you're using IPython, remember that you could type
# 'stats?' or 'stats.rvs?' and it would similarly print out the
# docstring for you.)

# Ok, so it's pretty clear that the 'circ' module is coming from
# circ.py, because of the 'import circ' statement.  But what about
# misc.py?  I purposefully chose not to have it be part of the module
# because I just wanted it to be a container for random functions.
# Instead, I wanted those functions to be available at the base
# package level, i.e. stats.normalize.

# (We've probably made the point pretty clear, but just to reiterate
# why not to do "import *"):
from numpy import *
npmean = mean
from stats.circ import *
circmean = mean
print "numpy's mean is:", npmean
print "circ's mean is:", circmean
print "Is 'mean' from numpy?", npmean == mean
print "Is 'mean' from circ?", circmean == mean

# 'rand' is just a variable I created in the package itself -- again,
# any code in an imported file gets run!  It's typically not a good
# idea to put many things in the __init__ file itself, though -- if
# you're going to do that, create a separate file and then import
# them in __init__.

# Last but not least, you can create packages inside packages: the
# 'rvs' folder is a second package, and works the same way as 'stats'
# (it has more files in it, including another __init__.py).  Because
# 'rvs' is inside 'stats', we can reference it as a subpackage,
# e.g. stats.rvs.GaussianRV.

print "stats.rvs.GaussianRV is a", type(stats.rvs.GaussianRV).__name__
print "stats.rvs.StandardNormalRV is a", type(stats.rvs.StandardNormalRV).__name__
print
print "stats.rvs.GaussianRV:", stats.rvs.GaussianRV.__doc__
print "stats.rvs.StandardNormalRV:", stats.rvs.StandardNormalRV.__doc__

# Remember how you can access imports made inside an module from the
# outside?  That's essentially all there is to the __init__.py file --
# it imports a bunch of stuff to make it accessible from the module.
# For example, even though we include 'other_stuff' in __all__, we
# can't use it unless we explicitly import it:

# this throws an AttributeError
print stats.other_stuff

# now it works!
import stats.other_stuff
print stats.other_stuff


# For more information on modules and packages, see:
# http://docs.python.org/tutorial/modules.html
# http://docs.python.org/tutorial/modules.html#packages
# http://pythonconquerstheuniverse.wordpress.com/2009/10/15/python-packages/
# http://groups.google.com/group/comp.lang.python/msg/26887482a432a0a6

