package com.biomesunseen.registry;

import net.minecraft.entity.EntityType;
import net.minecraft.entity.EntityClassification;
import net.minecraft.entity.ai.attributes.Attributes;
import net.minecraft.entity.MobEntity;

import com.biomesunseen.entity.boss.HeartOfTheForestEntity;
import com.biomesunseen.entity.boss.VoidSerpentEntity;
import com.biomesunseen.entity.mobs.*;

import me.shedaniel.architectury.registry.EntityAttributeRegistry;
import me.shedaniel.architectury.registry.RegistrySupplier;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * All 25 mobs and 2 bosses with their spawn attributes.
 * Spawn eggs are created in ModItems after these types exist.
 */
public final class ModEntities {

    public static RegistrySupplier<EntityType<LumoxEntity>> Lumox;
    public static RegistrySupplier<EntityType<BramblebackEntity>> Brambleback;
    public static RegistrySupplier<EntityType<SiltstriderEntity>> Siltstrider;
    public static RegistrySupplier<EntityType<GlimmermothEntity>> Glimmermoth;
    public static RegistrySupplier<EntityType<PeatHopperEntity>> PeatHopper;
    public static RegistrySupplier<EntityType<EmberCalfEntity>> EmberCalf;
    public static RegistrySupplier<EntityType<FrostFawnEntity>> FrostFawn;
    public static RegistrySupplier<EntityType<MurklingEntity>> Murkling;
    public static RegistrySupplier<EntityType<SporeSproutEntity>> SporeSprout;
    public static RegistrySupplier<EntityType<SkywispEntity>> Skywisp;
    public static RegistrySupplier<EntityType<ThunderRamEntity>> ThunderRam;
    public static RegistrySupplier<EntityType<MosshornEntity>> Mosshorn;
    public static RegistrySupplier<EntityType<CinderPupEntity>> CinderPup;
    public static RegistrySupplier<EntityType<EchoHowlerEntity>> EchoHowler;
    public static RegistrySupplier<EntityType<DuneSkimmerEntity>> DuneSkimmer;
    public static RegistrySupplier<EntityType<TideCallerEntity>> TideCaller;
    public static RegistrySupplier<EntityType<GloomStalkerEntity>> GloomStalker;
    public static RegistrySupplier<EntityType<CrystalHermitEntity>> CrystalHermit;
    public static RegistrySupplier<EntityType<WindDancerEntity>> WindDancer;
    public static RegistrySupplier<EntityType<MireGolemEntity>> MireGolem;
    public static RegistrySupplier<EntityType<LanternFoxEntity>> LanternFox;
    public static RegistrySupplier<EntityType<ReefGrazerEntity>> ReefGrazer;
    public static RegistrySupplier<EntityType<AshCrawlerEntity>> AshCrawler;
    public static RegistrySupplier<EntityType<StarWhaleEntity>> StarWhale;
    public static RegistrySupplier<EntityType<PetalWingEntity>> PetalWing;
    public static RegistrySupplier<EntityType<HeartOfTheForestEntity>> HeartOfTheForest;
    public static RegistrySupplier<EntityType<VoidSerpentEntity>> VoidSerpent;

    /** mob id -> entity type supplier (excludes bosses) */
    public static final Map<String, RegistrySupplier<EntityType<?>>> MOB_TYPES =
            new LinkedHashMap<String, RegistrySupplier<EntityType<?>>>();
    /** boss id -> entity type supplier */
    public static final Map<String, RegistrySupplier<EntityType<?>>> BOSS_TYPES =
            new LinkedHashMap<String, RegistrySupplier<EntityType<?>>>();

    private ModEntities() {
    }

