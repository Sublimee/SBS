package strong.ideas.lesson_7.after;

/*
 * Из исходных методов, которые хотим заменить, кроме ссылки на сам объект перетекают все аргументы исходных методов, в
 * нашем случае это T[]. Если исходные методы используют приватные поля, то к ним нужно будет как-то получить доступ.
 * Вероятно, лучшим решением будет сделать их deep copy и передать в качестве дополнительных параметров, что, однако, не
 * очень удобно. Если передавать в методы посетителя ссылки на приватные поля, то можем в будущем получить нежелательные
 * побочные эффекты.
 */
public class ToArrayVisitor implements Visitor {

    @Override
    public <T> T[] visitHM(HM hm, T[] a) {
        Object[] r = a;
        HM.Node[] tab;
        int idx = 0;
        if (hm.size > 0 && (tab = hm.table) != null) {
            for (HM.Node e : tab) {
                for (; e != null; e = e.next) {
                    r[idx++] = e.value;
                }
            }
        }
        return a;
    }

    @Override
    public <T> T[] visitLHM(LHM lhm, T[] a) {
        Object[] r = a;
        int idx = 0;
        for (LHM.Entry e = lhm.head; e != null; e = e.after) {
            r[idx++] = e.value;
        }
        return a;
    }
}