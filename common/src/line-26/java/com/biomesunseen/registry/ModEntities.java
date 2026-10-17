package com.biomesunseen.registry;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.Mob;

import com.biomesunseen.entity.boss.*;
import com.biomesunseen.entity.mobs.*;

import dev.architectury.registry.level.entity.EntityAttributeRegistry;
import dev.architectury.registry.registries.RegistrySupplier;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * All 55 mobs and 5 bosses with their spawn attributes.
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
    public static RegistrySupplier<EntityType<GlowmothEntity>> Glowmoth;
    public static RegistrySupplier<EntityType<TunnelHoundEntity>> TunnelHound;
    public static RegistrySupplier<EntityType<CrystalBeetleEntity>> CrystalBeetle;
    public static RegistrySupplier<EntityType<MagmaSnailEntity>> MagmaSnail;
    public static RegistrySupplier<EntityType<EchoBatEntity>> EchoBat;
    public static RegistrySupplier<EntityType<RootGnawerEntity>> RootGnawer;
    public static RegistrySupplier<EntityType<DeepLurkerEntity>> DeepLurker;
    public static RegistrySupplier<EntityType<LanternJellyEntity>> LanternJelly;
    public static RegistrySupplier<EntityType<StonebackEntity>> Stoneback;
    public static RegistrySupplier<EntityType<MycopathEntity>> Mycopath;
    public static RegistrySupplier<EntityType<SkyrayEntity>> Skyray;
    public static RegistrySupplier<EntityType<CloudHeronEntity>> CloudHeron;
    public static RegistrySupplier<EntityType<ZephyrPupEntity>> ZephyrPup;
    public static RegistrySupplier<EntityType<IslandTortoiseEntity>> IslandTortoise;
    public static RegistrySupplier<EntityType<DawnfinchEntity>> Dawnfinch;
    public static RegistrySupplier<EntityType<StormJayEntity>> StormJay;
    public static RegistrySupplier<EntityType<SummitRamEntity>> SummitRam;
    public static RegistrySupplier<EntityType<MistgrazEntity>> Mistgraz;
    public static RegistrySupplier<EntityType<StarSerpentEntity>> StarSerpent;
    public static RegistrySupplier<EntityType<WindlarkEntity>> Windlark;
    public static RegistrySupplier<EntityType<GlitchlingEntity>> Glitchling;
    public static RegistrySupplier<EntityType<NullStalkerEntity>> NullStalker;
    public static RegistrySupplier<EntityType<MirrorWispEntity>> MirrorWisp;
    public static RegistrySupplier<EntityType<ParadoxBeastEntity>> ParadoxBeast;
    public static RegistrySupplier<EntityType<StaticCrawlerEntity>> StaticCrawler;
    public static RegistrySupplier<EntityType<DreamEaterEntity>> DreamEater;
    public static RegistrySupplier<EntityType<ShardwingEntity>> Shardwing;
    public static RegistrySupplier<EntityType<InverseGrazerEntity>> InverseGrazer;
    public static RegistrySupplier<EntityType<EchoHuskEntity>> EchoHusk;
    public static RegistrySupplier<EntityType<UnravelSpawnEntity>> UnravelSpawn;
    public static RegistrySupplier<EntityType<HeartOfTheForestEntity>> HeartOfTheForest;
    public static RegistrySupplier<EntityType<VoidSerpentEntity>> VoidSerpent;
    public static RegistrySupplier<EntityType<WardenOfTheHollowDeepEntity>> WardenOfTheHollowDeep;
    public static RegistrySupplier<EntityType<TheSkywardCrownEntity>> TheSkywardCrown;
    public static RegistrySupplier<EntityType<TheUnravelingEntity>> TheUnraveling;

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
        Lumox = ModRegistries.ENTITIES.register("lumox", () -> EntityType.Builder.of(LumoxEntity::new, MobCategory.CREATURE)
                .sized(0.9F, 1.2F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "lumox"))));
        Brambleback = ModRegistries.ENTITIES.register("brambleback", () -> EntityType.Builder.of(BramblebackEntity::new, MobCategory.CREATURE)
                .sized(1.4F, 1.6F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "brambleback"))));
        Siltstrider = ModRegistries.ENTITIES.register("siltstrider", () -> EntityType.Builder.of(SiltstriderEntity::new, MobCategory.CREATURE)
                .sized(0.7F, 1.8F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "siltstrider"))));
        Glimmermoth = ModRegistries.ENTITIES.register("glimmermoth", () -> EntityType.Builder.of(GlimmermothEntity::new, MobCategory.CREATURE)
                .sized(0.8F, 0.6F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "glimmermoth"))));
        PeatHopper = ModRegistries.ENTITIES.register("peat_hopper", () -> EntityType.Builder.of(PeatHopperEntity::new, MobCategory.CREATURE)
                .sized(0.6F, 0.7F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "peat_hopper"))));
        EmberCalf = ModRegistries.ENTITIES.register("ember_calf", () -> EntityType.Builder.of(EmberCalfEntity::new, MobCategory.CREATURE)
                .sized(1.0F, 1.3F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "ember_calf"))));
        FrostFawn = ModRegistries.ENTITIES.register("frost_fawn", () -> EntityType.Builder.of(FrostFawnEntity::new, MobCategory.CREATURE)
                .sized(0.7F, 1.1F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "frost_fawn"))));
        Murkling = ModRegistries.ENTITIES.register("murkling", () -> EntityType.Builder.of(MurklingEntity::new, MobCategory.MONSTER)
                .sized(0.8F, 1.0F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "murkling"))));
        SporeSprout = ModRegistries.ENTITIES.register("spore_sprout", () -> EntityType.Builder.of(SporeSproutEntity::new, MobCategory.CREATURE)
                .sized(0.7F, 0.9F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "spore_sprout"))));
        Skywisp = ModRegistries.ENTITIES.register("skywisp", () -> EntityType.Builder.of(SkywispEntity::new, MobCategory.CREATURE)
                .sized(0.9F, 0.8F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "skywisp"))));
        ThunderRam = ModRegistries.ENTITIES.register("thunder_ram", () -> EntityType.Builder.of(ThunderRamEntity::new, MobCategory.CREATURE)
                .sized(1.1F, 1.4F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "thunder_ram"))));
        Mosshorn = ModRegistries.ENTITIES.register("mosshorn", () -> EntityType.Builder.of(MosshornEntity::new, MobCategory.CREATURE)
                .sized(1.2F, 1.5F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "mosshorn"))));
        CinderPup = ModRegistries.ENTITIES.register("cinder_pup", () -> EntityType.Builder.of(CinderPupEntity::new, MobCategory.CREATURE)
                .sized(0.7F, 0.8F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "cinder_pup"))));
        EchoHowler = ModRegistries.ENTITIES.register("echo_howler", () -> EntityType.Builder.of(EchoHowlerEntity::new, MobCategory.MONSTER)
                .sized(1.0F, 1.5F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "echo_howler"))));
        DuneSkimmer = ModRegistries.ENTITIES.register("dune_skimmer", () -> EntityType.Builder.of(DuneSkimmerEntity::new, MobCategory.CREATURE)
                .sized(0.8F, 0.7F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "dune_skimmer"))));
        TideCaller = ModRegistries.ENTITIES.register("tide_caller", () -> EntityType.Builder.of(TideCallerEntity::new, MobCategory.CREATURE)
                .sized(0.8F, 1.4F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "tide_caller"))));
        GloomStalker = ModRegistries.ENTITIES.register("gloom_stalker", () -> EntityType.Builder.of(GloomStalkerEntity::new, MobCategory.MONSTER)
                .sized(0.8F, 1.3F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "gloom_stalker"))));
        CrystalHermit = ModRegistries.ENTITIES.register("crystal_hermit", () -> EntityType.Builder.of(CrystalHermitEntity::new, MobCategory.CREATURE)
                .sized(1.0F, 1.1F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "crystal_hermit"))));
        WindDancer = ModRegistries.ENTITIES.register("wind_dancer", () -> EntityType.Builder.of(WindDancerEntity::new, MobCategory.CREATURE)
                .sized(0.9F, 0.7F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "wind_dancer"))));
        MireGolem = ModRegistries.ENTITIES.register("mire_golem", () -> EntityType.Builder.of(MireGolemEntity::new, MobCategory.CREATURE)
                .sized(1.6F, 2.2F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "mire_golem"))));
        LanternFox = ModRegistries.ENTITIES.register("lantern_fox", () -> EntityType.Builder.of(LanternFoxEntity::new, MobCategory.CREATURE)
                .sized(0.6F, 0.7F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "lantern_fox"))));
        ReefGrazer = ModRegistries.ENTITIES.register("reef_grazer", () -> EntityType.Builder.of(ReefGrazerEntity::new, MobCategory.CREATURE)
                .sized(1.3F, 1.0F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "reef_grazer"))));
        AshCrawler = ModRegistries.ENTITIES.register("ash_crawler", () -> EntityType.Builder.of(AshCrawlerEntity::new, MobCategory.MONSTER)
                .sized(0.6F, 0.5F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "ash_crawler"))));
        StarWhale = ModRegistries.ENTITIES.register("star_whale", () -> EntityType.Builder.of(StarWhaleEntity::new, MobCategory.CREATURE)
                .sized(3.5F, 2.8F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "star_whale"))));
        PetalWing = ModRegistries.ENTITIES.register("petal_wing", () -> EntityType.Builder.of(PetalWingEntity::new, MobCategory.CREATURE)
                .sized(0.5F, 0.5F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "petal_wing"))));
        Glowmoth = ModRegistries.ENTITIES.register("glowmoth", () -> EntityType.Builder.of(GlowmothEntity::new, MobCategory.CREATURE)
                .sized(0.8F, 0.6F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "glowmoth"))));
        TunnelHound = ModRegistries.ENTITIES.register("tunnel_hound", () -> EntityType.Builder.of(TunnelHoundEntity::new, MobCategory.MONSTER)
                .sized(0.9F, 1.0F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "tunnel_hound"))));
        CrystalBeetle = ModRegistries.ENTITIES.register("crystal_beetle", () -> EntityType.Builder.of(CrystalBeetleEntity::new, MobCategory.CREATURE)
                .sized(0.9F, 0.8F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "crystal_beetle"))));
        MagmaSnail = ModRegistries.ENTITIES.register("magma_snail", () -> EntityType.Builder.of(MagmaSnailEntity::new, MobCategory.CREATURE)
                .sized(1.1F, 0.9F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "magma_snail"))));
        EchoBat = ModRegistries.ENTITIES.register("echo_bat", () -> EntityType.Builder.of(EchoBatEntity::new, MobCategory.CREATURE)
                .sized(0.6F, 0.5F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "echo_bat"))));
        RootGnawer = ModRegistries.ENTITIES.register("root_gnawer", () -> EntityType.Builder.of(RootGnawerEntity::new, MobCategory.MONSTER)
                .sized(0.8F, 0.7F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "root_gnawer"))));
        DeepLurker = ModRegistries.ENTITIES.register("deep_lurker", () -> EntityType.Builder.of(DeepLurkerEntity::new, MobCategory.MONSTER)
                .sized(1.3F, 1.6F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "deep_lurker"))));
        LanternJelly = ModRegistries.ENTITIES.register("lantern_jelly", () -> EntityType.Builder.of(LanternJellyEntity::new, MobCategory.CREATURE)
                .sized(0.9F, 0.9F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "lantern_jelly"))));
        Stoneback = ModRegistries.ENTITIES.register("stoneback", () -> EntityType.Builder.of(StonebackEntity::new, MobCategory.CREATURE)
                .sized(1.5F, 1.5F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "stoneback"))));
        Mycopath = ModRegistries.ENTITIES.register("mycopath", () -> EntityType.Builder.of(MycopathEntity::new, MobCategory.CREATURE)
                .sized(1.0F, 1.2F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "mycopath"))));
        Skyray = ModRegistries.ENTITIES.register("skyray", () -> EntityType.Builder.of(SkyrayEntity::new, MobCategory.CREATURE)
                .sized(1.4F, 0.6F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "skyray"))));
        CloudHeron = ModRegistries.ENTITIES.register("cloud_heron", () -> EntityType.Builder.of(CloudHeronEntity::new, MobCategory.CREATURE)
                .sized(1.0F, 1.4F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "cloud_heron"))));
        ZephyrPup = ModRegistries.ENTITIES.register("zephyr_pup", () -> EntityType.Builder.of(ZephyrPupEntity::new, MobCategory.CREATURE)
                .sized(0.8F, 0.8F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "zephyr_pup"))));
        IslandTortoise = ModRegistries.ENTITIES.register("island_tortoise", () -> EntityType.Builder.of(IslandTortoiseEntity::new, MobCategory.CREATURE)
                .sized(1.8F, 1.4F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "island_tortoise"))));
        Dawnfinch = ModRegistries.ENTITIES.register("dawnfinch", () -> EntityType.Builder.of(DawnfinchEntity::new, MobCategory.CREATURE)
                .sized(0.5F, 0.5F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "dawnfinch"))));
        StormJay = ModRegistries.ENTITIES.register("storm_jay", () -> EntityType.Builder.of(StormJayEntity::new, MobCategory.CREATURE)
                .sized(0.7F, 0.6F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "storm_jay"))));
        SummitRam = ModRegistries.ENTITIES.register("summit_ram", () -> EntityType.Builder.of(SummitRamEntity::new, MobCategory.CREATURE)
                .sized(1.2F, 1.4F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "summit_ram"))));
        Mistgraz = ModRegistries.ENTITIES.register("mistgraz", () -> EntityType.Builder.of(MistgrazEntity::new, MobCategory.CREATURE)
                .sized(1.2F, 1.2F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "mistgraz"))));
        StarSerpent = ModRegistries.ENTITIES.register("star_serpent", () -> EntityType.Builder.of(StarSerpentEntity::new, MobCategory.MONSTER)
                .sized(1.2F, 1.0F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "star_serpent"))));
        Windlark = ModRegistries.ENTITIES.register("windlark", () -> EntityType.Builder.of(WindlarkEntity::new, MobCategory.CREATURE)
                .sized(0.6F, 0.5F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "windlark"))));
        Glitchling = ModRegistries.ENTITIES.register("glitchling", () -> EntityType.Builder.of(GlitchlingEntity::new, MobCategory.MONSTER)
                .sized(0.6F, 0.6F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "glitchling"))));
        NullStalker = ModRegistries.ENTITIES.register("null_stalker", () -> EntityType.Builder.of(NullStalkerEntity::new, MobCategory.MONSTER)
                .sized(0.9F, 1.4F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "null_stalker"))));
        MirrorWisp = ModRegistries.ENTITIES.register("mirror_wisp", () -> EntityType.Builder.of(MirrorWispEntity::new, MobCategory.CREATURE)
                .sized(0.7F, 0.7F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "mirror_wisp"))));
        ParadoxBeast = ModRegistries.ENTITIES.register("paradox_beast", () -> EntityType.Builder.of(ParadoxBeastEntity::new, MobCategory.MONSTER)
                .sized(1.4F, 1.6F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "paradox_beast"))));
        StaticCrawler = ModRegistries.ENTITIES.register("static_crawler", () -> EntityType.Builder.of(StaticCrawlerEntity::new, MobCategory.MONSTER)
                .sized(0.7F, 0.5F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "static_crawler"))));
        DreamEater = ModRegistries.ENTITIES.register("dream_eater", () -> EntityType.Builder.of(DreamEaterEntity::new, MobCategory.MONSTER)
                .sized(1.1F, 1.3F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "dream_eater"))));
        Shardwing = ModRegistries.ENTITIES.register("shardwing", () -> EntityType.Builder.of(ShardwingEntity::new, MobCategory.CREATURE)
                .sized(0.9F, 0.7F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "shardwing"))));
        InverseGrazer = ModRegistries.ENTITIES.register("inverse_grazer", () -> EntityType.Builder.of(InverseGrazerEntity::new, MobCategory.CREATURE)
                .sized(1.2F, 1.2F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "inverse_grazer"))));
        EchoHusk = ModRegistries.ENTITIES.register("echo_husk", () -> EntityType.Builder.of(EchoHuskEntity::new, MobCategory.MONSTER)
                .sized(0.9F, 1.5F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "echo_husk"))));
        UnravelSpawn = ModRegistries.ENTITIES.register("unravel_spawn", () -> EntityType.Builder.of(UnravelSpawnEntity::new, MobCategory.CREATURE)
                .sized(1.0F, 1.0F).clientTrackingRange(8).updateInterval(3)
                .build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "unravel_spawn"))));
        HeartOfTheForest = ModRegistries.ENTITIES.register("heart_of_the_forest", () -> EntityType.Builder.of(HeartOfTheForestEntity::new, MobCategory.MONSTER)
                .sized(2.6F, 4.2F).clientTrackingRange(12).updateInterval(2)
                .fireImmune().build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "heart_of_the_forest"))));
        VoidSerpent = ModRegistries.ENTITIES.register("void_serpent", () -> EntityType.Builder.of(VoidSerpentEntity::new, MobCategory.MONSTER)
                .sized(1.8F, 1.8F).clientTrackingRange(12).updateInterval(2)
                .fireImmune().build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "void_serpent"))));
        WardenOfTheHollowDeep = ModRegistries.ENTITIES.register("warden_of_the_hollow_deep", () -> EntityType.Builder.of(WardenOfTheHollowDeepEntity::new, MobCategory.MONSTER)
                .sized(3.2F, 5.0F).clientTrackingRange(12).updateInterval(2)
                .fireImmune().build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "warden_of_the_hollow_deep"))));
        TheSkywardCrown = ModRegistries.ENTITIES.register("the_skyward_crown", () -> EntityType.Builder.of(TheSkywardCrownEntity::new, MobCategory.MONSTER)
                .sized(2.4F, 3.8F).clientTrackingRange(12).updateInterval(2)
                .fireImmune().build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "the_skyward_crown"))));
        TheUnraveling = ModRegistries.ENTITIES.register("the_unraveling", () -> EntityType.Builder.of(TheUnravelingEntity::new, MobCategory.MONSTER)
                .sized(2.8F, 4.0F).clientTrackingRange(12).updateInterval(2)
                .fireImmune().build(net.minecraft.resources.ResourceKey.create(net.minecraft.core.registries.Registries.ENTITY_TYPE, net.minecraft.resources.Identifier.fromNamespaceAndPath(com.biomesunseen.core.ModConstants.MOD_ID, "the_unraveling"))));

        EntityAttributeRegistry.register(() -> Lumox.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 14.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.28D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Brambleback.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 28.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.24D)
                .add(Attributes.ATTACK_DAMAGE, 5.0D)
                .add(Attributes.ARMOR, 4.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Siltstrider.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 12.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.32D)
                .add(Attributes.ATTACK_DAMAGE, 1.5D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Glimmermoth.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 6.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.3D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> PeatHopper.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 8.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.33D)
                .add(Attributes.ATTACK_DAMAGE, 1.0D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> EmberCalf.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 20.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.26D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 1.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> FrostFawn.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 12.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.34D)
                .add(Attributes.ATTACK_DAMAGE, 1.5D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Murkling.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 16.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.3D)
                .add(Attributes.ATTACK_DAMAGE, 4.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> SporeSprout.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 10.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.22D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Skywisp.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 8.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.35D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> ThunderRam.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 26.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.3D)
                .add(Attributes.ATTACK_DAMAGE, 6.0D)
                .add(Attributes.ARMOR, 3.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Mosshorn.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 22.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.25D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> CinderPup.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 14.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.36D)
                .add(Attributes.ATTACK_DAMAGE, 4.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> EchoHowler.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 24.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.28D)
                .add(Attributes.ATTACK_DAMAGE, 5.0D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> DuneSkimmer.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 10.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.4D)
                .add(Attributes.ATTACK_DAMAGE, 1.5D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> TideCaller.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 18.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.27D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 1.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> GloomStalker.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 20.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.33D)
                .add(Attributes.ATTACK_DAMAGE, 6.0D)
                .add(Attributes.ARMOR, 1.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> CrystalHermit.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 16.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.2D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 5.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> WindDancer.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 7.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.38D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> MireGolem.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 40.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.18D)
                .add(Attributes.ATTACK_DAMAGE, 7.0D)
                .add(Attributes.ARMOR, 6.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> LanternFox.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 12.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.37D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> ReefGrazer.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 18.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.24D)
                .add(Attributes.ATTACK_DAMAGE, 1.5D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> AshCrawler.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 9.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.31D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> StarWhale.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 60.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.16D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 8.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> PetalWing.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 5.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.34D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Glowmoth.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 7.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.34D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> TunnelHound.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 22.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.32D)
                .add(Attributes.ATTACK_DAMAGE, 5.0D)
                .add(Attributes.ARMOR, 1.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> CrystalBeetle.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 14.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.22D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 4.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> MagmaSnail.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 18.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.14D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 3.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> EchoBat.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 8.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.38D)
                .add(Attributes.ATTACK_DAMAGE, 1.0D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> RootGnawer.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 16.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.3D)
                .add(Attributes.ATTACK_DAMAGE, 4.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> DeepLurker.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 30.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.26D)
                .add(Attributes.ATTACK_DAMAGE, 7.0D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> LanternJelly.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 12.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.2D)
                .add(Attributes.ATTACK_DAMAGE, 1.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Stoneback.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 34.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.2D)
                .add(Attributes.ATTACK_DAMAGE, 4.0D)
                .add(Attributes.ARMOR, 6.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Mycopath.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 16.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.24D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Skyray.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 18.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.36D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> CloudHeron.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 14.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.3D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> ZephyrPup.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 16.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.35D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> IslandTortoise.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 40.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.14D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 7.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Dawnfinch.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 6.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.4D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> StormJay.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 10.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.42D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> SummitRam.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 30.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.28D)
                .add(Attributes.ATTACK_DAMAGE, 6.0D)
                .add(Attributes.ARMOR, 3.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Mistgraz.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 22.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.22D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> StarSerpent.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 26.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.34D)
                .add(Attributes.ATTACK_DAMAGE, 6.0D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Windlark.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 8.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.44D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Glitchling.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 10.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.4D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> NullStalker.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 24.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.34D)
                .add(Attributes.ATTACK_DAMAGE, 6.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> MirrorWisp.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 8.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.36D)
                .add(Attributes.ATTACK_DAMAGE, 0.5D)
                .add(Attributes.ARMOR, 0.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> ParadoxBeast.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 34.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.26D)
                .add(Attributes.ATTACK_DAMAGE, 8.0D)
                .add(Attributes.ARMOR, 3.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> StaticCrawler.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 14.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.33D)
                .add(Attributes.ATTACK_DAMAGE, 4.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> DreamEater.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 28.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.29D)
                .add(Attributes.ATTACK_DAMAGE, 7.0D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> Shardwing.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 12.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.38D)
                .add(Attributes.ATTACK_DAMAGE, 3.0D)
                .add(Attributes.ARMOR, 0.5D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> InverseGrazer.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 20.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.22D)
                .add(Attributes.ATTACK_DAMAGE, 2.0D)
                .add(Attributes.ARMOR, 3.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> EchoHusk.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 20.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.31D)
                .add(Attributes.ATTACK_DAMAGE, 5.0D)
                .add(Attributes.ARMOR, 2.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> UnravelSpawn.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 16.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.27D)
                .add(Attributes.ATTACK_DAMAGE, 1.0D)
                .add(Attributes.ARMOR, 1.0D)
                .add(Attributes.FOLLOW_RANGE, 48D));
        EntityAttributeRegistry.register(() -> HeartOfTheForest.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 480.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.24D)
                .add(Attributes.ATTACK_DAMAGE, 12.0D)
                .add(Attributes.ARMOR, 8D)
                .add(Attributes.FOLLOW_RANGE, 96D)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0D));
        EntityAttributeRegistry.register(() -> VoidSerpent.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 520.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.36D)
                .add(Attributes.ATTACK_DAMAGE, 14.0D)
                .add(Attributes.ARMOR, 8D)
                .add(Attributes.FOLLOW_RANGE, 96D)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0D));
        EntityAttributeRegistry.register(() -> WardenOfTheHollowDeep.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 620.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.22D)
                .add(Attributes.ATTACK_DAMAGE, 16.0D)
                .add(Attributes.ARMOR, 8D)
                .add(Attributes.FOLLOW_RANGE, 96D)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0D));
        EntityAttributeRegistry.register(() -> TheSkywardCrown.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 560.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.34D)
                .add(Attributes.ATTACK_DAMAGE, 14.0D)
                .add(Attributes.ARMOR, 8D)
                .add(Attributes.FOLLOW_RANGE, 96D)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0D));
        EntityAttributeRegistry.register(() -> TheUnraveling.get(), () -> Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 700.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.3D)
                .add(Attributes.ATTACK_DAMAGE, 18.0D)
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
            return (RegistrySupplier) Lumox;
        }
        if ("brambleback".equals(id)) {
            return (RegistrySupplier) Brambleback;
        }
        if ("siltstrider".equals(id)) {
            return (RegistrySupplier) Siltstrider;
        }
        if ("glimmermoth".equals(id)) {
            return (RegistrySupplier) Glimmermoth;
        }
        if ("peat_hopper".equals(id)) {
            return (RegistrySupplier) PeatHopper;
        }
        if ("ember_calf".equals(id)) {
            return (RegistrySupplier) EmberCalf;
        }
        if ("frost_fawn".equals(id)) {
            return (RegistrySupplier) FrostFawn;
        }
        if ("murkling".equals(id)) {
            return (RegistrySupplier) Murkling;
        }
        if ("spore_sprout".equals(id)) {
            return (RegistrySupplier) SporeSprout;
        }
        if ("skywisp".equals(id)) {
            return (RegistrySupplier) Skywisp;
        }
        if ("thunder_ram".equals(id)) {
            return (RegistrySupplier) ThunderRam;
        }
        if ("mosshorn".equals(id)) {
            return (RegistrySupplier) Mosshorn;
        }
        if ("cinder_pup".equals(id)) {
            return (RegistrySupplier) CinderPup;
        }
        if ("echo_howler".equals(id)) {
            return (RegistrySupplier) EchoHowler;
        }
        if ("dune_skimmer".equals(id)) {
            return (RegistrySupplier) DuneSkimmer;
        }
        if ("tide_caller".equals(id)) {
            return (RegistrySupplier) TideCaller;
        }
        if ("gloom_stalker".equals(id)) {
            return (RegistrySupplier) GloomStalker;
        }
        if ("crystal_hermit".equals(id)) {
            return (RegistrySupplier) CrystalHermit;
        }
        if ("wind_dancer".equals(id)) {
            return (RegistrySupplier) WindDancer;
        }
        if ("mire_golem".equals(id)) {
            return (RegistrySupplier) MireGolem;
        }
        if ("lantern_fox".equals(id)) {
            return (RegistrySupplier) LanternFox;
        }
        if ("reef_grazer".equals(id)) {
            return (RegistrySupplier) ReefGrazer;
        }
        if ("ash_crawler".equals(id)) {
            return (RegistrySupplier) AshCrawler;
        }
        if ("star_whale".equals(id)) {
            return (RegistrySupplier) StarWhale;
        }
        if ("petal_wing".equals(id)) {
            return (RegistrySupplier) PetalWing;
        }
        if ("glowmoth".equals(id)) {
            return (RegistrySupplier) Glowmoth;
        }
        if ("tunnel_hound".equals(id)) {
            return (RegistrySupplier) TunnelHound;
        }
        if ("crystal_beetle".equals(id)) {
            return (RegistrySupplier) CrystalBeetle;
        }
        if ("magma_snail".equals(id)) {
            return (RegistrySupplier) MagmaSnail;
        }
        if ("echo_bat".equals(id)) {
            return (RegistrySupplier) EchoBat;
        }
        if ("root_gnawer".equals(id)) {
            return (RegistrySupplier) RootGnawer;
        }
        if ("deep_lurker".equals(id)) {
            return (RegistrySupplier) DeepLurker;
        }
        if ("lantern_jelly".equals(id)) {
            return (RegistrySupplier) LanternJelly;
        }
        if ("stoneback".equals(id)) {
            return (RegistrySupplier) Stoneback;
        }
        if ("mycopath".equals(id)) {
            return (RegistrySupplier) Mycopath;
        }
        if ("skyray".equals(id)) {
            return (RegistrySupplier) Skyray;
        }
        if ("cloud_heron".equals(id)) {
            return (RegistrySupplier) CloudHeron;
        }
        if ("zephyr_pup".equals(id)) {
            return (RegistrySupplier) ZephyrPup;
        }
        if ("island_tortoise".equals(id)) {
            return (RegistrySupplier) IslandTortoise;
        }
        if ("dawnfinch".equals(id)) {
            return (RegistrySupplier) Dawnfinch;
        }
        if ("storm_jay".equals(id)) {
            return (RegistrySupplier) StormJay;
        }
        if ("summit_ram".equals(id)) {
            return (RegistrySupplier) SummitRam;
        }
        if ("mistgraz".equals(id)) {
            return (RegistrySupplier) Mistgraz;
        }
        if ("star_serpent".equals(id)) {
            return (RegistrySupplier) StarSerpent;
        }
        if ("windlark".equals(id)) {
            return (RegistrySupplier) Windlark;
        }
        if ("glitchling".equals(id)) {
            return (RegistrySupplier) Glitchling;
        }
        if ("null_stalker".equals(id)) {
            return (RegistrySupplier) NullStalker;
        }
        if ("mirror_wisp".equals(id)) {
            return (RegistrySupplier) MirrorWisp;
        }
        if ("paradox_beast".equals(id)) {
            return (RegistrySupplier) ParadoxBeast;
        }
        if ("static_crawler".equals(id)) {
            return (RegistrySupplier) StaticCrawler;
        }
        if ("dream_eater".equals(id)) {
            return (RegistrySupplier) DreamEater;
        }
        if ("shardwing".equals(id)) {
            return (RegistrySupplier) Shardwing;
        }
        if ("inverse_grazer".equals(id)) {
            return (RegistrySupplier) InverseGrazer;
        }
        if ("echo_husk".equals(id)) {
            return (RegistrySupplier) EchoHusk;
        }
        if ("unravel_spawn".equals(id)) {
            return (RegistrySupplier) UnravelSpawn;
        }
        return null;
    }

    private static RegistrySupplier<EntityType<?>> byBossId(String id) {
        if ("heart_of_the_forest".equals(id)) {
            return (RegistrySupplier) HeartOfTheForest;
        }
        if ("void_serpent".equals(id)) {
            return (RegistrySupplier) VoidSerpent;
        }
        if ("warden_of_the_hollow_deep".equals(id)) {
            return (RegistrySupplier) WardenOfTheHollowDeep;
        }
        if ("the_skyward_crown".equals(id)) {
            return (RegistrySupplier) TheSkywardCrown;
        }
        if ("the_unraveling".equals(id)) {
            return (RegistrySupplier) TheUnraveling;
        }
        return null;
    }
}
