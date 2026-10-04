package concurrent.writer.threadwriter;

import concurrent.model.ProcessedRecord;
import concurrent.util.WriteHelper;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class LockRecordWriter implements RecordWriter {
    private final BufferedWriter writer;
    private final Lock lock = new ReentrantLock();

    public LockRecordWriter(String out) throws IOException {
        writer = new BufferedWriter(new FileWriter(out, true));
    }

    @Override
    public void write(ProcessedRecord record) throws IOException {
        lock.lock();
        try {
            WriteHelper.formatWrite(writer, record);
        } finally {
            lock.unlock();
        }
    }

    @Override
    public void close() throws IOException {
        writer.close();
    }
}
