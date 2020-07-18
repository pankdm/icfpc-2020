import sys

from syntax_tree import print_syntax_tree

for f in sys.stdin:
    print_syntax_tree(f)