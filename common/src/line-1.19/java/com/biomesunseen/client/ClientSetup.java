package com.biomesunseen.client;

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
        EntityRendererRegistry.register(ModEntities.Lumox, context -> new UnseenLegacyRenderer<>(context, "lumox"));
        EntityRendererRegistry.register(ModEntities.Brambleback, context -> new UnseenLegacyRenderer<>(context, "brambleback"));
        EntityRendererRegistry.register(ModEntities.Siltstrider, context -> new UnseenLegacyRenderer<>(context, "siltstrider"));
        EntityRendererRegistry.register(ModEntities.Glimmermoth, context -> new UnseenLegacyRenderer<>(context, "glimmermoth"));
        EntityRendererRegistry.register(ModEntities.PeatHopper, context -> new UnseenLegacyRenderer<>(context, "peat_hopper"));
        EntityRendererRegistry.register(ModEntities.EmberCalf, context -> new UnseenLegacyRenderer<>(context, "ember_calf"));
        EntityRendererRegistry.register(ModEntities.FrostFawn, context -> new UnseenLegacyRenderer<>(context, "frost_fawn"));
        EntityRendererRegistry.register(ModEntities.Murkling, context -> new UnseenLegacyRenderer<>(context, "murkling"));
        EntityRendererRegistry.register(ModEntities.SporeSprout, context -> new UnseenLegacyRenderer<>(context, "spore_sprout"));
        EntityRendererRegistry.register(ModEntities.Skywisp, context -> new UnseenLegacyRenderer<>(context, "skywisp"));
        EntityRendererRegistry.register(ModEntities.ThunderRam, context -> new UnseenLegacyRenderer<>(context, "thunder_ram"));
        EntityRendererRegistry.register(ModEntities.Mosshorn, context -> new UnseenLegacyRenderer<>(context, "mosshorn"));
        EntityRendererRegistry.register(ModEntities.CinderPup, context -> new UnseenLegacyRenderer<>(context, "cinder_pup"));
        EntityRendererRegistry.register(ModEntities.EchoHowler, context -> new UnseenLegacyRenderer<>(context, "echo_howler"));
        EntityRendererRegistry.register(ModEntities.DuneSkimmer, context -> new UnseenLegacyRenderer<>(context, "dune_skimmer"));
        EntityRendererRegistry.register(ModEntities.TideCaller, context -> new UnseenLegacyRenderer<>(context, "tide_caller"));
        EntityRendererRegistry.register(ModEntities.GloomStalker, context -> new UnseenLegacyRenderer<>(context, "gloom_stalker"));
        EntityRendererRegistry.register(ModEntities.CrystalHermit, context -> new UnseenLegacyRenderer<>(context, "crystal_hermit"));
        EntityRendererRegistry.register(ModEntities.WindDancer, context -> new UnseenLegacyRenderer<>(context, "wind_dancer"));
        EntityRendererRegistry.register(ModEntities.MireGolem, context -> new UnseenLegacyRenderer<>(context, "mire_golem"));
        EntityRendererRegistry.register(ModEntities.LanternFox, context -> new UnseenLegacyRenderer<>(context, "lantern_fox"));
        EntityRendererRegistry.register(ModEntities.ReefGrazer, context -> new UnseenLegacyRenderer<>(context, "reef_grazer"));
        EntityRendererRegistry.register(ModEntities.AshCrawler, context -> new UnseenLegacyRenderer<>(context, "ash_crawler"));
        EntityRendererRegistry.register(ModEntities.StarWhale, context -> new UnseenLegacyRenderer<>(context, "star_whale"));
        EntityRendererRegistry.register(ModEntities.PetalWing, context -> new UnseenLegacyRenderer<>(context, "petal_wing"));
        EntityRendererRegistry.register(ModEntities.Glowmoth, context -> new UnseenLegacyRenderer<>(context, "glowmoth"));
        EntityRendererRegistry.register(ModEntities.TunnelHound, context -> new UnseenLegacyRenderer<>(context, "tunnel_hound"));
        EntityRendererRegistry.register(ModEntities.CrystalBeetle, context -> new UnseenLegacyRenderer<>(context, "crystal_beetle"));
        EntityRendererRegistry.register(ModEntities.MagmaSnail, context -> new UnseenLegacyRenderer<>(context, "magma_snail"));
        EntityRendererRegistry.register(ModEntities.EchoBat, context -> new UnseenLegacyRenderer<>(context, "echo_bat"));
        EntityRendererRegistry.register(ModEntities.RootGnawer, context -> new UnseenLegacyRenderer<>(context, "root_gnawer"));
        EntityRendererRegistry.register(ModEntities.DeepLurker, context -> new UnseenLegacyRenderer<>(context, "deep_lurker"));
        EntityRendererRegistry.register(ModEntities.LanternJelly, context -> new UnseenLegacyRenderer<>(context, "lantern_jelly"));
        EntityRendererRegistry.register(ModEntities.Stoneback, context -> new UnseenLegacyRenderer<>(context, "stoneback"));
        EntityRendererRegistry.register(ModEntities.Mycopath, context -> new UnseenLegacyRenderer<>(context, "mycopath"));
        EntityRendererRegistry.register(ModEntities.Skyray, context -> new UnseenLegacyRenderer<>(context, "skyray"));
        EntityRendererRegistry.register(ModEntities.CloudHeron, context -> new UnseenLegacyRenderer<>(context, "cloud_heron"));
        EntityRendererRegistry.register(ModEntities.ZephyrPup, context -> new UnseenLegacyRenderer<>(context, "zephyr_pup"));
        EntityRendererRegistry.register(ModEntities.IslandTortoise, context -> new UnseenLegacyRenderer<>(context, "island_tortoise"));
        EntityRendererRegistry.register(ModEntities.Dawnfinch, context -> new UnseenLegacyRenderer<>(context, "dawnfinch"));
        EntityRendererRegistry.register(ModEntities.StormJay, context -> new UnseenLegacyRenderer<>(context, "storm_jay"));
        EntityRendererRegistry.register(ModEntities.SummitRam, context -> new UnseenLegacyRenderer<>(context, "summit_ram"));
        EntityRendererRegistry.register(ModEntities.Mistgraz, context -> new UnseenLegacyRenderer<>(context, "mistgraz"));
        EntityRendererRegistry.register(ModEntities.StarSerpent, context -> new UnseenLegacyRenderer<>(context, "star_serpent"));
        EntityRendererRegistry.register(ModEntities.Windlark, context -> new UnseenLegacyRenderer<>(context, "windlark"));
        EntityRendererRegistry.register(ModEntities.Glitchling, context -> new UnseenLegacyRenderer<>(context, "glitchling"));
        EntityRendererRegistry.register(ModEntities.NullStalker, context -> new UnseenLegacyRenderer<>(context, "null_stalker"));
        EntityRendererRegistry.register(ModEntities.MirrorWisp, context -> new UnseenLegacyRenderer<>(context, "mirror_wisp"));
        EntityRendererRegistry.register(ModEntities.ParadoxBeast, context -> new UnseenLegacyRenderer<>(context, "paradox_beast"));
        EntityRendererRegistry.register(ModEntities.StaticCrawler, context -> new UnseenLegacyRenderer<>(context, "static_crawler"));
        EntityRendererRegistry.register(ModEntities.DreamEater, context -> new UnseenLegacyRenderer<>(context, "dream_eater"));
        EntityRendererRegistry.register(ModEntities.Shardwing, context -> new UnseenLegacyRenderer<>(context, "shardwing"));
        EntityRendererRegistry.register(ModEntities.InverseGrazer, context -> new UnseenLegacyRenderer<>(context, "inverse_grazer"));
        EntityRendererRegistry.register(ModEntities.EchoHusk, context -> new UnseenLegacyRenderer<>(context, "echo_husk"));
        EntityRendererRegistry.register(ModEntities.UnravelSpawn, context -> new UnseenLegacyRenderer<>(context, "unravel_spawn"));
        EntityRendererRegistry.register(ModEntities.HeartOfTheForest, context -> new UnseenLegacyRenderer<>(context, "heart_of_the_forest"));
        EntityRendererRegistry.register(ModEntities.VoidSerpent, context -> new UnseenLegacyRenderer<>(context, "void_serpent"));
        EntityRendererRegistry.register(ModEntities.WardenOfTheHollowDeep, context -> new UnseenLegacyRenderer<>(context, "warden_of_the_hollow_deep"));
        EntityRendererRegistry.register(ModEntities.TheSkywardCrown, context -> new UnseenLegacyRenderer<>(context, "the_skyward_crown"));
        EntityRendererRegistry.register(ModEntities.TheUnraveling, context -> new UnseenLegacyRenderer<>(context, "the_unraveling"));

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
