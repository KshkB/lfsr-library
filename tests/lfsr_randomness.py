from context import LFSR

SEED = 0b110111001
ITERATIONS = 10000
try:
    DEGREE: int = len(bin(SEED))-2
except TypeError:
    DEGREE: int = len(SEED) 

TAPS: list[int] = [1, 4]

lfsr: LFSR = LFSR(degree=DEGREE, tap_positions=TAPS)
lfsr.generate(bitseq=SEED, iterations=ITERATIONS)

RANGE: range = range(100, 999)
lfsr.generate_num(num_range=RANGE)
lfsr.randomness(SIG_FIGS=2)

def main():
    print(f"""
    (pseudo) random number: {lfsr.random_num}
    """)
    for k, v in lfsr.randomness_dict.items():
        print(f"probability of {k} = {v}")
    for k, v in lfsr.LaplaceSuccession.items():
        print(f"Laplace succession probability of {k} = {v}")

if __name__ == '__main__':
    main()