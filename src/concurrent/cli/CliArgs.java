package concurrent.cli;

public class CliArgs {
    private ProcessMode processMode;
    private int threadCount;
    private String file;
    private WriteMode writeMode = WriteMode.NONE;
    private String out = "";

    private CliArgs() {}

    public static CliArgs parse(String[] args) {
//        java -jar <file-jar> <read-mode> <thread-count> <file-input>;

        CliArgs cliArgs = new CliArgs();
        parseRequiredArgs(args, cliArgs);
        parseOptionalArgs(args, cliArgs);
        return cliArgs;
    }

    private static void parseRequiredArgs(String[] args, CliArgs cliArgs) {
        cliArgs.processMode = ProcessMode.valueOf(args[0].toUpperCase());
        cliArgs.threadCount = Integer.parseInt(args[1]);
        cliArgs.file = args[2];
    }

    private static void parseOptionalArgs(String[] args, CliArgs cliArgs) {
        for (int i = 3; i < args.length; i++) {
            switch (args[i]) {
                case "-w", "--write" -> cliArgs.writeMode = WriteMode.from(args[++i]);
                case "-o", "--out" -> cliArgs.out = args[++i];
                default -> throw new RuntimeException("Missmatching");
            }
        }
    }

    public ProcessMode getProcessMode() {
        return processMode;
    }

    public int getThreadCount() {
        return threadCount;
    }

    public String getFile() {
        return file;
    }

    public WriteMode getWriteMode() {
        return writeMode;
    }

    public String getOut() {
        return out;
    }
}