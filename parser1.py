# Let's try to parse numbers first

# Every parser takes string as its input,
# and returns:
# - (None, input) if it couldn't parse the input
# - (result, tail) if it parsed the input
def keyword(s: str, *keywords) -> (str, str):
    for k in keywords:
        if s.startswith(k):
            return k, s[len(k):]
    return None, s

def first_of(s: str, *parsers) -> (str, str):
    for parser in parsers:
        r, s = parser(s)
        if r is not None:
            return r, s
    return None, s

def digit(s: str) -> (object, str):
    if len(s) == 0:
        return None, s
    d = ord(s[0]) - ord('0')
    if d < 0 or d > 9:
        return None, s
    return d, s[1:]

def simple_number(s: str) -> (object, str):
    r = None
    while True:
        d, s = digit(s)
        if d is None:
            return r, s

        # digit successfully parsed d here
        if r is None:
            r = d
        else:
            r = r * 10 + d

def fractional_number(s: str) -> (object, str):
    n, s = simple_number(s)
    if n is None:
        return None, s

    kw, s = keyword(s, '.')
    if kw is None:
        return n, s

    fs = s[1:]  # Skip '.'
    f, s = simple_number(fs)
    if f is None:
        return n, s

    fractional_digit_count = len(fs) - len(s)
    n = n + f / (10 ** fractional_digit_count)
    return n, s

def number(s: str) -> (object, str):
    if len(s) == 0:
        return None, s
    if s[0] != '-':
        return fractional_number(s)

    n, t = fractional_number(s[1:])
    if n is None:
        return None, s
    return -n, t

def bracket_expr(s: str) -> (object, str):
    kw, t = keyword(s, '(')
    if kw is None:
        return None, s

    e, t = expr(t)
    if e is None:
        return None, s

    kw, t = keyword(t, ')')
    if kw is None:
        return None, s
    return ("brackets", e), t

def mul_operand(s: str) -> (object, str):
    return first_of(s, bracket_expr, number)

def mul_expr(s: str) -> (object, str):
    l_value, s = mul_operand(s)
    if l_value is None:
        return None, s

    while True:
        op, t = keyword(s, '*', '/')
        if op is None:
            return l_value, s

        r_value, t = mul_operand(t)
        if r_value is None:
            return l_value, s

        l_value = (op, l_value, r_value)
        s = t

def add_expr(s: str) -> (object, str):
    l_value, s = mul_expr(s)
    if l_value is None:
        return None, s

    while True:
        op, t = keyword(s, '+', '-')
        if op is None:
            return l_value, s

        r_value, t = mul_expr(t)
        if r_value is None:
            return l_value, s

        l_value = (op, l_value, r_value)
        s = t

def expr(s: str) -> (object, str):
    return first_of(s, add_expr)