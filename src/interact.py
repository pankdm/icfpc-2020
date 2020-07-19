import io

from modulate import modulate as mod
from parse_modulated import parse as dem
from send import do_send
from lists import cons_list_to_py_list
from galaxy_evaluator import *

def recursive_list_convert(data):
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


def _send_to_alien_proxy(data):
  print("_send_to_alien_proxy")
  data_as_list = recursive_list_convert(data)
  print(f"data_as_list ={data_as_list}")

  # new_cons = list_to_cons(data_as_list)
  # data_as_list_again = recursive_list_convert(new_cons)
  # print(f"new_cons {new_cons}")
  # print(f"data_as_list_again {data_as_list_again}")
  # print(f"same? {data_as_list == data_as_list_again}")
  # exit()

  modulated = mod(data_as_list)
  print(f"Sending as {modulated}")
  response = do_send(modulated)
  print(f"Got {response}")
  demodulated = dem(io.StringIO(response))
  print(f"...parsed as {demodulated}")
  as_expr = list_to_cons(demodulated)
  print(f"as_expr {as_expr}")

  return as_expr

def draw_helper(functional_data, draw_dot_impl=None):
  data = cons_list_to_py_list(functional_data)
  for pt_data in data:
     pt = cons_list_to_py_list(pt_data)
     (x, y) = tuple(pt)
     if draw_dot_impl:
       draw_dot_impl(x, y)
     else:
       print(f"draw_dot({x}, {y})")

def multipledraw_helper(functional_data, draw_dot_impl=None):
  data = cons_list_to_py_list(functional_data)
  for item in data:
    draw_helper(item, draw_dot_impl=draw_dot_impl)

# https://message-from-space.readthedocs.io/en/latest/message38.html
def interact(protocol_evaluator, state, vector):
  print("Running protocol...")
  res = protocol_evaluator(state, vector)

  # Note: res will be modulatable here (consists of cons, nil and numbers only)
  (flag, newState, data) = tuple(cons_list_to_py_list(res))
  print(f"flag={flag} newState={newState} data={data}")
  if flag == 0:
      return (newState, data)

  return interact(protocol_evaluator, newState, _send_to_alien_proxy(data))

