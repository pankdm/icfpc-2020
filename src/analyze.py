import re

def sorted_defs(defs):
  defs_list = [[token, lexems] for token, lexems in defs.items()]
  return sorted(defs_list, key=lambda _def: len(_def[1]))

def get_trivial_and_nontrivial_defs(defs, iterations=10):
  inlined_defs = [[token, inline(defs, token, iterations)] for token, lexems in sorted_defs(defs)]
  trivial_defs = [[token, lexems] for token, lexems in inlined_defs if not get_unique_refs(lexems)]
  trivial_tokens = set([token for token, lexems in trivial_defs])
  nontrivial_tokens = [token for token, lexems in defs.items() if token not in trivial_tokens]
  nontrivial_defs = { token: lexems for token, lexems in defs.items() if token in nontrivial_tokens }
  nontrivial_defs = sorted_defs(nontrivial_defs)
  return trivial_defs, nontrivial_defs

def get_unique_fns(lexems, acc=None):
  acc = acc if acc else set()
  for l in lexems:
    if type(l) == list:
      acc = acc.union(get_unique_fns(l))
    elif type(l) == str and not re.match(r'^[\-:0-9]', l):
      acc.add(l)
  return acc

def get_unique_refs(lexems, acc=None):
  acc = acc if acc else set()
  for l in lexems:
    if type(l) == list:
      acc = acc.union(get_unique_refs(l))
    elif type(l) == str and l[0] == ':':
      acc.add(l)
  return acc

def get_all_unique_fns(defs):
  unique_fns = set()
  for token, lexems in defs.items():
    unique_fns = unique_fns.union(get_unique_fns(lexems))
  return unique_fns

def is_token(lexem):
  return type(lexem) == str and lexem[0] == ':'

def inline(defs, token, max_iterations=None):
  if not defs.get(token):
    raise Exception(f'Token "{token}" not found')

  def unfold(token, max_iterations=None):
    lexems = defs.get(token)
    iterations_left = None
    if type(max_iterations) == int:
      if max_iterations <= 0:
        return token
      else:
        iterations_left = max_iterations - 1
    unfolded = []
    for lexem in lexems:
      if is_token(lexem):
        unfolded_lexem = unfold(lexem, iterations_left)
        if len(unfolded_lexem) == 1:
          unfolded.append(unfolded_lexem[0])
        else:
          unfolded.append(unfolded_lexem)
      else:
        unfolded.append(lexem)
    return unfolded

  result = unfold(token, max_iterations)
  return result
