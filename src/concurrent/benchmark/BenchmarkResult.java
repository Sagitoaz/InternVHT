package concurrent.benchmark;

import concurrent.processor.ProcessResult;

public record BenchmarkResult(ProcessResult seqProcessResult, long processTime, int threadCount, String processName) {
}
