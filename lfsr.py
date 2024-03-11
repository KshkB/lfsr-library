import numpy as np
import matplotlib.pyplot as plt
from functions import count_func
import sympy as sp

class Analyzer:

    def __init__(self) -> None:
        pass

    def generate_num(self, num_range: list) -> None:
        """
        pseudo-random number generator in range num_range
        for num_range pass list [start, end]
        """
        stream = self.stream
        num = int(stream, 2)
        self.random_num = (num % (num_range[-1] - num_range[0])) + num_range[0]

    def randomness(self):

        stream = self.stream 
        stream_length = len(stream)
        self.randomness_dict = {
            '0': f"{round(100*count_func(stream, '0') / stream_length, 2)}%",
            '1': f"{round(100*count_func(stream, '1') / stream_length, 2)}%"
        }

    def randomness_plot(self):
        stream = self.stream
        xdata = [0]
        ydata = [100.0 if stream[0]=='1' else 0.0]
        for x in range(len((stream[1:]))):
            data = stream[:x+1]
            xdata += [float(x+1)]
            ydata += [round(100*count_func(data, '1')/(x + 1), 2)]

        plt.title('Randomness graph')
        plt.xlabel('State')
        plt.ylabel('Probability bit = 1')
        plt.axhline(y=50.0, color='r', linestyle='--')

        plt.plot(xdata, ydata)
        plt.tight_layout()
        plt.show()

    def plot_stream(self, **kwargs):
        """
        plot bits vs state in LFSR stream
        """
        stream = self.stream
        xvals = []
        yvals = []
        for state, bit in enumerate(stream):
            xvals += [state]
            yvals += [int(bit)]

        try:
            figsize = kwargs['figsize']
        except KeyError:
            figsize = (12, 7)
        plt.figure(figsize=figsize)

        plt.title('Bit stream plot')
        plt.xlabel('State')
        plt.ylabel('Bit')
        plt.plot(xvals, yvals)
        plt.show()

class LFSR(Analyzer):

    def __new__(cls, **kwargs):
        tap_positions = kwargs['tap_positions']
        degree = kwargs['degree']
        if all(abs(pos) < degree for pos in tap_positions): # LSb numbering => |tap position| < degree
            return super(LFSR, cls).__new__(cls)
        else:
            print("Invalid tap positions")
        
    def __init__(self, **kwargs) -> None:
        """
        Binary numbers are ordered according to LSb
        e.g., in 1000, 1 is in position 3 so that 1000 = 1 << 3 = 8
        Generally, m << n = m*(2**n)
        """
        super().__init__() # inherit from class Analyzer
        self.degree = kwargs['degree']
        self.tap_positions = kwargs['tap_positions'] 

        polynomial = 'X^0'
        for position in self.tap_positions:
            if position != 0:
                polynomial += f' + X^{position}'
            
        polynomial += f' + X^{self.degree}'
        self.feedback_polynomial = polynomial
        
    def generate_classical(self, bitseq, iterations):
        """
        taps are all zero except for the last and second-last entries
        i.e., tap_positions = [m-2, m-1] for degree m, so that input_{n+1} = output_n XOR MSb_{n+1}
        """
        self.period = 'Not found'
        degree = self.degree
        self.log = []
        self.stream = ''
        state = int(bin(bitseq), 2) # convert to int
        count=0
        for _ in range(iterations):
            newbit = (state ^ (state >> 1)) & 1
            state = (state >> 1) | (newbit << (degree-1))
            output = state & 1

            # convert bit-shifted ints to binary literals
            state_bits = format(state, '0' + str(degree) + 'b')
            output_bit = format(output, '01b')

            count += 1
            self.log += [state_bits]
            self.stream += str(output_bit)
            if state_bits == format(bitseq, f'0{degree}b'):
                if self.period == 'Not found':
                    self.period = count

    def generate(self, bitseq, iterations):
        self.period = "Not found"
        tap_positions = self.tap_positions
        degree = self.degree
        count = 0
        self.log = []
        first_output = format(bitseq & 1, '01b')
        self.stream = f'{first_output}'
        state = int(bin(bitseq), 2)
        for _ in range(iterations):
            new_bit = 0
            for position in tap_positions:
                bit = (state >> position) & 1
                new_bit ^= bit 

            state = (state >> 1) | (new_bit << (degree - 1))
            output = state & 1

            state_bits = format(state, f'0{degree}b')
            output_bit = format(output, f'01b')

            count += 1
            self.log += [state_bits]
            self.stream += str(output_bit)

            if state_bits == format(bitseq, f'0{degree}b'):
                if self.period == 'Not found':
                    self.period = count

            if count>(2**degree-1):
                if self.period == 'Not found':
                    self.period = 'sub-maximal'

