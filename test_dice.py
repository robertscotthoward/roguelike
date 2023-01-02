# http://pythex.org/
import unittest
import re
import random
from dice import Dice



class DiceTests(unittest.TestCase):
  def Role10(self, dice, expected):
    dice = Dice(dice, 123)
    a = [str(dice.Role()) for x in range(10)]
    r = ','.join(a)
    if r != expected:
        print(r)
    self.assertEqual(expected, r)

  def test_roles(self):
      self.Role10("2d10", "6,9,7,8,18,12,4,9,15,7")
      self.Role10("1d2", "1,2,1,2,2,1,1,2,2,2")
      self.Role10("2d2", "3,3,3,3,4,2,3,3,2,3")
      self.Role10("3d6+3", "8,11,13,14,8,14,13,9,13,13")
      self.Role10("3d6-3", "2,5,7,8,2,8,7,3,7,7")
      self.Role10("d2-1", "0,1,0,1,1,0,0,1,1,1")

  def test_str(self):
    dice = Dice("3d6", 111)
    self.assertEqual("9", str(dice))
    self.assertEqual("10", str(dice))
    self.assertEqual("13", str(dice))
    self.assertEqual("12", str(dice))

  def test_int(self):
    dice = Dice("3d6", 111)
    self.assertEqual(9, int(dice))
    self.assertEqual(10, int(dice))
    self.assertEqual(13, int(dice))
    self.assertEqual(12, int(dice))
    self.assertEqual(9, float(dice))

if __name__ == '__main__':
    unittest.main()
