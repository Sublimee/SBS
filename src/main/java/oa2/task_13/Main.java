package oa2.task_13;

class A1 {
    public void method() {
        System.out.println("Метод в классе A");
    }
}

class B1 extends A1 {
    @Override
    public void method() {
        System.out.println("Переопределенный метод в классе B");
    }
}

class A4 {
    private void method() {
        System.out.println("Скрытый метод в классе A");
    }
}

class B4 extends A4 {
    // @Override (метод родителя скрыт, поэтому его нельзя переопределить)
    private void method() {
        System.out.println("Скрытый метод в классе B");
    }
}