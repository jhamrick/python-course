#!/usr/bin/env python
""" Cocosci scientific Python course, Week 4: Part 1 - Classes"""

import numpy as np

# So far, we've seen a lot of functions.  Let's look at a few more
# that "go together", for example, let's say we wanted some functions
# to work with Gaussian distributions:

def gaussian_sample(mu, sigma, num=1, seed=0):
    """Draw samples from a Gaussian distribution parameterized by
    'mu' and 'sigma'."""
    rand = np.random.RandomState(seed)
    samples = rand.normal(mu, sigma, size=num)
    return samples

def gaussian_logpdf(vals, mu, sigma):
    """Evaluate the Gaussian logpdf (parameterized by 'mu' and
    'sigma') at 'vals'"""
    var = sigma ** 2
    Z = -0.5 * np.log(2 * np.pi * var)
    e = (-(x - mu) ** 2) / (2 * var)
    logpdf = Z + e
    return logpdf

def gaussian_pdf(vals, mu, sigma):
    """Evaluate the Gaussian pdf (parameterized by 'mu' and 'sigma')
    at 'vals'"""
    logpdf = gaussian_logpdf(vals, mu, sigma)
    pdf = np.exp(logpdf)
    return pdf

# However, this isn't necessarily the best solution.  If we're dealing
# with a lot of numbers, but the parameters of the distributions don't
# actually change, we're doing a lot of unnecessary computation when
# evaluating PDFs.  Furthermore, it's a little annoying to have to
# pass in mu and sigma every single time.


## Introduction to classes

# The solution to this is to use classes.  Classes can be thought of
# as instructions for how a particular "thing" should be handled and
# modified.  In the case of our distribution, we want a set of
# instructions that specifies how to sample, evaluate, and estimate
# the parameters of a Gaussian-distributed random variable.

# A second concept to understand is that of objects.  If classes
# specify instructions for how to deal with "things", then objects (or
# "instances" of a class) are said things.  A little more concretely:
# if we have a class to describe a Gaussian random variable, then an
# object (or instance of the class) is a /specific/ Gaussian random
# variable.

# Classes always begin with this invocation:
#     class MyClassName(object):
# The 'object' here is a special Python thing that basically specifies
# the default functionality for any class.  You don't worry about it
# too much for now -- just remember to always put it there in the
# paretheses.
class GaussianRV(object):

    # Classes also always have a special '__init__' function, which
    # specifies what to do to create an object/instance of the class.
    # In our case, we want to create a Gaussian random variable, so we
    # want to take in parameters for mu and sigma and then
    # store them.
    #
    # Note that there's also this 'self' parameter -- this is (almost)
    # always required as the first argument for a function in a class,
    # and it refers to the object that is currently being operated on.
    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

# Ok, that's a class!  It doesn't do much yet except act like a
# container for mu and sigma:
rv = GaussianRV(0, 1) # create a standard normal RV
print "rv is", rv
print "What is the mean of the random variable?", rv.mu
print "What is the stddev of the random variable?", rv.sigma

# Let's create a second standard normal:
rv2 = GaussianRV(0, 1)
print "rv2 is", rv2
print "Is the first RV the same as the second?", rv == rv2

# We can modify the objects post-creation, too:
rv.mu = 3
rv2.sigma = 5
print "rv's mu is now", rv.mu
print "rv2's sigma is now", rv2.sigma

# This can sometimes be dangerous, especially if you make new
# variables pointing to the same object:
rv3 = rv
print "rv3 is", rv3
print "rv is", rv
print "Are rv and rv3 the same?", rv == rv3
print "rv's sigma is", rv.sigma
rv3.sigma = 2
print "rv's sigma is", rv.sigma


## Methods

# Ok, so that wasn't a very interesting class.  Let's put some of our
# functions in it, which was our original goal.

# (Side note: functions which are in a class are typically called
# 'methods', to make it clear that they're not just standalone
# functions.)

