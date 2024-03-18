import matplotlib.pyplot as plt
from .analyser import Analyser
from .functions.functions import str_to_sp
from .functions.functions import count_func

class LFSR(Analyser):

    def __new__(cls, **kwargs):
        tap_positions: list[int] = kwargs['tap_positions']
        degree: int = kwargs['degree']
        if all(abs(pos) < degree for pos in tap_positions): # LSb numbering => |tap position| < degree
            return super(LFSR, cls).__new__(cls)
        else:
            raise IndexError("Invalid tap positions. Positioning is 0-indexed.")
        
    def __init__(self, **kwargs) -> None:
        """
        Binary numbers are ordered according to LSb
        e.g., in 1000, 1 is in position 3 so that 1000 = 1 << 3 = 8
        Generally, m << n = m*(2**n)
        """
        super().__init__() # inherit from class Analyzer
        self.degree: int = kwargs['degree']
        self.tap_positions: list[int] = kwargs['tap_positions'] 

        polynomial: str = 'X^0'
        for position in self.tap_positions:
            if position != 0:
                polynomial += f' + X^{position}'
            
        polynomial += f' + X^{self.degree}'
        self.feedback_polynomial: str = polynomial
        self.feedback_polynomial_sp = str_to_sp(self.feedback_polynomial) # class sp.core.add.Add

    def generate(self, bitseq: str, iterations: int) -> None:
        if isinstance(bitseq, str):
            bitseq: int = int(bitseq, 2) 

        self.period: str = "Not found"
        tap_positions: list[int] = self.tap_positions
        degree: int = self.degree

        count: int = 0
        first_output: str = format(bitseq & 1, '01b')
        log: list[int] = [format(bitseq, f'0{degree}b')]
        stream: str = f'{first_output}'
        state: int = int(bin(bitseq), 2)
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
            log += [state_bits]
            stream += str(output_bit)

            if state_bits == format(bitseq, f'0{degree}b'):
                if self.period == 'Not found':
                    self.period = f'{count}'

            if count>(2**degree-1):
                if self.period == 'Not found':
                    self.period = 'sub-maximal'
        
        self.log: list[str] = log
        self.stream: str = stream

