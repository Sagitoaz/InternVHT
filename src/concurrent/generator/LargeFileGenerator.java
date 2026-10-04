package concurrent.generator;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Random;

public class LargeFileGenerator {
    private final List<String> words;
    private final Random rand;

    public LargeFileGenerator(List<String> words) {
        this.words = words;
        this.rand = new Random();
    }

    public void genFile(Path out, long size) throws IOException {
        long countBytes = 0;

        try (BufferedWriter writer = Files.newBufferedWriter(out)) {
            long nextReport = 500L * 1024 * 1024;

            while (countBytes < size) {
                String line = genLine();
                writer.write(line);
                writer.newLine();

                countBytes += line.getBytes(StandardCharsets.UTF_8).length + 1;

                if (countBytes >= nextReport) {
                    System.out.printf("Current size: %.2f GB\n", countBytes / (1024.0 * 1024 * 1024));
                    nextReport += 500L * 1024 * 1024;
                }
            }
        }
        System.out.println("Finished!!!");
    }

    private String genLine() {
        StringBuilder sb = new StringBuilder();
        int wordCount = rand.nextInt(10, 20);
        for (int i = 0; i < wordCount; i++) {
            sb.append(words.get(rand.nextInt(words.size()))).append(" ");
        }
        return sb.toString();
    }
}
