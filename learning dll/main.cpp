#include <iostream>
#include <windows.h>

int main() {
    //����DLL
    HMODULE hDll = LoadLibrary("noextern.dll");
    if (!hDll){
        std::cerr << "�޷�����" << std::endl;
        return 1;
    }
    
    //��ȡ������ַ
    typedef void (*HelloFunc)();
    HelloFunc hello = (HelloFunc)GetProcAddress(hDll, "hello");
    
    if (!hello){
        std::cerr << "�Ҳ�������" << std::endl;
        return 2;
    }

    //���� DLL �еĺ���
    hello();

    //ж��DLL
    FreeLibrary(hDll);
    return 0;
}