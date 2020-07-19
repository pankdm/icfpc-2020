import io

from modulate import modulate as mod
from parse_modulated import parse as dem
from send import do_send
from lists import *
from galaxy_evaluator import *



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
  as_expr = demodulated_list_to_cons(demodulated)
  print(f"as_expr {as_expr}")

  return as_expr

def draw_helper(functional_data, img_index=0, draw_dot_impl=None):
  data = cons_list_to_py_list(functional_data)
  for pt_data in data:
     pt = cons_list_to_py_list(pt_data)
     x = asNum(pt[0])
     y = asNum(pt[1])
     if draw_dot_impl:
       draw_dot_impl(x, y, img_index)
     else:
       print(f"draw_dot({x}, {y}) img_index={img_index}")

def multipledraw_helper(functional_data, draw_dot_impl=None):
  data = cons_list_to_py_list(functional_data)
  layers = 0
  for (index, item) in enumerate(reversed(data)):
    layers = layers + 1
    draw_helper(item, img_index=len(data) - 1 - index, draw_dot_impl=draw_dot_impl)
  print(f'{layers} layers drawn!')

# https://message-from-space.readthedocs.io/en/latest/message38.html
def interact(protocol_evaluator, state, vector):
  print ()
  print("Running protocol...")
  res = protocol_evaluator(state, vector)

  # Note: res will be modulatable here (consists of cons, nil and numbers only)
  (flag, newState, data) = tuple(cons_list_to_py_list(res))
  before = recursive_list_convert(state)
  after = recursive_list_convert(newState)
  print(f"flag={flag}\nnewState={after}")  # data={recursive_list_convert(data)}
  if before == after:
    print("State remained unchanged")
  else:
    print (" >>> NEW STATE!!!")

  if asNum(flag) == 0:
      return (newState, data)

  return interact(protocol_evaluator, newState, _send_to_alien_proxy(data))
