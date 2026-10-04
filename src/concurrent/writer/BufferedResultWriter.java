package concurrent.writer;

import concurrent.benchmark.BenchmarkResult;
import concurrent.util.WriteHelper;

import java.io.*;

public class BufferedResultWriter implements ResultWriter{
    private final String out;

    public BufferedResultWriter(String out) {
        this.out = out;
    }

    @Override
    public void write(BenchmarkResult result, String message) {
        try {
            Writer writer = new BufferedWriter(new FileWriter(out, true));
            WriteHelper.formatWrite(writer, result, "   - Method: BufferedWriter\n");
            writer.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
