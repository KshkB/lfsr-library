from context import LFSR
"""
Test for LFSR.generate_classical
"""
TAP_POSITIONS = [0, 1]
SEED = 0b110
try:
    DEGREE = len(bin(SEED))-2
except TypeError:
    DEGREE = len(SEED)

ITERATIONS = 1

lfsr = LFSR(degree=DEGREE, tap_positions=TAP_POSITIONS)
lfsr.generate(bitseq=SEED, iterations=ITERATIONS)
log = lfsr.log
stream = lfsr.stream

if __name__ == '__main__':
    print(f"Feedback polynomial: {lfsr.feedback_polynomial}")
    print(f"Bitstream: {stream}")
    print(f"Period: {lfsr.period}")
    print(f"State 0:\t{format(SEED, '0' + str(DEGREE) + 'b')}")
    for iteration in range(1, ITERATIONS+1):
        print(f"State {iteration}:\t{log[iteration-1]}")