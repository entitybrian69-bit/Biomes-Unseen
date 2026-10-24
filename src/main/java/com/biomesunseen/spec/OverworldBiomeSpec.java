package com.biomesunseen.spec;

import com.google.gson.JsonObject;

/**
 * One generated Overworld biome from data/biomesunseen/specs/overworld.json (tools/gen_biomes.py).
 * t, h and l are climate band indices (temperature 0-4, humidity 0-4, land shape 0-3).
 */
public record OverworldBiomeSpec(String id, String name, String group, int t, int h, int l,
                                 String top, String under) {

    public static OverworldBiomeSpec fromJson(JsonObject o) {
        return new OverworldBiomeSpec(
                o.get("id").getAsString(), o.get("name").getAsString(), o.get("group").getAsString(),
                o.get("t").getAsInt(), o.get("h").getAsInt(), o.get("l").getAsInt(),
                o.get("top").getAsString(), o.get("under").getAsString());
    }
}
