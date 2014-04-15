//#ifndef _point_h
//#define _point_h

#define NONRIGOROUS_INTS

#include <iostream>
#include <iomanip>
#include <vector>

//#ifdef NONRIGOROUS_INTS // define in compile step using -DNONRIGOROUS_INTS

#include "interval_simple.hpp"  // local, non-rigorous interval standin

// #else // using CXSC interval lib
// #include "interval.hpp"
// #include "ivector.hpp"

// #endif

using namespace std;

template < class T >
class PointBase 
{
  public:
        
    interval < T > P;
    PointBase() {};

        // init empty PB interval vector of size = size
    PointBase(int size)
        : P ( size ){};

    PointBase(int size, const T &t)
        : P(size,t) {};

    T& operator[] (int i)
        { return P.vec[i]; };

    void set (int i, const T& t)
        { P.vec[i]=t; };
    
    const T& operator[] (int i) const
        { return P.vec[i]; };

    #ifdef NONRIGOROUS_INTS
    int size() const
        {
            return P.vec.size();
        }; 
    #else
	// CXSC version of dimension
    int size() const
        {
            return VecLen( v );
        }; 
    #endif

friend ostream& operator<< ( ostream &out, const PointBase<T> &p )
{

	for ( int i=0; i < p.size(); i++ )
	{
        if ( i==0 )
			out << "[";
		out << p[i];
		if ( i < p.size()-1 )
			out << "\t";
		if ( i == p.size()-1 )
			out << "]" << endl;
	}
	return out;
}

};


typedef PointBase< double > Point;
typedef PointBase< vector< double > > IPoint;

// #else
// typedef PointBase< interval > IPoint;
// #endif

//#include "treeutil.h"			// for the vector operator<< 
//#endif
