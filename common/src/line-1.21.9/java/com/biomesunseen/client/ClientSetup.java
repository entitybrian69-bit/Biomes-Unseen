package com.biomesunseen.client;

import dev.architectury.registry.client.level.entity.EntityRendererRegistry;
import dev.architectury.registry.client.particle.ParticleProviderRegistry;
import dev.architectury.registry.client.level.entity.EntityModelLayerRegistry;
import com.biomesunseen.client.legacy.UnseenLegacyModel;

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
        EntityRendererRegistry.register(ModEntities.HeartOfTheForest, UnseenLegacyRenderer.provider("heart_of_the_forest"));
        EntityRendererRegistry.register(ModEntities.VoidSerpent, UnseenLegacyRenderer.provider("void_serpent"));


    }
}
