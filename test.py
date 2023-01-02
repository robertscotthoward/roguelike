import test.test_fluid
import inspect

if __name__ == '__main__':
  test = test.test_fluid.FluidTests()
  for method in inspect.getmembers(test, inspect.ismethod):
    name = method[0]
    if name.startswith("test_"):
      print(name)
      getattr(test, name)()
