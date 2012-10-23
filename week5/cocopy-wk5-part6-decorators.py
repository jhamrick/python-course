#!/usr/bin/env python
""" Cocosci scientific Python course, Week 5: Part 5 - Decorators"""

# We've done a lot of cool tricks with wrapping functions in other
# functions and then returning the new function -- most notably to be
# able to bind functions to objects.  This behavior of modifying
# functions is so useful, in fact, that Python has a special shortcut
# for it: decorators.

# So, let's create a decorator that runs a function and reports the
# amount of time it took:
import datetime
dt = datetime.datetime 
def timeit(func):
    def new_func(*args, **kwargs):
        start = dt.now()
        out = func(*args, **kwargs)
        secs = (dt.now() - start).total_seconds()
        print "'%s' took %.5f secs" % (func.__name__, secs)
        return out
    return new_func

def hello():
    return "Hello, closures are fun!"
timed_hello = timeit(hello)
print timed_hello()

# If we never wanted to actually use 'hello', then we could do
# something like this:
def hello():
    return "Hello, closures are fun!"
decorator = timeit
hello = decorator(hello)
print hello()

# Or, we can use decorator syntax. You'll recognize the '@' symbol
# from staticmethods and classmethods.  Those are decorators, too --
# decorators aren't actually all that special.  Any function that
# takes another function and returns a function is a decorator.  They
# just get some fancy syntax, too.
@timeit
def hello():
    return "Hello, closures are fun!"
print hello()

# Decorators can take arguments, too, if you create another level of
# function wrapping:
def timeit_n(n):
    def timed_func(func):
        def new_func(*args, **kwargs):
            times = []
            outputs = []
            for i in xrange(n):
                start = dt.now()
                outputs.append(func(*args, **kwargs))
                secs = (dt.now() - start).total_seconds()
                times.append(secs)
            idx = np.argmin(times)
            best = times[idx]
            out = outputs[idx]
            print "'%s' took %.5f secs (best of %d)" % (func.__name__, best, n)
            return out
        return new_func
    return timed_func

# Without special syntax:
def hello():
    return "Hello, closures are fun!"
decorator = timeit_n(100)
hello = decorator(hello)
print hello()

# With special syntax:
@timeit_n(100)
def hello():
    return "Hello, closures are fun!"
print hello()

# Decorators can be used with properties, too! Here's an example first
# without decorators:

class A(object):
    def __init__(self, name):
        self.name = name
    def get_name(self):
        return self._name
    def set_name(self, val):
        self._name = name
    # The following two lines are equivalent to property(get_name,
    # set_name), but we can also use name.setter to specify the
    # "setter" function that we wish to use.
    name = property(get_name)
    name.setter(set_name)

# And now with decorators:
class A(object):
    def __init__(self, name):
        self.name = name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, val):
        self._name = name
