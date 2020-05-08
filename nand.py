from z3 import *

# input: ABC..., output: PQRS...
def name(i):
    return chr((ord('A') if i < I else (ord('P') - I)) + i)

I = 3 # num of curcuit inputs
P = 3 # num of NAND inputs

for N in range(1, 10): # num of NANDs
    S = Solver()
    p = [BitVec('p_%d' % i, (1 << I)) for i in range(N + I)]
    r = [[Int('r_%02d_%d' % (i, j)) for j in range(P)] for i in range(N + I)]

    for i in range(I):
        k = 0
        for j in range(1 << I):
            k |= ((j & (1 << i)) > 0) << j
        S.add(p[i] == k)

    for i in range(I, I + N):
        x = []
        for a in range(i):
            for b in range(i):
                for c in range(i):
                    # use 3-input NAND
                    x.append(And(p[i] == ~(p[a] & p[b] & p[c]),
                    r[i][0] == a, r[i][1] == b, r[i][2] == c))
        S.add(Or(x))

    # 3-input XNOR
    S.add(p[I + N - 1] == ~(p[0] ^ p[1] ^ p[2]))

    if S.check() == sat:
        rs = []
        for i in S.model().decls():
            if 'r_' in i.name(): rs.append(i)
        rs.sort(key=(lambda x: x.name()))
        cnt = 1
        for i in rs:
            print(name(S.model()[i].as_long()),
                end=' ' if cnt % P != 0 else ' -> %s\n' % name(int(i.name()[2:4])))
            cnt += 1
        break