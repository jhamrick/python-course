#-------------------------------------------------------------------------------
# if statements -- a way of doing different things depending on the condition.
# For example, let's say we need to compare two numbers (play around with
# changing x and y and see how that effects the value of 'compare'):

x = 2
y = 3
if x == y:
    print "x equals y"
elif x > y:
    print "x is greater than y"
else:
    print "y is greater than x"

# If statements can also be used as a one-liner, e.g. for setting values.  In
# the following, we set 'z' to the value of 'x' if x is greater than y,
# otherwise we use the value of 'y'.
z = x if x > y else y
print "z is", z


#-------------------------------------------------------------------------------
# for loops -- when you know the number of times you need to iterate.  For
# example, let's say we have collected some data:
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print "data is", data

# And let's say we need to square it.  We can use a for loop to square every
# element in the list of data and add it to a new list by iterating over the
# indices of the elements in data:
data_squared = []
for i in range(len(data)):
    data_squared.append(data[i] ** 2)
print "data_squared is", data_squared

# Python is really nice, because we don't need to go through the indices if we
# don't actually need them -- we can directly access the data points themselves,
# in order:
data_squared = []
for datapoint in data:
    data_squared.append(datapoint ** 2)
print "data_squared is", data_squared

# And if we wanted to automatically produce both indices and values at the same
# time, we can use enumerate, which produces tuples of (index, value) for each
# item in the list:
for (i, datapoint) in enumerate(data[:3]):
    print "element", i, "squared is", datapoint ** 2

# If you want to skip computation in an iteration of a loop, you can use the
# 'continue' statement.  For example, if we want only even numbers:
data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
even_data = []
for x in data:
    if x % 2 == 1:
        continue
    even_data.append(x)
print even_data

# If you want to end a for loop early, but a 'break' in.  For example, if we
# have an ordered stream of numbers that eventually become negative, but we only
# want to operate on the positive values, we would want to stop iteration once
# we reach a negative number:
data = [10, 9, 4, 2, 0, -1, -5]
posdata = []
for x in data:
    if x <= 0:
        break
    posdata.append(x)
print posdata

#-------------------------------------------------------------------------------
# list comprehensions -- another way to iterate over lists.  They are usually
# faster than for loops and often more readable as well.  In the following
# example, I'm able to shorted the code from three lines to one line!
data_squared = [(x ** 2) for x in data]
print data_squared

# Why is this faster?  Because it is one of many specific operations in python
# that have been optimized for a specific purpose: building lists.

# We can also use enumerate with list comprehensions:
idata_squared = [(i, x**2) for i, x in enumerate(data)]
print idata_squared

# You can exclude elements from list comprehensions, too:
even_data = [x for x in data if x % 2 == 0]
print even_data

# You can also use if-else one liners to affect the values of the elements that
# are included:
even_or_zero = [(x if x % 2 == 0 else 0) for x in data]
print even_or_zero

# You can make nested lists using list comprehensions inside of list
# comprehensions:
nested_data = [[(x + i) for i in range(3)] for x in data[:4]]
print nested_data

    
#-------------------------------------------------------------------------------
# while loops -- when you don't know how many times you need to iterate.  This
# is typically the case when you're dealing with data streams, user input, or
# asynchonous applications.

# Let's take the example above again.  We can use a while loop instead of a for
# loop with 'break':
data = [10, 9, 4, 2, 0, -1, -5]
i = 0
posdata = []
while data[i] > 0 and i < len(data):
    posdata.append(data[i])
    i += 1
print posdata


#-------------------------------------------------------------------------------
# functions -- a way of packaging a particular piece of code so it can be
# reused.  For example, let's say we want to calculate a logistic:

x = 2
y = 1.0 / (1.0 + 2.718281828459045 ** (-x))
print "l(%s) = %s" % (x, y)

# But if we use this code over and over again, it's going to be annoying to type
# it every time.  Especially with complicated equations, we might make mistakes.
# Hence, it is better to use a "function" and only write the code once:

def logistic(x):
    y = 1.0 / (1.0 + 2.718281828459045 ** (-x))
    return y
x = 4; print "l(%s) = %s" % (x, logistic(x))
x = 0; print "l(%s) = %s" % (x, logistic(x))
x = -1; print "l(%s) = %s" % (x, logistic(x))

# Functions can take arguments (like x) as well as "keyword arguments" --
# arguments that are optional and have a default value.  For example, we might
# want to specify a coefficient for the logistic:

def logistic(x, coeff=1):
    y = 1.0 / (1.0 + 2.718281828459045 ** (-coeff*x))
    return y
x = 4; print "l(%s) = %s" % (x, logistic(x, coeff=1))
x = 0; print "l(%s) = %s" % (x, logistic(x, coeff=2))
x = -1; print "l(%s) = %s" % (x, logistic(x, coeff=0))

# This is a HUGE improvement over MATLAB's absurd function syntax: one main
# function per file and subfunctions listed at the bottom.  Here, subfunctions
# can just be put inside the functions:

def logistic(x, coeff=1):
    print "I am a logistic"

def logistic_list(nums, coeff=1):
    def logistic(x, coeff=1):
        y = 1.0 / (1.0 + 2.718281828459045 ** (-coeff*x))
        return y
    vals = [logistic(x, coeff=coeff) for x in nums]
    return vals
print logistic_list([0, 1, 2, 3])
print [logistic(x, coeff=1) for x in [0, 1, 2, 3]]

# And you can define *as many* functions as you want, all in the same file.
# This makes it so easy to create libraries of related functions.

# Sometimes you don't want to go through all the 'def' syntax for creating a new
# function if it's something simple.  One line functions can be shortened using
# 'lambda's:
logistic = lambda x: 1.0 / (1.0 + 2.718281828459045 ** (-x))
print "l(10) =", logistic(10)
print "l(1) =", logistic(1)
print "l(-4) =", logistic(-4)

# Another note on keyword arguments: It's good practice to only use primitives
# as default values in keyword arguments -- e.g., int, float, string, tuple,
# None.  Using lists or dictionaries is a *very* bad idea, because they are
# mutable and you may get some unexpected behavior.  Let's say we want to append
# 0 to a list that's passed in, but the list is optional:

def foo(nums=[]):
    nums.append(0)
    return nums

print foo()
print foo()
bar = foo()
bar.append(10)
print foo(bar)
print foo()

# That's not right!  The output of 'foo' shouldn't be dependent on the last call
# to 'foo'!  To fix this, we need to not use a mutable list as the default
# value:

def foo(nums=None):
    if nums is None:
        nums = []
    nums.append(0)
    return nums

print foo()
print foo()
bar = foo()
bar.append(10)
print foo(bar)
print foo()


#-------------------------------------------------------------------------------
# Self-practice on CodingBat : http://codingbat.com/python
# You should be able to do problems from Warmup 1 and Warmup 2!
