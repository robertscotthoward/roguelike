import unittest
import os
import yaml
from tools import *
from fluid import Fluid


class ToolsTests(unittest.TestCase):
  def test_1(self):
    self.assertEqual("Hello There", "Hello" + " There")

  def test_yamlSchema(self):
    cls = """
root:
  type: dict
  properties:
    people:
      type: list
      of: person
    places:
      type: dict
      properties:
        countries:
          type: list
          of: country
    planets:
      type: set
      of: planet

person:
  type: dict
  properties:
    first:
      type: string
      required: True
    last:
      type: string
      required: True
    age:
      type: integer
      desc: Years old
      required: False

country:
  type: dict
  properties:
    name:
      required: True
    abbr:
      required: True
    population:
      type: integer

planet:
  type: dict
  properties:
    index: integer
"""

    obj = """
people:
  - first: Fred
    last: Flintstone
    age: 33
  - first: Wilma
    last: Flintstone
places:
  countries:
    - name: United States
      abbr: US
      population: 300000000
      capital: Washington DC
      states:
        - name: California
        - name: Arizona
    - name: France
  planets:
    - Mercury: ~
    - Venus: ~
    - Earth: ~
"""

    ValidateSchema(obj, cls)

  def test_yamlSchema1(self):
    cls = """
root:
  type: dict
  properties:
    first:
      type: string
      required: True
    last:
      type: string
      required: True
    age:
      type: integer
    dob:
      type: date
"""

    obj = """
first: Fred
last: Flintstone
age: 20
dob: Jun 30, 2021
"""

    ValidateSchema(obj, cls)

if __name__ == '__main__':
  unittest.main()
