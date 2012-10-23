import time

class Foo(object):

    def __init__(self, name):
        self._name = name
        self._time = time.time()

    def getName(self):
        return self._name
    def setName(self, newname):
        self._name = newname
    name = property(getName, setName)

    def getAge(self):
        timediff = time.time() - self._time
        msg = "%s says, \"I am %s seconds old.\"" % (self.name, timediff)
        return msg    
    def setAge(self, val):
        self._time = time.time() - val
    age = property(getAge, setAge)

    
if __name__ == '__main__':
    rob = Foo('Robert')
    print rob.name
    rob.name = 'Rob'
    print rob.name

    print rob.age
    time.sleep(1)
    print rob.age
    time.sleep(1)
    print rob.age
    time.sleep(1)
    print rob.age
    rob.age = 100
    print rob.age
