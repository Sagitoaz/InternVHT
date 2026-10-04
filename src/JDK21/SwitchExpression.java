package JDK21;

public class SwitchExpression {
    static void normalSwitch() {
        String day = "2";
        switch (day) {
            case "1" -> System.out.println("Monday");
            case "2" -> System.out.println("Tuesday");
            default -> System.out.println("Invalid day");
        }
    }

    static void moreCase() {
        String day = "2";
        switch (day) {
            case "1", "2" -> System.out.println("Weekday");
            case "3", "4" -> System.out.println("Weekend");
            default -> System.out.println("Invalid day");
        }
    }

    static void switchWithYield() {
        String day = "2";
        String res = switch (day) {
            case "1" -> "Monday";
            case "2" -> "Tuesday";
            default -> {
                System.out.println("Invalid day");
                yield "Invalid day";
            }
        };
    }

    static void main() {
        normalSwitch();
        moreCase();
        switchWithYield();
    }
}
