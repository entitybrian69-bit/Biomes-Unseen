package com.biomesunseen.client;

import dev.architectury.registry.EntityRendererRegistry;
import dev.architectury.registry.ParticleProviderRegistry;

import com.biomesunseen.registry.ModEntities;
import com.biomesunseen.registry.ModParticles;
import com.biomesunseen.client.render.BiomesUnseenGeoRenderer;
import com.biomesunseen.client.render.HeartOfTheForestRenderer;
import com.biomesunseen.client.render.VoidSerpentRenderer;

/**
 * Client bootstrap: registers animated renderers for every mob, both bosses
 * and the custom particle factories.  Called from the platform client
 * entrypoint.
 */
public final class ClientSetup {

    private ClientSetup() {
    }

    public static void init() {
        EntityRendererRegistry.register(ModEntities.Lumox, context -> new BiomesUnseenGeoRenderer<>(context, "lumox"));
        EntityRendererRegistry.register(ModEntities.Brambleback, context -> new BiomesUnseenGeoRenderer<>(context, "brambleback"));
        EntityRendererRegistry.register(ModEntities.Siltstrider, context -> new BiomesUnseenGeoRenderer<>(context, "siltstrider"));
        EntityRendererRegistry.register(ModEntities.Glimmermoth, context -> new BiomesUnseenGeoRenderer<>(context, "glimmermoth"));
        EntityRendererRegistry.register(ModEntities.PeatHopper, context -> new BiomesUnseenGeoRenderer<>(context, "peat_hopper"));
        EntityRendererRegistry.register(ModEntities.EmberCalf, context -> new BiomesUnseenGeoRenderer<>(context, "ember_calf"));
        EntityRendererRegistry.register(ModEntities.FrostFawn, context -> new BiomesUnseenGeoRenderer<>(context, "frost_fawn"));
        EntityRendererRegistry.register(ModEntities.Murkling, context -> new BiomesUnseenGeoRenderer<>(context, "murkling"));
        EntityRendererRegistry.register(ModEntities.SporeSprout, context -> new BiomesUnseenGeoRenderer<>(context, "spore_sprout"));
        EntityRendererRegistry.register(ModEntities.Skywisp, context -> new BiomesUnseenGeoRenderer<>(context, "skywisp"));
        EntityRendererRegistry.register(ModEntities.ThunderRam, context -> new BiomesUnseenGeoRenderer<>(context, "thunder_ram"));
        EntityRendererRegistry.register(ModEntities.Mosshorn, context -> new BiomesUnseenGeoRenderer<>(context, "mosshorn"));
        EntityRendererRegistry.register(ModEntities.CinderPup, context -> new BiomesUnseenGeoRenderer<>(context, "cinder_pup"));
        EntityRendererRegistry.register(ModEntities.EchoHowler, context -> new BiomesUnseenGeoRenderer<>(context, "echo_howler"));
        EntityRendererRegistry.register(ModEntities.DuneSkimmer, context -> new BiomesUnseenGeoRenderer<>(context, "dune_skimmer"));
        EntityRendererRegistry.register(ModEntities.TideCaller, context -> new BiomesUnseenGeoRenderer<>(context, "tide_caller"));
        EntityRendererRegistry.register(ModEntities.GloomStalker, context -> new BiomesUnseenGeoRenderer<>(context, "gloom_stalker"));
        EntityRendererRegistry.register(ModEntities.CrystalHermit, context -> new BiomesUnseenGeoRenderer<>(context, "crystal_hermit"));
        EntityRendererRegistry.register(ModEntities.WindDancer, context -> new BiomesUnseenGeoRenderer<>(context, "wind_dancer"));
        EntityRendererRegistry.register(ModEntities.MireGolem, context -> new BiomesUnseenGeoRenderer<>(context, "mire_golem"));
        EntityRendererRegistry.register(ModEntities.LanternFox, context -> new BiomesUnseenGeoRenderer<>(context, "lantern_fox"));
        EntityRendererRegistry.register(ModEntities.ReefGrazer, context -> new BiomesUnseenGeoRenderer<>(context, "reef_grazer"));
        EntityRendererRegistry.register(ModEntities.AshCrawler, context -> new BiomesUnseenGeoRenderer<>(context, "ash_crawler"));
        EntityRendererRegistry.register(ModEntities.StarWhale, context -> new BiomesUnseenGeoRenderer<>(context, "star_whale"));
        EntityRendererRegistry.register(ModEntities.PetalWing, context -> new BiomesUnseenGeoRenderer<>(context, "petal_wing"));
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
