package concurrent.processor;

public abstract class Processor {
    private long wordCount;
    private long lineCount;
    protected ProcessResult result;
    public abstract void process(String file);
    public ProcessResult getResult() {
        return result;
    }
    protected void createResult(long wordIncreasement, long lineIncreasement) {
        wordCount += wordIncreasement;
        lineCount += lineIncreasement;
        this.result = new ProcessResult(lineCount, wordCount);
    }
}
