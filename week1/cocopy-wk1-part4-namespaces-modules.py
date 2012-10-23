#!/usr/bin/env python
""" Cocosci scientific Python course, Week 1: Part 3 - namespaces and modules."""

# Namespaces

# You can think of Python's 'working memory' as 3 lookup tables that
# connect names to data, functions, and other lookup tables, e.g.
name = "steve"
# creates a variable called 'name' and points it to the string
# '"steve"', which it stores in memory).

# So, if you then do something with 'name', e.g.
print "The value connected to 'name' is:", name
# Python looks for 'name' in each of its lookup table, sequentially,
# grabs the data that it points to ('"steve"'), and hands it to the
# command 'print'.

# The 3 lookup tables, which are called 'namespaces', are:

# 1. local -- which belongs to the current 'function' (you can look at
# it directly by calling 'locals()')

# 2. global -- which belongs to the current 'module' (you can look at
# it directly by calling 'globals()')

# 3. builtin -- global to all modules (it doesn't actually have a way
# of being looked at directly, but the following makes a function to
# look at it, similar to 'globals' and 'locals')
builtins = lambda: dict([(name, getattr(__builtins__, name)) for name in dir(__builtins__)])
# (don't worry about how this works for now)

# You can check (and print) whether any name is in those namespaces by
# calling:
print "Is 'name' in local?", "name" in locals()
print "Is 'name' in global?",  "name" in globals()
print "Is 'name' in builtin?",  "name" in builtins()
# These 3 prints should return 2 Trues and 1 False
print "Is 'name2' in local?", "name2" in locals()
print "Is 'name2' in global?",  "name2" in globals()
print "Is 'name2' in builtin?",  "name2" in builtins()
# These 3 prints should return 3 Falses. But, if you add 'name2' to
# the namespace, e.g.
name2 = "jen"
print "Is 'name2' in local?", "name2" in locals()
print "Is 'name2' in global?",  "name2" in globals()
print "Is 'name2' in builtin?",  "name2" in builtins()
# Then you should see 2 Trues and 1 False.
# The builtin namespace cannot be modified directly, it contains
# Python's most fundamental names, e.g.
print "Is 'print' in builtin?", "print" in builtins()
print "Is 'list' in builtin?", "list" in builtins()
print "Is 'sum' in builtin?", "sum" in builtins()

# As you probably noticed, locals() and globals() appeared to be the
# same, and you can check this explicitly by:
print "Is local the same as global?", locals() is globals()
# This returns True because we are not currently inside any function,
# and so locals() defaults to globals(). However, if I define a
# function and perform the same test inside it, the result changes:
def function():
    print "Is local the same as global inside 'function'?",  locals() is globals()
function()

print # blank line

# And to demonstrate that Python first looks for a name in the local
# namespace, before moving to global, and then builtin:
def function2():
    # Set name2 locally
    name2 = "bob"
    # Find name
    name_locations = []
    if "name" in locals():
        name_locations.append("'local'")
    if "name" in globals():
        name_locations.append("'global'")
    elif "name" in builtins():
        name_locations.append("'builtin'")
    # Find name2
    name2_locations = []
    if "name2" in locals():
        name2_locations.append("'local'")
    if "name2" in globals():
        name2_locations.append("'global'")
    elif "name2" in builtins():
        name2_locations.append("'builtin'")

    # Print where name was found, and what it contained
    for loc in name_locations:
        # Pring where it was
        print "name was found in:", loc,
        # Get what it contained
        if loc == "'local'":
             value = locals()["name"]
        elif loc == "'global'":
             value = globals()["name"]
        elif loc == "'builtin'":
             value = builtins()["name"]
        # Print what it contained
        print "and had the value:", value

    print # blank line

    # Print where name2 was found, and what it contained
    for loc in name2_locations:
        # Pring where it was
        print "name2 was found in:", loc,
        # Get what it contained
        if loc == "'local'":
             value = locals()["name2"]
        elif loc == "'global'":
             value = globals()["name2"]
        elif loc == "'builtin'":
             value = builtins()["name2"]
        # Print what it contained
        print "and had the value:", value
function2()

print # blank line
print # blank line

# Modules

# Python uses 'modules' to keep larger programs organized and also to
# allow interchangeability and generic use of names. A module is a
# Python file (e.g. module.py) that contains Python definitions and
# statements. To use the contents of a module, you 'import' it:
import numpy
# You can simultaneously rename it by calling this, instead:
import numpy as np

# The imported module is attached to its own namespace, so that its
# names can be kept separate and distinct from those in other
# namespaces. I can make a a function that returns an explicit
# dictionary of a module's namespace by:
numpy_namespace = lambda: dict([(name, getattr(numpy, name)) for name in dir(numpy)])
# And check that the values of different namespaces don't overlap:
print "Is 'sum' the same in the 'numpy' and 'builtin' namespaces?", numpy_namespace()["sum"] is builtins()["sum"]
# (here, 'sum' is a function in both the 'numpy' and 'builtin' namespaces)

# To access the value attached to a name in a module's namespace, you type a "." (period) after the module's name:
A = numpy.mean([10, 11, 12])
B = np.mean([10, 11, 12])

# You can also import specific names from a module by:
from numpy import mean
# And, again, simultaneously rename them:
from numpy import mean as avg

# So, I've shown 4 ways of getting at the numpy name 'mean':
print "Are 'numpy.mean', 'np.mean', 'mean', and 'avg' all the same?",
print numpy.mean is np.mean,
print numpy.mean is mean,
print numpy.mean is avg

# You can also import modules that are part of other modules, i.e.
import numpy.random as nprandom
print "Is numpy.random.randn the same as nprandom.randn?", numpy.random.randn is nprandom.randn

# WARNING:
# You can also import every name from a module into your current
# namespace by calling:
from numpy import *
# BUT: this is bad. Although it might make it easier for you to type
# commands without using their full module path (e.g. mean vs
# np.mean), there are two big downsides:
#
# 1. It overwrites existing names in your namespace. So, if you used
# that * syntax to import 2 modules, any name in the first one that is
# also in the second one will be overwritten.
#
# 2. It makes it very hard for other people (or you, a few months
# later) to understand your code. Because the * star just means "add
# all of the stuff from the module to my namespace", there is no way
# to keep track of where the functions came from.
#
# Here's a demonstration of why * imports are bad:
import os
from numpy import *
from scipy import *
from os.path import *
print "Is os.path.split the same as split?", os.path.split is split
print "Is numpy.split the same as split?", numpy.split is split
# numpy.split is a completely different function than os.path.split,
# and, your 'from os.path import *' wiped it out. Now, if you want
# numpy.split, you have to import numpy and call 'split' explicitly
# anyway. Worse, if you're looking at your code 6 months later and you
# forget which module 'split' was in, it will be annoying to find --
# especially if there's 20 'from module import *' statements through
# which you need to dig.
