import matplotlib.pyplot as plt
import sympy as sp
from .functions.functions import count_func

class Analyser:

    SIG_FIGS: int = 4

    # error messages
    STREAM_ERROR: str = "No bitstream logged. Try generating stream from an LFSR before calling."
    DEGREE_ERROR: str = "Invalid degree for input stream"
    DEGREE_ERROR_SMALL : str = "Degree is too small"
    LINSOLVE_ERROR: str = "Cannot solve for given bitstream and degree"

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v) 

    def generate_num(self, num_range: range) -> None:
        """
        pseudo-random number generator in range num_range
        for num_range pass range object
        """
        stream: str = self.stream
        num: int = int(stream, 2)
        self.random_num : int = (num % (num_range.stop - num_range.start)) + num_range.start

    def randomness(self, **kwargs) -> None:

        try:
            sf: int = kwargs['SIG_FIGS']
        except KeyError:
            sf: int = self.SIG_FIGS

        try:
            stream: str = self.stream # error raised here if stream not logged

            stream_length: int = len(stream)
            zeros_count: int = count_func(stream, '0')
            ones_count: int = count_func(stream, '1')
            self.randomness_dict: dict = {
                '0': f"{100*zeros_count / stream_length:.{sf}f} %",
                '1': f"{100*ones_count / stream_length:.{sf}f} %"
            }
            self.LaplaceSuccession: dict = {
                '0': f'{100 * (zeros_count + 1) / (stream_length + 2):.{sf}f} %',
                '1': f'{100 * (ones_count + 1) / (stream_length + 2):.{sf}f} %'
            }
        except AttributeError:
            raise AttributeError(self.STREAM_ERROR)

    def randomness_plot(self, **kwargs) -> None:
        """
        plot probability of bit == 1 against state number
        """
        try:
            sf = kwargs['SIG_FIGS']
        except KeyError:
            sf = self.SIG_FIGS

        try:
            stream: str = self.stream
            xdata: list[int] = [0]
            ydata: list[float] = [100.0 if stream[0]=='1' else 0.0]
            for x in range(len((stream[1:]))):
                data = stream[:x+1]
                xdata += [int(x+1)]
                ones_count: int = count_func(data, '1')
                ones_prob: float = round(100*ones_count / (x+1), sf)
                ydata += [ones_prob]

            try:
                figure_size: tuple[int] = kwargs['figsize']
            except KeyError:
                figure_size: tuple[int] = (12, 7)

            # plotting
            plt.figure(figsize=figure_size)
            plt.title('Randomness graph')
            plt.xlabel('State number')
            plt.ylabel('Probability bit = 1 (%)')
            plt.axhline(y=50.0, color='r', linestyle='--')

            plt.plot(xdata, ydata)
            plt.tight_layout()
            plt.show()

        except AttributeError:
            raise AttributeError(self.STREAM_ERROR)

    def plot_stream(self, **kwargs) -> None:
        """
        plot bits vs state in LFSR stream
        """
        try:
            stream: str = self.stream
            xvals: list[int] = []
            yvals: list[int] = []
            for state, bit in enumerate(stream):
                xvals += [state]
                yvals += [int(bit)]

            try:
                figure_size: tuple[int] = kwargs['figsize']
            except KeyError:
                figure_size: tuple[int] = (12, 7)

            plt.figure(figsize=figure_size)

            plt.title('Bit stream plot')
            plt.xlabel('State number')
            plt.ylabel('Bit')

            plt.plot(xvals, yvals)
            plt.tight_layout()
            plt.show()

        except AttributeError:
            raise AttributeError(self.STREAM_ERROR)

    def lin_solve(self, **kwargs) -> None:
        
        try:
            stream: str = self.stream
            try: # if kwargs passed in lin_solve, override with class attr
                degree: int = kwargs['degree']
                if 2*degree > len(stream):
                    raise ValueError(self.DEGREE_ERROR)
            except KeyError: # if no kwargs passed, check class attr
                try:
                    degree: int = self.degree
                    if 2*degree > len(stream):
                        raise ValueError(self.DEGREE_ERROR)
                except AttributeError: # if no kwargs passed or class attrs logged, use default
                    degree: int = len(stream) // 2

            if degree <= 3:
                raise ValueError(self.DEGREE_ERROR_SMALL)
            
            self.degree: int = degree
            self.input_stream: str = stream[:2*degree]
            input_stream: str = self.input_stream

            bit_vect: list[int] = [int(bit) for bit in input_stream[degree:]]
            mtrx_rows: list[list] = []
            for i in range(degree):
                mtrx_rows += [
                    [int(bit) for bit in stream[i:i+degree]]
                ]
            mtrx: sp.matrices.dense.MutableDenseMatrix = sp.Matrix(mtrx_rows)
            try:
                taps: sp.matrices.dense.MutableDenseMatrix = mtrx.inv_mod(2) @ sp.Matrix(bit_vect)
                taps: sp.matrices.dense.MutableDenseMatrix = taps.__mod__(2)
                self.solution: list[int] = list(taps)
                self.tap_positions: list[int] = [i for i, x in enumerate(taps) if x==1]

            except ValueError:
                raise ValueError(self.LINSOLVE_ERROR)
            
        except AttributeError:
            raise AttributeError(self.STREAM_ERROR)

    def iter_solve(self) -> None:
        """
        iteratively solve, checking each valid degrees 
        """
        stream: str = self.stream
        lsfr_solutions: dict = {}
        MAX = len(stream) // 2
        if MAX <= 3:
            raise ValueError(self.DEGREE_ERROR_SMALL)
        
        for degree in range(3, MAX+1):
            lsfr_solutions[degree] = {}
            try:
                self.lin_solve(degree=degree)
                lsfr_solutions[degree]['taps'] = self.solution
                lsfr_solutions[degree]['tap_positions'] = self.tap_positions
            except ValueError:
                lsfr_solutions[degree]['taps'] = None
                lsfr_solutions[degree]['tap_positions'] = None

        self.lfsr_solutions: dict = lsfr_solutions
