from funcs import *

def cons_list_to_py_list(value, keep_last_nil=False):
  """Converts an AP/CONS function to a Python list."""
  if isinstance(value, AP):
    value = value.compute()
  l = [] 
  current_value = value
  while isinstance(current_value, CurriedFunction) and current_value.name == "CONS":
    l.append(AP(CAR, current_value).compute())
    current_value = AP(CDR, current_value).compute()
  if current_value != NIL or keep_last_nil:
    l.append(current_value)
  return l
