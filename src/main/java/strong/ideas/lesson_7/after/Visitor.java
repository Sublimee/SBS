package strong.ideas.lesson_7.after;

public interface Visitor {

    <T> T[] visitHM(HM hm, T[] a);

    <T> T[] visitLHM(LHM lhm, T[] a);
}
