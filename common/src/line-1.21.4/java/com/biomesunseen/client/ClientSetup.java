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
        EntityRendererRegistry.register(ModEntities.Lumox, UnseenLegacyRenderer.provider("lumox"));
        EntityRendererRegistry.register(ModEntities.Brambleback, UnseenLegacyRenderer.provider("brambleback"));
        EntityRendererRegistry.register(ModEntities.Siltstrider, UnseenLegacyRenderer.provider("siltstrider"));
        EntityRendererRegistry.register(ModEntities.Glimmermoth, UnseenLegacyRenderer.provider("glimmermoth"));
        EntityRendererRegistry.register(ModEntities.PeatHopper, UnseenLegacyRenderer.provider("peat_hopper"));
        EntityRendererRegistry.register(ModEntities.EmberCalf, UnseenLegacyRenderer.provider("ember_calf"));
        EntityRendererRegistry.register(ModEntities.FrostFawn, UnseenLegacyRenderer.provider("frost_fawn"));
        EntityRendererRegistry.register(ModEntities.Murkling, UnseenLegacyRenderer.provider("murkling"));
        EntityRendererRegistry.register(ModEntities.SporeSprout, UnseenLegacyRenderer.provider("spore_sprout"));
        EntityRendererRegistry.register(ModEntities.Skywisp, UnseenLegacyRenderer.provider("skywisp"));
        EntityRendererRegistry.register(ModEntities.ThunderRam, UnseenLegacyRenderer.provider("thunder_ram"));
        EntityRendererRegistry.register(ModEntities.Mosshorn, UnseenLegacyRenderer.provider("mosshorn"));
        EntityRendererRegistry.register(ModEntities.CinderPup, UnseenLegacyRenderer.provider("cinder_pup"));
        EntityRendererRegistry.register(ModEntities.EchoHowler, UnseenLegacyRenderer.provider("echo_howler"));
        EntityRendererRegistry.register(ModEntities.DuneSkimmer, UnseenLegacyRenderer.provider("dune_skimmer"));
        EntityRendererRegistry.register(ModEntities.TideCaller, UnseenLegacyRenderer.provider("tide_caller"));
        EntityRendererRegistry.register(ModEntities.GloomStalker, UnseenLegacyRenderer.provider("gloom_stalker"));
        EntityRendererRegistry.register(ModEntities.CrystalHermit, UnseenLegacyRenderer.provider("crystal_hermit"));
        EntityRendererRegistry.register(ModEntities.WindDancer, UnseenLegacyRenderer.provider("wind_dancer"));
        EntityRendererRegistry.register(ModEntities.MireGolem, UnseenLegacyRenderer.provider("mire_golem"));
        EntityRendererRegistry.register(ModEntities.LanternFox, UnseenLegacyRenderer.provider("lantern_fox"));
        EntityRendererRegistry.register(ModEntities.ReefGrazer, UnseenLegacyRenderer.provider("reef_grazer"));
        EntityRendererRegistry.register(ModEntities.AshCrawler, UnseenLegacyRenderer.provider("ash_crawler"));
        EntityRendererRegistry.register(ModEntities.StarWhale, UnseenLegacyRenderer.provider("star_whale"));
        EntityRendererRegistry.register(ModEntities.PetalWing, UnseenLegacyRenderer.provider("petal_wing"));
        EntityRendererRegistry.register(ModEntities.Glowmoth, UnseenLegacyRenderer.provider("glowmoth"));
        EntityRendererRegistry.register(ModEntities.TunnelHound, UnseenLegacyRenderer.provider("tunnel_hound"));
        EntityRendererRegistry.register(ModEntities.CrystalBeetle, UnseenLegacyRenderer.provider("crystal_beetle"));
        EntityRendererRegistry.register(ModEntities.MagmaSnail, UnseenLegacyRenderer.provider("magma_snail"));
        EntityRendererRegistry.register(ModEntities.EchoBat, UnseenLegacyRenderer.provider("echo_bat"));
        EntityRendererRegistry.register(ModEntities.RootGnawer, UnseenLegacyRenderer.provider("root_gnawer"));
        EntityRendererRegistry.register(ModEntities.DeepLurker, UnseenLegacyRenderer.provider("deep_lurker"));
        EntityRendererRegistry.register(ModEntities.LanternJelly, UnseenLegacyRenderer.provider("lantern_jelly"));
        EntityRendererRegistry.register(ModEntities.Stoneback, UnseenLegacyRenderer.provider("stoneback"));
        EntityRendererRegistry.register(ModEntities.Mycopath, UnseenLegacyRenderer.provider("mycopath"));
        EntityRendererRegistry.register(ModEntities.Skyray, UnseenLegacyRenderer.provider("skyray"));
        EntityRendererRegistry.register(ModEntities.CloudHeron, UnseenLegacyRenderer.provider("cloud_heron"));
        EntityRendererRegistry.register(ModEntities.ZephyrPup, UnseenLegacyRenderer.provider("zephyr_pup"));
        EntityRendererRegistry.register(ModEntities.IslandTortoise, UnseenLegacyRenderer.provider("island_tortoise"));
        EntityRendererRegistry.register(ModEntities.Dawnfinch, UnseenLegacyRenderer.provider("dawnfinch"));
        EntityRendererRegistry.register(ModEntities.StormJay, UnseenLegacyRenderer.provider("storm_jay"));
        EntityRendererRegistry.register(ModEntities.SummitRam, UnseenLegacyRenderer.provider("summit_ram"));
        EntityRendererRegistry.register(ModEntities.Mistgraz, UnseenLegacyRenderer.provider("mistgraz"));
        EntityRendererRegistry.register(ModEntities.StarSerpent, UnseenLegacyRenderer.provider("star_serpent"));
        EntityRendererRegistry.register(ModEntities.Windlark, UnseenLegacyRenderer.provider("windlark"));
        EntityRendererRegistry.register(ModEntities.Glitchling, UnseenLegacyRenderer.provider("glitchling"));
        EntityRendererRegistry.register(ModEntities.NullStalker, UnseenLegacyRenderer.provider("null_stalker"));
        EntityRendererRegistry.register(ModEntities.MirrorWisp, UnseenLegacyRenderer.provider("mirror_wisp"));
        EntityRendererRegistry.register(ModEntities.ParadoxBeast, UnseenLegacyRenderer.provider("paradox_beast"));
        EntityRendererRegistry.register(ModEntities.StaticCrawler, UnseenLegacyRenderer.provider("static_crawler"));
        EntityRendererRegistry.register(ModEntities.DreamEater, UnseenLegacyRenderer.provider("dream_eater"));
        EntityRendererRegistry.register(ModEntities.Shardwing, UnseenLegacyRenderer.provider("shardwing"));
        EntityRendererRegistry.register(ModEntities.InverseGrazer, UnseenLegacyRenderer.provider("inverse_grazer"));
        EntityRendererRegistry.register(ModEntities.EchoHusk, UnseenLegacyRenderer.provider("echo_husk"));
        EntityRendererRegistry.register(ModEntities.UnravelSpawn, UnseenLegacyRenderer.provider("unravel_spawn"));
        EntityRendererRegistry.register(ModEntities.HeartOfTheForest, UnseenLegacyRenderer.provider("heart_of_the_forest"));
        EntityRendererRegistry.register(ModEntities.VoidSerpent, UnseenLegacyRenderer.provider("void_serpent"));
        EntityRendererRegistry.register(ModEntities.WardenOfTheHollowDeep, UnseenLegacyRenderer.provider("warden_of_the_hollow_deep"));
        EntityRendererRegistry.register(ModEntities.TheSkywardCrown, UnseenLegacyRenderer.provider("the_skyward_crown"));
        EntityRendererRegistry.register(ModEntities.TheUnraveling, UnseenLegacyRenderer.provider("the_unraveling"));

        ParticleProviderRegistry.register(ModParticles.BY_ID.get("crystal_spark"),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("ember_flake"),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("void_mote"),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("spore_drift"),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("frost_mote"),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("storm_arc"),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("petal_burst"),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("heal_glow"),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("hollow_mote"),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("aurora_dust"),
                UnseenParticle.Provider::new);
        ParticleProviderRegistry.register(ModParticles.BY_ID.get("glitch_spark"),
                UnseenParticle.Provider::new);
    }
}
