package strong.ideas.lesson_8;

import java.util.ArrayList;
import java.util.List;

interface Commentable {

    List<String> getComments();

    default void addComment(String comment) {
        getComments().add(comment);
    }
}

class Post implements Commentable {

    private final List<String> comments = new ArrayList<>();

    public List<String> getComments() {
        return comments;
    }
}

class Main {

    public static void main(String[] args) {
        Post post = new Post();
        post.addComment("comment-1");
        post.addComment("comment-2");
        System.out.println(post.getComments()); // [comment-1, comment-2]
    }
}
