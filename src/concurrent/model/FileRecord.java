package concurrent.model;

public record FileRecord(long id, String originalText) {
    public static final FileRecord POISION_PILL = new FileRecord(-1, "");

    @Override
    public String toString() {
        return "FileRecord {\n" +
                "id: " + id + ",\n" +
                "text: " + originalText + "\n"
                + "}\n";
    }
}
