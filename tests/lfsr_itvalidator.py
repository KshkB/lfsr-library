from context import ItValidator

BITSTREAM = '1011101110010101001010001001011010001100111001'

itval: ItValidator = ItValidator(stream=BITSTREAM)
itval.validate()

def main():
    for k, v in itval.results.items():
        hamm, acc = v.items()
        print(f"""
        for degree {k}, Hamming length is: {hamm[-1]} with Accuracy {100*acc[-1]:.2f} %\n
        """)

if __name__ == '__main__':
    main()

