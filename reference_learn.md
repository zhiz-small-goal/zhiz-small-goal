# C++ 引用学习笔记

## 示例 1: 基本引用

```cpp
int x = 10;
int& y = x;
y = 30; // x = 30
```

## 示例 2: const 引用（只读引用）

```cpp
int x = 20;
const int& y = x;
y = 20; // ❌，const 是只读引用
```

## 示例 3: 函数返回引用

```cpp
int x = 10;
int& getValue() {
    return x;
}
int& y = getValue();
y = 30;
```

## 示例 4: const 引用返回值

```cpp
int x = 20;
const int& getValue() {
    return x;
}

int& y = getValue(); // ❌ 写法错误，因为有const
const int& y = getValue(); // ✅ 写法正确，因为有const
y = 40; // ❌，不能修改，const只读
```

## 示例 5: 类中的引用

```cpp
class myClass {
private:
    std::string name;
    int age;
    const int height = 165;

public:
    myClass(std::string& str, int& a): name(str), age(a) {}

    std::string& getName() {
        return name;
    }

    const int& getAge() {
        return age;
    }

    int& getHeight() {
        return height; // ❌，不能用非常量引用const
    }

    int getHeight() {
        return height; // ✅
    }

    void setAge(const int& newage) {
        age = newage;
    }
};
```

### 使用示例

```cpp
std::string name = "zhiz";
int age = 30;
myClass zhizclass(name, age);
int age = zhizclass.getAge();
age = 50;
std::string& name = zhizclass.getName();
name = "zhiz baby";
int height = zhizclass.getHeight();
height = 167; // ❌，不能修改const常量,不过改的是副本，不会报错，上面等于复制身高给height
```

## 总结

- **普通引用**：可以修改原变量的值
- **const 引用**：只能读取，不能修改
- **函数返回引用**：注意返回值的 const 性质要与引用类型匹配
- **类成员函数返回引用**：const 成员变量不能通过非 const 引用返回
- **返回值接收**：通过值接收（非引用）会创建副本，修改副本不会影响原值

