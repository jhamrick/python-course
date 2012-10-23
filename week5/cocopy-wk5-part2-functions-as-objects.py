#!/usr/bin/env python
""" Cocosci scientific Python course, Week 5: Part 2 - Functions as objects"""

hello = 3
def A(string='world'):
    """Prints 'Hello, string!'"""
    hello = 'Hello'
    print "%s, %s!" % (hello, string)

# All functions are objects, so we can treat the function 'A' just
# like any other variable.  There are a few special things about
# functions, though, including:

# 1. Docstrings (func_doc / __doc__)
print "A's docstring is:", A.func_doc
print "A's docstring is:", A.__doc__

# 2. Name (func_name / __name__)
print "A's name is:", A.func_name
print "A's name is:", A.__name__
B = A
print "B's name is:", B.__name__

# 3. Module (__module__) -- the module the function was defined in
print "A's module is:", A.__module__
# (Side note: remember the 'if __name__ == '__main__'" statement from
# last week?  Now it should make sense that we were looking at the
# name of the module and checking to see if it was __main__, which is
# also the module that A is defined in!)

# 4. Default arguments (func_defaults).  This gives you the ability to
# see what the default values are for keyword arguments.
print "A's default values are:" , A.func_defaults

# 5. Globals dictionary (func_globals) -- a dictionary containing
# references to all variables in the function's global scope.  Even
# though we define a local 'hello' variable inside A, the global value
# is still stored:
print "A's global value for 'hello' is:", A.func_globals['hello']

# 6. Attributes dictionary (func_dict / __dict__ ) -- this is empty by
# default, but if we set attributes on the function (like we can for
# any other object), we'll see that this dictionary becomes populated:
print "A's attributes are:", A.func_dict
print "A's attributes are:", A.__dict__
A.foo = 'bar'
print "A's attributes are:", A.func_dict
 
# 7. Closure (func_closure) -- this is another scoping-related
# attributed.  When we have functions inside functions and use
# variables from the parent function in the child function, we have
# what is called a 'closure'.  We can't actually easily access the
# values from the closure; this is more of a demonstration of how
# these sort of abstract concepts actually work under the hood.
def B():
    hello = 'hello'
    goodbye = 'goodbye'
    def C(string):
        print "%s, %s!" % (hello, string)
    def D(string):
        print "%s, %s!" % (hello, string)
        print "%s, %s!" % (goodbye, string)
    return C, D
C, D = B()
print "B's closure is:", B.func_closure
print "C's closure is:", C.func_closure
print "D's closure is:", D.func_closure

# 8. Code (func_code) -- yes, that's right, you can get information
# about the code itself using -- you guessed it -- another type of
# object!  We won't really go into code objects here, but it's kind of
# cool if you want to look at it more yourself.
print "A's code is:", A.func_code
