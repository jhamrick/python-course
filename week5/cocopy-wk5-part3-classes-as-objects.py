#!/usr/bin/env python
""" Cocosci scientific Python course, Week 5: Part 3 - Classes as objects"""

import numpy as np

## Creating objects

# Ok, now that we have a better understanding of objects and
# functions, let's make a function to create a custom object.  Imagine
# for the moment that classes don't exist, but we (again) want to
# create a data structure that can represent Gaussian random
# variables.  So let's use a function that creates a dictionary, and
# then store things in the dictionary that will operate on it:
def GaussianRV(mu, sigma):

    def set_mu(obj, mu):
        """Set the 'mu' parameter."""
        obj['_mu'] = mu
    def get_mu(obj):
        """Get the value of the 'mu' parameter."""
        return obj['_mu']
    def set_sigma(obj, sigma):
        """Set the 'sigma' parameter."""
        obj['_sigma'] = sigma
        obj['_var'] = sigma ** 2
        obj['_Z'] = -0.5 * np.log(2 * np.pi * obj['_var'])
    def get_sigma(obj):
        """Get the value of the 'sigma' parameter."""
        return obj['_sigma']
    def initialize(obj, mu, sigma):
        """Initialize parameter values 'mu' and 'sigma' for the random
        variable."""
        obj['set_mu'](obj, mu)
        obj['set_sigma'](obj, sigma)

    # create the variable
    newrv = {}
    # store function definitions
    newrv['set_mu'] = set_mu
    newrv['get_mu'] = get_mu
    newrv['set_sigma'] = set_sigma
    newrv['get_sigma'] = get_sigma
    newrv['initialize'] = initialize
    # initialize it
    newrv['initialize'](newrv, mu, sigma)
    return newrv

rv = GaussianRV(0, 1)
print rv
print "mu is", rv['get_mu'](rv)
print "sigma is", rv['get_sigma'](rv)

# This is a little weird, though -- we have to pass in the object
# every time we call one of the functions that operates on it!  We can
# get around this by using closures.
#
# We don't actually need to change the functions at all; we can create
# a new function called 'bind' that takes in the object and function
# as arguments, and creates a new function which calls the original
# function using the object that was passed in, bypassing the need to
# ever pass in the object again!  We'll call this 'binding', because
# we are explicitly binding the function to that particular object.
def GaussianRV(mu, sigma):

    def bind(obj, func):
        def newfunc(*args, **kwargs):
            return func(obj, *args, **kwargs)
        newfunc.__name__ = func.__name__
        return newfunc

    def set_mu(obj, mu):
        """Set the 'mu' parameter."""
        obj['_mu'] = mu
    def get_mu(obj):
        """Get the value of the 'mu' parameter."""
        return obj['_mu']
    def set_sigma(obj, sigma):
        """Set the 'sigma' parameter."""
        obj['_sigma'] = sigma
        obj['_var'] = sigma ** 2
        obj['_Z'] = -0.5 * np.log(2 * np.pi * obj['_var'])
    def get_sigma(obj):
        """Get the value of the 'sigma' parameter."""
        return obj['_sigma']
    def initialize(obj, mu, sigma):
        """Initialize parameter values 'mu' and 'sigma' for the random
        variable."""
        obj['set_mu'](mu)
        obj['set_sigma'](sigma)
 
    # We don't have to bind all the functions though -- maybe we want
    # a function to create a randomly-parameterized gaussian, that
    # doesn't depend on any particular object:
    def create_random():
        """Randomly parameterize a gaussian random variable."""
        # create the variable
        newrv = {}
        # store function definitions
        newrv['set_mu'] = bind(newrv, set_mu)
        newrv['get_mu'] = bind(newrv, get_mu)
        newrv['set_sigma'] = bind(newrv, set_sigma)
        newrv['get_sigma'] = bind(newrv, get_sigma)
        newrv['initialize'] = bind(newrv, initialize)
        newrv['create_random'] = create_random
        # pick random parameter values
        mu = np.random.rand()
        sigma = np.random.rand()
        # initialize it
        newrv['initialize'](mu, sigma)
        return newrv

    # create the variable
    newrv = {}
    # store function definitions
    newrv['set_mu'] = bind(newrv, set_mu)
    newrv['get_mu'] = bind(newrv, get_mu)
    newrv['set_sigma'] = bind(newrv, set_sigma)
    newrv['get_sigma'] = bind(newrv, get_sigma)
    newrv['initialize'] = bind(newrv, initialize)
    newrv['create_random'] = create_random
    # initialize it
    newrv['initialize'](mu, sigma)
    return newrv

rv = GaussianRV(0, 1)
rand_rv = rv['create_random']()
print rv
print "mu is", rv['get_mu']()
print "sigma is", rv['get_sigma']()
print rand_rv
print "mu is", rand_rv['get_mu']()
print "sigma is", rand_rv['get_sigma']()

