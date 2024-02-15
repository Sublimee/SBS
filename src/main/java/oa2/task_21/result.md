7) Наследование реализации (implementation inheritance)


Кажется, что в качестве примера можно привести реализацию стека поверх списка:

```java
public class Stack<T> extends List<T> { ...

```

Берем класс, который представляет список элементов и добавляем к нему новые возможности, чтобы он лучше подходил под наши задачи: элементы добавляются и удаляются по определённым правилам.

8) Льготное наследование (facility inheritance)

Класс UserAccount наследуется от SecurityUtils, получая доступ к его константам и методам. Это позволяет классу UserAccount использовать логику проверки сложности пароля при создании нового аккаунта и при изменении пароля. По факту это ООП-альтернатива использованию статичных методов утильных классов.

```java
public class SecurityUtils {
    public static final int MIN_PASSWORD_LENGTH = 8;
    public static final String SPECIAL_CHARS = "!@#$%";
    
    public static boolean isPasswordComplex(String password) {
        if (password.length() < MIN_PASSWORD_LENGTH) {
            return false;
        }

        for (char c : SPECIAL_CHARS.toCharArray()) {
            if (password.indexOf(c) >= 0) {
                return true;
            }
        }

        return false;
    }
}

public class UserAccount extends SecurityUtils {
    private String username;
    private String password;

    public UserAccount(String username, String password) {
        if (!isPasswordComplex(password)) {
            throw new IllegalArgumentException("Password does not meet the complexity requirements.");
        }
        this.username = username;
        this.password = password;
    }
    
    public boolean changePassword(String newPassword) {
        if (isPasswordComplex(newPassword)) {
            this.password = newPassword;
            System.out.println("Password changed successfully.");
            return true;
        } else {
            System.out.println("New password does not meet the complexity requirements.");
            return false;
        }
    }
}
```