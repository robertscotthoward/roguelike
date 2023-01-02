import unittest
import os
import yaml
import tools


class Fluid:
    '''
    A Fluid object is one that can model a dict or list, but can be used in a dotted javascript-like manner.
    Example:
      d = {'first': 'Fred', 'last': 'Flintstone'}
    Then you normally need to do this:
      print(d['first'])
    Instead, you can do this:
      fluid = Fluid(d)
      print(fluid.first)  --> which should be easier to read.

    REF: https://rszalski.github.io/magicmethods/
    '''

    def __init__(self, data=None):
        "Called when creating a new object of this class."
        self.setData(data)


def setData(self, data):
    if type(data) is dict:
        self.__dict__["_data"] = data
        self.__dict__["_type"] = 'dict'
    elif type(data) is list:
        self.__dict__["_data"] = data
        self.__dict__["_type"] = 'list'
    elif type(data) is str:
        self.__dict__["_data"] = tools.ParseYaml(data)
        self.__dict__["_type"] = 'dict'
    elif type(data) is Fluid:
        self.__dict__["_data"] = data.__dict__['_data']
        self.__dict__["_type"] = data.__dict__['_type']
    elif not data:
        self.__dict__["_data"] = None
        self.__dict__["_type"] = None
    else:
        raise Exception(f"Unexpected type '{type(data)}'")

    def get(self, key):
        if not self.__dict__["_data"]:
            self.__dict__["_data"] = Fluid()
            self.__dict__["_type"] == 'dict'
        data = self.__dict__["_data"]
        if self.__dict__["_type"] == 'dict':
            if key in data:
                o = data[key]
            if o == None:
              if type(o) is dict or type(o) is list:
                  data[key] = Fluid(o)
                  return data[key]
            return o
        # raising this exception allows getattr to return its default value.
        raise AttributeError

    def __getattr__(self, name):
        "Called when: myObject.SomeName"
        if name == None:
            raise f"Expecting type string for name. Got None instead."
        if type(name) != str:
            raise f"Expecting type string for name. Got '{type(name)}' instead."

    def __setattr__(self, name, value):
        "Called when: myObject.SomeName = SomeValue"
        if not self.__dict__["_data"]:
            self.__dict__["_data"] = Fluid()
        data = self.__dict__["_data"]
        # if name in data:
        #   o = data[name]
        #   if type(o) is dict or type(o) is list:
        #     return Fluid(o)
        data[name] = value

    def __getitem__(self, key):
        "Called when: myObject[n]. Returns None if n is out of the list range."
        data = self.__dict__["_data"]
        if not data:
            return None
        # if key < 0: return None
        # if key >= len(data): return None
        o = data[key]
        if type(o) is dict or type(o) is list:
            data[key] = Fluid(o)
            return data[key]
        return o

    def __setitem__(self, key, value):
        "Called when: myObject[n] = SomeValue. Sets the value even if n is out of the list range, and pads to do so."
        if isinstance(key, int):
            if key < 0:
                raise Exception("Cannot set negative list indexes.")
            if not self.__dict__["_data"]:
                self.__dict__["_data"] = []
                self.__dict__["_list"] = 'list'
            data = self.__dict__["_data"]
            while key >= len(data):
                data.append(None)
        else:
            if not self.__dict__["_data"]:
                self.__dict__["_data"] = {}
                self.__dict__["_list"] = 'dict'
            data = self.__dict__["_data"]
        if type(value) is dict or type(value) is list:
            data[key] = Fluid(value)
        else:
            data[key] = value

    def normalize(self):
        if not self.__dict__["_data"]:
            return ""
        data = self.__dict__["_data"]
        if type(data) is dict:
            for k in data:
                v = data[k]
                if type(v) is Fluid:
                    v.normalize()
                    v = v.__dict__["_data"]
                    data[k] = v
        elif type(data) is list:
            for i in range(len(data)):
                v = data[i]
                if type(v) is Fluid:
                    v.normalize()
                    v = v.__dict__["_data"]
                    data[i] = v
        return data

    def __nonzero__(self):
        """
        Defines behavior for when bool() is called on an instance of your class. Should return True or False,
        depending on whether you would want to consider the instance to be True or False.
        """
        if not self.__dict__["_data"]:
            return ""
        data = self.__dict__["_data"]
        if data:
            return True
        return False

    def __add__(self, other):
        if not self.__dict__["_data"]:
            self.__dict__["_data"] = []
            self.__dict__["_type"] = 'list'
        data = self.__dict__["_data"]
        if type(other) is list:
            return data + other
        return data + [other]

    def __iter__(self):
        type = self.__dict__['_type']
        data = self.__dict__['_data']
        if type == 'dict' or type == 'list':
            for i in data:
                yield i
        else:
            raise (f"Unhandled type '{type}'")

    def __len__(self):
        if self.__dict__["_data"] == None:
            return 0
        data = self.__dict__["_data"]
        return len(data)

    def __str__(self):
        if self.__dict__["_data"] == None:
            return ""
        s = yaml.dump(self.normalize(), )
        return s

    def __repr__(self):
        if self.__dict__["_data"] == None:
            return ""
        s = yaml.dump(self.normalize())
        return f'''"Fluid("{s}")'''

    # ===== STATIC =====

    def validate(Class, Object):
        """
        @Class (Fluid) contains the schema to valid @Object
        @Object (Fluid) contains the data to be validated
        """
