package com.biomesunseen.datagen;

import java.io.IOException;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Minimal JSON document builder used by the data generators.  Produces
 * stable, human-readable JSON without external dependencies so datagen runs
 * on every supported Minecraft line.
 */
public final class JsonWriter {

    private final Map<String, Object> values = new LinkedHashMap<String, Object>();

    public static JsonWriter obj() {
        return new JsonWriter();
    }

    public JsonWriter put(String key, String value) {
        values.put(key, value);
        return this;
    }

    public JsonWriter put(String key, double value) {
        values.put(key, Double.valueOf(value));
        return this;
    }

    public JsonWriter put(String key, boolean value) {
        values.put(key, Boolean.valueOf(value));
        return this;
    }

    public JsonWriter put(String key, JsonWriter child) {
        values.put(key, child);
        return this;
    }

    public JsonWriter putArray(String key, String... entries) {
        values.put(key, new java.util.ArrayList<String>(java.util.Arrays.asList(entries)));
        return this;
    }

    public JsonWriter putRawArray(String key, JsonWriter... entries) {
        values.put(key, new java.util.ArrayList<JsonWriter>(java.util.Arrays.asList(entries)));
        return this;
    }

    public JsonWriter putIntArray(String key, int... entries) {
        java.util.List<Integer> list = new java.util.ArrayList<Integer>();
        for (int v : entries) {
            list.add(Integer.valueOf(v));
        }
        values.put(key, list);
        return this;
    }

    /** Render as pretty JSON text. */
    public String render() {
        StringBuilder sb = new StringBuilder();
        renderInto(sb, 0);
        return sb.toString();
    }

    private void renderInto(StringBuilder sb, int indent) {
        sb.append("{\n");
        int i = 0;
        for (Map.Entry<String, Object> entry : values.entrySet()) {
            pad(sb, indent + 2);
            sb.append('"').append(escape(entry.getKey())).append("\": ");
            renderValue(sb, entry.getValue(), indent + 2);
            if (++i < values.size()) {
                sb.append(',');
            }
            sb.append('\n');
        }
        pad(sb, indent);
        sb.append('}');
    }

    private void renderValue(StringBuilder sb, Object value, int indent) {
        if (value instanceof JsonWriter) {
            ((JsonWriter) value).renderInto(sb, indent);
        } else if (value instanceof String) {
            sb.append('"').append(escape((String) value)).append('"');
        } else if (value instanceof Boolean || value instanceof Integer
                || value instanceof Long || value instanceof Double) {
            sb.append(value.toString());
        } else if (value instanceof java.util.List) {
            sb.append('[');
            java.util.List<?> list = (java.util.List<?>) value;
            for (int i = 0; i < list.size(); i++) {
                renderValue(sb, list.get(i), indent);
                if (i + 1 < list.size()) {
                    sb.append(", ");
                }
            }
            sb.append(']');
        } else {
            sb.append('"').append(escape(String.valueOf(value))).append('"');
        }
    }

    private static void pad(StringBuilder sb, int indent) {
        for (int i = 0; i < indent; i++) {
            sb.append(' ');
        }
    }

    private static String escape(String text) {
        return text.replace("\\", "\\\\").replace("\"", "\\\"");
    }

    /** Write this document to a file, creating parent directories. */
    public void writeTo(Path file) throws IOException {
        Path parent = file.getParent();
        if (parent != null) {
            Files.createDirectories(parent);
        }
        try (Writer writer = Files.newBufferedWriter(file, StandardCharsets.UTF_8)) {
            writer.write(render());
            writer.write('\n');
        }
    }
}
