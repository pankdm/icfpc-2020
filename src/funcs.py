class CurriedFunction():
  name = None
  body = None
  required_args_cnt = None
  applied_args = None
  def __repr__(self):
    if not self.applied_args:
      return f'<{self.name}()>'
    else:
      return f'<{self.name}() ({len(self.applied_args)} of {self.required_args_cnt} args applied)>'
  def __init__(self, name, required_args_cnt, body, applied_args=None):
    self.name = name
    self.__name__ = name
    self.required_args_cnt = required_args_cnt
    self.body = body
    if applied_args:
      self.applied_args = applied_args[:]
    else:
      self.applied_args = []
  def __add__(self, other):
    raise TypeError(f"unsupported operand type(s) for +: '{self.name}' and '{type(other).__name__}'")
  def __sub__(self, other):
    raise TypeError(f"unsupported operand type(s) for -: '{self.name}' and '{type(other).__name__}'")
  def __mul__(self, other):
    raise TypeError(f"unsupported operand type(s) for *: '{self.name}' and '{type(other).__name__}'")
  def __truediv__(self, other):
    raise TypeError(f"unsupported operand type(s) for /: '{self.name}' and '{type(other).__name__}'")
  def __floordiv__(self, other):
    raise TypeError(f"unsupported operand type(s) for //: '{self.name}' and '{type(other).__name__}'")
  def __mod__(self, other):
    raise TypeError(f"unsupported operand type(s) for %: '{self.name}' and '{type(other).__name__}'")
  def __pow__(self, other):
    raise TypeError(f"unsupported operand type(s) for **: '{self.name}' and '{type(other).__name__}'")
  def __call__(self, arg):
    fn = self.__class__(self.name, self.required_args_cnt, self.body, self.applied_args)
    if len(fn.applied_args) < fn.required_args_cnt:
      fn.applied_args.append(arg)
    else:
      raise Exception(f'Function already had all args applied. Start to panic!!'
                      f' fn={fn} fn.applied_args={fn.applied_args} arg={arg}')
    if len(fn.applied_args) == fn.required_args_cnt:
      return fn.body(*fn.applied_args)
    else:
      return fn


class Ref():
  name = None
  defs = None
  def __init__(self, defs, name):
    self.name = name
    self.defs = defs
  def __repr__(self):
    return f'ref:{self.name}'
  def resolve(self):
    ref_value = self.defs.get(self.name)
    if type(ref_value) is Ref:
      return ref_value.resolve()
    return ref_value

class AP():
  parent = None
  operand = None
  left_leaf = None
  right_leaf = None

  @staticmethod
  def apply(f, x):
    '''
    AP method application. Example usage:
    AP.apply(INC, 1)
    # -> 2
    AP.apply(AP.apply(ADD, 1), 2)
    # -> 3
    '''
    return AP.calc(f)(x)

  def compute(self):
    return AP.apply(self.left_leaf, self.right_leaf)

  @staticmethod
  def calc(node):
    if type(node) == Ref:
      node = node.resolve()
    if type(node) == AP:
      return node.compute()
    return node

  def __init__(self, left_node=None, right_node=None):
    '''
    AP tree node. Example usage:

    tree = AP(INC, 1)
    tree.compute()
    # -> 2

    tree = AP(ADD, 1)
    tree.compute()
    # -> <ADD() (1 of 2 args applied)>

    tree = AP(AP(ADD, 1), 2)
    tree.compute()
    # -> 3

    tree = AP(AP(ADD, 1), 2)
    print(tree)
    # -> (AP (AP <ADD()> 1) 2)
    '''
    self.add_left(left_node)
    self.add_right(right_node)

  def to_str(self, max_depth=5):
    if max_depth < 0:
      return '...'
    self_repr = 'AP'
    def leaf_repr(leaf):
      if not leaf:
        return None
      return leaf.to_str(max_depth-1) if type(leaf) == AP else f'{leaf}'
    left_repr = leaf_repr(self.left_leaf)
    right_repr = leaf_repr(self.right_leaf)
    if left_repr or right_repr:
      return '(' + " ".join(filter(lambda x: x, [self_repr, left_repr, right_repr])) + ')'
    else:
      return self_repr
  def __repr__(self):
    return self.to_str(5)
  def __str__(self):
    return self.to_str(5)

  def __eq__(self, other):
    if type(other) != AP:
      raise TypeError(f"unsupported operand type(s) for ==: '{type(self).__name__}' and '{type(other).__name__}'")
    return self.left_leaf == other.left_leaf and self.right_leaf == other.right_leaf

  def __add__(self, other):
    raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")
  def __sub__(self, other):
    raise TypeError(f"unsupported operand type(s) for -: '{type(self).__name__}' and '{type(other).__name__}'")
  def __mul__(self, other):
    raise TypeError(f"unsupported operand type(s) for *: '{type(self).__name__}' and '{type(other).__name__}'")
  def __truediv__(self, other):
    raise TypeError(f"unsupported operand type(s) for /: '{type(self).__name__}' and '{type(other).__name__}'")
  def __floordiv__(self, other):
    raise TypeError(f"unsupported operand type(s) for //: '{type(self).__name__}' and '{type(other).__name__}'")
  def __mod__(self, other):
    raise TypeError(f"unsupported operand type(s) for %: '{type(self).__name__}' and '{type(other).__name__}'")
  def __pow__(self, other):
    raise TypeError(f"unsupported operand type(s) for **: '{type(self).__name__}' and '{type(other).__name__}'")

  def leaf_complete(self, leaf):
    if leaf is None:
      return False
    return leaf.is_complete() if type(leaf) == AP else True

  def is_complete(self):
    return self.leaf_complete(self.left_leaf) and self.leaf_complete(self.right_leaf)

  def add_edge(self, leaf):
    '''
    Automatic edge-edding, according to lisp semantics.
    Example usage:

    tree = AP()
    tree.add_edge(AP())
    tree.add_edge(ADD)
    tree.add_edge(AP())
    tree.add_edge(INC)
    tree.add_edge(2)
    tree.add_edge(AP())
    tree.add_edge(INC)
    tree.add_edge(4)
    print(f'Tree complete: {tree.is_complete()}')
    tree
    # -> Tree complete: True
    # -> (AP (AP <ADD()> (AP <INC()> 2)) (AP <INC()> 4))
    '''
    if not self.left_leaf:
      self.add_left(leaf)
      return True
    if type(self.left_leaf) == AP and \
        self.left_leaf.add_edge(leaf):
      return True
    if not self.right_leaf:
      self.add_right(leaf)
      return True
    if type(self.right_leaf) == AP and \
        self.right_leaf.add_edge(leaf):
      return True
    return False

  def add_left(self, leaf):
    self.left_leaf = leaf
    if type(leaf) == AP:
      leaf.parent = self

  def add_right(self, leaf):
    self.right_leaf = leaf
    if type(leaf) == AP:
      leaf.parent = self


