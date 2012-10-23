# Classes give us the ability to create more complicated data structures that
# contain arbitrary content.  We can create a Participant class that keeps track
# of the information for a particular participant in an experiment.

# First, though, I want to clarify "class" vs. "instance". Let's say that the
# government has a particular tax form that it requires everybody to fill
# out. Everybody has to fill out the same type of form, but the content that
# people put into the form differs from person to person. A class is like the
# form: it specifies what content should exist. Your copy of the form with your
# specific information if like an instance of the class: it specifies what the
# content actually is.

class Participant(object):

    # This is the initialization function.  Every class must have one; it
    # specifies what variables are in the class (e.g., 'pid' and 'condition')
    # and does other initialization.
    def __init__(self, pid, condition):
        self.pid = pid
        self.condition = condition

    # This returns the pid of the participant.
    def getPid(self):
        return self.pid

    # This returns the condition that the participant is in.
    def getCondition(self):
        return self.condition


# Create some participants in different conditions
p1 = Participant(1, 1)
p2 = Participant(2, 2)
p3 = Participant(3, 3)

# Print out which participant is in which condition
print "Participant", p1.getPid(), "ran in condition", p1.getCondition()
print "Participant", p2.getPid(), "ran in condition", p2.getCondition()
print "Participant", p3.getPid(), "ran in condition", p3.getCondition()


#-------------------------------------------------------------------------------
# Sometimes just a single class isn't really enough.  For example, let's say our
# experiment has two conditions -- 'red' and 'blue'.  We may want separate
# classes for each type of participant.  Here's a class for the 'blue'
# condition:

class BlueCondition(Participant):
    
    def __init__(self, pid):
        Participant.__init__(self, pid, "blue")
        self.color = "blue"

    def getQuestion1(self):
        return "Instructions for question 1 for the blue condition"

# Our BlueCondition "inherits" from Participant so we don't have to reimplement
# functions like getPid.  Let's create a BlueCondition particpant (p4a) and a
# regular Particpant (p4b) so we can compare:
p4a = BlueCondition(4)
p4b = Participant(4, 'blue')

# p4b is not an instance of the 'BlueCondition' class, but p4a is an instance of
# both the 'Participant' and 'BlueCondition' classes.
print "Participant", p4a.getPid(), "is a Participant:", isinstance(p4a, Participant)
print "Participant", p4a.getPid(), "is a BlueCondition participant:", isinstance(p4a, BlueCondition)
print "Participant", p4b.getPid(), "is a Participant:", isinstance(p4b, Participant)
print "Participant", p4b.getPid(), "is a BlueCondition participant:", isinstance(p4b, BlueCondition)

# This will cause an error - 'Participant' doesn't have a method 'getQuestion1',
# only 'BlueCondition' does.
print p4b.getQuestion1()
# The rest of these statements should be fine:
print p4a.getQuestion1()
print p4b.getPid()
print p4a.getPid()


#-------------------------------------------------------------------------------
# Now let's create a similar class for the 'red' condition:

class RedCondition(Participant):

    def __init__(self, pid):
        Participant.__init__(self, pid, "red")
        self.color = "red"

    def getQuestion1(self):
        return "Instructions for question 1 for the red condition"


# Some more participants in different conditions -- demonstrating the different
# ways you can subclass things.
p5 = BlueCondition(5)
p6 = RedCondition(6)
print "Participant", p5.getPid(), "was told '", p5.getQuestion1(), "'"
print "Participant", p6.getPid(), "was told '", p6.getQuestion1(), "'"
