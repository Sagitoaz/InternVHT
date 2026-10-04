package concurrent.benchmark;

import concurrent.processor.Processor;

import java.nio.file.Path;

public class Runner {
    private  BenchmarkResult result;
    private final int threadCount;
    private final String processName;

    public Runner(int threadCount, String processName) {
        this.threadCount = threadCount;
        this.processName = processName;
    }

    public void run(Processor processor, String file) {
        long start = System.nanoTime();
        processor.process(file);
        long end = System.nanoTime();
        result = new BenchmarkResult(processor.getResult(), (end - start), threadCount, processName);
    }

    public BenchmarkResult getResult() {
        return result;
    }
}
