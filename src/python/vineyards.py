import numpy as np
from climate_attractors.src.python import perseus_wrap as perseus
import matplotlib.pyplot as plt
from itertools import ifilter


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

def concatenate_windows( fpath, tstart, tend, wstart, wend, wsteps, **kwargs ):
    """
    Plot a collection of persistence diargrams on one set of axes,
    (time) x (death time). We can do this because all 0-persistent
    generators share the same birth time (I think...).

    fpath -- full path plus prefix to collection of Perseus output files. 

             Eg., fpath = '/path/to/files/genbif0_pers' so that the
             full path becomes
             /path/to/files/genbif0_pers_[t0]_[window]_[dim].txt
             (dim==0 by default)

    tstart -- first t0 value at which persistence computed (int)

    tend -- final t0 value (int)
    
    wstart -- minimum window size (int)

    wend -- maximum window size (int)

    wsteps -- integer steps between window sizes. Eg., range( wstart,
    wend, wsteps )

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
    for w in range( wstart, wend, wsteps ):
        points[w] = []
        for t in xrange( t_scale*tstart, t_scale*tend ):
            persistence_file = fpath + str( t ) + under + str( w ) +\
                under + str( dim ) + '.txt'
            data = np.loadtxt( persistence_file, dtype=np.int )            
            try:
                points[w].append( data[:,1] ) # we only want death times
                dmax = data[:,1].max()
                # update maximum for plotting
                if max_y < dmax:
                    max_y = dmax
            except IndexError:
                points[w].append( data[1] ) # just 1D array
    # postprocess the points to account for the non-invertability of
    # the vineyard "function". This is solely for plotting purposes.
    for k in points.keys():
        points[k] = convert_infs( points[k], max_y )
        points[k] = combines_branches( points[k], t0 = tstart )

    return points 

def convert_infs( vals, max_val ):
    """
    Helper function to convert all -1's to max_val + 1
    
    vals -- list of singletons or arrays with death times.

    max_val -- maximum death time encountered.

    Returns list with all -1's replaced by max_val+1
    """
    m = max_val + 1
    for i, x in enumerate( vals ):
        # x is a singleton
        if hasattr( x, 'bit_length' ):
            if x == -1: vals[i] = m
        # x is an array of death times
        else:
            w = np.where( x==-1 )[0]
            x[w] = m
            vals[i] = x
    return vals

def combine_branches( vals, t0=0 ):
    """
    Extract arrays from lists of death times and rearrange into
    multiple 1D lists for plotting.

    vals -- list of death 'times', with some indices containing
    multiples deaths (hence the mixture of singletons and arrays that
    we're trying to separate).

    t0 -- (optional) start time to add to the enumeration.

    Returns a dict of key : (time,death) or key :
    [(time,death1),(time,death2)]
    """
    # list to hold the main array. We add extra lists to hold (n-1)
    # branches (one can continue in main list)
    vine = {}
    branch_idx = []
    for i,val in enumerate( vals ):
        if hasattr( val, 'bit_length' ):
            vine[i] = ( t0+i, val )
        else:
            branch_idx.append( i )
            # multiple death times; add the branches until back to
            # singletons
            branches = [ ( t0+i, y ) for y in val ]
            vine[ i ] = branches
    # single_idx = [ idx for idx in vine.iterkeys() 
    #                if idx not in branch_idx ]
    return vine, branch_idx

def create_vines( vineyard ):
    """
    A vineyard contains many deaths at the same time instance. Split
    these up to create separate 'functions' to be plotted. This allows
    the use of fun stuff like 'fill_between', etc.
    """
    vals = vineyard.values()
    vines = []
    single_vine = []
    single = True
    for i, current in enumerate( vals[:-1] ):
        if type( current ) == tuple:
            next = vals[i+1]
            # stepping up from single vine to multiple vines
            if type( next ) != tuple:
                # we're leaving a single strand, so set single to
                # false and append single strand to vines
                single = False
                vines.append( single_vine )
                
                # now deal with split
                next.sort() # min --> max
                min_death = next[0]
                max_death = next[-1]
                v1 = [ current, min_death ]
                v2 = [ current, max_death ]
                vines.append( v1 )
                vines.append( v2 )
            # just another point on a single vine
            else:
                if single:
                    single_vine.append( current )
                else:
                    # start a new single strand
                    single_vine = [ current ]
        else:
            next = vals[i+1]
            # we're already on multiple vines
            if type( next ) != tuple:
                next.sort()
                current.sort() # min --> max
                min_current = current[0]
                max_current = current[-1]
                min_next = next[0]
                max_next = next[-1]
                v1 = [ min_current, min_next ]
                v2 = [ max_current, max_next ]
                vines.append( v1 )
                vines.append( v2 )
            # step down from multiple vines to a single vine
            else:
                single = True
                current.sort()
                min_current = current[0]
                max_current = current[-1]
                v1 = [ min_current, next ]
                v2 = [ max_current, next ]
                vines.append( v1 )
                vines.append( v2 )
    return vines
    
        
            
def plot_vineyard( vine, aspect_ratio='auto', fig=None, **kwargs ):
    """
    Plot the (time) x (death time), accounting for multiple death
    times at a single time t.
    """
    fargs = { 'marker' : 'o',
              'markersize' : 4,
              'color' : 'b'
              }
    fargs.update( kwargs )

    if not fig:
        fig = plt.figure()
        ax = fig.gca()
        ax.set_aspect( aspect_ratio )    
    else:
        ax = fig.gca()
    

    for time_slice in vine.itervalues():
        if type( time_slice ) == tuple:
            ax.plot( time_slice[0], time_slice[1], **fargs )
        else:
            for x in time_slice:
                ax.plot( x[0], x[1], **fargs )
    return fig

def create_vineyard( datafile, tstart, tend, wstart, wend, 
                     wsteps=1, debug=False, **kwargs ):
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

    import cPickle as pkl

    #dfile = "./data/genbif0.txt"
    dfile = '/sciclone/data10/jberwald/climate_attractors/persistence/bif0/genbif0.txt'
    dprefix = '/sciclone/data10/jberwald/climate_attractors/persistence/bif0/genbif0_pers'

    # these are multiplied by 10 later on
    t0 = 8000
    t1 = 9000
    w0 = 50
    w1 = 300
    wsteps = 50

    length = 200
    bradius = 0.01
    radius_scaling = 1
    stepsize = 0.01
    timeseries_steps = 10 # steps sizes of 0.1


#    create_vineyard( dfile, 7000, 9000, 50, 300, 
#                     wsteps=10,timeseries_steps=1 )

    #pts = concatenate_windows( dprefix, t0, t1, w0, w1, wsteps, timeseries_steps=1 )
    
    with open( './data/vine_8000_9000_50_300.pkl' ) as fh:
        vines = pkl.load( fh )

    vine_segs = {}
    for k in vines.keys():
        vine_segs[k] = create_vines( vines[k] )
    # color = ['b','g','m','c']
    # aspect_ratio = 100
    # fig = plot_vineyard( vines[50], color='r', aspect_ratio=aspect_ratio )
    # keys = vines.keys()
    # keys.sort()
    # skip k=50
    # for i,k in enumerate( vines.keys()[1:] ):
    #     fig = plot_vineyard( vines[k], color=color[i], 
    #                          aspect_ratio=aspect_ratio, fig=fig )
    # fig.savefig( './data/vines_'+str(keys[0])+'_'+str(keys[-1])+'.png', 
    #              transparent=True )
    

    # for t in [ 800, 861 ]:
    #     t0 = timeseries_steps * t
    #     pin, pout = compute_diagrams_block( dfile, t0, length,
    #                                         nsteps=100, 
    #                                         bradius=bradius,
    #                                         radius_scaling=radius_scaling,
    #                                         stepsize=stepsize )

    
