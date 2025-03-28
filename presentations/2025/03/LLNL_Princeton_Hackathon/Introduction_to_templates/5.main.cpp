#include <iostream>

template <bool timesTwo, int x>
void timesTwoAndOrPrint() {
    if constexpr (timesTwo) { // requires C++ 17
        std::cout << x * 2 << std::endl;
    } else {
        std::cout << x << std::endl;
    }
}

void timesTwoAndOrPrint(bool timesTwo, int x) {
    if (timesTwo) {
        std::cout << x * 2 << std::endl;
    } else {
        std::cout << x << std::endl;
    }
}

template <bool timesTwo, int x, std::enable_if_t<timesTwo, int> = 0>
void timesTwoAndOrPrint2() {
    std::cout << x * 2 << std::endl;
}

template <bool timesTwo, int x, std::enable_if_t<!timesTwo, int> = 0>
void timesTwoAndOrPrint2() {
    std::cout << x << std::endl;
}

int main() {
    timesTwoAndOrPrint<true, 10>();
    timesTwoAndOrPrint<false, 3>();
    timesTwoAndOrPrint(true, 10);
    timesTwoAndOrPrint(false, 3);
    timesTwoAndOrPrint2<true, 10>();
    timesTwoAndOrPrint2<false, 3>();
    return 0;
}
