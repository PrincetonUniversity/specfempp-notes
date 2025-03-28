#include <iostream>

template <typename T>
T timesTwo(T x) {
    return x * 2;
}

int main() {
    std::cout << timesTwo(10) << std::endl;
    std::cout << timesTwo<int>(10) << std::endl;
    std::cout << timesTwo(10.5) << std::endl;
    std::cout << timesTwo<double>(10) << std::endl;
    return 0;
}