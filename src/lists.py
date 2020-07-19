# from funcs import *
from galaxy_evaluator import *


def cons_list_to_py_list(value, keep_last_nil=False):
  """Converts an AP/CONS function to a Python list."""

  l = [] 
  current_value = value
  while not isnil(current_value) and not isnum(current_value):
    # print(f"current_value {eval(current_value)}")
    l.append(eval(Ap(Atom("car"), current_value)))
    # print(f"l={l}")

    current_value = eval(Ap(Atom("cdr"), current_value))

  if not isnil(current_value) or keep_last_nil:
    l.append(current_value)

  # print(f"\n\n\nl = {l}")

  return l

def recursive_list_convert(data):
  """Same as cons_list_to_py_list, but recursive."""

  # print(f"_recursive_list_convert {data}")
  data_as_list = cons_list_to_py_list(data)
  # print(f"data_as_list {data_as_list}")
  result = []
  for item in data_as_list:
    if isnum(item):
      result.append(asNum(item))
    elif isnil(item):
      result.append([])
    else:
      result.append(recursive_list_convert(item))
  return result

def list_to_cons(l):
  """Python list to CONS, recursive."""

  # if len(l) == 0:
  #   return nil
  full_expr = nil
  for item in reversed(l):
    if isinstance(item, list):
      item_expr = list_to_cons(item)
    else:
      item_expr = Atom(str(item))
    full_expr = Ap(Ap(Atom("cons"), item_expr), full_expr)
  return full_expr
