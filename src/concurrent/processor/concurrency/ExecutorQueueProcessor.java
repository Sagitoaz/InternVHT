package concurrent.processor.concurrency;

import concurrent.model.consumer.RecordConsumer;
import concurrent.model.FileRecord;
import concurrent.model.producer.RecordProducer;
import concurrent.processor.Processor;
import concurrent.writer.threadwriter.RecordWriter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

public class ExecutorQueueProcessor extends Processor {
    private final int workerCount;
    private final RecordWriter writer;
    private final BlockingQueue<FileRecord> queue;
    private final List<RecordConsumer> consumers = new ArrayList<>();

    public ExecutorQueueProcessor(int workerCount, RecordWriter writer) {
        this.workerCount = workerCount;
        this.writer = writer;
        queue = new ArrayBlockingQueue<>(1000);
    }

    @Override
    public void process(String file) {
        RecordProducer producer = new RecordProducer(queue, file);
        Thread produceThread = new Thread(producer, "producer");
        produceThread.start();

        try (ExecutorService service = Executors.newFixedThreadPool(workerCount)) {
            for (int i = 0; i < workerCount; i++) {
                RecordConsumer consumer = new RecordConsumer(queue, writer);
                consumers.add(consumer);
                service.submit(consumer);
            }

            produceThread.join();
            for (int i = 0; i < workerCount; i++) {
                queue.put(FileRecord.POISION_PILL);
            }

            service.shutdown();

            service.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);

            long totalRecords = 0;
            long totalWords = 0;
            for (RecordConsumer consumer : consumers) {
                totalRecords += consumer.getProcessCount();
                totalWords += consumer.getWordCount();
            }
            createResult(totalRecords, totalWords);

            writer.close();
        } catch (InterruptedException | IOException e) {
            throw new RuntimeException(e);
        }
    }
}
