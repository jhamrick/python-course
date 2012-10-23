#!/usr/bin/env python
""" Cocosci scientific Python course, Week 1: Part 4 - numpy."""

# Numpy

# By convention, the numpy module is referenced by 'np'
import numpy as np

# Numpy is a module, written in C for speed, that uses a new kind of
# sequence, 'array':
A = np.array([1, 2, 3, 4, 5, 6])

# You can also create arrays of zeros, ones, random numbers, and sequences:
Z = np.zeros(7)
O = np.ones(8)
R = np.random.rand(9)
S = np.arange(10)

# Numpy arrays are designed for vectorized computation, which means
# that when you want to apply the same operation to every element of
# one or more arrays, you don't need to explicitly loop through the
# elements, e.g.
b = []
for a in A:
    b.append(a ** 2)
print b
# can be done like this:
B = A ** 2
# The only real difference is that 'B' is of type np.array, while 'b' is a list. The advantage to vectorized computations is that they are usually much faster, and their syntax is simpler and more flexible. 
print "type of 'b':", type(b)
print "type of 'B':", type(B)

# For small sequences, the speed difference may be small, but for
# larger ones, in this case 1,000,000, it can be orders of magnitude faster.
import time # a basic module for measuring times
# for loop method
A = np.arange(1000000)
b = []
start_time0 = time.time()
for a in A:
    b.append(a + 2)
end_time0 = time.time()
# vectorized method
A = np.arange(1000000)
start_time1 = time.time()
B = A + 2
end_time1 = time.time()
print "for loop time:", (end_time0 - start_time0)
print "vectorized time:", (end_time1 - start_time1)
print "speedup factor:", (end_time0 - start_time0) / (end_time1 - start_time1)
# On my computer the speedup was over 250x
#
# Even if you used a list comprehension, e.g.
A = np.arange(1000000)
start_time2 = time.time()
b2 = [a + 2 for a in A]
end_time2 = time.time()
print "list comprehension computation time:", (end_time2 - start_time2)
print "speedup factor:", (end_time2 - start_time2) / (end_time1 - start_time1)
# the performance is still much worse. On my computer the speedup was over 200x

# You can also perform elementwise operations between two numpy arrays
# of the same size
A = np.arange(4)
B = np.arange(4, 8) ** 2
C = A * B

# Numpy includes many functions that operate on arrays as well:
s = np.sum(C)
p = np.prod(C)
cs = np.cumsum(C)
d = np.diff(C)

# And, you can plot the results using pyplot:
import matplotlib.pyplot as plt
plt.plot(A, C)
plt.show()
