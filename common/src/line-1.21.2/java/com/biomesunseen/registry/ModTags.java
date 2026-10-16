package com.biomesunseen.registry;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.item.Item;
import net.minecraft.world.entity.EntityType;

/**
 * Interop tags (common "c" namespace plus mod-private tags) for wood, stone,
 * ores, plants and mobs so other mods can consume Biomes Unseen content.
 */
public final class ModTags {

    public static final TagKey<Block> ORES = TagKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath("c", "ores"));
    public static final TagKey<Block> ORES_IN_GROUND_STONE = TagKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath("c", "ores_in_ground/stone"));
    public static final TagKey<Block> ORES_IN_GROUND_DEEPSLATE = TagKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath("c", "ores_in_ground/deepslate"));
    public static final TagKey<Block> STONES = TagKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath("c", "stones"));
    public static final TagKey<Block> WOODS = TagKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath("c", "woods"));
    public static final TagKey<Block> PLANTS = TagKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath("c", "plants"));
    public static final TagKey<Block> UNSEEN_ORES = TagKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath("biomesunseen", "ores"));
    public static final TagKey<Block> UNSEEN_TERRAIN = TagKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath("biomesunseen", "terrain"));
    public static final TagKey<Block> UNSEEN_PLANTS = TagKey.create(Registries.BLOCK, ResourceLocation.fromNamespaceAndPath("biomesunseen", "plants"));

    public static final TagKey<Item> ITEM_ORES = TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath("c", "ores"));
    public static final TagKey<Item> ITEM_DUSTS = TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath("c", "dusts"));
    public static final TagKey<Item> ITEM_GEMS = TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath("c", "gems"));
    public static final TagKey<Item> ITEM_INGOTS = TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath("c", "ingots"));
    public static final TagKey<Item> UNSEEN_ITEM_ORES = TagKey.create(Registries.ITEM, ResourceLocation.fromNamespaceAndPath("biomesunseen", "ores"));

    public static final TagKey<EntityType<?>> UNSEEN_MOBS = TagKey.create(Registries.ENTITY_TYPE, ResourceLocation.fromNamespaceAndPath("biomesunseen", "mobs"));
    public static final TagKey<EntityType<?>> UNSEEN_BOSSES = TagKey.create(Registries.ENTITY_TYPE, ResourceLocation.fromNamespaceAndPath("biomesunseen", "bosses"));
    public static final TagKey<EntityType<?>> TAMEABLE = TagKey.create(Registries.ENTITY_TYPE, ResourceLocation.fromNamespaceAndPath("biomesunseen", "tameable"));
    public static final TagKey<EntityType<?>> PACK_MOBS = TagKey.create(Registries.ENTITY_TYPE, ResourceLocation.fromNamespaceAndPath("biomesunseen", "pack_mobs"));

    private ModTags() {
    }
}
