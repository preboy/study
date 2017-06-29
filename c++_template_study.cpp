
模板学习：

类模板在外定义成员函数：


template<typename A, typename B>
class myClass
{
    void h();
};

template<typename A, typename B>
void myClass<A,B>::h()
{
};

区别于普通成员函数的方法：
void myClass::h(){}

非类型型参，类型型参，


模板显示实例化：让程序员控制模板实例化的时间：

比如有：
template<typename T>void h(hT a){};
template void h<int>(int ); 这就创建了一个h函数的int实例。

template<typename T> T h(T a){} 
显示实例化为:
template int h<int>(int);

template class A<int, int>; 将类显示实例化为int类型。

显示模板实参：
template<typename A, typename B, typename C>A h(B b, C c){};
可以省略尾部的实参，如：
h<int>(2,3.4);只指定了A为int,B,C 自行推导。但只能省略尾部的哈，

模板特化：
如有：template<tpyename T> void h(T a){};
则特化为：
template<> void h<int>(int a){}
如果可以从实参是推演出模板的形参：则可以省略掉模板实参的部分：
比如：template<> void h(int a){}

在类外定义被特化的模板类的方法时，应当省略掉前面的“template<>”
如：void A<int>::h(){}

如有:template<typename T1, typename T2> class A{};
特化后为：
template<> class A<INT, CHAR>{};

类模板的部分特化：
template<typename T2>class A<int, T2>{}; T1为int;
template<typename T1>class A<T1, T1>{} 将T2特化为T1

模板类 类A内部定义了类B，函数g，
 template<typename T1>
class A
{
  public:
    template<typename T2>
      class B
      {
      };

    template<typename T3> void g(T3 a);

};

在外部实现时：

template<tpyename T1>
template<typename T2>
class A<T1>::B
{
};

 真是变态的东西，要是看到谁以后这么用了，我必杀之，




