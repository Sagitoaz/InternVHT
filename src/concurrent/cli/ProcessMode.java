package concurrent.cli;

import concurrent.processor.*;
import concurrent.processor.buffer.SeqBufProcessor;
import concurrent.processor.buffer.SeqUnbufProcessor;
import concurrent.processor.concurrency.BlockingQueueProcessor;
import concurrent.processor.concurrency.ExecutorQueueProcessor;
import concurrent.processor.concurrency.VirtualThreadProcessor;
import concurrent.writer.threadwriter.RecordWriter;

public enum ProcessMode {
    BUFFERED("Sequential Buffered", (threadCount, writer) -> new SeqBufProcessor()),
    UNBUFFERED("Sequential Unbuffered", (threadCount, writer) -> new SeqUnbufProcessor()),
    QUEUE("Blocking queue", BlockingQueueProcessor::new),
    EXECUTOR("Executor blocking queue", ExecutorQueueProcessor::new),
    VIRTUAL("Virtual thread", VirtualThreadProcessor::new);

    private final String processName;
    private final ProcessorFactory processorFactory;

    ProcessMode(String processName, ProcessorFactory processorFactory) {
        this.processName = processName;
        this.processorFactory = processorFactory;
    }

    public String getProcessName() {
        return processName;
    }

    public Processor createProcess(int threadCount, RecordWriter writer) {
        return processorFactory.create(threadCount, writer);
    }
}