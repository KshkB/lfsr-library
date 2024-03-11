from context import IterSolve
"""
Pass bitstream and iteratively solve for valid degree
"""
BITSTREAM = '10110010001111010110'
itsolver = IterSolve(BITSTREAM)
itsolver.start()
if __name__ == '__main__':
    itsolver.results() 
