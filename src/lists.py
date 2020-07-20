# from funcs import *
from galaxy_evaluator import *

def py_to_tree(item):
  if isinstance(item, int):
    return Val(item)
  elif item is None:
    return Atom("nil")
  elif type(item) == tuple:
    (first, second) = item
    first = py_to_tree(first)
    second = py_to_tree(second)
    return Ap(Ap(Atom("cons"), first), second)
  elif type(item) == list:
    if item:
      first = py_to_tree(item[0])
      second = py_to_tree(item[1:])
      return Ap(Ap(Atom("cons"), first), second)
    else:
      return Atom("nil")
  else:
    raise TypeError(f"WTF is {item}")

def tree_to_py(item):
  # print(f"tree_to_py {item}")
  if isinstance(item, Val):
    return item.Value
  elif isnil(item):
    return []
  elif isinstance(item, Ap):
    head = tree_to_py(eval(Ap(Atom("car"), item)))
    tail = tree_to_py(eval(Ap(Atom("cdr"), item)))
    if type(tail) == list:
      return [head] + tail
    else:
      return (head, tail)
  else:
    raise TypeError(f"WTF is {item}")


if __name__ == "__main__":
  test = [2, [1, -1], 0]
  print (test)
  print (py_to_tree(test))
  print (tree_to_py(py_to_tree(test)))
