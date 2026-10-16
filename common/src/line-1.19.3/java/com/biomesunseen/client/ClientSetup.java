package com.biomesunseen.client;

import dev.architectury.registry.client.level.entity.EntityRendererRegistry;
import dev.architectury.registry.client.particle.ParticleProviderRegistry;

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
