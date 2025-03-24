#include <iostream>

template <typename T>
T timesTwo(T x);

int main() {
    std::cout << timesTwo(10) << std::endl;
    std::cout << timesTwo(10.5) << std::endl;
    return 0;
}