package concurrent.model.producer;

import concurrent.model.FileRecord;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.concurrent.BlockingQueue;

public class RecordProducer implements Runnable{
    private final BlockingQueue<FileRecord> queue;
    private final String file;

    public RecordProducer(BlockingQueue<FileRecord> queue, String file) {
        this.queue = queue;
        this.file = file;
    }

    @Override
    public void run() {
        try {
            BufferedReader in = new BufferedReader(new FileReader(file));
            String line;
            long id = 1;
            while ((line = in.readLine()) != null) {
                FileRecord fileRecord = new FileRecord(id++, line);
                queue.put(fileRecord);
            }
            in.close();
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}
