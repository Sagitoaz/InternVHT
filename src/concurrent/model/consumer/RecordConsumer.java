package concurrent.model.consumer;

import concurrent.model.FileRecord;
import concurrent.model.ProcessedRecord;
import concurrent.writer.threadwriter.RecordWriter;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.concurrent.BlockingQueue;

public class RecordConsumer implements Runnable {
    private final BlockingQueue<FileRecord> queue;
    private final RecordWriter writer;

    private long wordCount = 0;
    private long processCount = 0;

    public RecordConsumer(BlockingQueue<FileRecord> queue, RecordWriter writer) {
        this.queue = queue;
        this.writer = writer;
    }

    @Override
    public void run() {
        try {
            while (true) {
                FileRecord fileRecord = queue.take();
                if (fileRecord.id() == -1) break;
                ProcessedRecord processedRecord = process(fileRecord);
                processCount++;
                wordCount += processedRecord.wordCount();
                writer.write(processedRecord);
            }
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    private ProcessedRecord process(FileRecord fileRecord) {
        String text = fileRecord.originalText();
        String modifiedText = text.toUpperCase();
        int wordCount = text.split("\\s+").length;
        Thread currentThread = Thread.currentThread();
        return new ProcessedRecord(
                fileRecord.id(),
                text,
                modifiedText,
                wordCount,
                currentThread.getName(),
                currentThread.isVirtual()
        );
    }

    public long getProcessCount() {
        return processCount;
    }

    public long getWordCount() {
        return wordCount;
    }
}