class GaussianRV(object):

    def __init__(self, mu, sigma, seed=0):
        self.seed = seed
        self.rand = np.random.RandomState(self.seed)

        # These are methods of the class, defined below.  This is an
        # interesting thing about classes, too -- definition order
        # doesn't matter.  You can have method A call method B, but
        # define A before B, and everything will still work!
        self.set_mu(mu)
        self.set_sigma(sigma)

    # Remember the 'Z' variable in the gaussian_logpdf function?
    # Because we're storing mu and sigma, it doesn't make sense to
    # recompute this constant every time we want to evaluate the pdf.
    # So, let's just create a function to compute it.
    def _calc_Z(self):
        """Calculate the constant for the logpdf"""
        self._Z = -0.5 * np.log(2 * np.pi * self._var)

    # We might want to be able to change the mu and sigma parameters
    # -- but because changing sigma will also cause the constant to
    # change, we create functions for setting these values that will
    # take care of those extra calculations:
    def set_mu(self, mu):
        """Set the value of mu"""
        self.mu = mu
    def set_sigma(self, sigma):
        """Set the value of sigma"""
        self.sigma = sigma
        self._var = self.sigma ** 2
        self._calc_Z()

    # Note that I sometimes prefix methods and variables with an
    # underscore -- this is a Python convention that means "private".
    # In other words, these are special functions/variables that we
    # only want used internally in the class.  You should avoid doing:
    #
    # obj = GaussianRV(0, 1)
    # obj._Z = 5
    #
    # Because this will cause unexpected behavior from the objects'
    # methods!

    # Now, onto our original functions. Note what changes with these
    # methods: first, we don't need the mu and sigma parameters
    # because we're already storing them in the class!  Second, we
    # have to add the 'self' parameter as the first parameter for all
    # of these functions.  This gives us access to variables in the
    # object we're dealing with. Third, I removed the 'gaussian_'
    # prefix because it's redundant if the function is a method in a
    # GaussianRV class!
    def sample(self, num=1):
        """Draw samples from the distribution"""
        samples = self.rand.normal(
            self.mu, self.sigma, size=num)
        return samples

    def logpdf(self, vals):
        """Evaluate the the logpdf at 'vals'"""
        logpdf = self._Z - (((vals - self.mu) ** 2) / (2 * self._var))
        return logpdf

    def pdf(self, vals):
        """Evaluate the pdf at 'vals'"""
        pdf = np.exp(self.logpdf(vals))
        return pdf


# Let's create some new instances:
rv = GaussianRV(0, 1)
rv2 = GaussianRV(2, 3)
print "rv is", rv, "and has mu", rv.mu, "and sigma", rv.sigma
print "rv2 is", rv2, "and has mu", rv2.mu, "and sigma", rv2.sigma

# Sample some numbers:
rv_samps = rv.sample(100000)
rv2_samps = rv2.sample(100000)
print "samples from rv:", rv_samps
print "samples from rv2:", rv2_samps

# Evaluate the pdf over a range of numbers:
X = np.linspace(-10, 10, 1000)
rv_pdf = rv.pdf(X)
rv2_pdf = rv2.pdf(X)

# Let's do a sanity check by looking at a histogram of the samples
# overlayed with the calculated PDF to make sure our distributions
# look approximately correct:
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.hist(rv_samps,
         normed=True, bins=100,
         histtype='stepfilled', label='samples')
ax1.plot(X, rv_pdf, 'r-', linewidth=2, label='pdf')
ax2.hist(rv2_samps,
         normed=True, bins=100,
         histtype='stepfilled', label='samples')
ax2.plot(X, rv2_pdf, 'r-', linewidth=2, label='pdf')
ax1.set_ylim(0, 0.5)
ax1.set_xlim(-10, 10)
ax1.set_title("rv")
ax2.set_ylim(0, 0.5)
ax2.set_xlim(-10, 10)
ax2.set_title("rv2")
ax1.legend()
ax2.legend()

# It was pretty useful to be able to plot that for a sanity check --
# why don't we add that functionality as another method of the class?
# Then, in the future, we won't have to repeat this plotting code.

