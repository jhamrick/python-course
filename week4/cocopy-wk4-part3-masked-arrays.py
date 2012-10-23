#!/usr/bin/env python
""" Cocosci scientific Python course, Week 4: Part 3 - masked arrays."""

import numpy as np

### Numpy's masked arrays
#
# Masked arrays provide an easy way of handling arrays with missing
# and/or invalid entries
#
# located in numpy.ma module
import numpy.ma as ma

# Create a normal array
x = np.array([1, 2, 3, -100, 5])
# Create a masked version, masking out all values < 0
mx = ma.array(x, mask=x < 0)
# print means
print "Mean of x", x.mean()
print "Mean of x (masking negative numbers)", mx.mean()

## Constructing masked arrays
#
# Masked arrays are intended to be able to replace normal np.ndarrays,
# and so the same construction functions work:
x = ma.array([5, 2, 9, -4])
y = ma.array([5, 2., 9, -4.])
o = ma.ones(5)
z = ma.zeros((3, 2))
e = ma.empty(3)
a = ma.arange(6)
# These functions create masked arrays with all elements not masked
# initially. However, masked arrays can be constructed in other ways,
# which automatically set more interesting masks.
mx = ma.masked_equal([5, 2, 9, -4], 2)
my = ma.masked_greater([5, 2., 9, -4.], 3)
mis = ma.masked_inside(x, 1, 6)
miv = ma.masked_invalid([1, np.nan, 5, np.inf])
## And more:
# ma.greater_equal
# ma.masked_less
# ma.masked_less_equal
# ma.masked_not_equal
# ma.masked_object
# ma.masked_outside
# ma.masked_values
# ma.masked_where

# To get a masked array's unmasked data, and fill in masked elements, use
# 'filled':
print "mx, with masked elements filled with 77", mx.filled(77)
print "mx, with masked elements filled with 88", ma.filled(mx, 88)
# To get just the unmasked data:
print "mx's unmasked data", mx.compressed()
print "mx's unmasked data", ma.compressed(mx)
# The mask can be accessed with the 'mask' attribute:
print "mx's mask", mx.mask
print "mx's mask", ma.getmask(mx)

# To mask data elements in an existing array:
print "initial value of mx and mx[0]", mx, mx[0]
mx[0] = ma.masked
print "final value of mx and mx[0]", mx, mx[0]

# To unmask a value, just give it a valid value:
print "initial value of mx and mx[0]", mx, mx[0]
mx[0] = 1000
print "final value of mx and mx[0]", mx, mx[0]

# Normal vectorized functions apply as they do with normal np.ndarrays
print np.log(mx)
print np.sum(mx)
