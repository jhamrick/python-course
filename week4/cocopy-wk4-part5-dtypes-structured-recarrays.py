#!/usr/bin/env python
""" Cocosci scientific Python course, Week 4: Part 5 - dtypes,
structured arrays, recarrays."""

import numpy as np

### Numpy's dtypes

# dtypes are data types that are specific to numpy (though the basic
# ones overlap with Python's)
# http://docs.scipy.org/doc/numpy/user/basics.types.html
X = np.array([1, 2, 3])
Y = np.array([1., 2, 3])
print "X and Y's types are:", type(X), "and", type(Y)
print "X and Y's dtypes are:", X.dtype, "and", Y.dtype
# Every numpy array is just a set of elements with the same dtype.

# You can force numpy to use a dtype when creating an array:
Z = np.array([1.5, 6.2, 8], dtype="int64")
# and, to convert arrays:
W = Z.astype("float64")
print "Z and W are:", Z, "and", W
print "Z and W's dtypes are:", Z.dtype, "and", W.dtype

# In fact, numpy arrays can even contain arbitrary Python objects:
# define a class
class SomeClass(object):
    def __init__(self, number=3, string="abc"):
        self.number = number
        self.string = string
        
    def log(self):
        rval = np.log(self.number)
        return rval
    
    def __add__(self, other):
        number = self.number + other.number
        string = self.string + other.string
        rval = SomeClass(number=number, string=string)
        return rval

        
# Make some instances of the class
obj0 = SomeClass(number=2)
obj1 = SomeClass(string="-hey-")
obj2 = SomeClass(number=10, string="now-")
obj3 = SomeClass()
# Make an array of these objects
A = np.array([obj0, obj1, obj2, obj3])
print "A's dtype is:", A.dtype

# For custom classes, numpy will check whether they contain attributes
# that match numpy's functions, and apply them if possible:
L = np.log(A)
S = np.sum(A)
print "log of A is:", L
print "sum of A is:", S.number, S.string

# Still, numpy arrays that contain Python objects aren't particularly
# efficient, and even the custom functionality must be explicitly
# defined.

# However, you can create custom numpy dtypes that act as a sort of
# intermediately flexible type between full Python classes and basic
# numpy dtypes. They are efficient and automatically supported by most
# of numpy's features.
#
# The most important point is that numpy has 'dtype' objects, that you
# can create and customize. There are multiple equivalent ways of
# specifying the dtype's structure:

# Create a dtype for normal strings
dt0 = np.dtype(("str"))
# A second argument specifies the item-width
dt1 = np.dtype(("str", 4))
# Now, create two arrays with different dtypes
B = np.array("abcdefgh", dtype=dt0)
C = np.array("abcdefgh", dtype=dt1)
print "B's data and dtype:\n", B, "\n", B.dtype
print "C's data and dtype:\n", C, "\n", C.dtype
print

# Create dtypes for multiple ints
dt2 = np.dtype(("int", 6))
dt3 = np.dtype(("int", (1, 3)))
# Now, create two arrays with different dtypes
D = np.zeros(2, dtype=dt2)
E = np.zeros(2, dtype=dt3)
print "D's data, dtype and shape:\n", D, "\n", D.dtype, "\n", D.shape
print "E's data, dtype and shape:\n", E, "\n", E.dtype, "\n", E.shape
print

# Create dtypes for multiple basic dtypes, using comma-separated strings
dt4 = np.dtype(("int,float"))
F = np.zeros(2, dtype=dt4)
print "F's data, dtype and shape:\n", F, "\n", F.dtype, "\n", F.shape
print

# There are many subtleties to dtype creation and conversion, check:
# http://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html


## Structured dtypes

# Here's where things get interesting. In the last example, notice how
# dt4 is defined:
print "dt4:", dt4
# Those 'f0' and 'f1' are default 'field names' that were added. dt4
# actually specifies a 'structured' dtype, which can be thought of as
# a simple class whose data are numpy types.
G = np.zeros((3, 4), dtype=dt4)
print "G's data, dtype and shape:\n", G, "\n", G.dtype, "\n", G.shape
print
# G is a (3,4) array with dtype dt4 and zeros as values.

