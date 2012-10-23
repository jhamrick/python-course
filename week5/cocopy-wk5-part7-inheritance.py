#!/usr/bin/env python
""" Cocosci scientific Python course, Week 5: Part 7 - Inheritance"""

# Let's return to inheritance, because there's more to it than what
# we covered last week.  First, a quick review:

# parent class
class GaussianRV(object):

    rand = np.random.RandomState(0)

    def __init__(self, mu, sigma):
        """Initialize parameter values 'mu' and 'sigma' for the random
        variable."""
        self.mu = mu
        self.sigma = sigma

    @property
    def mu(self):
        """Get the value of the 'mu' parameter."""
        return self._mu
    @mu.setter
    def mu(self, mu):
        """Set the 'mu' parameter."""
        self._mu = mu

    @property
    def sigma(self):
        """Get the value of the 'sigma' parameter."""
        return self._sigma
    @sigma.setter
    def sigma(self, sigma):
        """Set the 'sigma' parameter."""
        self._sigma = sigma
        self._var = sigma ** 2
        self._Z = -0.5 * np.log(2 * np.pi * self._var)

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

# child class
class StandardNormalRV(GaussianRV):

    def __init__(self):
        # Access the descriptor set methods from the parent directly
        # to set these variables initially.  We can't do 'self.mu = 0'
        # because we're overriding those properties to not have setter
        # methods.
        GaussianRV.mu.__set__(self, 0)
        GaussianRV.sigma.__set__(self, 1)

    # Recreate the 'mu' and 'sigma' properties to only have get
    # methods.
    def set_mu(self, val):
        raise NotImplementedError
    mu = property(GaussianRV.mu.__get__, set_mu)
    sigma = property(GaussianRV.sigma.__get__)

rv = GaussianRV(0, 1)
sn = StandardNormalRV()

print "rv:", rv.mu, rv.sigma
print "sb:", sn.mu, sn.sigma
rv.mu = 10
sn.mu = 10 # AttributeError: can't set attribute

# Note that we didn't override the 'create_random' method.  This will
# throw an error, because it's trying to pass in the 'mu' and 'sigma'
# arguments to the StandardNormalRV constructor, which takes no
# arguments.
sn2 = sn.create_random()

# But we can use 'sample' -- this is why inheritance can be useful:
samps = sn.sample(1000000)
print sn.mu, sn.est_mu(samps)
print sn.sigma, sn.est_sigma(samps)

## Multiple inheritance

# You can also have multiple inheritance in Python.  I personally
# don't find much use for this, but here's an example of something you
# could do:

class Cat(object):

    def __init__(self, name):
        self.name = "cat %s" % name

    def speak(self):
        return "meow"

    def climbTree(self):
        return "%s is in a tree!" % self.name

class Dog(object):
    def __init__(self, name):
        self.name = "dog %s" % name

    def speak(self):
        return "woof"

    def chaseCat(self):
        return "%s is chasing a cat!" % self.name

class CatDog(Cat, Dog):

    def speak(self, cls):
        return super(cls, self).speak()

class DogCat(Dog, Cat):

    def speak(self, cls):
        return super(cls, self).speak()

# resolution order is 'Cat' and then 'Dog' -- so this uses
# Cat.__init__:
fluffy = CatDog('Fluffy')
print fluffy.name
# But this uses dog.__init__:
scruffy = DogCat('Scruffy')
print scruffy.name

# Both have inherited methods from Cat and Dog:
print fluffy.climbTree()
print fluffy.chaseCat()
print scruffy.climbTree()
print scruffy.chaseCat()

# We can specify how we want to resolve inheritance conflicts: for
# example, Cat and Dog both have 'speak' methods.  We can take a look
# at the resolution order for CatDog (mro stands for 'method
# resolution order'):
print "resolution order for CatDog:", CatDog.__mro__
# And so we can specify at what point in this hierarchy we want to
# start looking for the relevant method.
print fluffy.speak(CatDog) # uses Cat.speak
print fluffy.speak(Cat)    # uses Dog.speak
print fluffy.speak(Dog)    # error, object doesn't have a speak method
