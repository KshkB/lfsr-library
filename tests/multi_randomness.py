from context import LFSR, MultiLFSR

SEED = 0b10011010
DEGREE = len(bin(SEED))-2
ITERATIONS = 100

taps1 = [2, 4]
lfsr1 = LFSR(degree=DEGREE, tap_positions=taps1)

taps2 = [0, 3, 4]
lfsr2 = LFSR(degree=DEGREE, tap_positions=taps2)

taps3 = [1, 2]
lfsr3 = LFSR(degree=DEGREE, tap_positions=taps3)

taps4 = [4, 6]
lfsr4 = LFSR(degree=DEGREE, tap_positions=taps4)

lfsrs = [lfsr1, lfsr2, lfsr3, lfsr4]
multi = MultiLFSR(lfsr_list=lfsrs, degree=DEGREE)
multi.generate(seed=SEED, iterations=ITERATIONS)

RANGE = range(100, 999)
multi.generate_num(num_range=RANGE)
multi.randomness(SIG_FIGS=2)

def main():
    print(f"""
    (pseudo) randum number: {multi.random_num}
    """)
    for k, v in multi.randomness_dict.items():
        print(f"Probability of {k} = {v}")
    for k, v in multi.LaplaceSuccession.items():
        print(f"Laplace succession probability of {k} = {v}")

if __name__ == '__main__':
    main()