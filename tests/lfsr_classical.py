from context import LFSR
"""
Test for LFSR.generate_classical
"""
DEGREE = 5
TAP_POSITIONS = [1, 3]
SEED = 0b11010
ITERATIONS = 20

lfsr = LFSR(degree=DEGREE, tap_positions=TAP_POSITIONS)
lfsr.generate_classical(bitseq=SEED, iterations=ITERATIONS)
log = lfsr.log
stream = lfsr.stream
if __name__ == '__main__':
    print(f"Bitstream: {stream}")
    print(f"State 0:\t{format(SEED, '0' + str(DEGREE) + 'b')}")
    for iteration in range(1, ITERATIONS+1):
        print(f"State {iteration}:\t{log[iteration-1]}")
     