class Dog(object):

    def __init__(self, name):
        self.name = name
        self.skills = []

    def teachSkill(self, skillname, skill):
        setattr(self, skillname, skill.__get__(self))

    def __str__(self):
        return self.name


if __name__ == '__main__':

    # monkey patching with variables
    fluffy = Dog("Fluffy")
    print fluffy
    fluffy.age = 2
    print fluffy.age

    # monkey patching with methods
    def sit(self):
        print "%s is sitting!" % self.name
    def speak(self):
        print "%s says 'WOOF!'" % self.name

    # Note that we're setting a function on the *class*, not an
    # instance of the class.  If we tried to call Dog.sit(), it would
    # throw an error because haven't given it the first argument,
    # 'self'.
    Dog.sit = sit
    rover = Dog("Rover") 
    print rover
    rover.sit()

    # What happens if we do try to set the function on the instance?
    fluffy.sit = sit
    fluffy.sit()
    # There's an error: "sit() takes exactly 1 arguments (0 given)"

    # This is because the method 'sit' is still just a function --
    # "methods" are "bound" to instances of a class.  So for sit to
    # work properly, we need to bind it to 'a'.
    rover.teachSkill('speak', speak)
    rover.speak()

    # So what does it mean for something to be bound?  It basically
    # means the class does some special stuff behind the scenes and
    # calls each bound method like this:
    Dog.speak = speak
    Dog.speak(fluffy)
    
    # Note how the instance is being passed into the function as the
    # first argument.  That's what that 'self' keyword is for!
