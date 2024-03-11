from context import LFSR
"""
Test for LFSR.generate_classical
"""
DEGREE = 10
TAP_POSITIONS = [2, 3, 4, 9]
SEED = 0b1011010001
ITERATIONS = 5000
RANGE = [12, 106]

lfsr = LFSR(degree=DEGREE, tap_positions=TAP_POSITIONS)
lfsr.generate(bitseq=SEED, iterations=ITERATIONS)
lfsr.randomness()
lfsr.generate_num(RANGE)

if __name__ == '__main__':
    print(lfsr.randomness_dict) 
    print(lfsr.random_num)
    lfsr.randomness_plot()
