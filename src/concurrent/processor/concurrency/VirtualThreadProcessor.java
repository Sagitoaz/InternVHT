package concurrent.processor.concurrency;

import concurrent.model.FileRecord;
import concurrent.model.consumer.RecordConsumer;
import concurrent.model.producer.RecordProducer;
import concurrent.processor.ProcessResult;
import concurrent.processor.Processor;
import concurrent.writer.threadwriter.RecordWriter;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

public class VirtualThreadProcessor extends Processor {
    private final int workerCount;
    private final RecordWriter writer;

    public VirtualThreadProcessor(int workerCount, RecordWriter writer) {
        this.workerCount = workerCount;
        this.writer = writer;
    }

    @Override
    public void process(String file) {

        BlockingQueue<FileRecord> queue = new ArrayBlockingQueue<>(1000);

        List<RecordConsumer> consumers = new ArrayList<>();

        try {
            ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
            RecordProducer producer = new RecordProducer(queue, file);
            Thread produceThread = new Thread(producer, "produceThread");
            produceThread.start();

            List<Future<?>> consumerFutures = new ArrayList<>();

            for (int i = 0; i < workerCount; i++) {
                RecordConsumer consumer = new RecordConsumer(queue, writer);
                consumers.add(consumer);
                Future<?> future = executor.submit(consumer);
                consumerFutures.add(future);
            }

            produceThread.join();

            for (int i = 0; i < workerCount; i++) {
                queue.put(FileRecord.POISION_PILL);
            }

            for (Future<?> future : consumerFutures) {
                future.get();
            }

            long totalRecords = 0;
            long totalWords = 0;
            for (RecordConsumer consumer : consumers) {
                totalRecords += consumer.getProcessCount();
                totalWords += consumer.getWordCount();
            }
            createResult(totalRecords, totalWords);

            writer.close();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
