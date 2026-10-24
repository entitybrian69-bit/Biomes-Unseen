package com.biomesunseen.datagen;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.registry.ModItems;
import com.biomesunseen.spec.OreSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.data.PackOutput;
import net.minecraftforge.client.model.generators.ItemModelProvider;
import net.minecraftforge.common.data.ExistingFileHelper;
import net.minecraftforge.registries.RegistryObject;
import net.minecraft.world.item.Item;

import java.util.List;

public class ModItemModelProvider extends ItemModelProvider {
    public ModItemModelProvider(PackOutput output, ExistingFileHelper helper) {
        super(output, BiomesUnseen.MOD_ID, helper);
    }

    @Override
    protected void registerModels() {
        // Requires textures/item/hollowite_ingot.png (tools/gen_textures.py) to exist.
        withExistingParent("hollowite_ingot", mcLoc("item/generated"))
                .texture("layer0", modLoc("item/hollowite_ingot"));

        List<RegistryObject<Item>> eggs = List.of(
                ModItems.HOLLOW_STALKER_SPAWN_EGG, ModItems.SPORELING_SPAWN_EGG,
                ModItems.GLOOM_CRAWLER_SPAWN_EGG, ModItems.CRYSTAL_GOLEM_SPAWN_EGG,
                ModItems.MIRE_WRAITH_SPAWN_EGG, ModItems.HEART_OF_THE_FOREST_SPAWN_EGG);
        for (RegistryObject<Item> egg : eggs) {
            withExistingParent(egg.getId().getPath(), mcLoc("item/template_spawn_egg"));
        }
        for (RegistryObject<Item> egg : ModItems.SPEC_EGGS.values()) {
            withExistingParent(egg.getId().getPath(), mcLoc("item/template_spawn_egg"));
        }
        for (OreSpec spec : Specs.ores()) {
            withExistingParent(spec.item(), mcLoc("item/generated"))
                    .texture("layer0", modLoc("item/" + spec.item()));
        }
    }
}
