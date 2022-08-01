# This file does not work in PyPy because numpy is imported.
# Please use Python when you use this file.

"""
Reference
https://ikatakos.com/pot/programming_algorithm/fft
https://maspypy.com/数学・numpy-高速フーリエ変換fftによる畳み込み
"""

import numpy as np

def convolution(f, g):
    fft_len = 1 << (len(f)+len(g)).bit_length()
    Ff = np.fft.rfft(f, fft_len)
    Fg = np.fft.rfft(g, fft_len)
    Ffg = Ff * Fg
    fg = np.fft.irfft(Ffg, fft_len)
    fg = np.rint(fg).astype(np.int64)
    return fg[:len(f)+len(g)-1]

def convolution_ll(f, g):
    f1, f2 = np.divmod(f, 1<<15)
    g1, g2 = np.divmod(g, 1<<15)
    a = convolution(f1, g1)
    c = convolution(f2, g2)
    b = (convolution(f1 + f2, g1 + g2) - (a + c))
    h = (a<<30) + (b<<15) + c
    return h
