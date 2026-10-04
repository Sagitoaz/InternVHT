package concurrent.writer;

import concurrent.benchmark.BenchmarkResult;

public interface ResultWriter {
    public void write(BenchmarkResult result, String message);
    public default void write(BenchmarkResult result) {
        write(result, null);
    }
}