class MultiLFSR(Analyser):
    """
    input into next state is the output of previous LFSR
    """
    def __new__(cls, **kwargs):
        
        lfsrs: list[LFSR] = kwargs['lfsr_list']
        if all(isinstance(lfsr, LFSR) for lfsr in lfsrs):
            degree: int = kwargs['degree']
            if all([lfsr.degree == degree for lfsr in lfsrs]):
                return super(MultiLFSR, cls).__new__(cls)
            else:
                print("The degree of all LFSRs must coincide")
        else:
            print("pass a list of LFSR objects.")

    def __init__(self, **kwargs) -> None:

        self.lfsr_list: list[LFSR] = kwargs['lfsr_list']
        self.feedback_polynomials: list[str] = [lfsr.feedback_polynomial for lfsr in self.lfsr_list]
        self.feedback_polynomials_sp: list = [lfsr.feedback_polynomial_sp for lfsr in self.lfsr_list]
        self.degree: int = kwargs['degree']

    def generate(self, seed, iterations) -> None:

        self.seed: int = seed 
        self.iterations: int = iterations

        degree = self.degree
        log: list[int] = [format(seed, f'0{degree}b')]
        stream: str = ''
        period: str = 'Not found'
        count: int = 0

        lfsr_list: list[LFSR] = self.lfsr_list
        curr_state: str = seed
        for _ in range(iterations):
            for lfsr in lfsr_list:
                lfsr.generate(curr_state, 1)
                new_state = lfsr.log[-1]
                curr_state = new_state
                curr_output = lfsr.stream[-1]

            log += [curr_state]
            stream += curr_output
            count += 1

            if curr_state == seed:
                period = count

        self.log = log
        self.stream = stream
        self.period = period

    def generate_comparison(self, **kwargs) -> None:
        """
        compare randomness of multilfsrs against each factor lfsr
        """
        self.randomness(**kwargs)
        self.multi_randDict: dict = self.randomness_dict
        try:
            lfsr_data = self.lfsr_data
        except AttributeError:
            lfsr_data: dict = {}
            for i, lfsr in enumerate(self.lfsr_list):
                lfsr_stream: str = lfsr.generate(bitseq=self.seed, iterations=self.iterations-1)
                lfsr_stream = lfsr.stream
                lfsr_data[i] = {
                    'tap_positions': lfsr.tap_positions,
                    'stream': lfsr_stream
                }
            self.lfsr_data: dict = lfsr_data
            return self.generate_comparison(**kwargs)
        
        lfsr_randData: dict = {}
        for i, lfsr in enumerate(self.lfsr_list):
            lfsr.randomness(**kwargs)
            lfsr_randDict: dict = lfsr.randomness_dict
            lfsr_randData[str(i)] = lfsr_randDict

        self.lfsr_randData: dict = lfsr_randData

    def print_comparisons(self) -> None:
        """
        print results to console
        """
        mult_rand: dict = self.multi_randDict
        lfsr_rand: dict = self.lfsr_randData

        for bit in mult_rand:
            prob: str = mult_rand[bit]
            print(f"Probability (bit = {bit} | Multi-LSFR) = {prob}")
        print('\n')
        for k, d in lfsr_rand.items():
            for bit in d:
                prob: str = d[bit]
                print(f"Probability (bit = {bit} | LFSR {k}) = {prob}")
            print('\n')

    def comparisons_plot(self, **kwargs):
        """
        plot randomness comparisons of multilfsr against randomness of each factor lfsr
        """
        try:
            sf = kwargs['SIG_FIGS']
        except KeyError:
            sf = self.SIG_FIGS

        multi_stream: str = self.stream 
        try:
            lfsr_data = self.lfsr_data
        except AttributeError:
            lfsr_data: dict = {}
            for i, lfsr in enumerate(self.lfsr_list):
                lfsr_stream: str = lfsr.generate(bitseq=self.seed, iterations=self.iterations-1)
                lfsr_stream = lfsr.stream
                lfsr_data[i] = {
                    'tap_positions': lfsr.tap_positions,
                    'stream': lfsr_stream
                }
            return self.comparisons_plot(**kwargs)

        xdata: list[int] = [0]
        multi_ydata: list[float] = [100.0 if multi_stream[0]=='1' else 0.0]
        for i in range(len(multi_stream[1:])):
            xdata += [i+1]
            data: str = multi_stream[:i+1]
            ones_count: int = count_func(data, '1')
            ones_prob: float = round(100*ones_count / (i+1), sf)
            multi_ydata += [ones_prob]

        try:
            FIGSIZE = kwargs['figsize']
        except KeyError:
            FIGSIZE = (8, 5) # default

        NUM_COLS = 2
        NUM_ROWS = len(lfsr_data)
        fig, axes = plt.subplots(ncols=NUM_COLS, nrows=NUM_ROWS, figsize=FIGSIZE)
        row_num = 0
        for row in axes:
            for i, col in enumerate(row):
                if i%2 == 0:
                    # plot multilfsr
                    ydata: list[float] = multi_ydata

                    col.set_title('Multi-LFSR')
                    col.set_xlabel('State')
                    col.set_ylabel('Probability bit = 1')
                    col.plot(xdata, ydata)
                else:
                    curr_index: int = (row_num + i) // 2
                    curr_stream: str = lfsr_data[curr_index]['stream']
                    curr_taps = lfsr_data[curr_index]['tap_positions']
                    curr_ydata: list[float] = [100.0 if curr_stream[0]=='1' else 0.0]
                    for i in range(len(curr_stream[1:])):
                        data: str = curr_stream[:i+1]
                        ones_count: int = count_func(data, '1')
                        ones_prob: float = round(100*ones_count / (i+1), sf)
                        curr_ydata += [ones_prob]

                    col.set_title(f'LFSR with taps at {curr_taps}')
                    col.set_xlabel('State')
                    col.set_ylabel('Probability bit = 1')
                    col.plot(xdata, curr_ydata)

            row_num += NUM_COLS

        plt.tight_layout()
        plt.show()
