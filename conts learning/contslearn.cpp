#include <iostream>

int x = 10;
char n = 'a';

class Myclass {
	int c = 30;

public:
	int getValue() const {
		return c;
	}

	void setValue(int value) {
		c = value;
	}
};

std::string userInput(const std::string& prompt) {
	//prompt = "hello" //error
	std::cout << "userInput: " << prompt << std::endl;
	return prompt;
}


int main() {
	/* �����ǵ�����˫������ϰ*/
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

	//������const��ϰ

	//1����������
	const int a = 10;
	//a = 20 //error

	//2,ָ�볣��
	int b = 20;
	const int* ptr1 = &b;
	//*ptr1 = 30; //error

	int* const ptr2 = &b;
	*ptr2 = 30;
	std::cout << "ptr2���Դ�20�ĳ�30" << *ptr2 << std::endl;

	const int* const ptr3 = &b;
	//*ptr2 = 30; //error
	//ptr2 = &a; //error
	
	//3,���ó���
	const int& ref = b;
	//ref = 20; //error

	//4,��Ա����
	const Myclass obj;
	obj.getValue();
	std::cout << "obj.getValue() = " << obj.getValue() << std::endl;
    //obj.setValue(30); //error

	Myclass obj2;
    obj2.setValue(40);
    std::cout << "obj2.getValue() = " << obj2.getValue() << std::endl;

	
	
	return 0;
}