class GaussianRV(object):

    def __init__(self, mu, sigma, seed=0):
        self.seed = seed
        self.rand = np.random.RandomState(self.seed)
        self.set_mu(mu)
        self.set_sigma(sigma)

    def _calc_Z(self):
        """Calculate the constant for the logpdf"""
        self._Z = -0.5 * np.log(2 * np.pi * self._var)

    def set_mu(self, mu):
        """Set the value of mu"""
        self.mu = mu
    def set_sigma(self, sigma):
        """Set the value of sigma"""
        self.sigma = sigma
        # Also calculate the variance and the Z constant
        self._var = self.sigma ** 2
        self._calc_Z()

    def sample(self, num=1):
        """Draw samples from the distribution"""
        samples = self.rand.normal(
            self.mu, self.sigma, size=num)
        return samples

    def logpdf(self, vals):
        """Evaluate the the logpdf at 'vals'"""
        logpdf = self._Z - (((vals - self.mu) ** 2) / (2 * self._var))
        return logpdf

    def pdf(self, vals):
        """Evaluate the pdf at 'vals'"""
        pdf = np.exp(self.logpdf(vals))
        return pdf

    def plot(self):
        # draw some samples
        samps = self.sample(100000)
        # create a range of values spanning 4 standard deviations on
        # either side of mu
        X = self.mu + np.linspace(-4*self.sigma, 4*self.sigma, 1000)
        # calculate the pdf for these values
        pdf = self.pdf(X)
        # plot a histogram of the samples
        plt.hist(samps,
                 normed=True, bins=100,
                 histtype='stepfilled',
                 label='samples (mu=%s, sigma=%s)' % (self.mu, self.sigma))
        # plot the pdf on top of the histogram
        plt.plot(X, pdf, 'r-', linewidth=2,
                 label='pdf (mu=%s, sigma=%s)' % (self.mu, self.sigma))

# And now let's recreate our variables and plot them using the class
# method:
rv = GaussianRV(0, 1)
rv2 = GaussianRV(2, 3)
plt.clf()
rv.plot()
rv2.plot()
plt.legend()

## Inheritance

# Classes can "inherit" from each other.  This means that that the
# child class has, by default, all of the same variables and methods
# as the parent class.  This is another handy way of avoiding the
# reuse of code -- for example, if we want a specific class for the
# standard normal, we can use the GaussianRV class we've already
# created, but "override" the initialization function so we can
# specify the standard normal parameters.

# Remember the 'object'?  We're now replacing that with the name of
# the parent class (now it's more obvious why we needed 'object' --
# our class was inheriting from 'object' and that's how it got all the
# default Python functionality!)
class StandardNormalRV(GaussianRV):

    def __init__(self, seed=0):
        # Here, we are calling the __init__ function directly from the
        # /class/, not the object, so we have to explicitly specify
        # the 'self' parameter.  Basically, this is saying "don't use
        # my default __init__ method, use the one from GaussianRV and
        # make it modify myself".
        GaussianRV.__init__(self, 0, 1, seed=seed)

        # We can also modify the defaults -- for example, we no longer
        # want to be able to set mu and sigma, so we'll just set those
        # functions to None.  Then, if anyone tries to call them, an
        # error will be thrown.
        self.set_mu = None
        self.set_sigma = None

# Now, it's much easier to create standard normal random variables:
rv1 = GaussianRV(0, 1)
rv2 = StandardNormalRV()

# We can check the type of these objects using 'isinstance', which is
# a Python builtin that checks the entire inheritance hierarchy.  So,
# although we created rv2 as a StandardNormalRV, it is /also/ an
# instance of GaussianRV because StandardNormalRV inherits from
# GaussianRV.
print "Is rv1 a GaussianRV?       ", isinstance(rv1, GaussianRV)
print "Is rv1 a StandardNormalRV? ", isinstance(rv1, StandardNormalRV)
print "Is rv2 a GaussianRV?       ", isinstance(rv2, GaussianRV)
print "Is rv2 a StandardNormalRV? ", isinstance(rv2, StandardNormalRV)

# For a much more detailed and thorough explanation of how inheritance
# works (and basic classes in general), see:
# http://jhamrick.mit.edu/2011/05/18/an-introduction-to-classes-and-inheritance-in-python/


## Magic built-in methods

# For the last class-related topic, we're going to briefly go over
# built-in methods.  These are special methods defined by Python that
# let create more flexible classes and objects.  For example, if you
# want to:
#
#   - change the way the object is displayed when you run "print obj"
#   - add/subtract/multiply two objects
#   - "index" into an object, like you would a dictionary
#   - define an ordering for objects
#   - pickle an object
#
# You need magic methods!  We're only going to go over the first two
# examples here, but you should take a look at the following website,
# which explains how /all/ the magic methods work:
# http://www.rafekettler.com/magicmethods.html
#
# All magic methods are prefixed and suffixed by the double
# underscore.  Remember the __init__ method?  That's a magic method,
# too!

