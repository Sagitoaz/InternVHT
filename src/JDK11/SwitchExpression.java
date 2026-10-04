package JDK11;

public class SwitchExpression {
    static void normalSwitch() {
        String day = "2";
        switch (day) {
            case "1":
                System.out.println("Monday");
                break;
            case "2":
                System.out.println("Tuesday");
                break;
            default:
                System.out.println("Invalid day");
        }
    }

    static void moreCase() {
        String day = "2";
        switch (day) {
            case "1":
            case "2":
                System.out.println("Weekday");
                break;
            case "3":
            case "4":
                System.out.println("Weekend");
                break;
            default:
                System.out.println("Invalid day");
        }
    }

    static void main() {
        normalSwitch();
        moreCase();
    }
}
