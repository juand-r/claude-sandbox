import sys, re
TABLE = re.compile(r"^(E-(\^\d)?|E(\^\d)?|\?\(22,17,w7\)|\?\(15,-4,w\d+\)|\?\(30,-8,w\d+\))@")
for line in sys.stdin:
    t, *objs = line.split()
    print(t, " ".join(o for o in objs if not TABLE.match(o)), "| nT", sum(bool(TABLE.match(o)) for o in objs))
