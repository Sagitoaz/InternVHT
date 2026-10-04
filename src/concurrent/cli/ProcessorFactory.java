package concurrent.cli;

import concurrent.processor.Processor;
import concurrent.writer.threadwriter.RecordWriter;

public interface ProcessorFactory {
    public Processor create(int threadCount, RecordWriter writer);
}
