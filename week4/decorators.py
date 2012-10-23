import time

class FooBar(object):
    
    @staticmethod
    def getInfo():
        return "I am a 'FooBar'"

    @classmethod
    def getClassInfo(cls):
        return "I am a '%s'" % cls.__name__

class Foo(FooBar):

    def __init__(self, name):
        self._name = name
        self._time = time.time()

    def getName(self):
        return self._name
    def setName(self, newname):
        self._name = newname
    name = property(getName, setName)

    @property
    def age(self):
        timediff = time.time() - self._time
        msg = "%s says, \"I am %s seconds old.\"" % (self.name, timediff)
        return msg    

if __name__ == '__main__':
    bob = Foo('Bobby')
    print bob.name
    bob.name = 'Bob'
    print bob.name

    # property decorator -- shorthand for the property function
    print bob.age
    time.sleep(1)
    print bob.age
    # This will throw an error because no setter exists for the
    # property:
    bob.age = 100
    
    # staticmethod and classmethod decorators
    print bob.getInfo()
    print Foo.getInfo()
    print FooBar.getInfo()
    print bob.getClassInfo()
    print Foo.getClassInfo()
    print FooBar.getClassInfo()

    # you can write your own decorators, too -- they're just a
    # function that takes another function, modifies it, and returns a
    # new function.  For example:

    def random(func):
        func.random = True
        return func

    class Bar(object):

        @random
        def a(self):
            pass

        def b(self):
            pass

    print Bar.a.random
    print Bar.b.random # error
