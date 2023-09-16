package strong.ideas.lesson_8.example_2;

import java.util.ArrayList;
import java.util.List;

interface Commentable {

    List<String> getComments();

    void addComment(String comment);
}

class CommentableMixin implements Commentable {

    private final List<String> comments = new ArrayList<>();

    @Override
    public List<String> getComments() {
        return comments;
    }

    @Override
    public void addComment(String comment) {
        this.getComments().add(comment);
    }
}

class Post implements Commentable {

    private final Commentable commentable = new CommentableMixin();

    @Override
    public List<String> getComments() {
        return commentable.getComments();
    }

    @Override
    public void addComment(String comment) {
        commentable.addComment(comment);
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
