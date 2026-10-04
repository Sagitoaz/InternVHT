package concurrent;

import concurrent.benchmark.BenchmarkResult;
import concurrent.benchmark.Runner;
import concurrent.cli.CliArgs;
import concurrent.cli.ProcessMode;
import concurrent.cli.WriteMode;
import concurrent.generator.LargeFileGenerator;
import concurrent.processor.Processor;
import concurrent.writer.BufferedResultWriter;
import concurrent.writer.ResultWriter;
import concurrent.writer.threadwriter.RecordWriter;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public class Main {
    public static void genFile() throws IOException {
        //gen small.txt file with 200MB size, test.txt file with 1GB size
        Path out = Path.of("small.txt");
        List<String> words = List.of("java",
                "spring",
                "kafka",
                "redis",
                "thread",
                "executor",
                "lock",
                "concurrent",
                "database",
                "socket"
        );
        LargeFileGenerator generator = new LargeFileGenerator(words);
        generator.genFile(out,  200 * 1024 * 1024);
    }

    public static void main(String[] args) throws IOException {
//        genFile();

        CliArgs config = CliArgs.parse(args);

        WriteMode writeMode = config.getWriteMode();
        ProcessMode processMode = config.getProcessMode();
        int threadCount = config.getThreadCount();

        RecordWriter writer = writeMode.createWriter(config.getOut());
        Processor processor = processMode.createProcess(threadCount, writer);

        Runner runner = new Runner(threadCount, processMode.getProcessName());
        runner.run(processor, config.getFile());
        BenchmarkResult result = runner.getResult();

        ResultWriter resWriter = new BufferedResultWriter("results.txt");
        resWriter.write(result);

        System.out.println(result);
    }
}
