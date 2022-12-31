# http://pythex.org/
import unittest
import re
import random


class Dice:
  def __init__(self, dice = "d100", seed = None):
    """
    @dice is a string in the format "NdD±A"; e.g. "d20", "2d6+3", "10d12-6"
    N is the number of dice to roll (default = 1)
    D is the type of die; can be any sided die; e.g. 33
    A is the optional adjustment to add to the sum of the dice

    USAGE:
      dice = Dice("3d6")
      print(dice)
    """
    self.dice = dice
    # See https://pythex.org/

    N, D, A, SIGN, AFTER = Dice.Parse(dice)
    self.N = N
    self.D = D
    self.A = A
    self.SIGN = SIGN
    random.seed(seed)

  def Role(self):
    n = 0
    for i in range(self.N):
      n += random.randint(1, self.D)
    if self.SIGN == "+":
        n += self.A
    else:
        n -= self.A
    return n

  def Parse(dice):
    match = re.search(r"(?P<N>[0-9]+)?d(?P<D>[0-9]+)((?P<SIGN>[+-])(?P<A>[0-9]+))?(?P<AFTER>.+)?", dice)
    if not match:
      raise Exception('Invalid dice string. Expected format "NdD±A"')
    N = int(match.group("N") or "1")
    D = int(match.group("D") or "100")
    A = int(match.group("A") or "0")
    SIGN = match.group("SIGN") or "+"
    AFTER = match.group("AFTER") or ""
    return N, D, A, SIGN, AFTER


  def __str__(self):
    return str(self.Role())

  def __int__(self):
    return self.Role()

  def __float__(self):
    return float(self.Role())
