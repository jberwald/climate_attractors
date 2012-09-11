import xppy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#ode_file = 'lorenz96.ode'; color='b'
#ode_file = 'lorenz96v2.ode'; color='r'

# Lorenz 84
ode_file = 'lorenz84.ode'; color='r'

# init the xppy object
xppy.createTmp( ode_file )

# run it
out = xppy.run( ode_file )
# equivalent to xpp continue

pars = xppy.parse.readOdePars(ode_file, False, True, False)

ts = list( out[0] )
xs = list( out[1] )
ys = list( out[2] )
zs = list( out[3] )


for i in range(20):
    out = xppy.runLast( out, verbose=False )

    # runLast() computes time from 0..20 only, even though it restarts
    # from the latest IC. Account for this below
    #0:time, 1:u[1], ..., 21:u[21]
    ts.extend( 20*(i+1)+out[0] )
    xs.extend( out[1] )
    ys.extend( out[2] )
    zs.extend( out[3] )

# first, 3d
fig = plt.figure(1)
ax = fig.gca(projection='3d')

ax.plot( xs, ys, zs, color=color )#, lw=3, alpha=0.8)
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")

# individual 2D plots
if 0:
    fig2 = plt.figure(2,figsize=(8,12))
    ax1 = fig2.add_subplot( 311 )
    ax1.plot( ts, xs, color=color, linestyle='-', lw=2, label='x' )
    ax2 = fig2.add_subplot( 312 )
    ax2.plot( ts, ys, color=color, linestyle='-', lw=2, label='y' )
    ax3 = fig2.add_subplot( 313 )
    ax3.plot( ts, zs, color=color, linestyle='-', lw=2, label='z' )
#ax1.legend()

# # X vs Y
# ax2 = fig2.add_subplot(322)
# ax2.plot( xs, ys, 'b-', lw=2, label='x vs y' )
# ax2.legend()
# # X vs Z
# ax3 = fig2.add_subplot( 324 )
# ax3.plot( xs, zs, 'r-', lw=2, label='x vs y' )
# ax3.legend()
# # Y vs Z
# ax4 = fig2.add_subplot( 326 )
# ax4.plot( ys, zs, 'g-', lw=2, label='y vs z' )
# ax4.legend()


fig.show()
#fig2.show()
