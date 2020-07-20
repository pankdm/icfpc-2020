import io

from modulate import modulate as mod
from parse_modulated import parse as dem
from send import do_send
from lists import *
from galaxy_evaluator import *

import time
import os

def create_log():
  timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
  # datetime.utcnow().isoformat()
  # folder = "annotations/tmp/{}".format(timestamp)
  folder = "send-alien-logs/"
  os.makedirs(folder, exist_ok=True)
  filepath = "{}/{}.txt".format(folder, timestamp)
  return open(filepath, 'w')

logfile = None
if logfile is None:
  print("created new log!!!")
  logfile = create_log()


def my_send_to_alien_proxy(data):
  global logfile
  print ()
  print("_send_to_alien_proxy: ", data)
  logfile.write('sent to aliens: ' + str(data) + '\n')
  logfile.flush()

  # new_cons = py_to_tree(data_as_list)
  # data_as_list_again = tree_to_py(new_cons)
  # print(f"new_cons {new_cons}")
  # print(f"data_as_list_again {data_as_list_again}")
  # print(f"same? {data_as_list == data_as_list_again}")
  # exit()

  modulated = mod(data)
  print(f"Sending as {modulated}")
  response = do_send(modulated)
  print(f"Got {response}")
  demodulated = dem(io.StringIO(response))
  print(f"...parsed as {demodulated}")
  as_expr = py_to_tree(demodulated)
  print(f"as_expr {as_expr}")

  return as_expr

def draw_helper(data, img_index=0, draw_dot_impl=None):
  for pt_data in data:
     (x, y) = pt_data
     if draw_dot_impl:
       draw_dot_impl(x, y, img_index)
     else:
       print(f"draw_dot({x}, {y}) img_index={img_index}")

def multipledraw_helper(data, draw_dot_impl=None, selected_layer=None):
  layers = 0
  for (index, item) in enumerate(reversed(data)):
    if selected_layer is not None:
      if index != selected_layer:
        # print (f"skipping layer {index} ({selected_layer}")
        continue
    layers = layers + 1
    draw_helper(item, img_index=len(data) - 1 - index, draw_dot_impl=draw_dot_impl)
  print(f'{layers} layers drawn! (selected layer = {selected_layer})')

# https://message-from-space.readthedocs.io/en/latest/message38.html
def interact(protocol_evaluator, state, vector):
  print ()
  print(" >>> Running protocol... <<<")
  print(f"current_state={tree_to_py(state)}\n")
  print(f"vector={tree_to_py(vector)}\n")
  res = protocol_evaluator(state, vector)

  # Note: res will be modulatable here (consists of cons, nil and numbers only)
  print(f"eval res {res}")
  (flag, newState, data) = tree_to_py(res)
  #newState = eval(Ap(Atom("car"), Ap(Atom("cdr"), res)))
  print(f"flag={flag}\nnewState={newState}")
  newState = py_to_tree(newState)
  if state == newState:
    print("State remained unchanged")
  else:
    print (" >>> NEW STATE!!!")

  if flag == 0:
      return (newState, data)

  return interact(protocol_evaluator, newState, my_send_to_alien_proxy(data))
