package com.biomesunseen.datagen;

import com.biomesunseen.core.Content;
import com.biomesunseen.core.MobDef;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.PlantDef;

import java.nio.file.Path;

/**
 * Generates block, item and entity tags in the "c" common namespace and the
 * "biomesunseen" namespace for full interop with other mods.
 */
public final class ModTagsProvider {

    private ModTagsProvider() {
    }

    public static void run(Path output) throws Exception {
        Path blockTags = output.resolve("data/c/tags/block");
        Path itemTags = output.resolve("data/c/tags/item");
        Path ownBlockTags = output.resolve("data/biomesunseen/tags/block");
        Path ownItemTags = output.resolve("data/biomesunseen/tags/item");
        Path entityTags = output.resolve("data/biomesunseen/tags/entity_type");

        JsonWriter ores = JsonWriter.obj().put("replace", false);
        JsonWriter ownOres = JsonWriter.obj().put("replace", false);
        JsonWriter values = JsonWriter.obj();
        String[] oreValues = new String[Content.ORES.size()];
        String[] stoneValues = new String[Content.ORES.size()];
        int n = 0;
        for (OreDef ore : Content.ORES) {
            oreValues[n] = "biomesunseen:" + ore.id + "_ore";
            stoneValues[n] = "biomesunseen:" + ore.id + "_ore";
            n++;
        }
        ores.putArray("values", oreValues);
        ownOres.putArray("values", oreValues);
        ores.writeTo(blockTags.resolve("ores.json"));
        ores.writeTo(itemTags.resolve("ores.json"));
        ownOres.writeTo(ownBlockTags.resolve("ores.json"));

        String[] plantValues = new String[Content.PLANTS.size()];
        int p = 0;
        for (PlantDef plant : Content.PLANTS) {
            plantValues[p++] = "biomesunseen:" + plant.id;
        }
        JsonWriter.obj().put("replace", false).putArray("values", plantValues)
                .writeTo(ownBlockTags.resolve("plants.json"));

        String[] mobValues = new String[Content.MOBS.size()];
        int m = 0;
        for (MobDef mob : Content.MOBS) {
            mobValues[m++] = "biomesunseen:" + mob.id;
        }
        JsonWriter.obj().put("replace", false).putArray("values", mobValues)
                .writeTo(entityTags.resolve("mobs.json"));

        String[] bossValues = new String[Content.BOSSES.size()];
        for (int i = 0; i < Content.BOSSES.size(); i++) {
            bossValues[i] = "biomesunseen:" + Content.BOSSES.get(i).id;
        }
        JsonWriter.obj().put("replace", false).putArray("values", bossValues)
                .writeTo(entityTags.resolve("bosses.json"));

        String[] tameable = new String[]{};
        java.util.List<String> tameList = new java.util.ArrayList<String>();
        java.util.List<String> packList = new java.util.ArrayList<String>();
        for (MobDef mob : Content.MOBS) {
            if (mob.tameable) {
                tameList.add("biomesunseen:" + mob.id);
            }
            if (mob.pack) {
                packList.add("biomesunseen:" + mob.id);
            }
        }
        JsonWriter.obj().put("replace", false)
                .putArray("values", tameList.toArray(new String[0]))
                .writeTo(entityTags.resolve("tameable.json"));
        JsonWriter.obj().put("replace", false)
                .putArray("values", packList.toArray(new String[0]))
                .writeTo(entityTags.resolve("pack_mobs.json"));
    }
}
