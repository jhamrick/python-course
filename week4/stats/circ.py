"""Module containing circular statistics functions, including resvec,
mean, var, and std.

"""

__all__ = ['resvec', 'mean', 'var', 'std']

import numpy as np

def resvec(vals, axis=None):
    """Calculate the mean resultant vector length for circular data.

    Parameters
    ----------
    vals : array-like
        The array of angles
    axis : int (default=None)
        The axis along which to take the mean

    Returns
    -------
    out : np.ndarray
        The resulting numpy array of resultant vector lengths

    References
    ----------
    http://www.jstatsoft.org/v31/i10

    """
    
    alpha = np.array(vals, dtype='f8')
    # sum of cos & sin angles
    t = np.exp(1j * alpha)
    r = np.sum(t, axis=axis)
    # obtain length 
    r = np.abs(r) / alpha.shape[axis]
    return r    

def mean(vals, axis=None):
    """Calculate the mean of an array of angles using circular
    statistics.

    Parameters
    ----------
    vals : array-like
        The array of angles
    axis : int (default=None)
        The axis along which to take the mean

    Returns
    -------
    out : np.ndarray
        The resulting numpy array of means

    References
    ----------
    http://www.jstatsoft.org/v31/i10

    """

    alpha = np.array(vals, dtype='f8')
    # sum of cos & sin angles
    t = np.exp(1j * alpha)
    r = np.sum(t, axis=axis)
    # obtain mean
    mu = np.angle(r) % (2.*np.pi)                        
    return mu

def var(vals, axis=None):
    """Computes circular variance for circular data.

    Parameters
    ----------
    vals : array-like
        The array of angles
    axis : int (default=None)
        The axis along which to take the variance

    Returns
    -------
    out : np.ndarray
        The calculated circular variance

    References
    ----------
    http://www.jstatsoft.org/v31/i10

    """

    alpha = np.array(vals, dtype='f8')
    var = 1. - resvec(alpha, axis=axis)
    return var

def std(vals, axis=None):
    """Computes circular standard deviation for circular data.

    Parameters
    ----------
    vals : array-like
        The array of angles
    axis : int (default=None)
        The axis along which to take the standard deviation

    Returns
    -------
    out : np.ndarray
        The calculated circular standard deviation

    References
    ----------
    http://www.jstatsoft.org/v31/i10
    http://en.wikipedia.org/wiki/Directional_statistics#Measures_of_location_and_spread

    """

    var = var(vals, axis=axis)
    std = np.sqrt(-2*np.log(1 - var))
    return std
