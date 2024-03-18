import sympy as sp
from sympy.abc import x

def count_state(element, condition):
    yield 1 if element==condition else 0

def count_func(enumerable, condition) -> int:
    count: int = 0
    for element in enumerable:
        count += next(count_state(element, condition))
    return count

def hamming_len(string1: str, string2: str) -> int:

    dist: int = 0
    if len(string1) == len(string2):
        for i, char in enumerate(string1):
            if char != string2[i]:
                dist += 1
        return dist
    else:
        raise IndexError(f"string lengths mismatch, found lengths {len(string1)} and {len(string2)}")
    
def str_to_sp(polystring):

    sp_construct: list[int] = []
    for i, char in enumerate(polystring):
        if char == '^':
            pwr: int = int(polystring[i+1])
            sp_construct += [pwr]

    sp_poly: sp.core.symbol.Symbol = x**0
    for pwr in sp_construct:
        if pwr == 0:
            pass 
        else:
            sp_poly += x**pwr 

    return sp_poly 

