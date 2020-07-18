# Usage:
#    python3 src-v2/run_galaxy.py galaxy.txt

import sys
import re
import os
import time
import copy
import shutil

ID_COUNTER = 0
GLOBAL_LOG_COUNTER = 0
  
def create_ap_node(left, right):
  expr = Expr("ap", left, right)
  left.parent = expr
  right.parent = expr
  return expr

def update_args_in_ap_node(ap_node, left, right):
  ap_node.left = left
  ap_node.right = right
  left.parent = ap_node
  right.parent = ap_node


class Expr:
  def __init__(self, name, left, right):
    global ID_COUNTER
    self.name = name
    self.left = left
    self.right = right
    self.parent = None
    self.id = ID_COUNTER
    ID_COUNTER += 1

  def __repr__(self):
    return f'({self.name}, id={self.id})'

  def deep_clone(self):
    if self.name == "ap":
        left = self.left.deep_clone()
        right = self.right.deep_clone()
        return create_ap_node(left, right)
    return Expr(self.name, None, None)

  def count(self):
    if self.name == "ap":
      return self.left.count() + self.right.count() + 1
    else:
      return 1


  def dump(self):
    if self.name == "ap":
      left = self.left.dump()
      right = self.right.dump()
      return f'({self.name}[{self.id}] {left} {right})'
    else:
      return self.name
  
  def dump_with_indent(self, indent = 0):
    shift = ' ' * indent
    if self.name == "ap":
      left = self.left.dump_with_indent(indent + 2)
      right = self.right.dump_with_indent(indent + 2)
      return f'{shift}({self.name}[{self.id}]\n{left}\n{right} \n{shift})'
    else:
      return f'{shift}{self.name}'


  def find_left(self):
    if self.name == "ap":
      return self.left.find_left()
    return self

  def validate_parents(self):
    if self.name == "ap":
      assert self.left.get_parent().id == self.id, f"Mismatched id at {self.left}"
      assert self.right.get_parent().id == self.id, f"Mismatched id at {self.right}"
      self.left.validate_parents()
      self.right.validate_parents()

  def get_parent(self):
    # print (f"calling parent on {self}")
    if not self.parent:
        print (self.dump())
        assert False, f"Error while calling parent on {self}"
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

def parse_next_expr(s):
  token = s.read()
  if token == "ap":
    x0 = parse_next_expr(s)
    x1 = parse_next_expr(s)

    expr = create_ap_node(x0, x1)
    return expr
  return Expr(token, left=None, right=None)

def read_source(filename='galaxy.txt'):
  with open(filename, 'r') as galaxy_txt:
    program = galaxy_txt.read()
    lines = program.split('\n')
    non_empty_lines = filter(lambda l: len(l), lines)
    return non_empty_lines



def parse_program(code_lines):
  # example code line:
  # ":1042 = ap ap cons 4 ap ap cons 63935 nil"
  #  ^       ^
  #  token   fn body
  defs = {}
  for ln in code_lines:
    [token, body] = [chunk.strip() for chunk in ln.split('=')]
    lexems = body.split()
    defs[token] = lexems
  return defs

# class to keep track of current eval state with all substituions
class TreeState:
  def __init__(self, tag):
    # main expression that evaluates main
    self.main_expr = None
    # all definitions
    self.defs_expr = None
    self.tag = tag

  def create_eval_log(self, counter):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    # datetime.utcnow().isoformat()
    # folder = "annotations/tmp/{}".format(timestamp)
    folder = "annotations/eval"
    os.makedirs(folder, exist_ok=True)
    filepath = "{}/{:08d}-{}-{:03d}.txt".format(folder, GLOBAL_LOG_COUNTER, self.tag, counter)
    return open(filepath, 'w')


  def dump(self, counter):
    global GLOBAL_LOG_COUNTER
    GLOBAL_LOG_COUNTER += 1
    with self.create_eval_log(counter) as output:
      output.write(f"Main: {self.main_expr.count()}\n")
      output.write(f"{self.main_expr.dump()}\n")
      output.write(f"{self.main_expr.dump_with_indent()}\n")

      output.write("\n\n")
  
  def validate(self):
    self.main_expr.validate_parents()
    print ("  Validation passed")

  def reduce(self, max_iter=100):
    # now we have a state
    # let's start doing substitutions
    self.dump(counter=0)
    for counter in range(1, max_iter):
      print ()
      print (f"iter = {counter}, main -> {self.main_expr.count()}")
      self.replace_left()
      # validate to make sure we updated parents correctly
      self.validate()
      self.dump(counter)    

  def replace_c_combinator(self, c_node):
    p0 = c_node.get_parent()
    p1 = p0.get_parent()
    p2 = p1.get_parent()

    x0 = p0.right
    x1 = p1.right
    x2 = p2.right

    new_left = create_ap_node(x0, x2)
    update_args_in_ap_node(p2, new_left, x1)

  def replace_b_combinator(self, b_node):
    p0 = b_node.get_parent()
    p1 = p0.get_parent()
    p2 = p1.get_parent()

    x0 = p0.right
    x1 = p1.right
    x2 = p2.right

    new_right = create_ap_node(x1, x2)
    update_args_in_ap_node(p2, x0, new_right)

  def replace_s_combinator(self, s_node):
    p0 = s_node.get_parent()
    p1 = p0.get_parent()
    p2 = p1.get_parent()

    x0 = p0.right
    x1 = p1.right
    x2 = p2.right

    new_left = create_ap_node(x0, x2.deep_clone())
    new_right = create_ap_node(x1, x2.deep_clone())
    update_args_in_ap_node(p2, new_left, new_right)

  def replace_eq_combinator(self, eq_node):
    p0 = eq_node.get_parent()
    p1 = eq_node.get_parent()
    
    x0 = p0.right
    x1 = p1.right

    x0.parent = None
    x1.parent = None

    left_state = TreeState(str(x0.id))
    left_state.main_expr = x0
    left_state.defs_expr = self.defs_expr
    left_state.reduce(max_iter=10)


  def replace_left(self):
    # find left-most node
    left_most = self.main_expr.find_left()
    print (f'Found {left_most} node, parent = {left_most.parent}')
    if left_most.name.startswith(":"):
      parent = left_most.parent
      assert parent, f"No parent found: {parent}"
      # do a substitution
      ref = self.defs_expr[left_most.name]
      subtree = ref.deep_clone()

      subtree.parent = parent
      parent.left = subtree
    elif left_most.name == "c":
      self.replace_c_combinator(left_most)
    elif left_most.name == "b":
      self.replace_b_combinator(left_most)
    elif left_most.name == "s":
      self.replace_s_combinator(left_most)
    # elif left_most.name == "eq":
    #   self.replace_eq_combinator(left_most)
    else:
      assert False, f"Unimplemented op: {left_most}"

def tree_eval(defs):
  print('Running eval')
  shutil.rmtree('annotations/eval', ignore_errors=True)

  state = TreeState("main")
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

  state.reduce(max_iter=100)


def main():
  sys.setrecursionlimit(10000)
  defs = parse_program(read_source(sys.argv[1]))

  run_eval = True
  if run_eval:
    tree_eval(defs)
    return


if __name__ == "__main__":
  main()

