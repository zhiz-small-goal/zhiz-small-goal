#include <iostream>
#include <windows.h>

int main() {
    //加载DLL
    HMODULE hDll = LoadLibrary("noextern.dll");
    if (!hDll){
        std::cerr << "无法加载" << std::endl;
        return 1;
    }
    
    //获取函数地址
    typedef void (*HelloFunc)();
    HelloFunc hello = (HelloFunc)GetProcAddress(hDll, "hello");
    
    if (!hello){
        std::cerr << "找不到函数" << std::endl;
        return 2;
    }

    //调用 DLL 中的函数
    hello();

    //卸载DLL
    FreeLibrary(hDll);
    return 0;
}