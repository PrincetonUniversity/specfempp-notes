#include <iostream>

template <bool timesTwo, int x, typename T>
class TimesTwoAndOrPrint;

template <int x, typename T>
class TimesTwoAndOrPrint<true, x, T> {
    T value;
public:
    TimesTwoAndOrPrint(T value) : value(value) {}
    void print() {
        std::cout << value * 2 << std::endl;
    }

    static void printx() {
        std::cout << x * 2 << std::endl;
    }
};

template <int x, typename T>
class TimesTwoAndOrPrint<false, x, T> {
    T value;
public:
    TimesTwoAndOrPrint(T value) : value(value) {}
    void print() {
        std::cout << value * 2 << std::endl;
    }

    static void printx() {
        std::cout << x * 2 << std::endl;
    }
};

int main() {
    TimesTwoAndOrPrint<true, 10, int> t1(10);
    t1.print();
    TimesTwoAndOrPrint<false, 3, int> t2(3);
    t2.print();
    return 0;
}