class LinSolve:

    def __new__(cls, **kwargs):
        bitstream = kwargs['bitstream']
        try:
            degree = kwargs['degree']
        except KeyError:
            degree = len(bitstream)//2

        if 2*degree <= len(bitstream):
            return super(LinSolve, cls).__new__(cls)
        else:
            print("Cannot solve for given bitstream input and degree.")

    def __init__(self, **kwargs) -> None:
        
        self.bitstream = kwargs['bitstream']
        try:
            self.degree = kwargs['degree']
            self.bitstream = self.bitstream[:2*self.degree]
        except KeyError:
            self.degree = len(self.bitstream)//2

    def find_period(self) -> None:
        """
        from bistream, reconstructs bitstate transitions and checks for period
        """
        degree = self.degree
        input_stream = self.bitstream # self.__init__() ensures bitstream has length 2*degree
        log = []
        for i in range(len(input_stream)):
            log += [input_stream[i:i+degree]]
        if len(log) == len(set(log)):
            self.find_period = "No period found"
        else:
            # find period
            period = None 
            while period==None:
                for i, state in enumerate(log):
                    count = 0
                    for state2 in log[1:]:
                        count += 1
                        if state==state2:
                            period = count            
                            break

    def solve(self) -> None:
        bitstream = self.bitstream
        degree = self.degree
        bit_vect = np.array([int(bit) for bit in bitstream[degree:]])
        mtrx_rows = []
        for i in range(degree):
            mtrx_rows += [np.array(
                [int(bit) for bit in bitstream[i:i+degree]]
            )]
        mtrx = sp.Matrix(mtrx_rows)
        try:
            taps = mtrx.inv_mod(2) @ sp.Matrix(bit_vect)
            taps = taps.__mod__(2)
            self.solution = taps
            self.tap_positions = [i for i, x in enumerate(taps) if x==1]
            self.LFSR = LFSR(degree=degree, tap_positions=self.tap_positions)
        except ValueError:
            print(f"""
                  Cannot solve for given bitstream, 
                  the period of corresponding {degree}-bit LFSR is sub-maximal.
                """)

    def solution_validate(self):
        """
        validate solution against given input stream
        """
        lfsr = self.LFSR
        input_bitstream = self.bitstream
        seed = int(input_bitstream[:self.degree][::-1], 2)
        lfsr.generate(seed, iterations=len(input_bitstream))
        new_stream = lfsr.stream

        for i, bit in enumerate(new_stream[:2*self.degree]):
            original = input_bitstream[i]
            rsult = bool(bit==original)
            print(f'Original: {original}\tPredicted: {bit}\tResult: {rsult}')

class IterSolve:

    def __new__(cls, bitstream):
        if len(bitstream) >= 6:
            return super(IterSolve, cls).__new__(cls)
        else:
            print("Bitstream is too small")

    def __init__(self, bitstream) -> None:
        """
        iterate through valid degrees and use LinSolve to solve for LFSR 
        """
        self.bitstream = bitstream
        self.degrees_checked = []
        self.lfsr_solutions = {}
        self.MAX = len(bitstream)//2

    def start(self):
        MAX = self.MAX
        stream = self.bitstream
        for deg in range(3, MAX+1):
            if deg in self.degrees_checked:
                pass
            else:
                self.degrees_checked += [deg]
                solver = LinSolve(bitstream=stream, degree=deg)
                solver.solve()
                try:
                    self.lfsr_solutions[f"Degree {deg}"] = solver.LFSR
                except AttributeError:
                    pass 

    def results(self):
        results = self.lfsr_solutions
        if len(results) == 0:
            print("No maximal LFSRs were found for this bitstream")
        else:
            print("LFSRs found:")
            for lfsr in results.values():
                print(f"Degree: {lfsr.degree}\
                      \tTap positions: {lfsr.tap_positions}\
                      \tPeriod: {2**lfsr.degree - 1}")

class MultiLFSR(Analyzer):
    """
    input into next state is the output of another LFSR
    """
    def __new__(cls, **kwargs):
        
        lfsrs = kwargs['lfsr_list']
        degree = kwargs['degree']
        if all([lfsr.degree == degree for lfsr in lfsrs]):
            tap_positions = kwargs['tap_positions']
            if all(abs(pos) < degree for pos in tap_positions):
                return super(MultiLFSR, cls).__new__(cls)
            else:
                print("Invalid tap positions")
        else:
            print("The degree of all LFSRs must coincide")

    def __init__(self, **kwargs) -> None:

        self.lfsr_list = kwargs['lfsr_list']
        self.degree = kwargs['degree']

    def generate(self, seed, iterations):
        self.log = []
        self.stream = ''

        lfsr_list = self.lfsr_list
        curr_state = seed
        for _ in range(iterations):
            for lfsr in lfsr_list:
                lfsr.generate(curr_state, 1)
                new_state = lfsr.log[-1]
                curr_state = new_state
                curr_output = lfsr.stream

            self.log += [curr_state]
            self.stream += curr_output

class CustomLFSR:
    """
    pass custom function Z_2^{num_taps} -> Z_2 to generate new input
    in LFSR, this function is poly-XOR
    """
    def __init__(self, **kwargs) -> None:
        pass 
