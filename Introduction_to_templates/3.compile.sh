#!/bin/sh
g++ -c -o main.o 3.main.cpp
g++ -c 3.header.cpp -o header.o
g++ -o a.out main.o header.o
rm main.o header.o