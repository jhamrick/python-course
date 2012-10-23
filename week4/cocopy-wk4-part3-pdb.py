#!/usr/bin/env python
""" Cocosci scientific Python course, Week 4: Part 3 - pdb."""

### pdb - Python's debugger
#
# The debugger lets you find and fix bugs more easily by letting you
# look around inside a running program, view and modify the data, etc.

# The debugger is accessed in several ways:
# 1. By importing the 'pdb' module in your code.
import pdb
# 2. When calling python from the command line, instructing it to import 'pdb':
# $ python -m pdb my-scripy.py
# 3. When using IPython, you can automatically jump to any exception using:
# %pdb, %pdb on, %pdb 1, %pdb off, %pdb 0
# 4. Also in IPython, you can immediately go to an exception by typing:
# %debug

# Import a buggy module to demonstrate debugging
import buggy_module as bm

# Try running this function
print bm.func1(3)
# This generated an exception (NameError: global name 'Z' is not defined)
# You can jump into 'func1' and look around by typing:
pdb.pm()
# Notice that your Python prompt changes to '(Pdb)', which is a
# special debugging interpreter that's similar to the normal
# interpreter, but has a few extra commands for examining your data
# and the call stack that generated the exception:
# 
# !statement : executes the exact statement (acts like normal interpreter)
# h(elp) [command] : get help, (optionally) about some 'command'
# w(here) : print where you are in the call stack
# l(list) [first[, last]] : list source code in the current file
# a(rgs) : print argument list for current function
# p expression : print some expression (e.g. 'p X' prints the variable X)
# pp : like 'p', but pretty-prints expression
# u(p) : move up one frame
# d(own) : move down one frame
# b(reak) [[filename:]lineno | function[, condition]]: set a breakpoint
# tbreak : same as 'break', but only gets triggered once
# cl(ear) [filename:lineno | bpnumber [bpnumber ...]] : clear a breakpoint
# s(tep) : execute exactly one line (smallest possible step forward)
# n(ext) : execute exactly one line in the current function
# unt(il) : continue executing until a higher line number is reached
# r(eturn) : continue executing until the current function returns
# c(ont(inue)) : continue executing until next break
# j(ump) lineno : lets you go back or forward to any line
# q(uit) : quit the debugger
#
# There are a few other commands that I don't use much (like setting
# conditional breakpoints etc.).

# Test out some of those commands
print bm.func3()
pdb.pm()

# The command 'pdb.set_trace()' sets an explicit breakpoint at some
# point in your code:
print bm.func2(4)

# You can also run a function under debugger control from the outset using:
pdb.run("bm.func3()")
# In effect, this puts a breakpoint before the function's first statement

# Two variants of 'run' are:
pdb.runeval("X")
# and
def func0(X):
    Z = 10 - Y
    return Z
pdb.runcall(func0, 3)
