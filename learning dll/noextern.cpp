#include <iostream>
__declspec(dllexport) void hello(){
    std::cout << "hello from nextern dll" << std::endl;
}