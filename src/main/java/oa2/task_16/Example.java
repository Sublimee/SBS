package oa2.task_16;

public class Example {

    public static void main(String[] args) {
        A a = new A();
        A ab = new B();

        System.out.println(a.returnSomething());
        System.out.println(ab.returnSomething());
    }
}

class A {

    public Number returnSomething() {
        return 0;
    }
}

class B extends A {

    @Override
    public Integer returnSomething() {
        return 1;
    }
}