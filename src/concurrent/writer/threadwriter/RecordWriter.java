package concurrent.writer.threadwriter;

import concurrent.model.FileRecord;
import concurrent.model.ProcessedRecord;

import java.io.IOException;

public interface RecordWriter {
    public void write(ProcessedRecord record) throws IOException;
    public void close() throws IOException;
}
