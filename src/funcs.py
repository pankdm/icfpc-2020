functions = {
  'ap': lambda f, x: f.__call__(x),
  'cons': lambda x1: lambda x2: [x1, x2],
  'add': lambda x1: lambda x2: [x1, x2],
  'inc': lambda x1: lambda x2: [x1, x2],
  'dec': lambda x1: lambda x2: [x1, x2],
  'cons',
  'b',
  'c',
  't',
  'ap',
  's': lambda x1: lambda x2: lambda x3: (lambda *args: x1(x3(x1(x3)(*args))))
  'mul': lambda x1: lambda x2: x1 * x2,
  'i': lambda x: x,
  'cdr',
  'nil',
  'eq',
  'add',
  'lt',
  'car',
  'div',
  'neg',,
  'isnil'
}

def B_combinator(x, y, z):
  return (x, y(z))

def C_combinator(x, y, z):
  return (x, z, y)

K_combinator = lambda x: lambda y: x

def W_combinator(x, y):
  return (x, y, y)

def S_combinator(x, y, z):
  return (x, z, y(z))

def I_combinator(x):
  return x

def if0(flag, arg1, arg2):
  return arg2 if flag else arg1
