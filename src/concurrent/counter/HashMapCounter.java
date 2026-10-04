package concurrent.counter;

import java.util.HashMap;
import java.util.Map;

public class HashMapCounter implements WordCounter{
    private final Map<String, Long> counter = new HashMap<>();

    @Override
    public void increase(String word) {
        counter.merge(word, 1L, Long::sum);
    }

    @Override
    public Map<String, Long> getCount() {
        return this.counter;
    }
}
