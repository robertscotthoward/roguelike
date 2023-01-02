import unittest
import os
import yaml
from tools import *
from fluid import Fluid


data1 = '''
animals: [bird, dog, cat]
people:
  fred:
    first: Fred
    last: Flintstone
  wilma:
    first: Wilma
    last: Flintstone
states:
  - name: Arizona
    capital: Phoenix
  - name: California
    capital: Sacremento
  - name: New York
    capital: Albany
pets:
  cat:
    sounds:
      - meow
      - purr
    verbs:
      - sleep
      - eat
      - chase
  dog:
    sounds:
      - bark
      - woof
      - howl
    verbs:
      - sleep
      - eat
      - sniff
'''

class FluidTests(unittest.TestCase):
  def test_aaa(self):
    f = Fluid(ParseYaml(data1))
    for x in f:
      print(x)



  def test_CreateByGet(self):
    # When getting a property that does not exist, it should create it
    # and then return a Fluid(None)
    f = Fluid()
    f = 111
    assert(f == 111)

    f = Fluid()
    f.a = 123
    assert(f.a == 123)
    print(f)

    f = Fluid()
    f.a.b = 123
    assert(f.a.b == 123)
    print(f)
    print()



  def test_Fluid(self):
    # Pick some useful YAML string that might cover a bunch of tests.
    o = ParseYaml(data1)

    # Create a Fluid object from the YAML
    f = Fluid(o)

    # Test some accessors
    self.assertEqual("dog", f.animals[1])
    f.animals[9] = "rabbit"
    self.assertEqual(None, f.animals[8])
    self.assertEqual("rabbit", f.animals[9])
    with self.assertRaises(IndexError):
      f.animals[10]

    self.assertEqual("Fred", f.people.fred.first)
    self.assertEqual("Flintstone", f.people.fred.last)
    self.assertEqual("Wilma", f.people.wilma.first)
    self.assertEqual("Arizona", f.states[0].name)
    self.assertEqual("Phoenix", f.states[0].capital)
    self.assertEqual("New York", f.states[2].name)
    self.assertEqual("Albany", f.states[2].capital)

    f.states[2].capital = "Whatever"
    self.assertEqual("Whatever", f.states[2].capital)

    # Enumerate some list
    s = ','.join([str(x) for x in f.pets.dog.sounds])
    self.assertEqual("bark,woof,howl", s)

    # Add a sound
    f.pets.dog.sounds += ['slobber']
    s = ','.join([str(x) for x in f.pets.dog.sounds])
    self.assertEqual("bark,woof,howl,slobber", s)

    #TODO: self.assertEqual("", repr(f.pets.dog.sounds))




  def test_FluidNew(self):
    f = Fluid()
    f[5] = "Hi"
    f[2] = {}
    f[2].color = "Orange"
    f[2].taste = "Yummy"
    f[2].properties = {}
    f[2].properties.weight = 10
    f[2].properties.shape = 'round'
    #print(f)
    self.assertEqual("""
- null
- null
- color: Orange
  properties:
    shape: round
    weight: 10
  taste: Yummy
- null
- null
- Hi
    """.strip(), str(f).strip())

  def xxtest_FluidNew1(self):
    f = Fluid()
    f.people = []

    f.people += {}
    f.people[-1].first = "Fred"
    f.people[-1].last = "Flintstone"
    f.people[-1].pets = []
    f.people[-1].pets += "Dino"
    f.people[-1].pets += "Baby Puss"

    f.people += {}
    f.people[-1].first = "Barnay"
    f.people[-1].last = "Rubble"

    # Find and update
    index = [i for i,x in enumerate(f.people) if x.first == "Barnay"][0]
    f.people[index].first = "Barney"

    #print()
    #print(str(f))


  def test_WriteFluid(self):
    data = ParseYaml("numbers: [1,2,3]")
    WriteYaml("testwritedata", data)

  def test_Boolean(self):
    data = ParseYaml("[]")
    self.assertFalse(data)
    data = ParseYaml("[1,2,3]")
    self.assertTrue(data)

    data = ParseYaml("{}")
    self.assertFalse(data)
    data = ParseYaml("{'name': 'value'}")
    self.assertTrue(data)

    data = ParseYaml("0")
    self.assertFalse(data)
    data = ParseYaml("1")
    self.assertTrue(data)

    data = ParseYaml("''")
    self.assertFalse(data)
    data = ParseYaml("'Hi'")
    self.assertTrue(data)

  def test_Add(self):
    data = ParseYaml("[1,2]")
    d = data + [3,4]
    self.assertEqual("[1, 2, 3, 4]", str(d))


if __name__ == '__main__':
  test = FluidTests()
  test.test_CreateByGet()
  unittest.main()
