from climate_attractors.src.python import perseus_wrap as perseus
from numpy import loadtxt, load


def compute_diagrams_block( datafile, t0, length, dtype='timeseries', persfile=None, **kwargs ):
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
    if persfile:
        persout = persfile
    else:
        if datafile.endswith( 'npy' ) or datafile.endswith( 'txt' ):
            dfile = datafile[:-4] # also strip '.'
            persin = dfile + '_pers_'+str( t0 )+'_'+str( length )+'.txt'
            kwargs.update( {'output': persin} )
            
    try:
        data = load( datafile )
    except IOError:
        data = loadtxt( datafile )
    data_window = data[ t0 : t0+length ]

    # convert timeseries window to perseus format
    perseus.convert2perseus( data_window, dtype=dtype, **kwargs )

    # run perseus on the output
    persout = persin[:-4]
    perseus.perseus( persin, persout, 'brips' ) 
    
    return persin, persout

def create_vineyard( datafile, t0, tstep, w0, wstep, **kwargs ):
    """
    """
    pass

if __name__ == "__main__":

    dfile = "./data/genbif0.txt"
    length = 200
    bradius = 0.01
    radius_scaling = 1
    stepsize = 0.01
    timeseries_steps = 10 # steps sizes of 0.1

    for t in [ 800, 861 ]:
        t0 = timeseries_steps * t
        pin, pout = compute_diagrams_block( dfile, t0, length,
                                            nsteps=100, 
                                            bradius=bradius,
                                            radius_scaling=radius_scaling,
                                            stepsize=stepsize )
