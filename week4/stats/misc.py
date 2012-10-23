import numpy as np


def normalize(logarr, axis=-1, max_log_value=709.78271289338397):
    """Normalize an array of log-values along an axis.  Returns a
    tuple of (normalization constants, normalized array), where both
    values are again in logspace.

    This function is useful for values that are in danger of
    underflowing when exponentiated.  It circumvents this problem by
    shifting all the values and normalizing by a shifted normalization
    constant.

    Parameters
    ----------
    logarr : array-like
        An array of values in log-space.
    axis : int (default=-1)
        The axis along which to normalize the values.
    max_log_value : float (default=709.78)
        The maximum value that can be exponentiated without causing an
        overflow exception.

    """

    # shape for the normalization constants (that would otherwise be
    # missing axis)
    shape = list(logarr.shape)
    shape[axis] = 1
    # get maximum value of array
    maxlogarr = np.max(logarr, axis=axis).reshape(shape)
    # calculate how much to shift the array up by
    shift = (max_log_value - maxlogarr - 2 - logarr.shape[axis])
    # shift the array
    unnormed = logarr + shift
    # convert from logspace
    arr = np.exp(unnormed)
    # calculate shifted log normalization constants
    _lognormconsts = np.log(np.sum(arr, axis=axis)).reshape(shape)
    # calculate normalized array
    lognormarr = unnormed - _lognormconsts
    # unshift normalization constants
    _lognormconsts -= shift
    # get rid of the dimension we normalized over
    lognormconsts = np.sum(_lognormconsts, axis=axis)

    return lognormconsts, lognormarr
