class TypedDictionary(dict):

    def __init__(self, keytype, valtype, *args, **kwargs):

        self.keytype = keytype
        self.valtype = valtype

        super(TypedDictionary, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        newkey = self.keytype(key)
        newval = self.valtype(value)
        super(TypedDictionary, self).__setitem__(newkey, newval)

if __name__ == '__main__':
    td = TypedDictionary(int, str)
    td[0] = 'foo'
    print td # should contain (0, 'foo')
    td[0.0] = 'bar'
    print td # should contain (0, 'bar')
    td[1] = 1 # should contain (0, 'bar') and (1, '1')
    print td
    td['foo'] = 'bar' # error
 
