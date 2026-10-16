package com.biomesunseen.datagen;

import com.biomesunseen.core.BiomeDef;
import com.biomesunseen.core.BossDef;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.DecorDef;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.core.ModConstants;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.PlantDef;

import java.nio.file.Path;

/**
 * Generates en_us.json with display names for every biome, block, item, mob,
 * boss, sound and translation key used by the mod.
 */
public final class ModLangProvider {

    private ModLangProvider() {
    }

    public static void run(Path output) throws Exception {
        JsonWriter json = JsonWriter.obj();
        json.put("itemGroup.biomesunseen", "Biomes Unseen");
        for (BiomeDef def : Content.BIOMES) {
            json.put("biome.biomesunseen." + def.id, def.displayName);
        }
        for (OreDef def : Content.ORES) {
            json.put("block.biomesunseen." + def.id + "_ore", def.displayName + " Ore");
            json.put("item.biomesunseen." + def.id, def.displayName);
            json.put("item.biomesunseen." + def.id + "_pickaxe", def.displayName + " Pickaxe");
            json.put("item.biomesunseen." + def.id + "_sword", def.displayName + " Sword");
            json.put("item.biomesunseen." + def.id + "_helmet", def.displayName + " Helmet");
            json.put("item.biomesunseen." + def.id + "_chestplate", def.displayName + " Chestplate");
            json.put("item.biomesunseen." + def.id + "_leggings", def.displayName + " Leggings");
            json.put("item.biomesunseen." + def.id + "_boots", def.displayName + " Boots");
            json.put("item.biomesunseen." + def.id + "_tonic", def.displayName + " Tonic");
        }
        for (DecorDef def : Content.DECOR) {
            json.put("block.biomesunseen." + def.id, def.displayName);
        }
        for (PlantDef def : Content.PLANTS) {
            json.put("block.biomesunseen." + def.id, def.displayName);
        }
        for (MobDef def : Content.MOBS) {
            json.put("entity.biomesunseen." + def.id, def.displayName);
            json.put("item.biomesunseen." + def.id + "_spawn_egg", def.displayName + " Spawn Egg");
            json.put("item.biomesunseen." + def.id + "_trophy", def.displayName + " Trophy");
        }
        for (BossDef def : Content.BOSSES) {
            json.put("entity.biomesunseen." + def.id, def.displayName);
            json.put("item.biomesunseen." + def.id + "_spawn_egg", def.displayName + " Spawn Egg");
        }
        for (int tier = 1; tier <= 4; tier++) {
            json.put("item.biomesunseen.machine_core_t" + tier, "Machine Core T" + tier);
        }
        json.put("item.biomesunseen.unseen_sigil", "Unseen Sigil");
        for (int i = 0; i < Content.STRUCTURES.size(); i++) {
            json.put("structure.biomesunseen." + Content.STRUCTURES.get(i).id,
                    Content.STRUCTURES.get(i).displayName);
            json.put("book.biomesunseen." + Content.STRUCTURES.get(i).loreTheme,
                    "Journal: " + Content.STRUCTURES.get(i).loreTheme);
        }
        json.writeTo(output.resolve("assets/biomesunseen/lang/en_us.json"));
    }
}
