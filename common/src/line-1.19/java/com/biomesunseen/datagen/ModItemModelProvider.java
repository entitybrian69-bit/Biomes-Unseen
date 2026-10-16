package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.core.OreDef;

import java.nio.file.Path;

/**
 * Generates item models for minerals, gear, tonics, spawn eggs, trophies,
 * lore books, machine cores and the sigil.
 */
public final class ModItemModelProvider {

    private ModItemModelProvider() {
    }

    public static void run(Path output) throws Exception {
        Path models = output.resolve("assets/biomesunseen/models/item");
        for (OreDef ore : Content.ORES) {
            flat(models, ore.id, "biomesunseen:item/" + ore.id);
            flat(models, ore.id + "_pickaxe", "biomesunseen:item/" + ore.id + "_pickaxe");
            flat(models, ore.id + "_sword", "biomesunseen:item/" + ore.id + "_sword");
            flat(models, ore.id + "_helmet", "biomesunseen:item/" + ore.id + "_helmet");
            flat(models, ore.id + "_chestplate", "biomesunseen:item/" + ore.id + "_chestplate");
            flat(models, ore.id + "_leggings", "biomesunseen:item/" + ore.id + "_leggings");
            flat(models, ore.id + "_boots", "biomesunseen:item/" + ore.id + "_boots");
            flat(models, ore.id + "_tonic", "biomesunseen:item/" + ore.id + "_tonic");
        }
        for (MobDef mob : Content.MOBS) {
            flat(models, mob.id + "_spawn_egg", "minecraft:item/template_spawn_egg");
            flat(models, mob.id + "_trophy", "biomesunseen:item/" + mob.id + "_trophy");
        }
        for (int i = 0; i < Content.BOSSES.size(); i++) {
            flat(models, Content.BOSSES.get(i).id + "_spawn_egg", "minecraft:item/template_spawn_egg");
        }
        for (int tier = 1; tier <= 4; tier++) {
            flat(models, "machine_core_t" + tier, "biomesunseen:item/machine_core_t" + tier);
        }
        flat(models, "unseen_sigil", "biomesunseen:item/unseen_sigil");
        java.util.LinkedHashSet<String> themes = new java.util.LinkedHashSet<String>();
        for (int i = 0; i < Content.STRUCTURES.size(); i++) {
            themes.add(Content.STRUCTURES.get(i).loreTheme);
        }
        for (String theme : themes) {
            flat(models, "lore_journal_" + theme, "biomesunseen:item/lore_journal_" + theme);
        }
    }

    private static void flat(Path models, String id, String texture) throws Exception {
        JsonWriter.obj()
                .put("parent", "minecraft:item/generated")
                .put("textures", JsonWriter.obj().put("layer0", texture))
                .writeTo(models.resolve(id + ".json"));
    }
}
