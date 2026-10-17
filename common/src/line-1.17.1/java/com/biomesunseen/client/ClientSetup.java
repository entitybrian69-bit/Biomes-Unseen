package com.biomesunseen.client;

import java.util.function.Supplier;
import net.minecraft.world.entity.EntityType;
import com.biomesunseen.entity.BiomesUnseenMob;
import dev.architectury.registry.client.level.entity.EntityRendererRegistry;
import dev.architectury.registry.client.particle.ParticleProviderRegistry;
import dev.architectury.registry.client.level.entity.EntityModelLayerRegistry;
import com.biomesunseen.client.legacy.UnseenLegacyModel;

import com.biomesunseen.registry.ModEntities;
import com.biomesunseen.registry.ModParticles;
import com.biomesunseen.client.legacy.UnseenLegacyRenderer;
import com.biomesunseen.client.particle.UnseenParticle;

/**
 * Client bootstrap: registers animated renderers for every mob, both bosses
 * and the custom particle factories.  Called from the platform client
 * entrypoint.
 */
public final class ClientSetup {

    private ClientSetup() {
    }

    public static void init() {
        EntityModelLayerRegistry.register(UnseenLegacyModel.LAYER, UnseenLegacyModel::createBodyLayer);
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Lumox,
                context -> new UnseenLegacyRenderer<>(context, "lumox"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Brambleback,
                context -> new UnseenLegacyRenderer<>(context, "brambleback"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Siltstrider,
                context -> new UnseenLegacyRenderer<>(context, "siltstrider"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Glimmermoth,
                context -> new UnseenLegacyRenderer<>(context, "glimmermoth"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.PeatHopper,
                context -> new UnseenLegacyRenderer<>(context, "peat_hopper"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.EmberCalf,
                context -> new UnseenLegacyRenderer<>(context, "ember_calf"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.FrostFawn,
                context -> new UnseenLegacyRenderer<>(context, "frost_fawn"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Murkling,
                context -> new UnseenLegacyRenderer<>(context, "murkling"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.SporeSprout,
                context -> new UnseenLegacyRenderer<>(context, "spore_sprout"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Skywisp,
                context -> new UnseenLegacyRenderer<>(context, "skywisp"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.ThunderRam,
                context -> new UnseenLegacyRenderer<>(context, "thunder_ram"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Mosshorn,
                context -> new UnseenLegacyRenderer<>(context, "mosshorn"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.CinderPup,
                context -> new UnseenLegacyRenderer<>(context, "cinder_pup"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.EchoHowler,
                context -> new UnseenLegacyRenderer<>(context, "echo_howler"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.DuneSkimmer,
                context -> new UnseenLegacyRenderer<>(context, "dune_skimmer"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.TideCaller,
                context -> new UnseenLegacyRenderer<>(context, "tide_caller"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.GloomStalker,
                context -> new UnseenLegacyRenderer<>(context, "gloom_stalker"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.CrystalHermit,
                context -> new UnseenLegacyRenderer<>(context, "crystal_hermit"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.WindDancer,
                context -> new UnseenLegacyRenderer<>(context, "wind_dancer"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.MireGolem,
                context -> new UnseenLegacyRenderer<>(context, "mire_golem"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.LanternFox,
                context -> new UnseenLegacyRenderer<>(context, "lantern_fox"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.ReefGrazer,
                context -> new UnseenLegacyRenderer<>(context, "reef_grazer"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.AshCrawler,
                context -> new UnseenLegacyRenderer<>(context, "ash_crawler"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.StarWhale,
                context -> new UnseenLegacyRenderer<>(context, "star_whale"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.PetalWing,
                context -> new UnseenLegacyRenderer<>(context, "petal_wing"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Glowmoth,
                context -> new UnseenLegacyRenderer<>(context, "glowmoth"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.TunnelHound,
                context -> new UnseenLegacyRenderer<>(context, "tunnel_hound"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.CrystalBeetle,
                context -> new UnseenLegacyRenderer<>(context, "crystal_beetle"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.MagmaSnail,
                context -> new UnseenLegacyRenderer<>(context, "magma_snail"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.EchoBat,
                context -> new UnseenLegacyRenderer<>(context, "echo_bat"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.RootGnawer,
                context -> new UnseenLegacyRenderer<>(context, "root_gnawer"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.DeepLurker,
                context -> new UnseenLegacyRenderer<>(context, "deep_lurker"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.LanternJelly,
                context -> new UnseenLegacyRenderer<>(context, "lantern_jelly"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Stoneback,
                context -> new UnseenLegacyRenderer<>(context, "stoneback"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Mycopath,
                context -> new UnseenLegacyRenderer<>(context, "mycopath"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Skyray,
                context -> new UnseenLegacyRenderer<>(context, "skyray"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.CloudHeron,
                context -> new UnseenLegacyRenderer<>(context, "cloud_heron"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.ZephyrPup,
                context -> new UnseenLegacyRenderer<>(context, "zephyr_pup"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.IslandTortoise,
                context -> new UnseenLegacyRenderer<>(context, "island_tortoise"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Dawnfinch,
                context -> new UnseenLegacyRenderer<>(context, "dawnfinch"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.StormJay,
                context -> new UnseenLegacyRenderer<>(context, "storm_jay"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.SummitRam,
                context -> new UnseenLegacyRenderer<>(context, "summit_ram"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Mistgraz,
                context -> new UnseenLegacyRenderer<>(context, "mistgraz"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.StarSerpent,
                context -> new UnseenLegacyRenderer<>(context, "star_serpent"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Windlark,
                context -> new UnseenLegacyRenderer<>(context, "windlark"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Glitchling,
                context -> new UnseenLegacyRenderer<>(context, "glitchling"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.NullStalker,
                context -> new UnseenLegacyRenderer<>(context, "null_stalker"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.MirrorWisp,
                context -> new UnseenLegacyRenderer<>(context, "mirror_wisp"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.ParadoxBeast,
                context -> new UnseenLegacyRenderer<>(context, "paradox_beast"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.StaticCrawler,
                context -> new UnseenLegacyRenderer<>(context, "static_crawler"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.DreamEater,
                context -> new UnseenLegacyRenderer<>(context, "dream_eater"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.Shardwing,
                context -> new UnseenLegacyRenderer<>(context, "shardwing"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.InverseGrazer,
                context -> new UnseenLegacyRenderer<>(context, "inverse_grazer"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.EchoHusk,
                context -> new UnseenLegacyRenderer<>(context, "echo_husk"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.UnravelSpawn,
                context -> new UnseenLegacyRenderer<>(context, "unravel_spawn"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.HeartOfTheForest,
                context -> new UnseenLegacyRenderer<>(context, "heart_of_the_forest"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.VoidSerpent,
                context -> new UnseenLegacyRenderer<>(context, "void_serpent"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.WardenOfTheHollowDeep,
                context -> new UnseenLegacyRenderer<>(context, "warden_of_the_hollow_deep"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.TheSkywardCrown,
                context -> new UnseenLegacyRenderer<>(context, "the_skyward_crown"));
        EntityRendererRegistry.register((Supplier<EntityType<? extends BiomesUnseenMob>>) (Supplier<?>) ModEntities.TheUnraveling,
                context -> new UnseenLegacyRenderer<>(context, "the_unraveling"));

        ParticleProviderRegistry.register(ModParticles.BY_ID.get("crystal_spark").get(),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("ember_flake").get(),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("void_mote").get(),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("spore_drift").get(),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("frost_mote").get(),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("storm_arc").get(),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("petal_burst").get(),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("heal_glow").get(),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("hollow_mote").get(),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("aurora_dust").get(),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("glitch_spark").get(),
                UnseenParticle.Provider::new);
    }
}
