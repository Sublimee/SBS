package strong.ideas.lesson_7.after;

public interface MyMap {
    <T> T[] valuesToArray(Visitor visitor, T[] a);
}
