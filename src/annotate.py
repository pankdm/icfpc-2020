# Usage:
#    python3 src/annotate.py galaxy.txt

import sys
import re
import os
import time
import copy

from decode import parse_program, read_source, sorted_defs
from funcs import *

def sorted_by_id(defs):
  return sorted(defs.items(), key=lambda _def: _def[0])

def create_log(it):
  timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
  # datetime.utcnow().isoformat()
  # folder = "annotations/tmp/{}".format(timestamp)
  folder = "annotations/tmp"
  os.makedirs(folder, exist_ok=True)
  filepath = "{}/{:03d}.txt".format(folder, it)
  return open(filepath, 'w')

def create_eval_log(it):
  timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
  # datetime.utcnow().isoformat()
  # folder = "annotations/tmp/{}".format(timestamp)
  folder = "annotations/eval"
  os.makedirs(folder, exist_ok=True)
  filepath = "{}/{:08d}.txt".format(folder, it)
  return open(filepath, 'w')

def expr_for_tokens(tokens):
  stream = TokenStream(tokens)
  expr = parse_next_expr(stream)
  return expr

def try_eval(expr, whitelist, allow_recursion=False, defs={}, recursion_depth_map={}):
  if expr.name.startswith(":"):
    maybe_eval = whitelist.get(expr.name, None)
    if maybe_eval:
        return maybe_eval
    if allow_recursion:
      print(f"Descending into {expr}, {recursion_depth_map}")
      if recursion_depth_map.get(expr.name, 0) > 1000:
        # raise RuntimeError(f"Recursion deeper than 1000, expr={expr}")

        # Returning zero just to see if we can progress elsewhere.
        return 0
      sub_expr = expr_for_tokens(defs[expr.name])
      new_recursion_depth_map = dict(recursion_depth_map)
      new_recursion_depth_map[expr.name] = recursion_depth_map.get(expr.name, 0) + 1
      return try_eval(sub_expr, whitelist, allow_recursion=allow_recursion, defs=defs, recursion_depth_map=new_recursion_depth_map)
    else:
      raise RuntimeError("Dereferencing is not supported")
  elif re.match(r'-?\d+', expr.name):
    return int(expr.name)
  elif expr.name == "ap":
    left = try_eval(expr.args[0], whitelist, allow_recursion=allow_recursion, defs=defs, recursion_depth_map=recursion_depth_map)
    right = try_eval(expr.args[1], whitelist, allow_recursion=allow_recursion, defs=defs, recursion_depth_map=recursion_depth_map)
    return AP(left, right)
  else:
    func = FUNCTIONS.get(expr.name, None)
    assert func, f'Unknown func: {expr.name}'
    return func

ID_COUNTER = 0
  
class Expr:
  def __init__(self, name, args):
    global ID_COUNTER
    self.name = name
    self.args = args
    self.parent = None
    self.id = ID_COUNTER
    ID_COUNTER += 1

  def __repr__(self):
    return f'({self.name}, id={self.id})'

  def dump(self):
    if self.name == "ap":
      left = self.args[0].dump()
      right = self.args[1].dump()
      return f'({self.name} {left} {right})'
    else:
      return self.name
  
  def find_left(self):
    if self.name == "ap":
      return self.args[0].find_left()
    return self

  def validate_parents(self):
    if self.name == "ap":
      assert self.args[0].get_parent().id == self.id, f"Mismatched id at {self.args[0]}"
      assert self.args[1].get_parent().id == self.id, f"Mismatched id at {self.args[1]}"
      self.args[0].validate_parents()
      self.args[1].validate_parents()

  def get_parent(self):
    print (f"calling parent on {self}")
    assert self.parent, f"Error while calling parent on {self}"
    return self.parent


class TokenStream:
  def __init__(self, vec):
    self.vec = vec
    self.index = 0

  def read(self):
    res = self.vec[self.index]
    self.index += 1
    return res

def parse_from_tokens(tokens):
  stream = TokenStream(tokens)
  expr = parse_next_expr(stream)
  return expr


def create_ap_node(arg1, arg2):
  expr = Expr("ap", [arg1, arg2])
  arg1.parent = expr
  arg2.parent = expr
  return expr

