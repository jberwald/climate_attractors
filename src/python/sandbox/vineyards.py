import numpy as np
from climate_attractors.src.python import perseus_wrap as perseus
import matplotlib.pyplot as plt


def compute_diagram_block( data, t0, length, persin=None, dtype='timeseries', **kwargs ):
    """
    Compute the persistence diagrams for the window from a time series.

    datafile -- path to the data file (text or numpy)

    t0 -- start of time series window

    length -- length of the window. eg., window = [t0, t0+window)

    Optional:
    ---------
    
    persfile -- full path to write perseus input file. (Default is to
    append '_pers' to datafile).

    For kwargs, see perseus_wrap.write_time_series().

    Returns filename of perseus-formatted file
    """
    # if persfile:
    #     persout = persfile
    # else:
    #     if datafile.endswith( 'npy' ) or datafile.endswith( 'txt' ):
    #         dfile = datafile[:-4] # also strip '.'
    #         persin = dfile + '_pers_'+str( t0 )+'_'+str( length )+'.txt'
    #         kwargs.update( {'output': persin} )  

#    data_window = data[ t0 : t0+length ]

    # convert timeseries window to perseus format
    perseus.convert2perseus( data, dtype=dtype, **kwargs )

    # run perseus on the output -- strip the '.txt'
    persout = persin[:-4]
    perseus.perseus( persin, persout, 'brips' ) 
    
    return persin, persout

def plot_diagram_window_range( fpath, tstart, tend, wstart, wend, wsteps, **kwargs ):
    """
    Plot a collection of persistence diargrams on one set of axes, (time) x (death time). We can do this because all 0-persistent generators share the same birth time (I think...).

    fpath -- full path plus prefix to collection of Perseus output files. 

             Eg., fpath = '/path/to/files/genbif0_pers' so that the full path becomes
             /path/to/files/genbif0_pers_[t0]_[window]_[dim].txt (dim==0 by default)

    tstart -- first t0 value at which persistence computed (int)

    tend -- final t0 value (int)
    
    wstart -- minimum window size (int)

    wend -- maximum window size (int)

    wsteps -- integer steps between window sizes. Eg., range( wstart, wend, wsteps )

    Note: This is far from optimized. It'll get the job done,though.
    """
    under = '_'
    fargs = { 'dim' : 0,
              'timeseries_steps' : 10 
              }
    fargs.update( kwargs )

    fig = plt.figure()
    ax = fig.gca()

    t_scale = fargs['timeseries_steps']
    dim = fargs['dim']
    if not fpath.endswith('_'):
        fpath += '_'
    points = dict()
    max_y = -1
    for t in xrange( t_scale*tstart, t_scale*tend ):
        points[t] = dict()
        for w in range( wstart, wend, wsteps ):
            persistence_file = fpath + str( t ) + under + str( w ) + under + str( dim ) + '.txt'
            data = np.loadtxt( persistence_file )            
            try:
                points[t][w] = data[:,1] # we only want death times
                dmax = data[:,1].max()
                # update maximum for plotting
                if max_y < dmax:
                    max_y = dmax
            except IndexError:
                points[t][w] = data[1] # just 1D array

    # concatenate window information for plotting
    windows = dict()    
    for w in range( wstart, wend, wsteps ):
        wy = []
        for t in xrange( t_scale*tstart, t_scale*tend ):
            ny = points[t][w]
            print t
            print w
            print ny
            print ""
            if hasattr( ny, "__index__" ):
                for death_time in ny:
                    if death_time == -1:
                        wy.append( death_time )
                    else: 
                        wy.append( max_y + 1 )
            # single real number, probably -1 (infinite generator)
            else:
                if ny == -1:
                    wy.append( max_y + 1 )
                else:
                    wy.append( ny )
        windows[ w ] = set( wy ) 
    return points, windows

def create_vineyard( datafile, tstart, tend, wstart, wend, wsteps=1, debug=False, **kwargs ):
    """
    Run loops across time and over various window sizes.

    
    """
    fargs = { 'nsteps' : 100,
              'bradius' : 0.01,
              'radius_scaling' : 1,
              'stepsize' : 0.01,
              'timeseries_steps' : 10
              }
    fargs.update( kwargs )

    # Load the time series data
    try:
        data = np.load( datafile )
    except IOError:
        data = np.loadtxt( datafile )

    # number of steps per unit time (eg., \delta t = 0.1)
    t_scale = fargs['timeseries_steps']
    # indices for time range
    for t in np.arange( t_scale*tstart, t_scale*tend ):
        for w in np.arange( wstart, wend, wsteps ):
            # create the data segment
            data_window = data[ t : t + w ]

            if debug:
                print data_window

            # create perseus input file name
            prefix = datafile[:-4] # also strip '.'
            # append t0 and window length
            persin = prefix + '_pers_'+str( t )+'_'+str( w )+'.txt'

            # update output for perseus.write_time_series(). This will be _input_ to perseus.
            fargs.update( {'output': persin} ) 

            # write the block of data to perseus format and compute persistence on said block.
            persfile = compute_diagram_block( data_window, t, w,  
                                              persin, **fargs )



if __name__ == "__main__":

    #dfile = "./data/genbif0.txt"
    dfile = '/sciclone/data10/jberwald/climate_attractors/persistence/bif0/genbif0.txt'

    # these are multiplied by 10 later on
    t0 = 700
    t1 = 900
    w0 = 50
    w1 = 300

    length = 200
    bradius = 0.01
    radius_scaling = 1
    stepsize = 0.01
    timeseries_steps = 10 # steps sizes of 0.1


    create_vineyard( dfile, 7000, 9000, 50, 300, 
                     wsteps=10,timeseries_steps=1 )

    # for t in [ 800, 861 ]:
    #     t0 = timeseries_steps * t
    #     pin, pout = compute_diagrams_block( dfile, t0, length,
    #                                         nsteps=100, 
    #                                         bradius=bradius,
    #                                         radius_scaling=radius_scaling,
    #                                         stepsize=stepsize )

    
