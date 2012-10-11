#!/usr/bin/python
"""
run_ode.py

Created: 30 September, 2012
"""
import sys
import timer
import argparse
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
try:
    import xppy
except ImportError:
    print "xppy package must be installed!"
    raise


class XPPWrap( object ):
    """
    Initialize XPPWrap for a single simulation instance of an ODE. Multiple
    instance of XPPWrap should be created when testing multiple IC's
    or parameter values.

    The XPPWrap object serves as an entry point into xppy, while also
    acting as a container for returned output analysis and plotting
    purposes.
    """
    def __init__( self, ODE_file, SET_file=None, IC=None, params=None,
                  discrete=False ):
        """
        """
        self.ode = ODE_file
        self.set = SET_file
        self.IC = IC
        self.params = params

        # Non-XPPY arguments
        self.discrete = discrete # for plotting 
        
    def __repr__( self ):
        s = "XPPWrap for " + self.ode
        return s
        

    def run( self ):
        """
        """
        # init the xppy object
        xppy.createTmp( self.ode )

        # run it
        self.out = xppy.run( )

        # omit first time axis in self.dim
        nx, ny = self.out.getRawData().shape
        self.tmax = nx - 1  # total number of steps/iterations
        self.dim = ny - 1

    def sample_points( self, npts=50 ):
        """
        Returns <npts> random samples from computed trajectory in
        self.out.
        """
        # shuffle the indices as a proxy for shuffling the
        # array. shuffle is in-place.
        idx = range( self.tmax )
        np.random.shuffle( idx )

        # choose the first <npts> indices, and sample self.out at
        # those indices. 
        self.samples = self.out.getRawData()[ idx[ :npts ] ]
        

    def plot3d( self, coords=[1,2,3], **kwargs ):
        """
        Pylab 3d axis plot.

        Customize plot arguments with kwargs. See matplotlib plot()
        for various args.

        coords -- Defaults to first three coordinate axes ( out[1],
        out[2], out[3] ). Change by passing list containing two
        integers in the range 0,..., <sys dim>. Eg. for Lorenz84,
        time==out[0], x==out[1], y=out[2], z=out[3]. To plot out
        (x,y,z), set coords=[1,2,3] (default).

        discrete -- set to True for maps, False for flows.
        """
        # some default plot arguments. 
        fargs = { 'color': 'b',
                  'lw': 3,
                  }
        fargs.update( kwargs )

        if self.discrete:
            fargs[ 'marker' ] = 'o'
            fargs[ 'linestyle' ] = 'None'
        else:
            fargs[ 'linestyle' ] = 'solid'

        # choose the axes, or use the default
        xs = self.out[ coords[0] ]
        ys = self.out[ coords[1] ]
        zs = self.out[ coords[2] ]
        
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot( xs, ys, zs, **fargs )#, lw=3, alpha=0.8)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        fig.show()

    def plot2d( self, coords=[1,2], **kwargs ):
        """
        Customize plot arguments with kwargs. See matplotlib plot()
        for various args.

        coords -- Defaults to first two coordinate axes ( out[1],
        out[2] ). Change by passing list containing two integers in
        the range 0,..., <sys dim>. Eg. for Henon, time==out[0],
        x==out[1], y=out[2]. To plot out time vs x, set coords=[0,2].

        discrete -- set to True for maps, False for flows.
        
        """
        # some default plot arguments. 
        fargs = { 'color': 'b',
                  'lw': 3,
                  }
        fargs.update( kwargs )

        if self.discrete:
            fargs[ 'marker' ] = 'o'
            fargs[ 'linestyle' ] = 'None'
        else:
            fargs[ 'linestyle' ] = 'solid'

        # choose the axes, or use the default
        xs = self.out[ coords[0] ]
        ys = self.out[ coords[1] ]

        # Now plot stuff
        fig = plt.figure()
        ax = fig.gca()
        ax.plot( xs, ys, **fargs )
        ax.set_xlabel( r"$x_"+str( coords[0] )+"$" )
        ax.set_ylabel( r"$y_"+str( coords[1] )+"$" )
        fig.show()

def main( args ):
    """
    Parse args, write IC file if necessary. Hand off ti XPP object,
    then handle output.
    """
    xp = XPPWrap( args.ode, discrete=args.discrete )
    return xp


#############################
## BEGIN ARGUMENT PARSING
#############################
parser = argparse.ArgumentParser()

# 
parser.add_argument( "-v", "--verbosity",
                    help="increase output verbosity",
                    action="store_true",
                    default=False )
parser.add_argument( "-o", "--ode",
                     help="Path to ODE file [Mandatory arg]" )
parser.add_argument( "-i", "--init_cond",
                     help="Path to file containing IC's [optional]" )
# parser.add_argument( "-p", "--plot",
#                      help="Plot data. Used in conjunction with plot_vars." )
parser.add_argument( "-d", "--discrete",
                     help="Toggle discrete flag for maps (True) or flows (False). "\
                     "For plotting purposes only. [False]",
                     action="store_true",
                     default=False )
parser.add_argument( "-p", "--plot",
                     help="Toggle plotting. [False]",
                     action="store_true",
                     default=False )
                     
args = parser.parse_args()
if args.verbosity:
    print "verbosity turned on"
if not args.ode:
    raise ValueError, "Must pass path to IDE file! See usage."


if __name__ == "__main__":
    
    #################
    ##  Run main()
    #################
    XP = main( args )
    XP.run()

    if args.plot:
        XP.plot2d( coords=[1,2] )
        if 'lorenz' in args.ode:
            XP.plot3d( )
