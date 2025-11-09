#include <iostream>
#include <string>



class Person {
private:
	std::string name;
	int age;

public:
	Person(std::string n, int a) : name(n), age(a) {}

	std::string zhiz = "zhiz";
	const std::string const_zhiz = "const_zhiz";

	std::string getName() const {
		return name;
	}

	const int& getAge() const {
		return age;
	}

	void setName(const std::string& n) {
		name = n;
	}

	void setAge(const int& a) {
		age = a;
	}

	int& getAge() {
		return age;
	}
};

constexpr int getValue() {
	return 10 + 20;
}

constexpr int square(int a) {
	return a * a;
}

//const没意义
const int setValue2(int a, int b) {
    	return (a > b) ? a : b;
}

//const 有意义
int aa = 10;
const int& getValue3() {
	return aa;
}
const int* getValue4() {
	return &aa;
}

constexpr int getValue2(int a, int b) {
	return (a > b) ? a : b;
}

class Counts {
private:
	mutable int counts;
	std::string s;

public:
	Counts(const std::string& str): counts(0), s(str) {}
	void printstr() const {
		std::cout << s << std::endl;
		counts++;
		int x = 10;
		x = 100;
	}

	int getCounts() const {
		return counts;
	}
};


int main() {
	Person z("zhiz", 25);
	std::cout << "Name= " << z.getName() << std::endl;
	std::cout << "age=" << z.getAge() << std::endl;

	int& age1 = z.getAge();
	age1 = 34;
	std::cout << "new age = " << z.getAge() << std::endl;

	std::cout << " 枝枝：" << z.zhiz << std::endl;
	std::cout << "const_zhiz===" << z.const_zhiz << std::endl;
	
	const Person zz("zhiz", 20);
	zz.zhiz;
	std::cout << " 枝枝：" << zz.zhiz << std::endl;

	const int MAX = 100;
	const int MIN = 20;
	const int* ptr2 = &MIN;
	const int min = 11;
    const int* ptr = &MAX;
	const int* const ptr3 = &MAX;
	int e = 200;

	std::cout << "第三个指针值" << *ptr3 << std::endl;
	std::cout << "ptr3的地址" << ptr << std::endl;
	//ptr3 = &MIN; //error
	//*ptr3 = 200; //error
	std::cout << "MAX=" << MAX << std::endl;
	std::cout << "指针指向的值" << *ptr << std::endl;
	//MAX = 200; //error
	//*ptr = 200; //error
	//ptr = &MIN; //error
	ptr = &min;
	std::cout << "指针指向的值" << *ptr << std::endl;
	ptr = ptr2;
	std::cout << "指针指向的值" << *ptr << std::endl;


	constexpr int a = 20;
	//a = 30; //error

	constexpr int b = getValue();
	std::cout << "输出的b = " << b << std::endl;

	constexpr int c = getValue2(20, 40);
	std::cout << "输出的c = " << c << std::endl;

	constexpr int ss = square(4);
	std::cout << "ss = " << ss << std::endl;

	Counts c1("hello");
	c1.printstr();
	c1.printstr();
	c1.printstr();
	std::cout << "counts: " << c1.getCounts() << std::endl;


	int* py = const_cast<int*>(ptr);
	std::cout << "py指向的值" << *py << std::endl;
	//py = 30; //error

	const int* ptr4 = &e;
	std::cout << "ptr4指向的值" << *ptr4 << std::endl;
	//ptr4 = 30; //error
	int* py2 = const_cast<int*>(ptr4);
	*py2 = 300;
	std::cout << "ptr4 最后指向的值" << *ptr4 << std::endl;

	const int& py3 = e;
	//py3 = 30000;//error
	std::cout << "py3 reference value" << py3 << std::endl;
	int py4 = const_cast<int&>(py3);
	std::cout << "py4 = " << py4 << std::endl;
	py4 = 30000;
	std::cout << "py4 = " << py4 << std::endl;
	std::cout << "py3最后的值" << py3 <<std::endl;

	int& py5 = const_cast<int&>(py3);
	std::cout << "py5=" << py5 << std::endl;
	py5 = 5000;
	std::cout << "py3 last value" << py3 << std::endl;
	
	return 0;
}