def update_args_in_ap_node(ap_node, arg1, arg2):
  ap_node.args = [arg1, arg2]
  arg1.parent = ap_node
  arg2.parent = ap_node

def parse_next_expr(s):
  token = s.read()
  if token == "ap":
    x0 = parse_next_expr(s)
    x1 = parse_next_expr(s)

    expr = create_ap_node(x0, x1)
    return expr
  return Expr(token, [])


def simplification(sorted_defs):
  whitelist = {}
  for it in range(10):
    current_whitelist = {}
    with create_log(it) as output:
      for name, tokens in sorted_defs:
        stream = TokenStream(tokens)
        expr = parse_next_expr(stream)
        dump = expr.dump()

        try:
          maybe_eval = try_eval(expr, whitelist)
          current_whitelist[name] = maybe_eval
        except RuntimeError:
          maybe_eval = "???"
        output.write(f'{name} = {dump}\n')
        output.write(f'      {maybe_eval}\n')
    whitelist.update(current_whitelist)
  
  return whitelist

def honest_eval(def_to_eval, defs, args, whitelist):
  tokens = defs[def_to_eval]




# class to keep track of current eval state with all substituions
class TreeState:
  def __init__(self):
    # main expression that evaluates main
    self.main_expr = None
    # all definitions
    self.defs_expr = None

  def dump(self, counter):
    with create_eval_log(counter) as output:
      output.write("Main: \n")
      output.write(f"{self.main_expr.dump()}")

      output.write("\n\n")
  
  def validate(self):
    self.main_expr.validate_parents()
    print ("  Validation passed")

  def replace_c_combinator(self, c_node):
    p0 = c_node.get_parent()
    p1 = p0.get_parent()
    p2 = p1.get_parent()

    x0 = p0.args[1]
    x1 = p1.args[1]
    x2 = p2.args[2]

    new_p0 = create_ap_node(x0, x2)
    update_args_in_ap_node(p2, new_p0, x1)

  def replace_left(self):
    # find left-most node
    left = self.main_expr.find_left()
    print (f'Found {left} node, parent = {left.parent}')
    if left.name.startswith(":"):
      parent = left.parent
      assert parent, f"No parent found: {parent}"
      # do a substitution
      subtree = copy.copy(self.defs_expr[left.name])
      subtree.parent = parent
      parent.args[0] = subtree
      return
    if left.name == "c":
      self.replace_c_combinator(left)
      return




def tree_eval(defs):
  print('Running eval')
  state = TreeState()
  # running galaxy(state, vector) with
  #   state = nil
  #   vector = (0, 0)
  # ap ap ap interact x0 nil ap ap vec 0 0
  # ap ap ap interact x2 x4 x3 = ap (ap f38 x2) (ap (ap x2 x4) x3)
  galaxy = " ".join(defs["galaxy"])
  main_expr_tokens = f"ap ap {galaxy} nil ap ap cons 0 0".split(" ")

  state.main_expr = parse_from_tokens(main_expr_tokens)
  state.defs_expr = {}
  for name, tokens in defs.items():
    state.defs_expr[name] = parse_from_tokens(tokens)

  # now we have a state
  # let's start doing substitutions
  state.dump(counter=0)
  for counter in range(1, 10):
    print ()
    print (f"iter = {counter}")
    state.replace_left()
    # validate to make sure we updated parents correctly
    state.validate()
    state.dump(counter)


def main():
  sys.setrecursionlimit(10000)
  defs = parse_program(read_source(sys.argv[1]))

  run_eval = True
  if run_eval:
    tree_eval(defs)
    return

  run_simplification=True
  if run_simplification:
    sorted_defs = sorted_defs(defs)
    whitelist = simplification(sorted_defs)
  else:
    # Try to run the naive recursive evaluation. See "return 0" above, where to try to abort recusions that are too deep.
    # Currently it hangs with the following expr call depths:
    #   Descending into :1141, {':1338': 1, ':1342': 1, ':1343': 44, ':1141': 555}
    result = try_eval(expr_for_tokens(["ap", "ap", ":1338", "0", "0"]), whitelist={}, allow_recursion=True, defs=defs)
    print("result={result}")

if __name__ == "__main__":
  main()


