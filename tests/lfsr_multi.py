from context import LFSR, MultiLFSR

SEED = 0b10011010
DEGREE = len(bin(SEED))-2
ITERATIONS = 1000

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
multi.randomness()

stream = multi.stream
log = multi.log
randomness_dict = multi.randomness_dict
if __name__ == '__main__':
    print(stream)
    print(randomness_dict)
    multi.randomness_plot()
    # for entry in log:
    #     print(entry)
   