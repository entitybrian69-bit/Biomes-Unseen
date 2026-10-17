package com.biomesunseen.client;

import me.shedaniel.architectury.registry.entity.EntityRenderers;
import me.shedaniel.architectury.registry.ParticleProviderRegistry;

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
        EntityRenderers.register(ModEntities.Lumox.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "lumox"));
        EntityRenderers.register(ModEntities.Brambleback.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "brambleback"));
        EntityRenderers.register(ModEntities.Siltstrider.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "siltstrider"));
        EntityRenderers.register(ModEntities.Glimmermoth.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "glimmermoth"));
        EntityRenderers.register(ModEntities.PeatHopper.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "peat_hopper"));
        EntityRenderers.register(ModEntities.EmberCalf.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "ember_calf"));
        EntityRenderers.register(ModEntities.FrostFawn.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "frost_fawn"));
        EntityRenderers.register(ModEntities.Murkling.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "murkling"));
        EntityRenderers.register(ModEntities.SporeSprout.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "spore_sprout"));
        EntityRenderers.register(ModEntities.Skywisp.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "skywisp"));
        EntityRenderers.register(ModEntities.ThunderRam.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "thunder_ram"));
        EntityRenderers.register(ModEntities.Mosshorn.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "mosshorn"));
        EntityRenderers.register(ModEntities.CinderPup.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "cinder_pup"));
        EntityRenderers.register(ModEntities.EchoHowler.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "echo_howler"));
        EntityRenderers.register(ModEntities.DuneSkimmer.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "dune_skimmer"));
        EntityRenderers.register(ModEntities.TideCaller.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "tide_caller"));
        EntityRenderers.register(ModEntities.GloomStalker.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "gloom_stalker"));
        EntityRenderers.register(ModEntities.CrystalHermit.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "crystal_hermit"));
        EntityRenderers.register(ModEntities.WindDancer.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "wind_dancer"));
        EntityRenderers.register(ModEntities.MireGolem.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "mire_golem"));
        EntityRenderers.register(ModEntities.LanternFox.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "lantern_fox"));
        EntityRenderers.register(ModEntities.ReefGrazer.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "reef_grazer"));
        EntityRenderers.register(ModEntities.AshCrawler.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "ash_crawler"));
        EntityRenderers.register(ModEntities.StarWhale.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "star_whale"));
        EntityRenderers.register(ModEntities.PetalWing.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "petal_wing"));
        EntityRenderers.register(ModEntities.Glowmoth.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "glowmoth"));
        EntityRenderers.register(ModEntities.TunnelHound.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "tunnel_hound"));
        EntityRenderers.register(ModEntities.CrystalBeetle.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "crystal_beetle"));
        EntityRenderers.register(ModEntities.MagmaSnail.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "magma_snail"));
        EntityRenderers.register(ModEntities.EchoBat.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "echo_bat"));
        EntityRenderers.register(ModEntities.RootGnawer.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "root_gnawer"));
        EntityRenderers.register(ModEntities.DeepLurker.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "deep_lurker"));
        EntityRenderers.register(ModEntities.LanternJelly.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "lantern_jelly"));
        EntityRenderers.register(ModEntities.Stoneback.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "stoneback"));
        EntityRenderers.register(ModEntities.Mycopath.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "mycopath"));
        EntityRenderers.register(ModEntities.Skyray.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "skyray"));
        EntityRenderers.register(ModEntities.CloudHeron.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "cloud_heron"));
        EntityRenderers.register(ModEntities.ZephyrPup.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "zephyr_pup"));
        EntityRenderers.register(ModEntities.IslandTortoise.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "island_tortoise"));
        EntityRenderers.register(ModEntities.Dawnfinch.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "dawnfinch"));
        EntityRenderers.register(ModEntities.StormJay.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "storm_jay"));
        EntityRenderers.register(ModEntities.SummitRam.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "summit_ram"));
        EntityRenderers.register(ModEntities.Mistgraz.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "mistgraz"));
        EntityRenderers.register(ModEntities.StarSerpent.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "star_serpent"));
        EntityRenderers.register(ModEntities.Windlark.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "windlark"));
        EntityRenderers.register(ModEntities.Glitchling.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "glitchling"));
        EntityRenderers.register(ModEntities.NullStalker.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "null_stalker"));
        EntityRenderers.register(ModEntities.MirrorWisp.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "mirror_wisp"));
        EntityRenderers.register(ModEntities.ParadoxBeast.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "paradox_beast"));
        EntityRenderers.register(ModEntities.StaticCrawler.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "static_crawler"));
        EntityRenderers.register(ModEntities.DreamEater.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "dream_eater"));
        EntityRenderers.register(ModEntities.Shardwing.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "shardwing"));
        EntityRenderers.register(ModEntities.InverseGrazer.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "inverse_grazer"));
        EntityRenderers.register(ModEntities.EchoHusk.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "echo_husk"));
        EntityRenderers.register(ModEntities.UnravelSpawn.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "unravel_spawn"));
        EntityRenderers.register(ModEntities.HeartOfTheForest.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "heart_of_the_forest"));
        EntityRenderers.register(ModEntities.VoidSerpent.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "void_serpent"));
        EntityRenderers.register(ModEntities.WardenOfTheHollowDeep.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "warden_of_the_hollow_deep"));
        EntityRenderers.register(ModEntities.TheSkywardCrown.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "the_skyward_crown"));
        EntityRenderers.register(ModEntities.TheUnraveling.get(), dispatcher -> new UnseenLegacyRenderer<>(dispatcher, "the_unraveling"));

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
