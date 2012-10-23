#!/usr/bin/env python
""" Cocosci scientific Python course, Week 5: Part 1 - Objects"""

import numpy as np

# 'objects' are the most fundamental thing about Python.  They are,
# essentially, the way the Python represents all data.  From the
# Python documentation,
#
#    "All data in a Python program is represented by objects or by
#    relations between objects."
#
# Literally, _everything_ in Python is an object.  Everything.  This
# is the most important thing to remember if you're trying to
# understand how something in this lecture works -- everything in
# Python is an object.

# Ok, so creating objects is the same as what we've seen before:
obj = object()
# Objects always have two associated pieces of information. First, the
# identifier, which is essentially the object's address in memory:
print "obj's id is", id(obj), hex(id(obj))
# And second, the 'type', which defines what the object can do and
# what values it can hold:
print "obj is a", type(obj)
# Basic objects have type 'object', and 'object' types have type
# 'type'.  Remember, everything in Python is an object, so types are
# also objects:
print "type(obj) is a", type(type(obj))
print "is an object type an object?", isinstance(type(obj), object)
print "is a type type an object?", isinstance(type(type(obj)), object)

# By default, there are multiple types defined in Python.  Anything
# with one of these types is still an objects -- so these types are
# like the next level up the abstraction tree:
#  - None
#  - NotImplemented
#  - Ellipsis
#  - numbers.Number (e.g., int, float, bool, complex)
#  - Sequence types (e.g., string, tuple, list)
#  - Set types (e.g., set)
#  - Mapping types (e.g., dict)
#  - Callable types (e.g., functions)
#  - Modules
#  - Classes
#  - Class instances
#  - Files
#  - Internal types (e.g., slice, code)
#
# For more details, see:
#   http://docs.python.org/reference/datamodel.html#the-standard-type-hierarchy

# The types in the above list that I want to focus on are:
#  - Callable types (e.g., functions)
#  - Classes
#  - Class instances
