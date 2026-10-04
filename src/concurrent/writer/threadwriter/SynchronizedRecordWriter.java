package concurrent.writer.threadwriter;

import concurrent.model.ProcessedRecord;
import concurrent.util.WriteHelper;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class SynchronizedRecordWriter implements RecordWriter {
    private final BufferedWriter writer;

    public SynchronizedRecordWriter(String out) throws IOException {
        writer = new BufferedWriter(new FileWriter(out, true));
    }

    @Override
    public synchronized void write(ProcessedRecord record) throws IOException {
        WriteHelper.formatWrite(writer, record);
    }

    @Override
    public void close() throws IOException {
        writer.close();
    }
}
