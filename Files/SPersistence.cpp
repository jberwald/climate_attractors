
#include "CPersistence.h"

#include <vector>

#include <sstream>
#include <string>
#include <algorithm>


#include "Cells/All.h"
#include "Complexes/All.h"
#include "Algos/All.h"


#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <cmath>
#include <stdio.h>
#define PI 3.141592653589793 
 
using namespace std; 

main (int argc, char* argv[]){
  char* input_file;
  input_file = "genbif0.txt";
  ifstream in(input_file);
   ofstream xout("genbif0cubcom.txt");
  const int D = 10000;     // The maximum number of  data entries;
  int N=0; //The size of the data
  double M=0.0;
  double x[D];
  const int t0=8610;
  const int T=200; 

for(int j=0;j<=D;j++){
    if (in.eof()){ break;}
    in >> x[N];
    if (x[N]>M) {M=x[N];}
    //cout<<x[N]<<endl;
    N++;    
    }
    
  

  
//const int number_of_bins=100;
//double h = M/number_of_bins; 

	/*declare cubical data with integer chains and int births*/
	DenseCToplex< int, double> cubical_complex;

	/* define dimension of the image */
	std::vector< num > dimensions;
	dimensions.push_back( N );


	/* initialize cubical complex with the given dimensions */
	cubical_complex.Init( dimensions );

    const double s=0.001;
    const int k=1; 
    const int steps=1000; 
	vector<num> coords;
	coords.resize( 1 );
     xout<<1<<" "<<endl;
     xout<<k<<" "<<s<<" "<<steps<< " "<<endl;
		for(unsigned int t = t0; t < t0+T-1; ++ t){

					coords[ 0 ] =  t;
					/* we need to do binning on data_ */
					//std::cout << "Adding cube " << t << " " << x[t] << "\n";
					//TODO bining to number_of_bins */
                    xout << x[t]<< " " << s /* ceil(x[t]/h)*h */<< " " << endl;
                    }

cout << "The size of the data is=" << N <<endl; 
  cout << "Maximum value="<< M <<endl; 
 // cout << "h="<< h <<endl; 
  
  system("PAUSE");	
  return 0;
} 




