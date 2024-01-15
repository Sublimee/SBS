package oa2.task_12;

import java.io.Serializable;

class General implements Serializable {
    static General assignmentAttempt(General target, General source) {
        if (target.getClass().isAssignableFrom(source.getClass())) {
            return source;
        }
        return new Void();
    }
}

class Any extends General {
    static Any assignmentAttempt(Any target, Any source) {
        if (target.getClass().isAssignableFrom(source.getClass())) {
            return source;
        }
        return new Void();
    }
}

final class Void extends Any /*A, B, ....*/ {
}