#!/usr/bin/env python
""" Cocosci scientific Python course, Week 5: Part 5 - Properties"""

import numpy as np

## Properties

# It's kind of annoying to constantly use get_mu/set_mu and
# get_sigma/set_sigma.  Python has this neat thing called 'property'
# that lets you take these getter and setter functions and turn them
# into a single object that acts like both a variable and a function.

class GaussianRV(object):

    rand = np.random.RandomState(0)

    def __init__(self, mu, sigma):
        """Initialize parameter values 'mu' and 'sigma' for the random
        variable."""
        self.mu = mu
        self.sigma = sigma

    def _set_mu(self, mu):
        """Set the 'mu' parameter."""
        self._mu = mu
    def _get_mu(self):
        """Get the value of the 'mu' parameter."""
        return self._mu

    # note that we just refer to the methods by their names, not
    # self.whatever -- this scope is the class definition, which acts
    # just like any other scope (think of the GaussianRV function we
    # created earlier).  So, after the class is created, we'll be able
    # to see GaussianRV.mu ...
    mu = property(_get_mu, _set_mu)

    def _set_sigma(self, sigma):
        """Set the 'sigma' parameter."""
        self._sigma = sigma
        self._var = None
        self._Z = -0.5 * np.log(2 * np.pi * self._var)
    def _get_sigma(self):
        """Get the value of the 'sigma' parameter."""
        return self._sigma

    # ... and GaussianRV.sigma
    sigma = property(_get_sigma, _set_sigma)

    def _get_var(self):
        if self._var is None:
            self._var = self.sigma ** 2
        return self._var
    var = property(_get_var)

    def sample(self, size=None):
        samps = self.rand.normal(
            self.mu, self.sigma, size=size)
        return samps

    @classmethod
    def create_random(cls):
        """Randomly parameterize a gaussian random variable."""
        mu = np.random.rand()
        sigma = np.random.rand()
        newrv = cls(mu, sigma)
        return newrv
    
    @staticmethod
    def est_mu(vals, axis=-1):
        mean = np.mean(vals, axis=axis)
        return mean
    @staticmethod
    def est_sigma(vals, axis=-1):
        std = np.std(vals, axis=axis, ddof=1)
        return std

rv = GaussianRV(0, 1)
print rv.mu, rv.sigma # acting like a variable
print rv._var, rv._Z
rv.sigma = 2          # acting like a function
print rv.mu, rv.sigma # acting like a variable again
print rv._var, rv._Z 


## Descriptors

# Properties are actually just a special case scenario of
# 'descriptors'.  A descriptor is any object that has __get__,
# __set__, and/or __delete__ method(s).  So, the 'property' function
# creates a descriptor:
class A(object):
    def __init__(self, name):
        self.name = name
        
    def get_name(self):
        return self._name
    def set_name(self, val):
        self._name = str(val)
    name = property(get_name, set_name)
    
a = A('foo')
print "a's name:", a.name
print "'name' descriptor:", A.name
print "'name' descriptor's set method:", A.name.__set__
print "'name' descriptor's set method can set a's name:", A.name.__set__(a, 'bar')
print "'name' descriptor's get method:", A.name.__get__
print "'name' descriptor's get method can get a's name:", A.name.__get__(a)

# What's going on here, exactly?  When we do:
print a.name

# It is equivalent to:
print type(a).__dict__['name'].__get__(a)

# 'name' doesn't actually exist in a's scope:
print "Is 'name' in a?", 'name' in a.__dict__

# So Python looks in the next scope: that of the actual class, i.e.,
# type(a).  It finds it there:
print type(a).__dict__['name']

# And then, because we are simply accessing the value, calls the
# __get__ method of the descriptor that is bound to a.

# This now ties back to when we need to bind methods: functions are
# descriptors as well.  We can create our own custom descriptors, too.
# The following example is from the Python documentation:
# http://docs.python.org/howto/descriptor.html

# This will act just like a property, except that we don't need to
# define new methods for the same type of operation over and over.

class RevealAccess(object):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print 'Retrieving', self.name
        return self.val

    def __set__(self, obj, val):
        print 'Updating' , self.name
        self.val = val

class MyClass(object):
    x = RevealAccess(10, 'var "x"')
    y = 5
    
cls = MyClass()
print cls.x
cls.x = 5
print cls.x
print cls.y
cls.y = 6
