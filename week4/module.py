import pickle

def hello(name):
    return "Hello, %s!" % name

def pickled_hello(name):
    string = hello(name)
    pstring = pickle.dumps(string)
    return pstring

print hello("Bob")
print pickled_hello("Bob")

if __name__ == "__main__":
    print hello("Alice")
