#-------------------------------------------------------------------------------
# if statements -- a way of doing different things depending on the condition.
# For example, let's say we need to compare two numbers (play around with
# changing x and y and see how that effects the value of 'compare'):

x = 2
y = 3
if x == y:
    compare = 'equal'
elif x > y:
    compare = 'x > y'
else:
    compare = 'x < y'
print (x, y), compare



#-------------------------------------------------------------------------------
# for loops -- when you know the number of times you need to iterate.  For
# example, let's say we have collected some data:
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# And let's say we need to square it.  We can use a for loop to square every
# element in the list of data and add it to a new list:

data_squared = []
for datapoint in data:
    data_squared.append(datapoint ** 2)

print data
print data_squared

# We can also use "iterators" and "enumerators" to make things easier in some
# cases.  Maybe we want to square the *indices* of each data point instead of
# the data itself:

indices_squared = []
for i in range(len(data)):
    indices_squared.append(i ** 2)

# 'range' gives us a list of integers from 0 to len(data).  We can alternately
# use 'xrange', which is an "iterator".  It returns a function that produces a
# list of integers, one-by-one, from 0 to len(data).  It is more
# memory-efficient and probably the better choice.

indices_squared = []
for i in xrange(len(data)):
    indices_squared.append(i ** 2)

# And if we wanted to do both at the same time, we can use enumerate, which
# returns a function that produces tuples of (index, value) for each item in
# 'data':

indices_squared = []
data_squared = []
for i, datapoint in enumerate(data):
    indices_squared.append(i ** 2)
    data_squared.append(datapoint ** 2)



#-------------------------------------------------------------------------------
# list comprehensions -- another way to iterate over lists.  They are usually
# faster than for loops and often more readable as well.  In the following
# example, I'm able to shorted the code from three lines to one line!
data_squared = [x**2 for x in data]
print data_squared

# Why is this faster?  Because function calls in python can be pretty slow -- in
# the for loop above, we call the 'append' function every single time.  In the
# list comprehension, the list is built for us so we cut out a lot of function
# calls!

# We can also use xrange and enumerate with list comprehensions:
indices_squared = [i**2 for i in xrange(len(data))]
print indices_squared
pairs_squared = [(i**2, x**2) for i, x in enumerate(data)]
print pairs_squared

# You can exclude elements from list comprehensions, too:
even_data = [x for x in data if x % 2 == 0]
print even_data



#-------------------------------------------------------------------------------
# while loops -- when you don't know how many times you need to iterate.  This
# is typically the case when you're dealing with data streams, user input, or
# asynchonous applications.

# We'll use an example of user input.  Say you need to ask a subject for their
# name, but you want to make sure they actually give you a valid name.  We'll
# need to loop until they give us valid input:

name = None
while name is None:
    # Prompt the user to type their name.  'raw_input' will wait the user to
    # type something and hit enter.
    print "Please enter your name: ",
    name = raw_input()

    # Check to see if their name consisted only of letters (it should probably
    # be ok to include dashes and spaces, too, but we'll ignore that for the
    # moment).  If it's not valid, tell them so and set name back to 'None' so
    # we can re-prompt them.
    if not name.isalpha():
        print "Invalid name!  Try again."
        name = None

    # If the name was valid, then the condition on the while loop will fail on
    # the next iteration, causing it to terminate.
    
print "Your name is '%s'" % name



#-------------------------------------------------------------------------------
# functions -- a way of packaging a particular piece of code so it can be
# reused.  For example, let's say we want to calculate a logistic:

import math
x = 2
y = 1.0 / (1.0 + math.e ** (-x))
print "l(%s) = %s" % (x, y)

# But if we use this code over and over again, it's going to be annoying to type
# it every time.  Especially with complicated equations, we might make mistakes.
# Hence, it is better to use a "function" and only write the code once:

def logistic(x):
    y = 1.0 / (1.0 + math.e ** (-x))
    return y
x = 4; print "l(%s) = %s" % (x, logistic(x))
x = 0; print "l(%s) = %s" % (x, logistic(x))
x = -1; print "l(%s) = %s" % (x, logistic(x))

# Functions can take arguments (like x) as well as "keyword arguments" --
# arguments that are optional and have a default value.  For example, we might
# want to specify a coefficient for the logistic:

def logistic(x, coeff=1):
    y = 1.0 / (1.0 + math.e ** (-coeff*x))
    return y
x = 4; print "l(%s) = %s" % (x, logistic(x, coeff=1))
x = 0; print "l(%s) = %s" % (x, logistic(x, coeff=2))
x = -1; print "l(%s) = %s" % (x, logistic(x, coeff=0))


#-------------------------------------------------------------------------------
# practice on CodingBat : http://codingbat.com/python
# Should be able to do problems from Warmup 1 and Warmup 2
