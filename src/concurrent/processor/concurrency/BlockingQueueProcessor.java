package concurrent.processor.concurrency;

import concurrent.model.consumer.RecordConsumer;
import concurrent.model.FileRecord;
import concurrent.model.producer.RecordProducer;
import concurrent.processor.Processor;
import concurrent.writer.threadwriter.RecordWriter;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class BlockingQueueProcessor extends Processor {
    private final int workerCount;
    private final BlockingQueue<FileRecord> queue;
    private final RecordWriter writer;
    private List<RecordConsumer> consumers = new ArrayList<>();
    private List<Thread> consumerThreads = new ArrayList<>();

    public BlockingQueueProcessor(int workerCount, RecordWriter writer) {
        this.workerCount = workerCount;
        this.writer = writer;
        this.queue = new ArrayBlockingQueue<>(1000);
    }

    @Override
    public void process(String file) {
        RecordProducer producer = new RecordProducer(queue, file);
        Thread produceThread = new Thread(producer, "producer");
        produceThread.start();


        for (int i = 0; i < workerCount; i++) {
            RecordConsumer consumer = new RecordConsumer(queue, writer);
            consumers.add(consumer);
            Thread consumeThread = new Thread(consumer, "consumer-" + (i + 1));
            consumerThreads.add(consumeThread);
        }

        for (Thread consumer : consumerThreads) {
            consumer.start();
        }

        try {
            produceThread.join();
            for (int i = 0; i < workerCount; i++) {
                queue.put(FileRecord.POISION_PILL);
            }

            for (Thread consumer : consumerThreads) {
                consumer.join();
            }

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
