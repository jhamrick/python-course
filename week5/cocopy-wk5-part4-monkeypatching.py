#!/usr/bin/env python
""" Cocosci scientific Python course, Week 5: Part 4 - Monkeypatching"""

import numpy as np

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

# Now that you know what bound/unbound methods are, I can explain
# monkeypatching.  Monkeypatching isn't that complicated, it literally
# just is adding variables/functions/methods to an object after the
# fact.  With variables, it's very straightforward:
rv = GaussianRV(0, 1)
rv.foo = 'bar'
print rv.foo

# With functions, too, very straightforward:
def bar():
    print "Hello, world!"
rv.bar = bar
rv.bar()

# With methods, however, we have to keep in mind bound vs. unbound
# constraints.  For example, we can't just create a method like this:
def sample(self, size=None):
    samps = np.random.normal(self.get_mu(), self.get_sigma(), size=size)
    return samps
rv.sample = sample
print rv.sample()

# We have to do:
print rv.sample(rv)

# Why?  Because technically, the 'sample' method isn't a method --
# it's just a function that is also an attribute of an instance
# object.  To make it a method, we have to explicitly bind it:
rv.sample = sample.__get__(rv)
print rv.sample()

# This __get__ method of function objects is essentially the same as
# the 'bind' function we defined above: it takes in an object and
# produces a new function that doesn't require the object to be passed
# in.

# Another way we could do this would be to monkeypatch the function
# into the class itself, and then recreate our variable:
GaussianRV.sample = sample
rv = GaussianRV(0, 1)
print rv.sample()

# This works because when the object is created, Python goes through
# and tries to bind all methods that are attributes of the class.
# This is also why we needed that special '@staticmethod' syntax
# earlier: otherwise, Python would try to bind the method, which would
# fail because we didn't give it enough arguments.

# So, because the difference between static methods and bound methods
# and unbound methods, etc., can get a little confusing, we'll make
# the distinction clear by using 'instance variable/method' (e.g., any
# bound method, variables defined in __init__) vs. 'class
# variable/method' (unbound methods, class methods, variables defined
# in the class definition itself) vs. 'functions' (static methods,
# functions).

class GaussianRV(object):

    # class variable, because it is defined in the class definition
    rand = np.random.RandomState(0)

    # instance methods, because they take the object as the first
    # parameter and will be bound upon instance creation
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

    def sample(self, size=None):
        samps = self.rand.normal(
            self.get_mu(), self.get_sigma(), size=size)
        return samps

    # class method, because it takes a type as the first parameter
    # which is the type of the class -- like 'self', this will
    # automatically be passed in.  Why would we want a class method
    # instead of a static method here?  Imagine if we created a
    # subclass (e.g., NamedGaussianRV, which additionally has a name
    # associated with it).  Then we might not need to override
    # create_random, but we would want the new variable to be a
    # NamedGaussianRV.  Because the class is passed in here, that's
    # possible!
    @classmethod
    def create_random(cls):
        """Randomly parameterize a gaussian random variable."""
        mu = np.random.rand()
        sigma = np.random.rand()
        newrv = cls(mu, sigma)
        return newrv
    
    # static methods, or functions, because they are not bound
    @staticmethod
    def est_mu(vals, axis=-1):
        mean = np.mean(vals, axis=axis)
        return mean
    @staticmethod
    def est_sigma(vals, axis=-1):
        std = np.std(vals, axis=axis, ddof=1)
        return std


rv = GaussianRV(0, 1)
rv2 = rv.create_random()
samps = rv2.sample(100000)
mu = GaussianRV.est_mu(samps)
sigma = GaussianRV.est_sigma(samps)
print rv2.get_mu(), mu
print rv2.get_sigma(), sigma


# Monkeypatching is typically regarded as bad coding practice, but
# there are definitely uses for it.  For example, if we have a class
# that represents some entity (like a dog), we might want to "teach"
# it new things:

class Dog(object):

    def __init__(self, name):
        self.name = name
        self.skills = []

    def teachSkill(self, skillname, skill):
        setattr(self, skillname, skill.__get__(self))

    def __str__(self):
        return self.name

def bark(self):
    print "woof!"

rover = Dog("Rover")
print rover
rover.teachSkill("bark", bark)
rover.bark()
