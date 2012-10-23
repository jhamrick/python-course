""" Example of a buggy module, for demonstrating 'pdb'."""

def func1(X):
    Z = 5 * Y
    # There is a bug here -- Y is not defined
    return Z

def func2(X):
    import pdb
    pdb.set_trace()
    Z = 5 * Y
    return Z

def func3():
    W = func1(10)
    return W

