from context import Analyser, LFSR

BITSTREAM = '1011101110010101001010001001011010001100111001'
analyser: Analyser = Analyser(stream=BITSTREAM)
analyser.iter_solve()

def main():
    for k, v in analyser.lfsr_solutions.items():
        for v_key, v_val in v.items():
            print(f"For degree {k} found: {v_key} = {v_val}")
        print('\n')
if __name__ == '__main__':
    main()