    @SuppressWarnings("unchecked")
    public static void registerContent() {
        Lumox = ENTITIES.register("lumox", () -> EntityType.Builder.of(LumoxEntity::new, MobCategory.CREATURE)
                .sized(0.9F, 1.2F).clientTrackingRange(8).updateInterval(3)
                .build("lumox"));
        Brambleback = ENTITIES.register("brambleback", () -> EntityType.Builder.of(BramblebackEntity::new, MobCategory.CREATURE)
                .sized(1.4F, 1.6F).clientTrackingRange(8).updateInterval(3)
                .build("brambleback"));
        Siltstrider = ENTITIES.register("siltstrider", () -> EntityType.Builder.of(SiltstriderEntity::new, MobCategory.CREATURE)
                .sized(0.7F, 1.8F).clientTrackingRange(8).updateInterval(3)
                .build("siltstrider"));
        Glimmermoth = ENTITIES.register("glimmermoth", () -> EntityType.Builder.of(GlimmermothEntity::new, MobCategory.CREATURE)
                .sized(0.8F, 0.6F).clientTrackingRange(8).updateInterval(3)
                .build("glimmermoth"));
        PeatHopper = ENTITIES.register("peat_hopper", () -> EntityType.Builder.of(PeatHopperEntity::new, MobCategory.CREATURE)
                .sized(0.6F, 0.7F).clientTrackingRange(8).updateInterval(3)
                .build("peat_hopper"));
        EmberCalf = ENTITIES.register("ember_calf", () -> EntityType.Builder.of(EmberCalfEntity::new, MobCategory.CREATURE)
                .sized(1.0F, 1.3F).clientTrackingRange(8).updateInterval(3)
                .build("ember_calf"));
        FrostFawn = ENTITIES.register("frost_fawn", () -> EntityType.Builder.of(FrostFawnEntity::new, MobCategory.CREATURE)
                .sized(0.7F, 1.1F).clientTrackingRange(8).updateInterval(3)
                .build("frost_fawn"));
        Murkling = ENTITIES.register("murkling", () -> EntityType.Builder.of(MurklingEntity::new, MobCategory.MONSTER)
                .sized(0.8F, 1.0F).clientTrackingRange(8).updateInterval(3)
                .build("murkling"));
        SporeSprout = ENTITIES.register("spore_sprout", () -> EntityType.Builder.of(SporeSproutEntity::new, MobCategory.CREATURE)
                .sized(0.7F, 0.9F).clientTrackingRange(8).updateInterval(3)
                .build("spore_sprout"));
        Skywisp = ENTITIES.register("skywisp", () -> EntityType.Builder.of(SkywispEntity::new, MobCategory.CREATURE)
                .sized(0.9F, 0.8F).clientTrackingRange(8).updateInterval(3)
                .build("skywisp"));
        ThunderRam = ENTITIES.register("thunder_ram", () -> EntityType.Builder.of(ThunderRamEntity::new, MobCategory.CREATURE)
                .sized(1.1F, 1.4F).clientTrackingRange(8).updateInterval(3)
                .build("thunder_ram"));
        Mosshorn = ENTITIES.register("mosshorn", () -> EntityType.Builder.of(MosshornEntity::new, MobCategory.CREATURE)
                .sized(1.2F, 1.5F).clientTrackingRange(8).updateInterval(3)
                .build("mosshorn"));
        CinderPup = ENTITIES.register("cinder_pup", () -> EntityType.Builder.of(CinderPupEntity::new, MobCategory.CREATURE)
                .sized(0.7F, 0.8F).clientTrackingRange(8).updateInterval(3)
                .build("cinder_pup"));
        EchoHowler = ENTITIES.register("echo_howler", () -> EntityType.Builder.of(EchoHowlerEntity::new, MobCategory.MONSTER)
                .sized(1.0F, 1.5F).clientTrackingRange(8).updateInterval(3)
                .build("echo_howler"));
        DuneSkimmer = ENTITIES.register("dune_skimmer", () -> EntityType.Builder.of(DuneSkimmerEntity::new, MobCategory.CREATURE)
                .sized(0.8F, 0.7F).clientTrackingRange(8).updateInterval(3)
                .build("dune_skimmer"));
        TideCaller = ENTITIES.register("tide_caller", () -> EntityType.Builder.of(TideCallerEntity::new, MobCategory.CREATURE)
                .sized(0.8F, 1.4F).clientTrackingRange(8).updateInterval(3)
                .build("tide_caller"));
        GloomStalker = ENTITIES.register("gloom_stalker", () -> EntityType.Builder.of(GloomStalkerEntity::new, MobCategory.MONSTER)
                .sized(0.8F, 1.3F).clientTrackingRange(8).updateInterval(3)
                .build("gloom_stalker"));
        CrystalHermit = ENTITIES.register("crystal_hermit", () -> EntityType.Builder.of(CrystalHermitEntity::new, MobCategory.CREATURE)
                .sized(1.0F, 1.1F).clientTrackingRange(8).updateInterval(3)
                .build("crystal_hermit"));
        WindDancer = ENTITIES.register("wind_dancer", () -> EntityType.Builder.of(WindDancerEntity::new, MobCategory.CREATURE)
                .sized(0.9F, 0.7F).clientTrackingRange(8).updateInterval(3)
                .build("wind_dancer"));
        MireGolem = ENTITIES.register("mire_golem", () -> EntityType.Builder.of(MireGolemEntity::new, MobCategory.CREATURE)
                .sized(1.6F, 2.2F).clientTrackingRange(8).updateInterval(3)
                .build("mire_golem"));
        LanternFox = ENTITIES.register("lantern_fox", () -> EntityType.Builder.of(LanternFoxEntity::new, MobCategory.CREATURE)
                .sized(0.6F, 0.7F).clientTrackingRange(8).updateInterval(3)
                .build("lantern_fox"));
        ReefGrazer = ENTITIES.register("reef_grazer", () -> EntityType.Builder.of(ReefGrazerEntity::new, MobCategory.CREATURE)
                .sized(1.3F, 1.0F).clientTrackingRange(8).updateInterval(3)
                .build("reef_grazer"));
        AshCrawler = ENTITIES.register("ash_crawler", () -> EntityType.Builder.of(AshCrawlerEntity::new, MobCategory.MONSTER)
                .sized(0.6F, 0.5F).clientTrackingRange(8).updateInterval(3)
                .build("ash_crawler"));
        StarWhale = ENTITIES.register("star_whale", () -> EntityType.Builder.of(StarWhaleEntity::new, MobCategory.CREATURE)
                .sized(3.5F, 2.8F).clientTrackingRange(8).updateInterval(3)
                .build("star_whale"));
        PetalWing = ENTITIES.register("petal_wing", () -> EntityType.Builder.of(PetalWingEntity::new, MobCategory.CREATURE)
                .sized(0.5F, 0.5F).clientTrackingRange(8).updateInterval(3)
                .build("petal_wing"));
        HeartOfTheForest = ENTITIES.register("heart_of_the_forest", () -> EntityType.Builder.of(HeartOfTheForestEntity::new, MobCategory.MONSTER)
                .sized(2.6F, 4.2F).clientTrackingRange(12).updateInterval(2)
                .fireImmune().build("heart_of_the_forest"));
        VoidSerpent = ENTITIES.register("void_serpent", () -> EntityType.Builder.of(VoidSerpentEntity::new, MobCategory.MONSTER)
                .sized(1.8F, 1.8F).clientTrackingRange(12).updateInterval(2)
                .fireImmune().build("void_serpent"));

        EntityAttributeRegistry.register(Lumox, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 14.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.28D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(Brambleback, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 28.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.24D)
                .add(Attributes.ATTACK_DAMAGE, 5.0D)
                .add(Attributes.ARMOR, 4.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(Siltstrider, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 12.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.32D)
                .add(Attributes.ATTACK_DAMAGE, 1.5D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(Glimmermoth, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 6.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.3D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(PeatHopper, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 8.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.33D)
                .add(Attributes.ATTACK_DAMAGE, 1.0D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(EmberCalf, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 20.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.26D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 1.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(FrostFawn, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 12.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.34D)
                .add(Attributes.ATTACK_DAMAGE, 1.5D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(Murkling, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 16.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.3D)
                .add(Attributes.ATTACK_DAMAGE, 4.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(SporeSprout, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 10.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.22D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(Skywisp, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 8.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.35D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(ThunderRam, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 26.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.3D)
                .add(Attributes.ATTACK_DAMAGE, 6.0D)
                .add(Attributes.ARMOR, 3.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(Mosshorn, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 22.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.25D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(CinderPup, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 14.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.36D)
                .add(Attributes.ATTACK_DAMAGE, 4.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(EchoHowler, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 24.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.28D)
                .add(Attributes.ATTACK_DAMAGE, 5.0D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(DuneSkimmer, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 10.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.4D)
                .add(Attributes.ATTACK_DAMAGE, 1.5D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(TideCaller, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 18.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.27D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 1.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(GloomStalker, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 20.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.33D)
                .add(Attributes.ATTACK_DAMAGE, 6.0D)
                .add(Attributes.ARMOR, 1.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(CrystalHermit, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 16.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.2D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 5.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(WindDancer, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 7.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.38D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(MireGolem, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 40.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.18D)
                .add(Attributes.ATTACK_DAMAGE, 7.0D)
                .add(Attributes.ARMOR, 6.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(LanternFox, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 12.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.37D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(ReefGrazer, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 18.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.24D)
                .add(Attributes.ATTACK_DAMAGE, 1.5D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(AshCrawler, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 9.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.31D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(StarWhale, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 60.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.16D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 8.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(PetalWing, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 5.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.34D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(HeartOfTheForest, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 480.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.24D)
                .add(Attributes.ATTACK_DAMAGE, 12.0D)
                .add(Attributes.ARMOR, 8D)
                .add(Attributes.FOLLOW_RANGE, 96D)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0D));
        EntityAttributeRegistry.register(VoidSerpent, () -> MobEntity.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 520.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.36D)
                .add(Attributes.ATTACK_DAMAGE, 14.0D)
                .add(Attributes.ARMOR, 8D)
                .add(Attributes.FOLLOW_RANGE, 96D)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0D));

        for (int i = 0; i < com.biomesunseen.core.Content.MOBS.size(); i++) {
            String id = com.biomesunseen.core.Content.MOBS.get(i).id;
            MOB_TYPES.put(id, (RegistrySupplier<EntityType<?>>) (RegistrySupplier<?>) byMobId(id));
        }
        for (int i = 0; i < com.biomesunseen.core.Content.BOSSES.size(); i++) {
            String id = com.biomesunseen.core.Content.BOSSES.get(i).id;
            BOSS_TYPES.put(id, (RegistrySupplier<EntityType<?>>) (RegistrySupplier<?>) byBossId(id));
        }
    }

    private static RegistrySupplier<EntityType<?>> byMobId(String id) {
        if ("lumox".equals(id)) {
            return Lumox;
        }
        if ("brambleback".equals(id)) {
            return Brambleback;
        }
        if ("siltstrider".equals(id)) {
            return Siltstrider;
        }
        if ("glimmermoth".equals(id)) {
            return Glimmermoth;
        }
        if ("peat_hopper".equals(id)) {
            return PeatHopper;
        }
        if ("ember_calf".equals(id)) {
            return EmberCalf;
        }
        if ("frost_fawn".equals(id)) {
            return FrostFawn;
        }
        if ("murkling".equals(id)) {
            return Murkling;
        }
        if ("spore_sprout".equals(id)) {
            return SporeSprout;
        }
        if ("skywisp".equals(id)) {
            return Skywisp;
        }
        if ("thunder_ram".equals(id)) {
            return ThunderRam;
        }
        if ("mosshorn".equals(id)) {
            return Mosshorn;
        }
        if ("cinder_pup".equals(id)) {
            return CinderPup;
        }
        if ("echo_howler".equals(id)) {
            return EchoHowler;
        }
        if ("dune_skimmer".equals(id)) {
            return DuneSkimmer;
        }
        if ("tide_caller".equals(id)) {
            return TideCaller;
        }
        if ("gloom_stalker".equals(id)) {
            return GloomStalker;
        }
        if ("crystal_hermit".equals(id)) {
            return CrystalHermit;
        }
        if ("wind_dancer".equals(id)) {
            return WindDancer;
        }
        if ("mire_golem".equals(id)) {
            return MireGolem;
        }
        if ("lantern_fox".equals(id)) {
            return LanternFox;
        }
        if ("reef_grazer".equals(id)) {
            return ReefGrazer;
        }
        if ("ash_crawler".equals(id)) {
            return AshCrawler;
        }
        if ("star_whale".equals(id)) {
            return StarWhale;
        }
        if ("petal_wing".equals(id)) {
            return PetalWing;
        }
        return null;
    }

    private static RegistrySupplier<EntityType<?>> byBossId(String id) {
        if ("heart_of_the_forest".equals(id)) {
            return HeartOfTheForest;
        }
        if ("void_serpent".equals(id)) {
            return VoidSerpent;
        }
        return null;
    }
}
