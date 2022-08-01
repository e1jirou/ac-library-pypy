# This file does not work in PyPy because numpy is imported.
# Please use Python when you use this file.

"""
Reference
https://ikatakos.com/pot/programming_algorithm/fft
https://maspypy.com/%E6%95%B0%E5%AD%A6%E3%83%BBnumpy-%E9%AB%98%E9%80%9F%E3%83%95%E3%83%BC%E3%83%AA%E3%82%A8%E5%A4%89%E6%8F%9Bfft%E3%81%AB%E3%82%88%E3%82%8B%E7%95%B3%E3%81%BF%E8%BE%BC%E3%81%BF
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
