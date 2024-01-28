package oa2.task_16;

public class OtherCovariance {
    public static void main(String[] args) {
        Optional<Integer> integerOptional = new Optional<>(5);
        Optional<Number> numberOptional = Optional.widen(integerOptional);

        Integer integer = integerOptional.value();
        Number number = numberOptional.value();
    }
}

record Optional<A>(A value) {
    public static <B, A extends B> Optional<B> widen(Optional<A> optional) {
        return (Optional) optional;
    }
}
