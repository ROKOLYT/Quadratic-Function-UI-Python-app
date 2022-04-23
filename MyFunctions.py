from sympy import solve, Eq, sqrt, symbols as sym
import re


# noinspection PyBroadException
def coefficients(value):
    place_holder = value
    coef = ['', '', '', False]
    if 'x**2' in place_holder:

        try:
            coef[1] = re.search(r'xffffff2(.*)fffx', place_holder.replace('*', 'fff'))
            coef[1] = coef[1].group(1).replace('fff', '*')
        except Exception:
            pass
        if coef[1] is None:
            coef[1] = '1'
        if '*x' not in place_holder or len(place_holder.split('*x')) == 2:
            coef[1] = '0'
        try:
            coef[0] = place_holder.split('*x**')[0]
            if coef[0] == place_holder:
                coef[0] = '1'
        except Exception:
            coef[0] = '1'
        try:
            coef[2] = place_holder.split('*x')[2]
        except Exception:
            try:
                coef[2] = place_holder.split('*x')[1]
                if '**' in coef[2] and coef[1] != '0':
                    coef[2] = '0'
                else:
                    coef[2] = coef[2].replace('**2', '')

            except Exception:
                coef[2] = '0'
        print(coef)
        for i in range(3):
            coef[i] = eval(coef[i])
        coef[3] = True
    elif ')**2' in place_holder:
        coef[0] = eval(place_holder.split('*(x')[0])
        coef[1] = re.search(r'x(.*)bracketffffff2', place_holder.replace('*', 'fff').replace(')', 'bracket'))
        coef[1] = eval(coef[1].group(1))
        coef[1] = -coef[1]
        coef[2] = eval(place_holder.split(')**2')[1])
        print(coef)

    return coef


def mergeDicts(original, new):
    FinalDict = original.copy()
    FinalDict.update(new)
    return FinalDict


def missingVariables(dictOfVariables):
    symbols = dict(a=sym('a'), b=sym('b'), c=sym('c'), p=sym('p'), q=sym('q'), x1=sym('x1'), x2=sym('x2'),
                   delta=sym('delta'))
    var = mergeDicts(symbols, dictOfVariables)
    deltaEQ = Eq((var['b'] ** 2 - 4 * var['a'] * var['c']), var['delta'])
    x1EQ = Eq(((-var['b'] - sqrt(var['delta'])) / (2 * var['a'])), var['x1'])
    x2EQ = Eq(((-var['b'] + sqrt(var['delta'])) / (2 * var['a'])), var['x2'])
    pEQ = Eq((-var['b']) / (2 * var['a']), var['p'])
    pEQ2 = Eq(((var['x1'] + var['x2']) / 2), var['p'])
    qEQ = Eq(((-var['delta']) / (4 * var['a'])), var['q'])
    bEQ = Eq((-2 * var['a'] * var['p']), var['b'])
    cEQ = Eq((var['a'] * var['p'] ** 2 + var['q']), var['c'])
    solution = solve((deltaEQ, x1EQ, x2EQ, pEQ, pEQ2, qEQ, bEQ, cEQ))
    return solution


def ToBeReplaced(string):
    disallowed_characters = ['sqrt', '^', ':']
    equivalent = ['math.sqrt', '**', '/']
    string = string.strip()
    for i in range(len(disallowed_characters)):
        string = string.replace(disallowed_characters[i], equivalent[i])
    return string

