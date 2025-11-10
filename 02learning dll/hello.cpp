#include <iostream>

extern "C" __declspec(dllexport) void hello(){
    std::cout << "hello from dll" << std::endl;
}