#include <iostream>

int timesTwo(int x) {
    return x * 2;
}

double timesTwo(double x) {
    return x * 2;
}

int main() {
    std::cout << timesTwo(10) << std::endl;
    std::cout << timesTwo(10.5) << std::endl;
    return 0;
}