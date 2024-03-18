"""
validate solution for inverted lfsr
"""
from .lfsr import LFSR
from .analyser import Analyser
from .functions.functions import hamming_len

class Validator:

    def __init__(self, **kwargs) -> None:
        
        self.stream: str = kwargs['stream']
        self.tap_positions: list[int] = kwargs['tap_positions']
        self.degree: int = kwargs['degree']

    def validate(self) -> None:
        
        deg: int = self.degree
        taps: list[int] = self.tap_positions
        stream: str = self.stream

        # from stream, generate new stream from lfsr
        lfsr: LFSR = LFSR(degree=deg, tap_positions=taps)
        SEED: int = int(stream[:deg][::-1], 2)
        ITERATIONS: int = len(stream)-1
        lfsr.generate(bitseq=SEED, iterations=ITERATIONS)

        new_stream: str = lfsr.stream

        # validate
        self.hamming_length: int = hamming_len(stream, new_stream)
        self.accuracy: float = 1 - self.hamming_length / len(stream)

class ItValidator:

    def __init__(self, **kwargs) -> None:
        
        self.stream: str = kwargs['stream']
        self.iterations: int = len(self.stream)-1

    def validate(self):
        
        analyser: Analyser = Analyser(stream=self.stream)
        analyser.iter_solve()

        lfsr_solutions: dict = analyser.lfsr_solutions
        validator_rsults: dict = {}
        ITERATIONS: int = self.iterations
        for soln, params in lfsr_solutions.items():
            degree = soln 

            SEED: int = int(self.stream[:degree][::-1], 2)
            tap_positions: list[int] = params['tap_positions']
            if tap_positions == None: # no solution found for given bitstream and degree
                pass 
            else:
                lfsr = LFSR(degree=degree, tap_positions=tap_positions)
                lfsr.generate(bitseq=SEED, iterations=ITERATIONS)

                validator: Validator = Validator(stream=self.stream, tap_positions=tap_positions, degree=degree)
                validator.validate()
                validator_rsults[degree] = {
                    'hamming_length': validator.hamming_length,
                    'accuracy': validator.accuracy
                }
        
        self.results: dict = validator_rsults

