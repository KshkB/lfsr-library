from context import LFSR

SEED = 0b110111001
ITERATIONS = 100
try:
    DEGREE: int = len(bin(SEED))-2
except TypeError:
    DEGREE: int = len(SEED) 

TAPS: list[int] = [1, 4]

lfsr: LFSR = LFSR(degree=DEGREE, tap_positions=TAPS)
lfsr.generate(bitseq=SEED, iterations=ITERATIONS)

def main():
    lfsr.plot_stream()

if __name__ == '__main__':
    main()