import datetime
import unittest
import os
import yaml
from fluid import Fluid
from dateutil.parser import parse

def subloadYaml(data):
  '''
  Modify data by loading in any references to external files.
  This is sort of like an "include" statement.
  '''
  # If it's a list, then recur on each item.
  if type(data) == list:
    for x in data:
      subloadYaml(x)

  # If it's a dict then look for a 'ref'.
  elif type(data) == dict:
    # Does it have a 'ref' property?
    if 'ref' in data:
      # Yes, so that means to replace it with the external file.
      data['ref'] = ReadYaml(data['ref'])
    else:
      # No, so recur on each property.
      for k in data:
        subloadYaml(data[k])


def ParseYaml(s):
  '''
  Parses a yaml string into an object.
  If any parts of the file refer to other files, read those in recursively.
  See: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
  '''
  data = yaml.safe_load(s)
  subloadYaml(data)
  return data


def ReadYaml(fn):
  '''
  Read a *.yaml file from the "data" folder into a dict (i.e. dictionary) object.
  If any parts of the file refer to other files, read those in recursively.
  See: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
  '''
  dn = GetDataPath(fn)
  with open(dn) as f:
    data = yaml.safe_load(f)
    subloadYaml(data)
    return data


def WriteYaml(fn, obj):
  '''
  Write a dict object to a *.yaml file in the "data" folder.
  '''
  dn = GetDataPath(fn)
  dir = os.path.dirname(os.path.abspath(dn))
  os.makedirs(dir, exist_ok=True)
  with open(dn, 'w') as f:
    yaml.dump(obj, f)


def ValidateSchema(obj, cls):
  "Ensure that an object (obj) conforms to the structure defined in a class (cls)."
  o = Fluid(obj)
  c = Fluid(cls)

  if not 'root' in c:
    raise Exception("Schema missing 'root' property.")
  type = c.root.type

  ValidateSchema1(c, o, c.root)

def ValidateSchema1(schema, o, c):
  # ================================================================================
  # @schema is a global constant reference to the schema.
  # @c is the current schema.
  # @o is the current object being validated against @c.
  if c.type == 'dict':
    if not isinstance(o._data, dict):
      raise("Expected a dict", str(o))
    if c.properties:
      for pn in c.properties:
        p = c.properties[pn]
        t = p['type'] if 'type' in p else 'any'
        required = p['required'] if 'required' in p else False

        # If the property is required but it doesn't exist, then error!
        if not pn in o._data:
          if required:
            raise Exception(f"INVALID YAML: Missing required property '{cn}'")
          else:
            continue

        # If the type does not match, then error!
        v = o._data[pn]
        if not v:
          continue
        if t == 'any':
          pass
        elif t == 'dict':
          if not isinstance(v, dict):
            raise Exception(f"INVALID YAML: Expected property value of '{pn}' to be '{type}'. Was '{type(v)}' instead")
        elif t == 'list':
          if not isinstance(v, list):
            raise Exception(f"INVALID YAML: Expected property value of '{pn}' to be '{type}'. Was '{type(v)}' instead")
        elif t == 'string':
          if not isinstance(v, str):
            raise Exception(f"INVALID YAML: Expected property value of '{pn}' to be '{type}'. Was '{type(v)}' instead")
        elif t == 'number':
          if not isinstance(v, (int, float)):
            raise Exception(f"INVALID YAML: Expected property value of '{pn}' to be a number. Was '{type(v)}' instead")
        elif t == 'int' or t == 'integer':
          if not isinstance(v, int):
            raise Exception(f"INVALID YAML: Expected property value of '{pn}' to be a int. Was '{type(v)}' instead")
        elif t == 'float':
          if not isinstance(v, float):
            raise Exception(f"INVALID YAML: Expected property value of '{pn}' to be a float. Was '{type(v)}' instead")
        elif t == 'date':
          if not isinstance(v, datetime.date):
            if not isinstance(v, str):
              raise Exception(f"INVALID YAML: Expected property value of '{pn}' to be a string date. Was '{type(v)}' instead")
            try:
              dt = parse(v)
            except Exception as e:
              raise Exception(f"INVALID YAML: Expected property value of '{pn}' to be a valid date. Was '{v}' instead. {e}")
        else:
          raise Exception(f"INVALID SCHEMA: 'type' of '{t}' is not defined.")

  # ================================================================================
  elif c.type == 'set':
    if not isinstance(o._data, dict):
      raise("Expected a dict", str(o))
    of = c.of
    if of:
      if not of in schema:
        raise(f"Class '{of}' is not defined.")
      c = schema[of]
      for key in o._data:
        x = o[key]
        try:
          ValidateSchema1(schema, x, c)
        except ex:
          raise f"Key '{key}' " from ex

  # ================================================================================
  elif c.type == 'list':
    if not isinstance(o._data, list):
      raise("Expected a list", str(o))
    of = c.of
    if of:
      if not of in schema:
        raise(f"Class '{of}' is not defined.")
      c = schema[of]
      for x in o:
        ValidateSchema1(schema, x, c)
  else:
    raise f"Unexpected type '{c.type}'"




def GetDataPath(fn):
  '''
  @fn is a relative path; e.g. "x.txt" or "mystuff/x.txt"
  This function defines where these data items are to be stored;
  currently in the "data/" folder, but we might change it later.
  '''
  return os.path.join("data", fn)


def DataFileExists(fn):
  return os.path.exists(GetDataPath(fn))


def YN(prompt='', default=True):
  'Prompt for yes or no. Return boolean'
  a = input(prompt).upper()[:1]
  if a == '': return default
  if a == 'Y': return True
  if a == '1': return True
  if a == 'T': return True
  return False
