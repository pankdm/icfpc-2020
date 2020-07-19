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
