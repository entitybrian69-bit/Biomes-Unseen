package com.biomesunseen.client;

import me.shedaniel.architectury.registry.EntityRendererRegistry;
import me.shedaniel.architectury.registry.ParticleProviderRegistry;

import com.biomesunseen.registry.ModEntities;
import com.biomesunseen.registry.ModParticles;
import com.biomesunseen.client.legacy.UnseenLegacyRenderer;

/**
 * Client bootstrap: registers animated renderers for every mob, both bosses
 * and the custom particle factories.  Called from the platform client
 * entrypoint.
 */
public final class ClientSetup {

    private ClientSetup() {
    }

    public static void init() {
        EntityRendererRegistry.register(ModEntities.Lumox, manager, ctx -> new UnseenLegacyRenderer<>(manager, "lumox"));
        EntityRendererRegistry.register(ModEntities.Brambleback, manager, ctx -> new UnseenLegacyRenderer<>(manager, "brambleback"));
        EntityRendererRegistry.register(ModEntities.Siltstrider, manager, ctx -> new UnseenLegacyRenderer<>(manager, "siltstrider"));
        EntityRendererRegistry.register(ModEntities.Glimmermoth, manager, ctx -> new UnseenLegacyRenderer<>(manager, "glimmermoth"));
        EntityRendererRegistry.register(ModEntities.PeatHopper, manager, ctx -> new UnseenLegacyRenderer<>(manager, "peat_hopper"));
        EntityRendererRegistry.register(ModEntities.EmberCalf, manager, ctx -> new UnseenLegacyRenderer<>(manager, "ember_calf"));
        EntityRendererRegistry.register(ModEntities.FrostFawn, manager, ctx -> new UnseenLegacyRenderer<>(manager, "frost_fawn"));
        EntityRendererRegistry.register(ModEntities.Murkling, manager, ctx -> new UnseenLegacyRenderer<>(manager, "murkling"));
        EntityRendererRegistry.register(ModEntities.SporeSprout, manager, ctx -> new UnseenLegacyRenderer<>(manager, "spore_sprout"));
        EntityRendererRegistry.register(ModEntities.Skywisp, manager, ctx -> new UnseenLegacyRenderer<>(manager, "skywisp"));
        EntityRendererRegistry.register(ModEntities.ThunderRam, manager, ctx -> new UnseenLegacyRenderer<>(manager, "thunder_ram"));
        EntityRendererRegistry.register(ModEntities.Mosshorn, manager, ctx -> new UnseenLegacyRenderer<>(manager, "mosshorn"));
        EntityRendererRegistry.register(ModEntities.CinderPup, manager, ctx -> new UnseenLegacyRenderer<>(manager, "cinder_pup"));
        EntityRendererRegistry.register(ModEntities.EchoHowler, manager, ctx -> new UnseenLegacyRenderer<>(manager, "echo_howler"));
        EntityRendererRegistry.register(ModEntities.DuneSkimmer, manager, ctx -> new UnseenLegacyRenderer<>(manager, "dune_skimmer"));
        EntityRendererRegistry.register(ModEntities.TideCaller, manager, ctx -> new UnseenLegacyRenderer<>(manager, "tide_caller"));
        EntityRendererRegistry.register(ModEntities.GloomStalker, manager, ctx -> new UnseenLegacyRenderer<>(manager, "gloom_stalker"));
        EntityRendererRegistry.register(ModEntities.CrystalHermit, manager, ctx -> new UnseenLegacyRenderer<>(manager, "crystal_hermit"));
        EntityRendererRegistry.register(ModEntities.WindDancer, manager, ctx -> new UnseenLegacyRenderer<>(manager, "wind_dancer"));
        EntityRendererRegistry.register(ModEntities.MireGolem, manager, ctx -> new UnseenLegacyRenderer<>(manager, "mire_golem"));
        EntityRendererRegistry.register(ModEntities.LanternFox, manager, ctx -> new UnseenLegacyRenderer<>(manager, "lantern_fox"));
        EntityRendererRegistry.register(ModEntities.ReefGrazer, manager, ctx -> new UnseenLegacyRenderer<>(manager, "reef_grazer"));
        EntityRendererRegistry.register(ModEntities.AshCrawler, manager, ctx -> new UnseenLegacyRenderer<>(manager, "ash_crawler"));
        EntityRendererRegistry.register(ModEntities.StarWhale, manager, ctx -> new UnseenLegacyRenderer<>(manager, "star_whale"));
        EntityRendererRegistry.register(ModEntities.PetalWing, manager, ctx -> new UnseenLegacyRenderer<>(manager, "petal_wing"));
        EntityRendererRegistry.register(ModEntities.HeartOfTheForest, HeartOfTheForestRenderer::new);
        EntityRendererRegistry.register(ModEntities.VoidSerpent, VoidSerpentRenderer::new);

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
    }
}
