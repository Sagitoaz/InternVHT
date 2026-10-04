package concurrent.util;

import concurrent.benchmark.BenchmarkResult;
import concurrent.model.ProcessedRecord;

import java.io.IOException;
import java.io.Writer;
import java.time.LocalDateTime;

public class WriteHelper {
    public static void formatWrite(Writer writer, BenchmarkResult result, String message) {
        try {
            StringBuilder sb = new StringBuilder();
            sb.append("APPEND TIME ").append(LocalDateTime.now()).append("\n");
            sb.append("Thread count: ").append(result.threadCount()).append("\n");
            sb.append("Process name: ").append(result.processName()).append("\n");
            if (message != null) {
                sb.append("MESSAGE: \n").append(message);
            }
            if (result.seqProcessResult() != null) {
                sb.append("Word count: ").append(result.seqProcessResult().wordCount()).append("\n");
                sb.append("Line count: ").append(result.seqProcessResult().lineCount()).append("\n");
            }
            sb.append("Time process (ns): ").append(result.processTime()).append("\n");
            sb.append("Time process (ms): ").append(result.processTime() / 1000000.0).append("\n");
            sb.append("Time process (s): ").append(result.processTime() / 1000000000.0).append("\n");
            sb.append("----------------------------------\n");
            writer.write(sb.toString());
            writer.flush();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static void formatWrite(Writer writer, ProcessedRecord record) throws IOException {
        writer.write("FileRecord {\n");
        writer.write("   id: " + record.id() + ",\n");
        writer.write("   original: " + record.originalText() + ",\n");
        writer.write("   modified: " + record.modifiedText() + ",\n");
        writer.write("   wordCount: " + record.wordCount() + ",\n");
        writer.write("   processedBy: " + record.processedBy() + ",\n");
        writer.write("   virtualThread: " + record.virtualThread() + "\n");
        writer.write("}\n");
    }
}
