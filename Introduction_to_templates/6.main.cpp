#include <iostream>

template <bool timesTwo, int x, typename T>
class TimesTwoAndOrPrint {
    T value;
public:
    TimesTwoAndOrPrint(T value) : value(value) {}
    void print() {
        if constexpr (timesTwo) { // requires C++ 17
            std::cout << value * 2 << std::endl;
        } else {
            std::cout << value << std::endl;
        }
    }

    static void printx() {
        if constexpr (timesTwo) { // requires C++ 17
            std::cout << x * 2 << std::endl;
        } else {
            std::cout << x << std::endl;
        }
    }
};

int main() {
    TimesTwoAndOrPrint<true, 10, int> t1(10);
    t1.print();
    TimesTwoAndOrPrint<false, 3, int> t2(3);
    t2.print();
    return 0;
}
