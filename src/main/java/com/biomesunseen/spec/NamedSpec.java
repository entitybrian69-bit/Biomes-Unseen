package com.biomesunseen.spec;

import com.google.gson.JsonObject;

/** An id with a display name, used for the Hollow Deep biome list (specs/dimension_biomes.json). */
public record NamedSpec(String id, String name) {

    public static NamedSpec fromJson(JsonObject o) {
        return new NamedSpec(o.get("id").getAsString(), o.get("name").getAsString());
    }
}
