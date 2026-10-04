package concurrent.processor.buffer;

import concurrent.counter.HashMapCounter;
import concurrent.processor.Processor;

import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;

public class SeqUnbufProcessor extends Processor {
    private final HashMapCounter counter;

    public SeqUnbufProcessor() {
        this.counter = new HashMapCounter();
    }

    @Override
    public void process(String file) {
        try {
            Reader reader = new FileReader(file);
            StringBuilder line = new StringBuilder();
            int data;
            while ((data = reader.read()) != -1) {
                char c = (char) data;
                if (c == '\n') {
                    processLine(line);
                    line = new StringBuilder();
                } else {
                    line.append(c);
                }
            }
            if (!line.isEmpty()) {
                processLine(line);
            }
            reader.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private void processLine(StringBuilder line) {
        String[] words = line.toString().split("\\s+");
        createResult(words.length, 1);
        for (String word : words) {
            counter.increase(word);
        }
    }
}
