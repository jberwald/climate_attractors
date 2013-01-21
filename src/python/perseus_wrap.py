import subprocess as sp
from numpy import loadtxt, load
import matplotlib.pyplot as plt
import argparse
import os

space = " "
slash = "/"

def perseus ( fname, output, dtype='scubtop', path=None, debug=False ):
    """
    Call perseus with the command

    '/usr/bin/perseus DTYPE FNAME OUTPUT'

    fname -- full path to data file

    output -- prefix of output file, will be appended with
        output_*.txt by perseus

    dtype -- input to perseus, eg., cubtop, scubtop, etc.

    See http://www.math.rutgers.edu/~vidit/perseus.html for more
    details.
    """
    if os.uname()[0] == 'Darwin':
        cmd = [ '/usr/bin/perseus3', dtype, fname, output ]
    else:
        cmd = [ 'perseus', dtype, fname, output ]

    if debug:
        print "Command: "
        print cmd
    try:
        result = sp.call( cmd )
    except OSError:
        print "subprocess failed!"
        print "command passed to subprocess:", cmd
    return result

def convert2perseus( data, dtype, **kwargs ):
    """
    Convert an array, or text or numpy file to perseus format.
    """
    if dtype == 'dmatrix':
        out = write_distance_matrix( data, **kwargs )
    elif dtype == 'timeseries':
        out = write_time_series( data, **kwargs )
    else:
        print "Unknown data type!"
    return out

def write_time_series( data, **kwargs ):
    """
    data -- numpy array
    """
    fargs = {'output' : None,
             'radius_scaling' : 1,
             'stepsize' : 0.2,
             'nsteps' : 10,
             'bradius' : None,
             'tstepsize' : 1,
             'embed_dim' : 1
             }
    fargs.update( kwargs )

    # load from file if data is not an array of points already
    if not hasattr( data, '__index__' ):
        # .npy or .txt
        try:
            data = load( data )
        except IOError:
            data = loadtxt( data )

    if not fargs['output'].endswith( 'txt' ):
        fargs['output'] += '.txt'

    # This gets appended to the end of every line
    br = str( fargs['bradius'] )
        
    with open( fargs['output'], 'w' ) as fh:
        # ambient dimension
        fh.write( str( fargs['embed_dim'] )+'\n' )
        
        # initial threshold, step size, num steps, dimension cap==ny
        params = [ str( fargs['radius_scaling'] ),
                   str( fargs['stepsize'] ),
                   str( fargs['nsteps'] )
                   ]
        params = space.join( params )
        params += '\n'
        fh.write( params )

        # now write the time series and birth radii to disk
        for obs in data:
            try:
                r = [ str( x ) for x in obs ]
            except TypeError:
                # quicker than if/else 
                r = [ str( obs ) ]
            r += [ br ] # add the birth radius
            r = space.join( r )
            r += '\n'
            fh.write( r )
    print "wrote file to ", fargs['output']
    out = { 'filename' : fargs['output'],
            'data' : data }
    return out

def plot_diagram( persFile, fontsize=12, scale=None, color='b',
                  show_fig=True, fig=None, title=None ):
    """
    persFile -- path to <perseus output>_*.txt, where * is the dimension.

    scale -- Factor to scale the birth/death times. 
    """
    if scale:
        # cast values as floats for division
        s = np.loadtxt( persFile, dtype=np.float, delimiter=' ' )
        s /= scale
    else:
        s = np.loadtxt( persFile, dtype=np.int, delimiter=' ' )
        
    try:
        births = s[:,0]
        deaths = s[:,1]
    except IndexError:
        # s is an (n,) array, so it must be reshaped in-place for
        # proper indexing
        print s.shape
        s.resize( ( s.shape[0], 1 ) )
        print s
        births = s[0] 
        deaths = s[1]

    # max death time
    if deaths.max() > 0:
        maxd = deaths.max()
    else:
        maxd = births.max()
    print "Max death time ",  maxd

    # non-infinite gens
    normal_idx = np.where( deaths != -1 )[0]

    # add to an existing figure if necessary
    if not fig:
        fig = plt.figure( ) 
        fig.patch.set_alpha( 0.0 )
    ax = fig.gca()

    if len( normal_idx ) > 0:
        ax.plot( births[normal_idx], deaths[normal_idx], color+'o' )

    # create diagonal
    diag = [0, maxd+2]
    ax.plot(diag, diag, 'g-')

    # infinite gens
    inf_idx = np.where( deaths == -1 )[0]
    inf_vec = (maxd + 1) * np.ones( len( inf_idx ) )

    # plot the infinite generators
    ax.plot( births[inf_idx[0]], inf_vec, 'ro' )

    print ax.get_xticks()

    # xticks = [ int( tk ) for tk in ax.get_xticks() ]
    # yticks = [ int( tk ) for tk in ax.get_yticks() ]
    ax.set_xticklabels( ax.get_xticks(), fontsize=fontsize )
    ax.set_yticklabels( ax.get_yticks(), fontsize=fontsize )
    # fix the left x-axis boundary at 0
    ax.set_xlim( left=0 )
    ax.set_ylim( bottom=0 )

    if title:
        ax.set_title( title, fontsize=16 )
    if show_fig:
        fig.show()
        
    print "Total number of persistence intervals", len( births ) 
    return fig




if __name__ == "__main__":

    import os, sys

    # # create a parser and add some arguments
    # parser = argparse.ArgumentParser( prog='perseus_wrap',
    #                                   description='Run Perseus persistence software on a time series,'\
    #                                   'point cloud data, or cubical complex.')

    # parser.add_argument( '--data', help='Path to data file' )
    # parser.add_argument( '--dtype', default='ts',
    #                      help='ts -- time series, cc -- cubical complex. [ts]' )
    # parser.add_argument( '--start', type=int,
    #                      help='Start (index in array) of windowed time series' )
    # parser.add_argument( '--window', type=int,
    #                      help='Length of window' )

    # parser.parse_args()


    fname = '../../data/genbif0.txt'
    pers = '../../data/genbif0_pers'
    outprefix = '../../data/genbif0'

    if not os.path.exists( fname ):
        print "Data file not found, ", data
        sys.exit(1)

    data = np.loadtxt( fname )
    birth_rad = 0.01
    for start in [800]: #[400,800,860,861,862,865]:
        for window in range(190,206): #[190, 195, 200, 205]: #[150,199,200]:
            t0 = 10*start  # time steps = 0.1
            end = start + window
            data_window = data[ t0 : t0+window  ]
            print "data_window.shape:", data_window.shape
            suffix = '_' + str( start ) + '_' + str( window )
            persfile = pers + suffix
            out = convert2perseus( data_window, dtype='timeseries',
                                   output=persfile, radius_scaling=1,
                                   stepsize=0.01, nsteps=100,
                                   bradius=birth_rad,
                                   )
            persout = outprefix + '_' + str( start ) + '_' + str( window ) + '_out'
            res = perseus( out['filename']+'.txt', persout, dtype='brips', debug=True )

            # now plot a diagram
            fig = plot_diagram( persout + '_0.txt', title=persout+r'-- $\beta_0$',
                                show_fig=True)
            fig.savefig( '../../figures/genbif_figs/window_800/genbif0_'\
                         +str(start)+'_w'+str(window)+'_0.png' ) 
