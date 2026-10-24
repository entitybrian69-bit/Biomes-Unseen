package com.biomesunseen.registry;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.entity.CrystalGolemEntity;
import com.biomesunseen.entity.GloomCrawlerEntity;
import com.biomesunseen.entity.HollowStalkerEntity;
import com.biomesunseen.entity.MireWraithEntity;
import com.biomesunseen.entity.SpecMobEntity;
import com.biomesunseen.entity.SporelingEntity;
import com.biomesunseen.entity.boss.HeartOfTheForestEntity;
import com.biomesunseen.spec.MobSpec;
import com.biomesunseen.spec.Specs;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.LinkedHashMap;
import java.util.Map;

public final class ModEntities {
    public static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(ForgeRegistries.ENTITY_TYPES, BiomesUnseen.MOD_ID);

    public static final RegistryObject<EntityType<HollowStalkerEntity>> HOLLOW_STALKER =
            register("hollow_stalker", HollowStalkerEntity::new, 0.8F, 2.8F, 10);
    public static final RegistryObject<EntityType<SporelingEntity>> SPORELING =
            register("sporeling", SporelingEntity::new, 0.7F, 0.95F, 8);
    public static final RegistryObject<EntityType<GloomCrawlerEntity>> GLOOM_CRAWLER =
            register("gloom_crawler", GloomCrawlerEntity::new, 1.0F, 0.8F, 8);
    public static final RegistryObject<EntityType<CrystalGolemEntity>> CRYSTAL_GOLEM =
            register("crystal_golem", CrystalGolemEntity::new, 1.5F, 2.6F, 10);
    public static final RegistryObject<EntityType<MireWraithEntity>> MIRE_WRAITH =
            register("mire_wraith", MireWraithEntity::new, 0.7F, 2.3F, 10);
    public static final RegistryObject<EntityType<HeartOfTheForestEntity>> HEART_OF_THE_FOREST =
            register("heart_of_the_forest", HeartOfTheForestEntity::new, 2.8F, 5.0F, 16);

    /** Generated mobs from specs/mobs.json, keyed by id. */
    public static final Map<String, RegistryObject<EntityType<SpecMobEntity>>> SPEC_MOBS = new LinkedHashMap<>();

    static {
        for (MobSpec spec : Specs.mobs()) {
            SPEC_MOBS.put(spec.id(), register(spec.id(), SpecMobEntity::new, spec.width(), spec.height(), 10));
        }
    }

    private ModEntities() {
    }

    private static <T extends Entity> RegistryObject<EntityType<T>> register(
            String name, EntityType.EntityFactory<T> factory, float width, float height, int tracking) {
        return ENTITIES.register(name, () -> EntityType.Builder.of(factory, MobCategory.MONSTER)
                .sized(width, height)
                .clientTrackingRange(tracking)
                .build(new ResourceLocation(BiomesUnseen.MOD_ID, name).toString()));
    }

    public static void register(IEventBus bus) {
        ENTITIES.register(bus);
    }
}
