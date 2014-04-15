#ifndef _point_h
#define _point_h

#include <iostream>
#include <iomanip>
#include <vector>
#include "point.h"

using namespace std;

//typedef PointBase< double > IPoint;


int main()
{

    int d = 2;
    double x = 3.14;
    double y = 5.5;
    
        // initialize a vector of intervals (an interval point)
        // PointBase< double > P(d); // ( d );

    Point P(d);

    P[0] = x;
    P[1] = y;

    cout << P << endl;
    cout << "P.size() = " << P.size() << endl;
    
	IPoint IP(2);
    
    
    return 0;

}

#endif
