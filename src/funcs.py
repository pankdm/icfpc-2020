class CurriedFunction():
  name = None
  body = None
  required_args_cnt = None
  applied_args = None
  def __repr__(self):
    return f'<{self.name}() ({len(self.applied_args)} of {self.required_args_cnt} args applied)>'
  def __init__(self, name, required_args_cnt, body, applied_args=None):
    self.name = name
    self.__name__ = name
    self.required_args_cnt = required_args_cnt
    self.body = body
    if applied_args:
      self.applied_args = applied_args
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
      raise Exception(f'Function already had all args applied. Start to panic!!')
    if len(fn.applied_args) == fn.required_args_cnt:
      return fn.body(*fn.applied_args)
    else:
      return fn


AP = lambda f, x: f(x)

ADD = CurriedFunction('ADD', 2, lambda x1, x2: x1 + x2)
INC = CurriedFunction('INC', 1, lambda x0: x0 + 1)
DEC = CurriedFunction('DEC', 1, lambda x0: x0 - 1)
MUL = CurriedFunction('MUL', 2, lambda x0, x1: x0 * x1)
DIV = CurriedFunction('DIV', 2, lambda x0, x1: x0 / x1)
PWR2 = CurriedFunction('PWR2', 1, lambda x: x ** 2)
S = CurriedFunction('S', 3, lambda x0, x1, x2: AP(AP(x0, x2), AP(x1, x2)))
B = CurriedFunction('B', 3, lambda x0, x1, x2: AP(x0, AP(x1, x2)))
C = CurriedFunction('C', 3, lambda x0, x1, x2: AP(AP(x0, x2), x1))
T = CurriedFunction('T', 2, lambda x0, x1: x0)
F = CurriedFunction('F', 2, lambda x0, x1: x1)
I = CurriedFunction('I', 1, lambda x0: x0)
EQ = CurriedFunction('EQ', 2, lambda x0, x1: T if x0 == x1 else F)
LT = CurriedFunction('LT', 2, lambda x0, x1: T if x0 < x1 else F)
CONS = CurriedFunction('CONS', 3, lambda x0, x1, x2: AP(AP(x2, x0), x1))
NIL = CurriedFunction('NIL', 1, lambda x0: T)
ISNIL = CurriedFunction('ISNIL', 1, lambda x0: T if x0 == NIL else F)
CAR = CurriedFunction('CAR', 1, lambda x0: AP(x0, T))
CDR = CurriedFunction('CDR', 1, lambda x0: AP(x0, F))
NEG = CurriedFunction('NEG', 1, lambda x0: -x0)
DEAD_RECUR_LOOP = CurriedFunction('DEAD_RECUR_LOOP', 1, lambda x0: AP(DEAD_RECUR_LOOP, x0))



class Node():
  parent = None
  operand = None
  left_leaf = None
  right_leaf = None
  def __init__(self, operand, left_node=None, right_node=None):
    self.operand = operand
    self.left_node = left_node
    self.right_node = right_node
  def __str__(self):
    self_repr = str(self.operand)
    left_repr = str(self.left_leaf) if self.left_leaf else None
    right_repr = str(self.right_leaf) if self.right_leaf else None
    return " ".join(filter(lambda x: x, [self_repr, left_repr, right_repr]))
