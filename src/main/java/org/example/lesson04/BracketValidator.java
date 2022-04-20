package org.example.lesson04;

public class BracketValidator {

    public boolean validate(String sequence) {
        Stack<Character> stack = new Stack<>();
        for (char bracket : sequence.toCharArray()) {
            if (bracket == '(') {
                stack.push(bracket);
            } else {
                if (stack.pop() == null) {
                    return false;
                }
            }
        }
        return stack.size() == 0;
    }
}
