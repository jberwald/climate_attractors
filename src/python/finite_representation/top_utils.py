"""
top_utils.py

Author: Jesse Berwald

Opened: Oct. 14, 2012

Suite of utility functions. 
"""
import numpy as np
import cPickle as pkl


def write_perseus( data, pers_type, dim, fname=None ):
    """
    Perseus accepts the following file formats:

    See http://www.math.rutgers.edu/~vidit/perseus.html for more details.

    VR Complex (dtype='vr'):
    
        3: the ambient dimension, i.e., the number of coordinates per vertex.
        1 0.01 100: the radius scaling factor k=1, the step size s=0.01, the number of steps N=100
        1.2 3.4 -0.9 0.5: the vertex (1.2, 3.4, -0.9) with associated radius r = 0.5
        2.0 -6.6 4.1 0.3: the vertex (2.0, -6.6, 4.1) with associated radius r = 0.3 
        and so on!

    Simplicial Complex (dtype='simplex'):

        < Uniform Triangulation >

        3: this is the dimension of the simplices, so each simplex has 3+1 = 4 vertices. 
        2: this is the number of coordinates per vertex. 
        0 0 0 1 1 0 1 1 1: this is the 3-simplex with vertices (0,0), (0,1), (1,0), (1,1) and birth time 1. 
        and so on!

        < Nonuniform triangulation >

        1: this is the number of coordinates per vertex. 
        2 1 3 5 1: this is the 2D simplex with vertices 1, 3 and 5; the birth time is 1.
        3 1 2 4 6 2 this is the 3D simplex with vertices 1, 2, 4 and 6; the birth time 2.
        6 1 2 3 4 5 6 7 4: 6D simplex, but only faces of dimension up to 5 are constructed because of the cap. 
        and so on.

    Cubical Complex (dtype='cube'):

        < This is _sparse_ cubical grid format >

        3: this is the dimension of the cubical grid 
        1 3 4 2: this is the 3D cube anchored at (1,3,4) with birth time 2. 
        2 12 -4 7: this is the 3D cube anchored at (2, 12, -4) with birth time 7. 
        0 2 3 1: this is the 3D cube anchored at (0,2,3) with birth time 1. 
    """
    if pers_type == 'cube':
        _write_pers_cube( data, dim )

def _write_pers_cube( data, dim ):
    """
    From K. Spendlove's rbc_npy2Perseus.py implementation.
    """
    
    #dimension array
    numDim = 2
    with open (output + ".txt", "w") as fh:
        #Write number of dimensions
        fh . write ( str( dim ) + "\n")
        #Write strictly 2D file
    if fname.endswith( 'npy' ):
        data = numpy.load(fname)
    else:
        data = numpy.loadtxt(fname)
    size = data.shape
    for i in range(0,size[0]):
        for j in range(0,size[1]):
            if int(data[i][j]) != 0:
                pos = str(i) + ' ' + str(j) + ' '
                fh . write (pos + str(int(data[i][j])) + "\n")
    fh . close()

def _make_tmp_file():
    return 

import os
import tempfile

temp = tempfile.NamedTemporaryFile()
try:
    print 'temp:', temp
    print 'temp.name:', temp.name
finally:
    # Automatically cleans up the file
    temp.close()
print 'Exists after close:', os.path.exists(temp.name)
