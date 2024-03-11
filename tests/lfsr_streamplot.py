from context import LFSR
"""
Test for method LFSR.plot_stream
"""
TAP_POSITIONS = [1, 17, 20]
SEED = 0b100111101101101101101
DEGREE = len(bin(SEED))-2
ITERATIONS = 200

lfsr = LFSR(degree=DEGREE, tap_positions=TAP_POSITIONS)
lfsr.generate(bitseq=SEED, iterations=ITERATIONS)

if __name__ == '__main__':
    lfsr.plot_stream()
