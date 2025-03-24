#include <iostream>

template <typename T>
T timesTwo(T x) {
    return x * 2;
}

// commenting out these lines will result in error
template int timesTwo<int>(int);
template double timesTwo<double>(double);


