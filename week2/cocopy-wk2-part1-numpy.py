#!/usr/bin/env python
""" Cocosci scientific Python course, Week 2: Part 1 - numpy."""

### Numpy

## By convention, the numpy module is referenced by 'np'
import numpy as np

## Numpy is a module, written in C for speed, that uses a new kind of
# sequence, 'array':
A = np.array([1, 2, 3, 4, 5, 6])

# You can also create arrays of zeros, ones, random numbers, and sequences:
Z = np.zeros(7)
O = np.ones(8)
R = np.random.rand(9)
S = np.arange(3, 10)

## "shape", "size"
print R.shape, S.shape
print R.size, S.size

## Single array operations
print Z - 4.
print R ** 2.4
print np.log(S)

## Multiple array operations (on same-size arrays)
A = np.array([1., 6., 10., -4., 3.])
A2 = np.array([3., 3., 0.2, 7., 9.])
print A.shape, A2.shape
print A * A2
print A ** A2

# Numpy includes many functions that operate on arrays as well
print np.sum(A)
print np.prod(A)
print np.cumsum(A)
print np.diff(A)

## Accessing subsets of an array's elements - slicing + indexing
# any slicing that works on lists also works on numpy arrays
print A[:2], A[2:], A[2:4], A[::-1]
# but there are additional indexing techniques, like using:
# - lists
print A[[0, 2, 3]]
print A[[0, 0, 4, 4]]
# - boolean arrays
b = np.array([True, False, True, True, False])
print A[b]

## Boolean arrays
b = A > 3
print b
b2 = A % 2 == 1
print b2
# They allow techniques for advanced indexing
print A[b], A[b2]
# (you'll often just put the boolean inside the indexing expression)
print A[A > 3]
# Several numpy functions are specific to boolean arrays
print np.any(b)
print np.all(b2)
print np.nonzero(b)
print np.flatnonzero(b)
print np.where(b2, A, A2)


## "nan" & "inf": not-a-number & infinity
# nan is a special value in numpy that signifies a value that is not a
# number. inf means infinity. 
a = np.array([0., 5., -3.]) / np.array([0., 0., 0.])
print a
# "isnan", "isinf"
print np.isnan(a)
print np.isinf(a)
# when an array contains nans, it can interfere with numpy functions
# that operate across the array:
b = a.copy()
b[np.isinf(b)] = 7.
b[2] = 4.
print b
print np.sum(b)
print np.max(b)
print np.min(b)
print np.argmax(b)
print np.argmin(b)
# So, numpy has some nan-robust variants (scipy has some more, too)
# "nansum", "nanmax", "nanmin", "nanargmax", "nanargmin", "nan_to_num"
b = a.copy()
b[np.isinf(b)] = 7.
b[2] = 4.
# return the sum across the array, ignoring nans
print np.nansum(b)
# return the max and min values, ignoring nans
print np.nanmax(b)
print np.nanmin(b)
# return the index of the max and min values, ignoring nans
print np.nanargmax(b)
print np.nanargmin(b)
# replace nans with 0
print np.nan_to_num(b)
# I think the reason for numpy not just defaulting to the nan-robust
# variants is that you often need to be made aware when you arrays
# have nans -- e.g. you'd probably want to know if your computation of
# the sum of a 1000-element array was automatically ignoring nans.


## Multidimensional arrays
# hyperrectangle of values
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
B = np.ones([4, 3])
C = np.random.rand(2, 6)
print A.shape, B.shape, C.shape
print A.size, B.size, C.size
print A.ndim, B.ndim, C.ndim
print A
print B
print C

# index using multiple subscripts
print A[2, 1]
print B[:, 0]
print C[0, [1, 2]]
print C[[0, 1], [1, 2]]

import numpy.lib.index_tricks as it


# single- and multiple-array operations still apply for arrays of the
# same shape
print A ** 2
print A + B

## "reshape" - changing the length of an array's dimensions while
# keeping its size the same. numpy has several reshape (resize)
# methods, some of which create a new array with the target shape and
# others which reshape the array in-place.
print A.shape, A.size
A2 = np.reshape(A, (3, 4))
A3 = A.reshape((3, 4))
print A2.shape, A2.size
print np.all(A2 == A3)
A2.shape = 6, 2
A3.resize((6, 2))
print A2.shape, A2.size
print np.all(A2 == A3)
# "ravel" - makes the array 1D
print np.ravel(A), A.ravel()