ADD = CurriedFunction('ADD', 2, lambda x1, x2: AP.calc(x1) + AP.calc(x2))
INC = CurriedFunction('INC', 1, lambda x0: AP.calc(x0) + 1)
DEC = CurriedFunction('DEC', 1, lambda x0: AP.calc(x0) - 1)
MUL = CurriedFunction('MUL', 2, lambda x0, x1: AP.calc(x0) * AP.calc(x1))
DIV = CurriedFunction('DIV', 2, lambda x0, x1: AP.calc(x0) / AP.calc(x1))
PWR2 = CurriedFunction('PWR2', 1, lambda x: AP.calc(x) ** 2)
S = CurriedFunction('S', 3, lambda x0, x1, x2: AP.apply(AP.apply(x0, x2), AP.apply(x1, x2)))
B = CurriedFunction('B', 3, lambda x0, x1, x2: AP.apply(x0, AP.apply(x1, x2)))
C = CurriedFunction('C', 3, lambda x0, x1, x2: AP.apply(AP.apply(x0, x2), x1))
T = CurriedFunction('T', 2, lambda x0, x1: x0)
F = CurriedFunction('F', 2, lambda x0, x1: x1)
I = CurriedFunction('I', 1, lambda x0: x0)
EQ = CurriedFunction('EQ', 2, lambda x0, x1: T if x0 == x1 or AP.calc(x0) == AP.calc(x1) else F)
LT = CurriedFunction('LT', 2, lambda x0, x1: T if AP.calc(x0) < AP.calc(x1) else F)
CONS = CurriedFunction('CONS', 3, lambda x0, x1, x2: AP.apply(AP.apply(x2, x0), x1))
NIL = CurriedFunction('NIL', 1, lambda x0: T)
ISNIL = CurriedFunction('ISNIL', 1, lambda x0: T if x0 == NIL else F)
CAR = CurriedFunction('CAR', 1, lambda x0: AP.apply(x0, T))
CDR = CurriedFunction('CDR', 1, lambda x0: AP.apply(x0, F))
NEG = CurriedFunction('NEG', 1, lambda x0: -AP.calc(x0))
DEAD_RECUR_LOOP = CurriedFunction('DEAD_RECUR_LOOP', 1, lambda x0: AP.apply(DEAD_RECUR_LOOP, x0))

FUNCTIONS = {
  'ap': AP,
  'add': ADD,
  'inc': INC,
  'dec': DEC,
  'mul': MUL,
  'div': DIV,
  's': S,
  'b': B,
  'c': C,
  't': T,
  'f': F,
  'i': I,
  'eq': EQ,
  'lt': LT,
  'cons': CONS,
  'nil': NIL,
  'isnil': ISNIL,
  'car': CAR,
  'cdr': CDR,
  'neg': NEG,
}
