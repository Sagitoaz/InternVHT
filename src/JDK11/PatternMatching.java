package JDK11;

public class PatternMatching {
    static void main() {
        Object obj = "Hello";
        if (obj instanceof String) {
            String s = (String) obj;
            System.out.println(s);
        }
    }
}
