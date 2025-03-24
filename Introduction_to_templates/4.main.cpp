#include <iostream>

template <typename T>
void print(T x);

template<>
void print<int>(int x) {
    std::cout << "int: " << x << std::endl;
}

template<>
void print<double>(double x) {
    std::cout << "double: " << x << std::endl;
}

template <typename T>
void nonTemplatePrint(T x) {
    if (std::is_same<T, int>::value) {
        std::cout << "int: " << x << std::endl;
    } else if (std::is_same<T, double>::value) {
        std::cout << "double: " << x << std::endl;
    }
}

template <typename T>
void timesTwoAndPrint(T x) {
    print(x * 2);
}

int main() {
    timesTwoAndPrint(10);
    timesTwoAndPrint(10.5);
    return 0;
}