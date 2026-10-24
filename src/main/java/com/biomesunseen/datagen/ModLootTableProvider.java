package com.biomesunseen.datagen;

import com.biomesunseen.registry.ModBlocks;
import com.biomesunseen.registry.ModEntities;
import com.biomesunseen.registry.ModItems;
import com.biomesunseen.spec.OreSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.data.PackOutput;
import net.minecraft.data.loot.BlockLootSubProvider;
import net.minecraft.data.loot.EntityLootSubProvider;
import net.minecraft.data.loot.LootTableProvider;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.flag.FeatureFlags;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.enchantment.Enchantments;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.storage.loot.LootPool;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.level.storage.loot.entries.LootItem;
import net.minecraft.world.level.storage.loot.functions.ApplyBonusCount;
import net.minecraft.world.level.storage.loot.functions.LootingEnchantFunction;
import net.minecraft.world.level.storage.loot.functions.SetItemCountFunction;
import net.minecraft.world.level.storage.loot.parameters.LootContextParamSets;
import net.minecraft.world.level.storage.loot.providers.number.ConstantValue;
import net.minecraft.world.level.storage.loot.providers.number.UniformGenerator;
import net.minecraftforge.registries.RegistryObject;

import java.util.List;
import java.util.Set;
import java.util.stream.Stream;

/** Block and mob loot. The boss table is hand-written JSON (lore book) and is not generated here. */
public final class ModLootTableProvider {
    private ModLootTableProvider() {
    }

    public static LootTableProvider create(PackOutput output) {
        return new LootTableProvider(output, Set.of(), List.of(
                new LootTableProvider.SubProviderEntry(BlockLoot::new, LootContextParamSets.BLOCK),
                new LootTableProvider.SubProviderEntry(EntityLoot::new, LootContextParamSets.ENTITY)));
    }

    public static class BlockLoot extends BlockLootSubProvider {
        public BlockLoot() {
            super(Set.of(), FeatureFlags.REGISTRY.allFlags());
        }

        @Override
        protected void generate() {
            add(ModBlocks.HOLLOWITE_ORE.get(),
                    block -> createOreDrop(block, ModItems.HOLLOWITE_INGOT.get()));
            for (OreSpec spec : Specs.ores()) {
                Item drop = ModItems.ORE_ITEMS.get(spec.id()).get();
                add(ModBlocks.ORES.get(spec.id()).get(), block -> createSilkTouchDispatchTable(block,
                        applyExplosionDecay(block, LootItem.lootTableItem(drop)
                                .apply(SetItemCountFunction.setCount(
                                        UniformGenerator.between(spec.dropMin(), spec.dropMax())))
                                .apply(ApplyBonusCount.addOreBonusCount(Enchantments.BLOCK_FORTUNE)))));
            }
        }

        @Override
        protected Iterable<Block> getKnownBlocks() {
            return ModBlocks.BLOCKS.getEntries().stream().map(RegistryObject::get)::iterator;
        }
    }

    public static class EntityLoot extends EntityLootSubProvider {
        public EntityLoot() {
            super(FeatureFlags.REGISTRY.allFlags());
        }

        @Override
        public void generate() {
            drop(ModEntities.HOLLOW_STALKER.get(), Items.BONE, 0, 2);
            drop(ModEntities.SPORELING.get(), Items.BROWN_MUSHROOM, 0, 2);
            drop(ModEntities.GLOOM_CRAWLER.get(), Items.STRING, 0, 2);
            drop(ModEntities.CRYSTAL_GOLEM.get(), Items.AMETHYST_SHARD, 1, 4);
            drop(ModEntities.MIRE_WRAITH.get(), Items.SLIME_BALL, 0, 2);
        }

        private void drop(EntityType<?> type, Item item, float min, float max) {
            add(type, LootTable.lootTable()
                    .withPool(LootPool.lootPool().setRolls(ConstantValue.exactly(1.0F))
                            .add(LootItem.lootTableItem(item)
                                    .apply(SetItemCountFunction.setCount(UniformGenerator.between(min, max)))
                                    .apply(LootingEnchantFunction.lootingMultiplier(UniformGenerator.between(0.0F, 1.0F)))))
                    .withPool(LootPool.lootPool().setRolls(ConstantValue.exactly(1.0F))
                            .add(LootItem.lootTableItem(ModItems.HOLLOWITE_INGOT.get())
                                    .apply(SetItemCountFunction.setCount(UniformGenerator.between(0.0F, 1.0F))))));
        }

        // VERIFY: getKnownEntityTypes signature in Forge 47.x EntityLootSubProvider.
        @Override
        protected Stream<EntityType<?>> getKnownEntityTypes() {
            return Stream.<EntityType<?>>of(ModEntities.HOLLOW_STALKER.get(), ModEntities.SPORELING.get(),
                    ModEntities.GLOOM_CRAWLER.get(), ModEntities.CRYSTAL_GOLEM.get(),
                    ModEntities.MIRE_WRAITH.get());
        }
    }
}
