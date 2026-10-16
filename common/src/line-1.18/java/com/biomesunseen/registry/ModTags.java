package com.biomesunseen.registry;

import net.minecraft.core.Registry;
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

    public static final TagKey<Block> ORES = TagKey.create(Registry.BLOCK_REGISTRY, new ResourceLocation("c", "ores"));
    public static final TagKey<Block> ORES_IN_GROUND_STONE = TagKey.create(Registry.BLOCK_REGISTRY, new ResourceLocation("c", "ores_in_ground/stone"));
    public static final TagKey<Block> ORES_IN_GROUND_DEEPSLATE = TagKey.create(Registry.BLOCK_REGISTRY, new ResourceLocation("c", "ores_in_ground/deepslate"));
    public static final TagKey<Block> STONES = TagKey.create(Registry.BLOCK_REGISTRY, new ResourceLocation("c", "stones"));
    public static final TagKey<Block> WOODS = TagKey.create(Registry.BLOCK_REGISTRY, new ResourceLocation("c", "woods"));
    public static final TagKey<Block> PLANTS = TagKey.create(Registry.BLOCK_REGISTRY, new ResourceLocation("c", "plants"));
    public static final TagKey<Block> UNSEEN_ORES = TagKey.create(Registry.BLOCK_REGISTRY, new ResourceLocation("biomesunseen", "ores"));
    public static final TagKey<Block> UNSEEN_TERRAIN = TagKey.create(Registry.BLOCK_REGISTRY, new ResourceLocation("biomesunseen", "terrain"));
    public static final TagKey<Block> UNSEEN_PLANTS = TagKey.create(Registry.BLOCK_REGISTRY, new ResourceLocation("biomesunseen", "plants"));

    public static final TagKey<Item> ITEM_ORES = TagKey.create(Registry.ITEM_REGISTRY, new ResourceLocation("c", "ores"));
    public static final TagKey<Item> ITEM_DUSTS = TagKey.create(Registry.ITEM_REGISTRY, new ResourceLocation("c", "dusts"));
    public static final TagKey<Item> ITEM_GEMS = TagKey.create(Registry.ITEM_REGISTRY, new ResourceLocation("c", "gems"));
    public static final TagKey<Item> ITEM_INGOTS = TagKey.create(Registry.ITEM_REGISTRY, new ResourceLocation("c", "ingots"));
    public static final TagKey<Item> UNSEEN_ITEM_ORES = TagKey.create(Registry.ITEM_REGISTRY, new ResourceLocation("biomesunseen", "ores"));

    public static final TagKey<EntityType<?>> UNSEEN_MOBS = TagKey.create(Registry.ENTITY_TYPE_REGISTRY, new ResourceLocation("biomesunseen", "mobs"));
    public static final TagKey<EntityType<?>> UNSEEN_BOSSES = TagKey.create(Registry.ENTITY_TYPE_REGISTRY, new ResourceLocation("biomesunseen", "bosses"));
    public static final TagKey<EntityType<?>> TAMEABLE = TagKey.create(Registry.ENTITY_TYPE_REGISTRY, new ResourceLocation("biomesunseen", "tameable"));
    public static final TagKey<EntityType<?>> PACK_MOBS = TagKey.create(Registry.ENTITY_TYPE_REGISTRY, new ResourceLocation("biomesunseen", "pack_mobs"));

    private ModTags() {
    }
}
