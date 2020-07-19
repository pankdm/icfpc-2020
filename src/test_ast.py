from decode import read_test_source, parse_program_with_ast
from funcs import *
test_defs_ast = parse_program_with_ast(read_test_source())
print(test_defs_ast)
# {':1': 1,
#  ':2': 2,
#  ':3': 3,
#  ':4': <INC()>,
#  ':5': <ADD()>,
#  ':6': (AP <ADD()> 2),
#  ':7': (AP (AP <CONS()> 4) 5),
#  ':8': (AP (AP ref::5 (AP <CAR()> ref::7)) 3),
#  'galaxy': ref::8}
AP.calc(test_defs_ast['galaxy'])
#  7