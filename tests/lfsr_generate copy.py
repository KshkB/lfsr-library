from context import LFSR

SEED = 0b110
ITERATIONS = 10
try:
    DEGREE: int = len(bin(SEED))-2
except TypeError:
    DEGREE: int = len(SEED) 

TAPS: list[int] = [1, 2]

lfsr: LFSR = LFSR(degree=DEGREE, tap_positions=TAPS)
lfsr.generate(bitseq=SEED, iterations=ITERATIONS)

def main():
    print(f"""
    degree: {lfsr.degree}\n
    feedback polynomial: {lfsr.feedback_polynomial}\n
    stream: {lfsr.stream}\n
    period: {lfsr.period}
    """)
    for state in lfsr.log:
        print(state)

if __name__ == '__main__':
    main()