# You can access and set its elements by number and/or field name:
print G[1, 2]
print G["f0"]
print G["f1"][1, 2]
G["f1"][1, 2] = 22.0
print G["f1"][1, 2]
print

# You could also create the dtype and explicitly define field names:
dt5 = np.dtype([("field_A", "int"), ("field_B", "float")])
H = np.zeros(2, dtype=dt5)
print "H's data, dtype and shape:\n", H, "\n", H.dtype, "\n", H.shape
print


## recarray
# recarrays are just structured arrays with attributes that are the fields:
H["field_A"] = 22, 13.7
H["field_B"][1] = 4.3
R = H.view(np.recarray)
print R.field_A
print R.field_B


# Structured arrays have many uses, but here's a demo in the context
# of experiment data analysis.
#
# Create dtypes to hold data collected from an experiment
n_trials = 35
dt = np.dtype([("subject_initials", "3str"),
               ("subject_id", "uint16"),
               ("age", "uint8"),
               ("trial", "uint64", n_trials),
               ("block", "uint8", n_trials),
               ("stimulus", "int64", n_trials),
               ("correct", "int8", n_trials),
               ("response", "bool", n_trials),
               ("response_time", "float64", n_trials)])
print dt.names

# Make up some fake data as a demo
seed = 0
RSO = np.random.RandomState(seed)
subjs = ("pb", "jh", "yz", "ms")
n_subjs = len(subjs)
n_blocks = 5
stims = np.linspace(-3, 3, n_trials / n_blocks)
data = np.empty(n_subjs, dtype=dt)
data["subject_initials"] = subjs
data["subject_id"] = np.arange(n_subjs)
data["age"] = RSO.randint(18, 40, size=n_subjs)
data["trial"] = np.arange(n_trials)
data["block"] = np.arange(n_trials) % n_blocks
data["stimulus"] = np.ravel([RSO.permutation(stims) for b in xrange(n_blocks)])
data["correct"] = np.sign(data["stimulus"])
data["response"] = data["stimulus"] + RSO.randn(n_subjs, n_trials) * 1.5 > 0.
data["response_time"] = RSO.rand(n_subjs, n_trials) * 2 + 1

# View the histograms of participants' responses and response time
plt.figure(1)
plt.clf()
plt.suptitle("Histograms")
plt.subplot(1, 2, 1)
plt.title("Responses {0,1}")
plt.hist(data["response"].T)
plt.subplot(1, 2, 2)
plt.title("Response times")
plt.hist(data["response_time"].T)

# Use masked arrays to calculate percent correct
import numpy.ma as ma
mcorrect = ma.masked_equal(data["correct"], 0)
mresponse = ma.array(data["response"], mask=mcorrect.mask)
percent_correct = (~((mcorrect == 1) ^ (mresponse == 1))).mean()
print "Percent correct (ignore stim level 0):", percent_correct

# Compute empirical psychometric function
n_stims = len(stims)
counts_per_subj = np.empty((n_subjs, n_stims))
for istim, stim in enumerate(stims):
    idx = data["stimulus"] == stim
    counts_per_subj[:, istim] = ma.array(data["response"], mask=~idx).sum(axis=1)
psychometric_subjs = counts_per_subj / n_blocks
psychometric_all = psychometric_subjs.mean(axis=0)
    
# Plot it
plt.figure(2)
plt.clf()
plt.title("Psychometric functions")
plt.plot(stims, psychometric_all, "k--", linewidth=3.)
plt.plot(stims, psychometric_subjs.T, linewidth=2.)
plt.xlabel("Stimulus level")
plt.ylabel("Proportion judged '1'")
plt.legend(np.hstack(("All", data["subject_initials"])), loc="lower right")
