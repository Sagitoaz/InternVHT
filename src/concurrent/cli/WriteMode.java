package concurrent.cli;

import concurrent.writer.threadwriter.*;

import java.io.IOException;

public enum WriteMode {
    NONE,
    UNSAFE,
    SYNCHRONIZE,
    REENTRANT_LOCK;

    public static WriteMode from(String str) {
        return switch (str.toLowerCase()) {
            case "none" -> NONE;
            case "unsafe" -> UNSAFE;
            case "sync" -> SYNCHRONIZE;
            case  "lock" -> REENTRANT_LOCK;
            default -> throw new RuntimeException("Writer mode not found");
        };
    }

    public RecordWriter createWriter(String out) throws IOException {
        return switch (this) {
            case NONE -> new NoOpsRecordWriter();
            case UNSAFE -> new UnsafeRecordWriter(out);
            case SYNCHRONIZE -> new SynchronizedRecordWriter(out);
            case REENTRANT_LOCK -> new LockRecordWriter(out);
        };
    }
}
