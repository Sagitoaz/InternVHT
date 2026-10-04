package concurrent.writer.threadwriter;

import concurrent.model.FileRecord;
import concurrent.model.ProcessedRecord;

import java.io.IOException;

public class NoOpsRecordWriter implements RecordWriter {
    @Override
    public void write(ProcessedRecord record) throws IOException {

    }

    @Override
    public void close() throws IOException {

    }
}
