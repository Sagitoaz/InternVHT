package concurrent.model;

public record ProcessedRecord(
        long id,
        String originalText,
        String modifiedText,
        int wordCount,
        String processedBy,
        boolean virtualThread
) {}