## Order: numpy defaults to C ordering for most shape-manipulation
# functions on multidimensional arrays, which means that the outer
# (rightmost) dimensions are "fastest". However, most of these
# functions take an keyword argument "order" that lets you specify C
# or Fortran ordering (order="C" / order="F"). Fortran ordering means
# the inner (leftmost) dimensions are fastest, and is the default that
# Matlab uses.
print A
print np.ravel(A, order="C")
print np.ravel(A, order="F")
print np.reshape(A, (2, 6), order="C")
print np.reshape(A, (2, 6), order="F")
B = np.arange(12)
print np.reshape(B, (2, 6), order="C")
print np.reshape(B, (2, 6), order="F")

## Broadcasting
# Broadcasting refers to numpy's rules for operating on multiple
# arrays of different shapes. Basically, if the arrays satisfy the
# broadcasting contraints, then no error is generated, otherwise it
# will fail with the following error:
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
C = np.random.rand(2, 6)
print A.shape, C.shape
print A - C

# Broadcasting rules have 2 constraints:

# 1. If two arrays have the same number of dimensions, but have
# different shapes, then for any dimension where the arrays have
# different lengths, at least one array must have a dimension shape of
# 1.
a0 = np.zeros((3, 4, 1, 1))
a1 = np.ones((3, 1, 5, 1))
b = a0 + a1
print a0.shape, a1.shape, b.shape

# 2. Two arrays can have different numbers of dimensions but the
# broadcasting rules cause them to be aligned along their outermost
# (right) dimension, and implicitly reshapes the array with fewer
# dimensions to match the number of dimensions of the other array by
# adding new dimensions of length 1 to the inside (left) of the
# lower-dimension array. Then, it checks that constraint (1) applies.
a0 = np.zeros((3, 4, 5))
a1 = np.ones((4, 5))
b = a0 + a1
print a0.shape, a1.shape, b.shape
# Broadcasting provides a big advantage over Matlab because it means
# you don't have to use repmat() every time you want to perform
# operations between arrays of different shapes. repmat() is slow and
# uses more RAM (because each incoming array must be copied up to the
# shape of the output array).

# You can add dimensions to an array by:
a0 = np.zeros((3, 4, 5))
print a0.shape
print np.expand_dims(a0, axis=2).shape
# or
print a0[:, :, None, :, None].shape


## In-place modification
# You can modify array elements in place:
A = np.ones(8)
A[[1, 3, 4, 7]] = [6., 3., -2, 6]
print A
# Or, using Python's normal in-place sets:
A += 11
print A
A %= 4
print A


## "Views" - i.e pointers

# You can reference subsets of a numpy array's elements with a
# separate variable by creating a view of it (which slicing does
# implicitly):
A = np.ones(8)
A[[1, 3, 4, 7]] = [6., 3., -2, 6]
B = A[4:-1]
print A
print B
# B will reflect changes to A
A[5] = 1000
print A
print B
# But beware, so will A:
B[0] = 555
print A
print B
# So, this technique is powerful, but potentially hazardous too,
# because you might not realize you're referencing another array. To
# avoid this, instruct numpy to make a copy of A's data:
C = A[4:-1].copy()
A[6] = 77777
print A
print B
print C
# You can check whether an array's data is owned by another:
A = np.ones(6)
B = A
C = A[:]
D = A[2:4]
print "Is B the same as A?", B is A
print "Does B's data belong to A?", B.base is A
print "Does B own its own data?", B.flags.owndata
print
print "Is C the same as A?", C is A
print "Does C's data belong to A?", C.base is A
print "Does C own its own data?", C.flags.owndata
print
print "Is D the same as A?", D is A
print "Does D's data belong to A?", D.base is A
print "Does D own its own data?", D.flags.owndata
print

# Here's the scary part: some other numpy functions also return views
A = np.ones(6)
B = A.reshape((3, 2))
C = np.reshape(A, (3, 2))
B[1, 0] = 5
C[1, 1] = 7
print A, "\n", B, "\n", C
print "Is B the same as A?", B is A
print "Does B's data belong to A?", B.base is A
print "Does B own its own data?", B.flags.owndata
print
print "Is C the same as A?", C is A
print "Does C's data belong to A?", C.base is A
print "Does C own its own data?", C.flags.owndata

# Bottom line:
# Be careful when you modify array elements, and try to be sure about
# who the data belongs to.


