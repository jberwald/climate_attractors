//#ifndef _interval__h
//#define _interval__h

#include <iostream>
#include <iomanip>
#include <vector>

using namespace std;

// Class for the non-rigorous computation of interval arithmetic. This
// class replaces all functionality required by PointBase class and
// Box class. see point.h and box.h (box.cpp)
template < class T >
class interval
{

public:

    vector < T > vec;

         // constructor for interval class: to be filled with a
         // sequence of d 'lower left' endpoints for the boxes
    interval( int size ) 
        : vec ( size ) 
        {};
    interval( int size, const T& t ) 
        : vec ( size, t ) 
        {};


    T& operator[] ( int i )
        {
            return vec[i];
        };
    
    int size() const
        {
            return vec.size();
        };

    // ostream& operator<<( ostream &out, const vector<T> &v )
    // {
    //     out << "vec " << v << "\n";
    //     return out;
    // } 
    
    

};
 
//#endif
