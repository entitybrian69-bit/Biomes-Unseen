package com.biomesunseen.spec;

import com.google.gson.JsonObject;

/** One generated mob, parsed from data/biomesunseen/specs/mobs.json (written by tools/gen_models.py). */
public record MobSpec(String id, String name, String archetype, String theme, float width, float height,
                      double health, double damage, double speed, double armor, double knockback, int xp,
                      String effect, int effectTicks, int effectAmp, int eggPrimary, int eggSecondary) {

    public static MobSpec fromJson(JsonObject o) {
        return new MobSpec(
                o.get("id").getAsString(), o.get("name").getAsString(), o.get("archetype").getAsString(),
                o.get("theme").getAsString(), o.get("width").getAsFloat(), o.get("height").getAsFloat(),
                o.get("health").getAsDouble(), o.get("damage").getAsDouble(), o.get("speed").getAsDouble(),
                o.get("armor").getAsDouble(), o.get("knockback").getAsDouble(), o.get("xp").getAsInt(),
                o.get("effect").getAsString(), o.get("effectTicks").getAsInt(), o.get("effectAmp").getAsInt(),
                o.get("eggPrimary").getAsInt(), o.get("eggSecondary").getAsInt());
    }
}
