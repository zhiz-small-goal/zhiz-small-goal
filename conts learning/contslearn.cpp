#include <iostream>

int x = 10;
char n = 'a';


int main() {
	const int y = 20;
	std::cout << "x = " << x << "\n";

	char* p = &n;
	std::cout << "p = " << *p << std::endl;
	std::cout << "type:" << typeid(*p).name() << std::endl;
	std::cout << "size" << sizeof(*p) << "zijie" << std::endl;
	std::cout << "sizelf(char):" << sizeof(char) << std::endl;
	std::cout << "sizeof(int):" << sizeof(int) << "zijie\n";
	*p = 'b';
	std::cout << "p=" << *p << std::endl;

	int* ptr = &x;
	std::cout << "ptr= " << *ptr << std::endl;

	*ptr = 30;
	std::cout << "x= " << x << std::endl;

	auto g = 'H';
	std::cout << "g type:" << typeid(g).name() << std::endl;
	//std::cout << "ptr2 type:" << typeid(ptr2).name() << std::endl;
	
	return 0;
}