## Random numbers
# Until now, I've been generating random numbers using
# np.random.<generate_function>, but this is very bad practice. You
# always want to be able to recreate the random numbers you have
# generated for several reasons. First, it's much easier to debug
# problems in how they are used, second, it's easier to understand how
# they influence the outcome of your programs, and third, it is nice
# to be able to create the exact same conditions at a later time.
# So, to seed a random stream in numpy, use:
seed = 0
RSO = np.random.RandomState(seed)
# this allows you to generate pseudo-random numbers, which can be
# recreated later:
print RSO.rand(), RSO.rand(), RSO.rand()
seed = 2
RSO2 = np.random.RandomState(seed)
print RSO2.rand(), RSO2.rand(), RSO2.rand()
# RandomState objects (RSO) have various generator methods:
print RSO.rand(), RSO.randn(), RSO.vonmises(0, 1), RSO.triangular(1, 2, 3)


## "save" / "load"

# Often you need to save your data to disk, and load it later. For
# instance, if you do some time-consuming computations on a large set
# of data, you might want to save the results so that next time, you
# can avoid waiting for the computations to complete. Numpy's save and
# load functions let you save/load arrays as binary files -- similar
# to C's fwrite/fread or Matlab's save/load:

# make an array of random numbers
seed = 5
RSO = np.random.RandomState(seed)
A = RSO.randn(3, 4, 5)
# location on disk to save it (you can, optionally specify ".npy")
filename = "my_save_test_data"
# perform the save
np.save(filename, A)
# load it as array B -- here you MUST specify the extension ".npy"
B = np.load(filename + ".npy")
print np.all(A == B)

# You can also save multiple arrays into one file, using the "savez"
# function, which creates a file with the extension ".npz"
seed = 3
RSO = np.random.RandomState(seed)
A = RSO.randn(3, 4, 5)
B = RSO.randn(6, 10)
C = RSO.randn(1000)
filename = "my_save_test_data"
# savez will add the extension ".npz", if you don't provide it.
np.savez(filename, A, B, C)
# When you load a ".npz" file, numpy returns a data structure that is
# similar to a dict, with keys that point to each saved array. The key
# names are "arr_0" ... "arr_N" for N saved arrays.
loaded_data = np.load(filename + ".npz")
print loaded_data.keys()
a = loaded_data["arr_0"]
b = loaded_data["arr_1"]
c = loaded_data["arr_2"]
# If you want, you can specify the names of the keys when you savez,
# but giving keyword arguments to np.savez:
np.savez(filename, A=A, B=B, C=C)
loaded_data = np.load(filename + ".npz")
print loaded_data.keys()
a = loaded_data["A"]
b = loaded_data["B"]
c = loaded_data["C"]

# Because the saved files are binary, they are *hard* to read using an
# outside text viewer/editor. Here, I'm just opening the ".npy" file
# and storing each line in "lines", then printing it:
fid = open(filename + ".npy", "r")
lines = [line for line in fid.readlines()]
fid.close()
print lines

## Numpy can also save and load text, which are easier to read:
seed = 6
RSO = np.random.RandomState(seed)
A = RSO.randn(3, 4)
filename = "my_save_test_data"
# savetxt does NOT add any extension
np.savetxt(filename, A)
B = np.loadtxt(filename)
print B

# Because it's text, it's easier to read:
fid = open(filename, "r")
lines = [line for line in fid.readlines()]
fid.close()
print lines

# Also, you can use numpy's genfromtxt to handle data files with
# missing elements:
lines = ["1,2,3,4\n", "11,,13,\n"]
fid = open(filename, "w")
for line in lines:
    fid.write(line)
fid.close()
try:
    B = np.loadtxt(filename, delimiter=",")
except:
    print "'B = np.loadtxt(filename)' failed."
    B = np.genfromtxt(filename, delimiter=",", filling_values=-1.0)
    print "'B = np.genfromtxt(filename)' worked!"
print B

# scipy provides a function for reading Matlab data files:
# import scipy
# scipy.io.loadmat


## dtype
# Numpy arrays have different types, indicated by "dtype":
A = np.array([1, 2, 3], dtype=np.int)
B = np.array([1.7, 2.2, 3.0], dtype=np.int)
C = np.array([1, 2, 3], dtype=np.float)
D = np.array([1, 2, 3], dtype=np.str)
Z = np.zeros(5, dtype=np.bool)
print A
print B
print C
print D
print Z
# You can query an array's dtype using A.dtype:
print A.dtype
print C.dtype
print D.dtype
print Z.dtype
# To return a different type:
print A.dtype, A
E = A.astype(np.str)
print E.dtype, E
# or
print Z.dtype, Z
F = Z.astype(np.float)
print F.dtype, F


