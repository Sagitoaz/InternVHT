package concurrent.processor.buffer;

import concurrent.counter.HashMapCounter;
import concurrent.processor.Processor;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class SeqBufProcessor extends Processor {
    private final HashMapCounter counter;

    public SeqBufProcessor() {
        this.counter = new HashMapCounter();
    }

    @Override
    public void process(String file) {
        try {
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line;
            while ((line = reader.readLine()) != null) {
                String[] words = line.split("\\s+");
                for (String word : words) {
                    counter.increase(word);
                }
                createResult(words.length, 1);
            }
            reader.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
