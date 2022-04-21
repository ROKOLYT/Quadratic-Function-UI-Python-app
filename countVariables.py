from sympy import solve, Eq, sqrt, symbols as sym


def missingVariables(dictOfVariables):
    a, b, c, x1, x2, p, q, delta = sym('a,b,c,x1,x2,p,q,delta', real=True)
    filtered = {k: v for k, v in dictOfVariables.items() if v is not None}
    if not True:
        pass
    else:
        try:
            a = filtered['a']
        except Exception:
            pass
        try:
            b = filtered['b']
        except Exception:
            pass
        try:
            c = filtered['c']
        except Exception:
            pass
        try:
            p = filtered['p']
        except Exception:
            pass
        try:
            q = filtered['q']
        except Exception:
            pass
        try:
            delta = filtered['delta']
        except Exception:
            pass
        try:
            x1 = filtered['x1']
        except Exception:
            pass
        try:
            x2 = filtered['x2']
        except Exception:
            pass

    deltaEQ = Eq((b ** 2 - 4 * a * c), delta)
    x1EQ = Eq(((-b - sqrt(delta)) / (2 * a)), x1)
    x2EQ = Eq(((-b + sqrt(delta)) / (2 * a)), x2)
    pEQ = Eq((-b) / (2 * a), p)
    pEQ2 = Eq(((x1 + x2) / 2), p)
    qEQ = Eq(((-delta) / (4 * a)), q)
    bEQ = Eq((-2 * a * p), b)
    cEQ = Eq((a * p ** 2 + q), c)
    try:
        solution = solve((deltaEQ, x1EQ, x2EQ, pEQ, pEQ2, qEQ, bEQ, cEQ))
        return solution
    except ValueError:
        return 'Not enough data'



