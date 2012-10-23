#!/usr/bin/env python
""" Cocosci scientific Python course, Week 1: Part 1 - basics."""

# Python as a calculator
x = 4
y = 7
print "x times y equals:", x * y
# Python as a string processor
s = "bob "
t = "hope"
print "s plus t equals:", s + t


# Types: the space that a name's value can be in

# Single elements
# integer (number with no decimal point)
i = 2
# boolean (True or False)
b = True
# float (number with a decimal point)
f = 7.0
# long
L = long(2)
# complex
c = complex(5, 3)
c = 5 + 3j


# Sequences
# string
s = "bill"
# list
l = [10, -20., "bill", 40, ["list", 2]]
l = list((10, -20., "bill", 40, ["another", "list"])) # convert tuple (below) to list)
# tuple
t = (100, -200., "hope", 400, ["list", 2])
t = tuple([100, -200., "hope", 400, ["list", 2]]) # convert from list to tuple
# Lists and tuples can contain different types. Above, I've placed
# integers, floats, strings, other lists, etc. inside the lists and
# tuples I've created.


# To access an element from a string, list or tuple, use square brackets:
print s[1]
print l[1]
print t[1]
# Notice that it prints -20., not 10 -- Python, unlike Matlab, uses
# 'zero-indexing', meaning that the first element is l[0].

# You can access a contiguous range of elements in strings, lists and tuples by:
print "elements from 1 to the end:", l[1:]
print "elements from 0 up to, but not including, 2:", l[:2]
print "elements from 1 up to, but not including, 2:", l[1:2]
print "elements from 1 up to, but not including, whatever the last element is:", l[1:-1]
print "elements from 1 up to, but not including, the last element:", l[1:-1]
print "elements from 1 up to, but not including, the second-to-last element:", l[1:-2]

# Sets
# Sets are unordered collections of unique elements
S = set([4, 1, 1, 3, 3, 3, 2])
print S


# Dictionaries
# Dictionaries are not sequences, they are lookup tables. They map
# keys to values. Keys can be numbers, strings, or even tuples (they
# just have to be 'hashable'). Values can be anything.
d = {"A": 22, "B": 100, 20: "red", (1, 5): 7.3}
d = dict((("A", 22), ("B", 100), (20, "red"), ((1, 5), 7.3)))
# You use square brackets to access the elements:
print d["A"]


# Mutable vs. immutable
# 'mutable' means changeable, so mutable types mean that the values
# can be changed after they've been created, while immutable means
# they cannot. You'll have to remember these things at some point, but
# for now, just remember that some data types let you modify the
# elements and some don't.

# lists are mutable
l[1] = -5
# dicts are mutable
d["A"] = "aaaa"
# strings are immutable (this will cause an error)
s[0] = "T"
# tuples are immutable (this will cause an error)
t[1] = -5

# Mutable objects can also have their sizes changed:
print "'l' currently has", len(l), "elements."
l.append("new element") # Append a new element to the end
print "'l' now has", len(l), "elements."

# When you're deciding whether to use a mutable or immutable container
# (e.g. a list vs a tuple), use the immutable one unless you know you
# want to change it later -- that way, if you hand the object to a
# function, you can know for sure that it will not be changed on
# accident.
