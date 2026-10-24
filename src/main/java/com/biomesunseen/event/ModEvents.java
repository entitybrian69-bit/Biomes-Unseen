package com.biomesunseen.event;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.entity.CrystalGolemEntity;
import com.biomesunseen.entity.GloomCrawlerEntity;
import com.biomesunseen.entity.HollowStalkerEntity;
import com.biomesunseen.entity.MireWraithEntity;
import com.biomesunseen.entity.SporelingEntity;
import com.biomesunseen.entity.boss.HeartOfTheForestEntity;
import com.biomesunseen.registry.ModEntities;
import com.biomesunseen.entity.SpecMobEntity;
import com.biomesunseen.spec.MobSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.world.entity.SpawnPlacements;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraftforge.event.entity.EntityAttributeCreationEvent;
import net.minecraftforge.event.entity.SpawnPlacementRegisterEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = BiomesUnseen.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public final class ModEvents {
    private ModEvents() {
    }

    @SubscribeEvent
    public static void registerAttributes(EntityAttributeCreationEvent event) {
        event.put(ModEntities.HOLLOW_STALKER.get(), HollowStalkerEntity.createAttributes().build());
        event.put(ModEntities.SPORELING.get(), SporelingEntity.createAttributes().build());
        event.put(ModEntities.GLOOM_CRAWLER.get(), GloomCrawlerEntity.createAttributes().build());
        event.put(ModEntities.CRYSTAL_GOLEM.get(), CrystalGolemEntity.createAttributes().build());
        event.put(ModEntities.MIRE_WRAITH.get(), MireWraithEntity.createAttributes().build());
        event.put(ModEntities.HEART_OF_THE_FOREST.get(), HeartOfTheForestEntity.createAttributes().build());
        for (MobSpec spec : Specs.mobs()) {
            event.put(ModEntities.SPEC_MOBS.get(spec.id()).get(), SpecMobEntity.attributes(spec).build());
        }
    }

    @SubscribeEvent
    public static void registerSpawnPlacements(SpawnPlacementRegisterEvent event) {
        place(event, ModEntities.HOLLOW_STALKER.get());
        place(event, ModEntities.SPORELING.get());
        place(event, ModEntities.GLOOM_CRAWLER.get());
        place(event, ModEntities.CRYSTAL_GOLEM.get());
        place(event, ModEntities.MIRE_WRAITH.get());
        for (MobSpec spec : Specs.mobs()) {
            place(event, ModEntities.SPEC_MOBS.get(spec.id()).get());
        }
    }

    private static <T extends Monster> void place(SpawnPlacementRegisterEvent event,
                                                  net.minecraft.world.entity.EntityType<T> type) {
        event.register(type, SpawnPlacements.Type.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                Monster::checkMonsterSpawnRules, SpawnPlacementRegisterEvent.Operation.REPLACE);
    }
}
