import pprocess
import time
import numpy as np
 
# Define a function to parallelize:
def takeuptime(ntrials):
    """A function to waste CPU cycles"""
    for ii in range(ntrials):
        junk = np.std(np.random.randn(1e5))
    return junk
 
list_of_args = 8*[500]
 
# Serial computation:
tic=time.time()
serial_results = [takeuptime(args) for args in list_of_args]
print "%f s for traditional, serial computation." % (time.time()-tic)
 
# Parallel computation:
nproc = 8  	# maximum number of simultaneous processes desired
results = pprocess.Map(limit=nproc, reuse=1)
parallel_function = results.manage(pprocess.MakeReusable(takeuptime))
tic=time.time()
[parallel_function(args) for args in list_of_args];  # Start computing things
parallel_results = results[0:3]
print "%f s for parallel computation." % (time.time() - tic)
