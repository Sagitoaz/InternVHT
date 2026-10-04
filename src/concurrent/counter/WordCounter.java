package concurrent.counter;

import java.util.Map;

public interface WordCounter {
    public void increase(String word);
    public Map<String, Long> getCount();
}
