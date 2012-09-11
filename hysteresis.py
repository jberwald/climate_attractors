import numpy as np
import matplotlib.pyplot as plt

def cubic( x ):
    return -x**3 + 50*x

nx = np.linspace( -6, 6, 100 )
vc = np.vectorize( cubic )
ny = vc( nx )