# So, currently when we print an object, we see the type and its
# memory address:
print rv

# Let's change this so we can actually see the parameters of the
# distribution.  To do this, we need to define a __str__ method.  This
# method should return a string; this is what Python will display when
# 'print' is used.

# We might also want to add/subtract/multiply Gaussians -- this is one
# of the really nice parts of Python.  We can make our random
# variables act exactly how they should in a completely transparent
# manner, e.g.:
# rv1 = GaussianRV(0, 1)
# rv2 = GaussianRV(1, 2)
# rv3 = rv1 * rv2

# To do this, we need to implement the __mul__ method.  We'll also go
# ahead and implement __imul__, __add__, __iadd__, __sub__, and
# __isub__, __div__, and __idiv__.

# The __iadd__, __isub__, etc. methods don't return a new object; they
# actually act on the object itself, e.g.:
# a = 5
# a += 2 # __iadd__ is invoked, now a = 7

class GaussianRV(object):

    def __init__(self, mu, sigma, seed=0):
        self.seed = seed
        self.rand = np.random.RandomState(self.seed)
        self.set_mu(mu)
        self.set_sigma(sigma)

    def _calc_Z(self):
        """Calculate the constant for the logpdf"""
        self._Z = -0.5 * np.log(2 * np.pi * self._var)

    def set_mu(self, mu):
        """Set the value of mu"""
        self.mu = mu
    def set_sigma(self, sigma):
        """Set the value of sigma"""
        self.sigma = sigma
        # Also calculate the variance and the Z constant
        self._var = self.sigma ** 2
        self._calc_Z()

    def sample(self, num=1):
        """Draw samples from the distribution"""
        samples = self.rand.normal(
            self.mu, self.sigma, size=num)
        return samples

    def logpdf(self, vals):
        """Evaluate the the logpdf at 'vals'"""
        logpdf = self._Z - (((vals - self.mu) ** 2) / (2 * self._var))
        return logpdf

    def pdf(self, vals):
        """Evaluate the pdf at 'vals'"""
        pdf = np.exp(self.logpdf(vals))
        return pdf

    def plot(self):
        # draw some samples
        samps = self.sample(100000)
        # create a range of values spanning 4 standard deviations on
        # either side of mu
        X = self.mu + np.linspace(-4*self.sigma, 4*self.sigma, 1000)
        # calculate the pdf for these values
        pdf = self.pdf(X)
        # plot a histogram of the samples
        plt.hist(samps,
                 normed=True, bins=100,
                 histtype='stepfilled',
                 label='samples (mu=%s, sigma=%s)' % (self.mu, self.sigma))
        # plot the pdf on top of the histogram
        plt.plot(X, pdf, 'r-', linewidth=2,
                 label='pdf (mu=%s, sigma=%s)' % (self.mu, self.sigma))

    def __str__(self):
        """String representation of the GaussianRV"""
        mytype = type(self).__name__
        s = "<%s; mu=%s; sigma=%s>" % (mytype, self.mu, self.sigma)
        return s

    def __add__(self, other):
        """Create a new GaussianRV with mu=mu+other"""
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu + other,
                self.sigma,
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv

    def __iadd__(self, other):
        """Shift mu=mu+other"""
        if isinstance(other, (int, float)):
            self.set_mu(self.mu + other)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self

    def __sub__(self, other):
        """Create a new GaussianRV with mu=mu-other"""
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu - other,
                self.sigma,
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv

    def __isub__(self, other):
        """Shift mu=mu-other"""
        if isinstance(other, (int, float)):
            self.set_mu(self.mu - other)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self

    def __mul__(self, other):
        """Create a new GaussianRV, either by multiplying the mean and
        standard deviation by 'other' or by computing the product of
        two Gaussians:

        https://ccrma.stanford.edu/~jos/sasp/Product_Two_Gaussian_PDFs.html

        """
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu*other,
                self.sigma*other,
                seed=self.seed)
        elif isinstance(other, GaussianRV):
            m0 = float(self.mu)
            m1 = float(other.mu)
            v0 = float(self._var)
            v1 = float(other._var)
            new_m = (m0 * v1 + m1 * v0) / (v0 + v1)
            new_v = v0 * v1 / (v0 + v1)
            new_rv = GaussianRV(
                new_m,
                np.sqrt(new_v),
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv
        
    def __imul__(self, other):
        """Multiply the mean and standard deviation by 'other' or
        compute the product of two Gaussians:

        https://ccrma.stanford.edu/~jos/sasp/Product_Two_Gaussian_PDFs.html

        """
        if isinstance(other, (int, float)):
            self.set_mu(self.mu * other)
            self.set_sigma(self.sigma * other)
        elif isinstance(other, GaussianRV):
            m0 = float(self.mu)
            m1 = float(other.mu)
            v0 = float(self._var)
            v1 = float(other._var)
            new_m = (m0 * v1 + m1 * v0) / (v0 + v1)
            new_v = v0 * v1 / (v0 + v1)
            self.set_mu(new_m)
            self.set_sigma(np.sqrt(new_v))
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self

    def __div__(self, other):
        """Create a new GaussianRV by dividing the mean and variance
        by 'other'.

        """
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu / other,
                self.sigma / other,
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv

    def __idiv__(self, other):
        """Divide the mean and standard deviation by 'other'."""
        if isinstance(other, (int, float)):
            self.set_mu(self.mu / other)
            self.set_sigma(self.sigma / other)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self

# Now let's see how these magic methods all work:
rv1 = GaussianRV(0, 1)
rv2 = GaussianRV(2, 3)
# use __str__
print "rv1:", rv1
print "rv2:",rv2

# use __mul__
rv3 = rv1 * rv2
rv4 = rv1 * 5
print "rv1 * rv2:", rv3
print "rv1 * 5:", rv4
# use __add__
rv5 = rv1 + 1
print "rv1 + 1:", rv5
# use __sub__
rv6 = rv1 - 3
print "rv1 - 3:", rv6
# use __idiv__
rv6 /= 2.
print "rv6:", rv6

plt.clf()
rv1.plot()
rv2.plot()
rv3.plot()
plt.legend()

# That's all we're going to cover about classes for now, but there are
# many more complex/advanced things that you can do with classes.  It
# would take too long even to explain what they are, so I'm just going
# to give you the topic names and some useful links if you want to
# learn more about them.  You may not even want to look at them yet,
# but once you're very comfortable with python, knowing how to use
# these things can be very useful!
#
#   - decorators:
#        decorators.py, in this folder
#        http://pythonconquerstheuniverse.wordpress.com/2012/04/29/python-decorators/
#        (skip to "The right way to explain decorators")
#        http://www.artima.com/weblogs/viewpost.jsp?thread=240808
#        http://www.artima.com/weblogs/viewpost.jsp?thread=240845
#
#   - properties:
#        http://adam.gomaa.us/blog/2008/aug/11/the-python-property-builtin/
#
#   - static methods and class methods
#        http://stackoverflow.com/questions/136097/what-is-the-difference-between-staticmethod-and-classmethod-in-python
#        (second answer)
#
#   - monkeypatching, bound, and unbound methods
#        http://stackoverflow.com/questions/114214/class-method-differences-in-python-bound-unbound-and-static
#        monkeypatching.py, in this folder
#        http://en.wikipedia.org/wiki/Monkey_patch





class GaussianRV(object):
    """Gaussian distributed random variable"""

    def __init__(self, mu, sigma, seed=0):
        self.seed = seed
        self.rand = np.random.RandomState(self.seed)
        self.mu = mu # equivalent to self.set_mu(mu)
        self.sigma = sigma # equivalent to self.set_sigma(sigma)
        

    def _calc_Z(self):
        """Calculate the constant for the logpdf"""
        self._Z = -0.5 * np.log(2 * np.pi * self._var)

    def get_mu(self):
        return self._mu
    def set_mu(self, mu):
        """Set the value of mu"""
        self._mu = mu
    def get_sigma(self):
        return self._sigma
    def set_sigma(self, sigma):
        """Set the value of sigma"""
        self._sigma = sigma
        # Also calculate the variance and the Z constant
        self._var = self.sigma ** 2
        self._calc_Z()

    mu = property(get_mu, set_mu, doc="mu parameter")
    sigma = property(get_sigma, set_sigma, doc="sigma parameter")

    def sample(self, num=1):
        """Draw samples from the distribution"""
        samples = self.rand.normal(
            self.mu, self.sigma, size=num)
        return samples

    def logpdf(self, vals):
        """Evaluate the the logpdf at 'vals'"""
        logpdf = self._Z - (((vals - self.mu) ** 2) / (2 * self._var))
        return logpdf

    def pdf(self, vals):
        """Evaluate the pdf at 'vals'"""
        pdf = np.exp(self.logpdf(vals))
        return pdf

    def plot(self):
        # draw some samples
        samps = self.sample(100000)
        # create a range of values spanning 4 standard deviations on
        # either side of mu
        X = self.mu + np.linspace(-4*self.sigma, 4*self.sigma, 1000)
        # calculate the pdf for these values
        pdf = self.pdf(X)
        # plot a histogram of the samples
        plt.hist(samps,
                 normed=True, bins=100,
                 histtype='stepfilled',
                 label='samples (mu=%s, sigma=%s)' % (self.mu, self.sigma))
        # plot the pdf on top of the histogram
        plt.plot(X, pdf, 'r-', linewidth=2,
                 label='pdf (mu=%s, sigma=%s)' % (self.mu, self.sigma))

    def __str__(self):
        """String representation of the GaussianRV"""
        mytype = type(self).__name__
        s = "<%s; mu=%s; sigma=%s>" % (mytype, self.mu, self.sigma)
        return s

    def __add__(self, other):
        """Create a new GaussianRV with mu=mu+other"""
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu + other,
                self.sigma,
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv

    def __iadd__(self, other):
        """Shift mu=mu+other"""
        if isinstance(other, (int, float)):
            self.set_mu(self.mu + other)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self

    def __sub__(self, other):
        """Create a new GaussianRV with mu=mu-other"""
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu - other,
                self.sigma,
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv

    def __isub__(self, other):
        """Shift mu=mu-other"""
        if isinstance(other, (int, float)):
            self.set_mu(self.mu - other)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self

    def __mul__(self, other):
        """Create a new GaussianRV, either by multiplying the mean and
        standard deviation by 'other' or by computing the product of
        two Gaussians:

        https://ccrma.stanford.edu/~jos/sasp/Product_Two_Gaussian_PDFs.html

        """
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu*other,
                self.sigma*other,
                seed=self.seed)
        elif isinstance(other, GaussianRV):
            m0 = float(self.mu)
            m1 = float(other.mu)
            v0 = float(self._var)
            v1 = float(other._var)
            new_m = (m0 * v1 + m1 * v0) / (v0 + v1)
            new_v = v0 * v1 / (v0 + v1)
            new_rv = GaussianRV(
                new_m,
                np.sqrt(new_v),
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv
        
    def __imul__(self, other):
        """Multiply the mean and standard deviation by 'other' or
        compute the product of two Gaussians:

        https://ccrma.stanford.edu/~jos/sasp/Product_Two_Gaussian_PDFs.html

        """
        if isinstance(other, (int, float)):
            self.set_mu(self.mu * other)
            self.set_sigma(self.sigma * other)
        elif isinstance(other, GaussianRV):
            m0 = float(self.mu)
            m1 = float(other.mu)
            v0 = float(self._var)
            v1 = float(other._var)
            new_m = (m0 * v1 + m1 * v0) / (v0 + v1)
            new_v = v0 * v1 / (v0 + v1)
            self.set_mu(new_m)
            self.set_sigma(np.sqrt(new_v))
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self

    def __div__(self, other):
        """Create a new GaussianRV by dividing the mean and variance
        by 'other'.

        """
        if isinstance(other, (int, float)):
            new_rv = GaussianRV(
                self.mu / other,
                self.sigma / other,
                seed=self.seed)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return new_rv

    def __idiv__(self, other):
        """Divide the mean and standard deviation by 'other'."""
        if isinstance(other, (int, float)):
            self.set_mu(self.mu / other)
            self.set_sigma(self.sigma / other)
        else:
            raise ValueError(
                "'other' is a %s" % type(other).__name__)
        return self



class Foo(object):
    @staticmethod
    def do_something():
        print "I am doing something!"
