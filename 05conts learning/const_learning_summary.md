zhiz const学习总结：

1，变量不可改：const int a = 10;  

2,普通函数返回类型前面：指针或者引用才会用到 int a = 10; const int& getvalue(){
return a;}

3,类成员 函数：const 限定返回类型不会修改，const在函数体前面代表函数内部不会修改类中的变量，不影响函数体内部变量变化

4，const放在类函数成员的参数前面表示不会修改传入参数，一般搭配引用

5，const实例化的类只能调用const修饰的成员函数,但是可以调用普通成员变量（不能修改）

6,mutable 修饰的允许修改，在const中是例外，一般用于缓存，不能滥用

7，const int* ptr = &a; 修饰指针指向的值不可改； int* const ptr = &a; 修饰指针指向不可改； const int* const ptrt = &a 修饰指针指向的值以及指针指向不可改

8，int a = 10; const int& ref = a; 修饰引用不可改值：ref = 20 报错，但是可以用 int& ref1 = const_cast<int&>(ref); ref1 = 200; 修改，但是a得是非cosnt变量；

9，constexpr ，编译期确定的变量，编译期可确定的表达式求值

10，cosnt 可以绑定临时值的引用，让临时值的生命周期变成变量生命周期。
int setValue(const int& x) {
    return x;
}
int main() {
    std::cout << setValue(10) << std::endl; // 10 被临时值绑定到 const 引用
}

却决于变量所在位置，比如
变量位置	作用域	生命周期
局部变量/函数内	函数/块内	函数/块执行期间
类成员变量	类内部（通过对象访问）	对象存在期间
全局变量	整个文件或程序	程序运行期间
临时值 + const 引用	引用作用域	延长到引用结束（作用域结束）

11，const_cast<引用/指针>(变量) 可以去掉const修饰，但是得注意原来的变量不是const否则是未定义行为。比如int a = 10; cosnt int& b = a; int& c = const_cast<int&>(b); b = 20;可以改
const_cast只能用于引用或者指针类型

