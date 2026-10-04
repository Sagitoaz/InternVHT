package concurrent.writer.threadwriter;

import concurrent.model.FileRecord;
import concurrent.model.ProcessedRecord;
import concurrent.util.WriteHelper;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class UnsafeRecordWriter implements RecordWriter{
    private final BufferedWriter writer;

    public UnsafeRecordWriter(String out) throws IOException {
        this.writer = new BufferedWriter(new FileWriter(out, true));
    }

    @Override
    public void write(ProcessedRecord record) throws IOException {
        WriteHelper.formatWrite(writer, record);
    }

    @Override
    public void close() throws IOException {
        writer.close();
    }
}
