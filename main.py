from parser1 import *

e = "(2-1)+(3/(1+1)"

# test change 2

print(e)
r, t = expr(e)
if r is None:
    print("Couldn't parse.")
else:
    print(r)
    if len(t) != 0:
        print("Remaining part: " + t)

