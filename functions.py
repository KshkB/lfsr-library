"""
count_state and count_func below perform counts via yields rather than in-memory array manipulation
"""
def count_state(element, condition):
    yield 1 if element==condition else 0

def count_func(enumerable, condition) -> int:
    count = 0
    for element in enumerable:
        count += next(count_state(element, condition))
    return count