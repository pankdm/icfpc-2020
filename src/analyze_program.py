from src.decode import read_source, parse_program
import re

defs = parse_program(read_source())

def sorted_defs(defs):
  defs_list = [[token, lexems] for token, lexems in defs.items()]
  return sorted(defs_list, key=lambda _def: len(_def[1]))

def get_unique_lexems(defs):
  unique_lexems = set()
  for token, lexems in defs.items():
    for lexem in lexems:
      if not re.match(r'^[:\-0-9]', lexem):
        unique_lexems.add(lexem)
  return unique_lexems

def is_token(lexem):
  return lexem[0] == ':'

def inline(defs, token, max_iterations=None):
  if not defs.get(token):
    raise Exception(f'Token "{token}" not found')

  unfold_stats = {
    'calls': 0,
  }
  def unfold(token, max_iterations=None, stats=unfold_stats):
    unfold_stats['calls'] = unfold_stats['calls'] + 1
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
        unfolded_lexem = unfold(lexem, iterations_left, stats=stats)
        if len(unfolded_lexem) == 1:
          unfolded.append(unfolded_lexem[0])
        else:
          unfolded.append(unfolded_lexem)
      else:
        unfolded.append(lexem)
    return unfolded

  result = unfold(token, max_iterations)
  print(f'Called `unfold()` {unfold_stats["calls"]} times')
  return result
