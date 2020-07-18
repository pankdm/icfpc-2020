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

DEBUG_OUTPUT = False
DUMP_ALL_LOGS = False
  
def create_ap_node(left, right):
  expr = Expr("ap", left, right)
  left.parent = expr
  return expr

def update_node_in_place(node, name, left, right):
  node.left = left
  if left:
    left.parent = node
  node.right = right
  node.name = name


class Expr:
  def __init__(self, name, left, right):
    assert isinstance(name, str), f"type mismatch: {name}"
    assert left is None or isinstance(left, Expr), f"type mismatch {left}"
    assert right is None or isinstance(right, Expr), f"type mismatch {right}"

    global ID_COUNTER
    self.name = name
    self.left = left
    self.right = right
    self.parent = None
    self.id = ID_COUNTER
    ID_COUNTER += 1

  def __repr__(self):
    return f'({self.name}, id={self.id})'

  def __eq__(self, other):
    if self.name != other.name:
      return False
    if self.name == "ap":
      return (self.left == other.left) and (self.right == other.right)
    else:
      return True

  def deep_clone(self):
    if self.name == "ap":
        left = self.left.deep_clone()
        right = self.right.deep_clone()
        return create_ap_node(left, right)
    return Expr(self.name, None, None)

  def count(self):
    return len(self.collect_ids())
    # if self.name == "ap":
    #   return self.left.count() + self.right.count() + 1
    # else:
    #   return 1

  def collect_ids(self):
    if self.name == "ap":
      return set.union(self.left.collect_ids(), self.right.collect_ids(), {self.id})
    else:
      return {self.id}


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
      left = self.left.dump_with_indent(indent + 4)
      right = self.right.dump_with_indent(indent + 4)
      return f'{shift}({self.name}[{self.id}]\n{left}\n{right} \n{shift})'
    else:
      return f'{shift}{self.name}'


  def find_left(self):
    if self.name == "ap":
      return self.left.find_left()
    return self

  def validate_parents(self):
    if DEBUG_OUTPUT:
        print (f"{self}, parent = {self.parent}")
    if self.name == "ap":
      assert self.left.get_parent().id == self.id, f"Mismatched id at {self.left}"
      # assert self.right.get_parent().id == self.id, f"Mismatched id at {self.right}"
      self.left.validate_parents()
      self.right.validate_parents()

  def get_num_parents(self, num):
    if num == 1:
      return (self.parent, )
    if not self.parent:
      return None
    res = self.parent.get_num_parents(num - 1)
    if res is None:
      return None
    return (self.parent, ) + res
    

  def get_parent(self):
    # print (f"calling parent on {self}")
    if not self.parent:
        print ('Error: \n', self.dump())
        # print ('Error: \n', self.dump_with_indent())
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
    with self.create_eval_log(counter) as output:
      output.write(f"Function {self.tag}: {self.main_expr.count()}\n")
      output.write(f"{self.main_expr.dump()}\n")
      output.write(f"{self.main_expr.dump_with_indent()}\n")

      output.write("\n\n")
  
  def validate(self):
    self.main_expr.validate_parents()
    if DEBUG_OUTPUT:
      print ("  Validation passed")

  def reduce(self, max_iter=100):
    global GLOBAL_LOG_COUNTER
    # now we have a state
    # let's start doing substitutions
    self.dump(counter=0)
    for counter in range(1, max_iter):
      print ()
      print (f"{GLOBAL_LOG_COUNTER}: iter = {counter}, {self.tag} -> {self.main_expr.count()}")
      changed = self.replace_left()
      if changed is None:
        assert False, "Got None from replace_left()!"
      if not changed:
        print (" >> Noting to replace, breaking")
        break
      # validate to make sure we updated parents correctly
      print ("Running validation after replacemenet")
      self.validate()
      if DUMP_ALL_LOGS:
        self.dump(counter)    

  def replace_c(self, c_node):
    parents = c_node.get_num_parents(3)
    if not parents:
      return False
    p0, p1, p2 = parents

    x0 = p0.right
    x1 = p1.right
    x2 = p2.right

    new_left = create_ap_node(x0, x2)
    update_node_in_place(p2, "ap", new_left, x1)
    return True

  def replace_b(self, b_node):
    parents = b_node.get_num_parents(3)
    if not parents:
      return False
    p0, p1, p2 = parents

    x0 = p0.right
    x1 = p1.right
    x2 = p2.right

    new_right = create_ap_node(x1, x2)
    update_node_in_place(p2, "ap", x0, new_right)
    return True

  def replace_s(self, s_node):
    parents = s_node.get_num_parents(3)
    if not parents:
      return False
    p0, p1, p2 = parents

    x0 = p0.right
    x1 = p1.right
    x2 = p2.right

    new_left = create_ap_node(x0, x2)
    new_right = create_ap_node(x1, x2)
    update_node_in_place(p2, "ap", new_left, new_right)
    return True

  def replace_t(self, t_node):
    parents = t_node.get_num_parents(2)
    if not parents:
      return False
    p0, p1 = parents

    x0 = p0.right
    # x1 = p1.right

    update_node_in_place(p1, x0.name, x0.left, x0.right)
    return True

  def replace_f(self, f_node):
    parents = f_node.get_num_parents(2)
    if not parents:
      return False
    p0, p1 = parents

    # x0 = p0.right
    x1 = p1.right

    update_node_in_place(p1, x1.name, x1.left, x1.right)
    return True

  def replace_i(self, i_node):
    parents = i_node.get_num_parents(1)
    if not parents:
      return False
    p0 = parents[0]

    x0 = p0.right

    update_node_in_place(p0, x0.name, x0.left, x0.right)
    return True


  def replace_eq(self, eq_node):
    parents = eq_node.get_num_parents(2)
    if not parents:
      return False
    p0, p1 = parents
    
    x0 = p0.right
    x1 = p1.right

    x0.parent = None
    x1.parent = None

    left_state = TreeState(str(x0.id))
    left_state.main_expr = x0
    left_state.defs_expr = self.defs_expr
    left_state.reduce(max_iter=10)

    right_state = TreeState(str(x1.id))
    right_state.main_expr = x1
    right_state.defs_expr = self.defs_expr
    right_state.reduce(max_iter=10)

    if left_state.main_expr == right_state.main_expr:
      new_name = "t"
    else:
      new_name = "f"
    update_node_in_place(p1, new_name, None, None)
    return True


  # returns True/False is there was replacement
  def replace_left(self):
    global GLOBAL_LOG_COUNTER
    GLOBAL_LOG_COUNTER += 1

    # find left-most node
    left_most = self.main_expr.find_left()
    print (f'Found {left_most} node, parent = {left_most.parent}')
    if left_most.name.startswith(":"):
      # parent = left_most.parent
      # assert parent, f"No parent found: {parent}"
      # do a substitution
      # ref = self.defs_expr[left_most.name].deep_clone()
      ref = self.defs_expr[left_most.name]
      update_node_in_place(left_most, ref.name, ref.left, ref.right)
      return True
    elif left_most.name == "c":
      return self.replace_c(left_most)
    elif left_most.name == "b":
      return self.replace_b(left_most)
    elif left_most.name == "s":
      return self.replace_s(left_most)
    elif left_most.name == "eq":
      return self.replace_eq(left_most)
    elif left_most.name == "f":
      return self.replace_f(left_most)
    elif left_most.name == "t":
      return self.replace_t(left_most)
    elif left_most.name == "i":
      return self.replace_i(left_most)
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
  if "galaxy" in defs:
    galaxy = " ".join(defs["galaxy"])
    main_expr_tokens = f"ap ap {galaxy} nil ap ap cons 0 0".split(" ")
  else:
    main_expr_tokens = defs["main"]

  state.main_expr = parse_from_tokens(main_expr_tokens)
  state.defs_expr = {}
  for name, tokens in defs.items():
    state.defs_expr[name] = parse_from_tokens(tokens)

  state.reduce(max_iter=1000)


def main():
  sys.setrecursionlimit(10000)
  defs = parse_program(read_source(sys.argv[1]))

  run_eval = True
  if run_eval:
    tree_eval(defs)
    return


if __name__ == "__main__":
  main()