# Now imagine we replaced 'obj' with 'self':
def GaussianRV(mu, sigma):

    def bind(self, func):
        def newfunc(*args, **kwargs):
            return func(self, *args, **kwargs)
        newfunc.__name__ = func.__name__
        return newfunc

    def set_mu(self, mu):
        """Set the 'mu' parameter."""
        self['_mu'] = mu
    def get_mu(self):
        """Get the value of the 'mu' parameter."""
        return self['_mu']
    def set_sigma(self, sigma):
        """Set the 'sigma' parameter."""
        self['_sigma'] = sigma
        self['_var'] = sigma ** 2
        self['_Z'] = -0.5 * np.log(2 * np.pi * self['_var'])
    def get_sigma(self):
        """Get the value of the 'sigma' parameter."""
        return self['_sigma']
    def initialize(self, mu, sigma):
        """Initialize parameter values 'mu' and 'sigma' for the random
        variable."""
        self['set_mu'](mu)
        self['set_sigma'](sigma)
 
    def create_random():
        """Randomly parameterize a gaussian random variable."""
        # create the variable
        newrv = {}
        # store function definitions
        newrv['set_mu'] = bind(newrv, set_mu)
        newrv['get_mu'] = bind(newrv, get_mu)
        newrv['set_sigma'] = bind(newrv, set_sigma)
        newrv['get_sigma'] = bind(newrv, get_sigma)
        newrv['initialize'] = bind(newrv, initialize)
        newrv['create_random'] = create_random
        # pick random parameter values
        mu = np.random.rand()
        sigma = np.random.rand()
        # initialize it
        newrv['initialize'](mu, sigma)
        return newrv

    # create the variable
    newrv = {}
    # store function definitions
    newrv['set_mu'] = bind(newrv, set_mu)
    newrv['get_mu'] = bind(newrv, get_mu)
    newrv['set_sigma'] = bind(newrv, set_sigma)
    newrv['get_sigma'] = bind(newrv, get_sigma)
    newrv['initialize'] = bind(newrv, initialize)
    newrv['create_random'] = create_random
    # initialize it
    newrv['initialize'](mu, sigma)
    return newrv

# This is starting to look an awful lot like a class!  Note that there
# isn't anything special about 'self' -- it's just a convention to
# name the variable that refers to the instance object as 'self'.

# Ok, so this is a little impractical because we have to index into a
# dictionary to access all our variables and functions.  That's why
# classes exist -- to make this sort of thing easier.  The following
# code basically does the same thing:
class GaussianRV(object):
    
    def __init__(self, mu, sigma):
        """Initialize parameter values 'mu' and 'sigma' for the random
        variable."""
        self.set_mu(mu)
        self.set_sigma(sigma)

    def set_mu(self, mu):
        """Set the 'mu' parameter."""
        self._mu = mu
    def get_mu(self):
        """Get the value of the 'mu' parameter."""
        return self._mu
    def set_sigma(self, sigma):
        """Set the 'sigma' parameter."""
        self._sigma = sigma
        self._var = sigma ** 2
        self._Z = -0.5 * np.log(2 * np.pi * self._var)
    def get_sigma(self):
        """Get the value of the 'sigma' parameter."""
        return self._sigma

    # This special syntax indicates that the function should not be
    # bound to the instance.  Instead, it takes a class parameter and
    # is bound to the class object!  We'll come back to this later.
    @classmethod
    def create_random(cls):
        """Randomly parameterize a gaussian random variable."""
        mu = np.random.rand()
        sigma = np.random.rand()
        newrv = cls(mu, sigma)
        return newrv
    # We can also have static methods, which do not take any
    # instance/class parameters and are not bound at all -- these act
    # just like functions:
    @staticmethod
    def est_mu(vals, axis=-1):
        mean = np.mean(vals, axis=axis)
        return mean
    @staticmethod
    def est_sigma(vals, axis=-1):
        std = np.std(vals, axis=axis, ddof=1)
        return std


## Classes vs. instances

# Now, let's talk about the differences between class objects and
# instance objects.
classobj = GaussianRV
instanceobj = GaussianRV(0, 1)
print "classobj is a", type(classobj)
print "instanceobj is a", type(instanceobj)
print "Is instanceobj's type equal to classobj?", type(instanceobj) == classobj

# Notice that 'classobj' -- the variable referring to the class itself
# -- is a type of type 'type'.  'instanceobj' -- the variable
# referring to an instance of the class -- is a class of type
# 'GaussianRV'. Essentially, the class itself is a template or list of
# instructions for creating custom objects.  Those objects then have
# type equal to the class.

# A more concrete analogy is that of paperwork.  For example, everyone
# in the US who wants to work has to fill out an I-9.  The type of
# form is like the class -- it contains fields to be filled out, etc.
# Forms filled out by specific people are like instances -- they all
# have the same basic structure, but the data changes from person to
# person, and there can be many copies (instantiations) of the same
# type of form.

# Similarly, we see the same methods in class objects as we do in
# instance objects.  Or, at least, they have the same names, but are
# different objects in memory:
print classobj.get_sigma.__name__
print instanceobj.get_sigma.__name__
print classobj.get_sigma
print instanceobj.get_sigma
print "Are the two 'get_sigma's the same?", classobj.get_sigma == instanceobj.get_sigma

# Notice how the class object method is unbound whereas the instance
# object method is bound.  This is why I used the 'bind' terminology
# earlier with our fake class: it actually refers to cases when the
# methods as associated with a specific object or not.  When creating
# an instance of a class, Python automatically binds all the methods
# for you.  But, if you access them through the class object, they
# won't be bound (it's not even clear what they would be bound to!)
#
# This also implies that methods called through the class object need
# that first 'self' parameter to be passed in:
print instanceobj.get_sigma()         # bound
print classobj.get_sigma(instanceobj) # unbound
