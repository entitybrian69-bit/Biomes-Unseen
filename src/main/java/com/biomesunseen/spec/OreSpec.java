package com.biomesunseen.spec;

import com.google.gson.JsonObject;

/** One generated ore, parsed from data/biomesunseen/specs/ores.json (written by tools/gen_ores.py). */
public record OreSpec(String id, String name, String item, String itemName, int tier,
                      float hardness, int light, int xpMin, int xpMax, int dropMin, int dropMax) {

    /** Block registry name, e.g. "azurite_ore". */
    public String blockId() {
        return id + "_ore";
    }

    public static OreSpec fromJson(JsonObject o) {
        return new OreSpec(
                o.get("id").getAsString(), o.get("name").getAsString(), o.get("item").getAsString(),
                o.get("itemName").getAsString(), o.get("tier").getAsInt(), o.get("hardness").getAsFloat(),
                o.get("light").getAsInt(), o.get("xpMin").getAsInt(), o.get("xpMax").getAsInt(),
                o.get("dropMin").getAsInt(), o.get("dropMax").getAsInt());
    }
}
