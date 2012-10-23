class Fibonacci(object):

    _allfibs = [0, 1]

    def __init__(self, ifib):

        if len(self._allfibs) <= ifib:
            for i in xrange(len(self._allfibs), ifib+1):
                self._allfibs.append(self._allfibs[i-1] + self._allfibs[i-2])

        self.val = self._allfibs[ifib]
        self.index = ifib

    def __repr__(self):
        return str(self.val)

    def __str__(self):
        return str(self.val)

    def __add__(self, other):
        return self.val + other

    def __radd__(self, other):
        return other + self.val

    def __mul__(self, other):
        return self.val * other

    def __rmul__(self, other):
        return other * self.val

    def __sub__(self, other):
        return self.val - other

    def __rsub__(self, other):
        return other - self.val

    def __pow__(self, other):
        return self.val ** other

    def __rpow__(self, other):
        return other ** self.val

if __name__ == '__main__':
    fib = Fibonacci(1)
    print fib
    fib = Fibonacci(10)
    print fib

    # look, all the fibonaccis up to 10
    print fib._allfibs

    # these are the magic methods we implemented
    print "sub", fib - 1
    print "rsub", 1 - fib
    print "add", fib + 1
    print "radd", 1 + fib
    print "pow", fib ** 2
    print "rpow", 2 ** fib
    print "mul", fib * 2
    print "rmul", 2 * fib

    # throws an error, because this isn't implemented
    print "neg", -fib

    # a better way to do this would have been to subclass Integer -- then we
    # wouldn't have to write the magic methods ourselves
