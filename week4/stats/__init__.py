"""A general statistics package.

"""

# import the circular statistics module
import circ
# import the normalize function from the misc module
from misc import normalize
# create a random state for the stats package
import numpy as np
rand = np.random.RandomState(0)

# import the random variables package
import rvs

# Specify which of these things are "officially" part of the stats
# package.  These things must have previously been imported; i.e.,
# they must exist in the current namespace.
__all__ = ['circ', 'rvs', 'rand', 'normalize', 'other_stuff']
