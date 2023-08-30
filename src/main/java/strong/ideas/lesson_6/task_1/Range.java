package strong.ideas.lesson_6.task_1;

import java.util.Objects;

public class Range {
    int indexFrom;
    int indexTo;

    public Range(int indexFrom, int indexTo) {
        this.indexFrom = indexFrom;
        this.indexTo = indexTo;
    }

    public int getIndexFrom() {
        return indexFrom;
    }

    public int getIndexTo() {
        return indexTo;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Range range = (Range) o;
        return indexFrom == range.indexFrom && indexTo == range.indexTo;
    }

    @Override
    public int hashCode() {
        return Objects.hash(indexFrom, indexTo);
    }
}
