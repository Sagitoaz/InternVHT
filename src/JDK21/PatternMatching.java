package JDK21;

public class PatternMatching {
    static void main() {
        Object obj = "Hello";
        if (obj instanceof String s) {
            System.out.println(s);
        }

        switch (obj) {
            case String s -> System.out.println(s.length());
            case Integer i -> System.out.println(i);
            default -> System.out.println(obj);
        }
    }
}
