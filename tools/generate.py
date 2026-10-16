#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Biomes Unseen project generator.

Stamps the complete multi-version, multi-loader source tree:
  - root build files, wrapper, README, BUILD.md
  - common/src/main/java (pure-Java content core)
  - common/src/line-*/java + resources (per API line: registries, worldgen,
    entities, bosses, client, datagen)
  - common/src/main/resources (assets: textures, geo, animations, lang)
  - common/src/data-*/resources (datapack trees per data style)
  - every fabric-*/forge-*/neoforge-* platform module

Usage:  python3 tools/generate.py [repo_root]
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import emit_root
import emit_common
import emit_families
import emit_families2
import emit_worldgen
import emit_entities
import emit_client_datagen
import emit_assets
import emit_data
import emit_platforms
from lines import LINES, types_for
from content import TARGETS

# Architectury registry package moved at Architectury 2.x (1.17+).
ARCH_PKG_OLD = "me.shedaniel.architectury.registry."
ARCH_PKG_NEW = "dev.architectury.registry."

# 1.16.5 Mojang-mapping rewrites (packages moved in 1.17).
LEGACY_REWRITES = [
    # Model render signature: modern EntityModel#renderToBuffer -> 1.16 render.
    ("public void renderToBuffer(com.mojang.blaze3d.vertex.PoseStack matrixStack,\n"
     "            com.mojang.blaze3d.vertex.VertexConsumer buffer,\n"
     "            int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {",
     "public void render(com.mojang.blaze3d.matrix.MatrixStack matrixStack,\n"
     "            net.minecraft.client.renderer.vertex.IVertexBuilder buffer,\n"
     "            int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {"),
    ("new ModelPart(", "new ModelRenderer(this, "),
    ("net.minecraft.client.model.ModelPart", "net.minecraft.client.model.ModelRenderer"),
    ("com.mojang.blaze3d.vertex.PoseStack", "com.mojang.blaze3d.matrix.MatrixStack"),
    ("com.mojang.blaze3d.vertex.VertexConsumer", "net.minecraft.client.renderer.vertex.IVertexBuilder"),
    ("net.minecraft.client.renderer.MultiBufferSource", "net.minecraft.client.renderer.RenderTypeBuffer"),
    ("net.minecraft.world.level.block.state.BlockBehaviour", "net.minecraft.block.AbstractBlock"),
    ("net.minecraft.world.level.block.state.BlockState", "net.minecraft.block.BlockState"),
    ("net.minecraft.world.level.block.Blocks", "net.minecraft.block.Blocks"),
    ("net.minecraft.world.level.block.Block", "net.minecraft.block.Block"),
    ("net.minecraft.world.level.block.SoundType", "net.minecraft.block.SoundType"),
    ("net.minecraft.world.item.crafting.Ingredient", "net.minecraft.item.crafting.Ingredient"),
    ("net.minecraft.world.item.ItemStack", "net.minecraft.item.ItemStack"),
    ("net.minecraft.world.item.SpawnEggItem", "net.minecraft.item.SpawnEggItem"),
    ("net.minecraft.world.item.BlockItem", "net.minecraft.item.BlockItem"),
    ("net.minecraft.world.item.Item", "net.minecraft.item.Item"),
    ("net.minecraft.world.entity.EntityType", "net.minecraft.entity.EntityType"),
    ("net.minecraft.world.entity.MobCategory", "net.minecraft.entity.EntityClassification"),
    ("net.minecraft.world.entity.LivingEntity", "net.minecraft.entity.LivingEntity"),
    ("net.minecraft.world.entity.PathfinderMob", "net.minecraft.entity.CreatureEntity"),
    ("net.minecraft.world.entity.player.Player", "net.minecraft.entity.player.PlayerEntity"),
    ("net.minecraft.world.entity.Mob", "net.minecraft.entity.MobEntity"),
    ("net.minecraft.world.entity.ai.goal.Goal", "net.minecraft.entity.ai.goal.Goal"),
    ("net.minecraft.world.entity.ai.goal.", "net.minecraft.entity.ai.goal."),
    ("net.minecraft.world.entity.ai.attributes.Attributes", "net.minecraft.entity.ai.attributes.Attributes"),
    ("net.minecraft.world.entity.ai.attributes.AttributeSupplier", "net.minecraft.entity.ai.attributes.AttributeModifierMap"),
    ("net.minecraft.world.level.levelgen.Heightmap.Types.MOTION_BLOCKING_NO_LEAVES",
     "net.minecraft.world.gen.Heightmap.Type.MOTION_BLOCKING_NO_LEAVES"),
    ("net.minecraft.world.level.Level", "net.minecraft.world.World"),
    ("net.minecraft.server.level.ServerLevel", "net.minecraft.world.server.ServerWorld"),
    ("net.minecraft.world.damagesource.DamageSource", "net.minecraft.util.DamageSource"),
    ("net.minecraft.resources.ResourceLocation", "net.minecraft.util.ResourceLocation"),
    ("net.minecraft.sounds.SoundEvent", "net.minecraft.util.SoundEvent"),
    ("net.minecraft.sounds.SoundEvents", "net.minecraft.util.SoundEvents"),
    ("net.minecraft.sounds.SoundSource", "net.minecraft.util.SoundCategory"),
    ("net.minecraft.core.particles.ParticleType", "net.minecraft.particles.ParticleType"),
    ("net.minecraft.core.particles.SimpleParticleType", "net.minecraft.particles.BasicParticleType"),
    ("net.minecraft.world.phys.AABB", "net.minecraft.util.math.AxisAlignedBB"),
    ("net.minecraft.world.phys.Vec3", "net.minecraft.util.math.vector.Vector3d"),
    ("net.minecraft.core.BlockPos", "net.minecraft.util.math.BlockPos"),
    ("net.minecraft.core.Direction", "net.minecraft.util.Direction"),
    ("net.minecraft.nbt.CompoundTag", "net.minecraft.nbt.CompoundNBT"),
    ("net.minecraft.network.syncher.SynchedEntityData", "net.minecraft.network.datasync.EntityDataManager"),
    ("net.minecraft.network.syncher.EntityDataAccessor", "net.minecraft.network.datasync.DataParameter"),
    ("net.minecraft.network.syncher.EntityDataSerializers", "net.minecraft.network.datasync.DataSerializers"),
    ("net.minecraft.world.effect.MobEffectInstance", "net.minecraft.potion.EffectInstance"),
    ("net.minecraft.world.effect.MobEffects", "net.minecraft.potion.Effects"),
    ("net.minecraft.world.effect.MobEffect", "net.minecraft.potion.Effect"),
    ("net.minecraft.world.InteractionResultHolder", "net.minecraft.util.ActionResult"),
    ("net.minecraft.world.InteractionResult", "net.minecraft.util.ActionResultType"),
    ("net.minecraft.world.InteractionHand", "net.minecraft.util.Hand"),
    ("net.minecraft.world.item.crafting.Ingredient", "net.minecraft.item.crafting.Ingredient"),
    ("net.minecraft.client.gui.screens.Screen", "net.minecraft.client.gui.screen.Screen"),
    ("net.minecraft.client.multiplayer.ClientLevel", "net.minecraft.client.world.ClientWorld"),
    ("net.minecraft.client.particle.ParticleEngine", "net.minecraft.client.particle.ParticleManager"),
    ("net.minecraft.core.Registry", "net.minecraft.util.registry.Registry"),
    ("net.minecraft.util.registry.BuiltinRegistries", "net.minecraft.util.registry.BuiltinRegistries"),
    ("net.minecraft.tags.TagKey", "net.minecraft.tags.Tag"),
    ("net.minecraft.world.level.biome.Biome", "net.minecraft.world.biome.Biome"),
    ("getInventory().items", "inventory.items"),
    ("SynchedEntityData.defineId", "EntityDataManager.defineId"),
    ("sendSystemMessage(net.minecraft.util.text.", "sendMessage(net.minecraft.util.text."),
    ("import net.minecraft.client.renderer.entity.EntityRendererProvider;",
     "import net.minecraft.client.renderer.entity.EntityRendererManager;"),
    ("EntityRendererProvider.Context context", "EntityRendererManager manager"),
    ("super(context, new UnseenLegacyModel<T>(), 0.5F)", "super(manager, new UnseenLegacyModel<T>(), 0.5F)"),
    ("context -> new UnseenLegacyRenderer<>(context,", "manager, ctx -> new UnseenLegacyRenderer<>(manager,"),
    ("EntityRendererProvider.Context", "EntityRendererManager"),
    ("public void renderToBuffer(net.minecraft.client.renderer.RenderTypeBuffer ignored,\n"
     "            net.minecraft.client.renderer.MatrixStack matrixStack,\n"
     "            net.minecraft.client.renderer.vertex.IVertexBuilder buffer,\n"
     "            int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {",
     "public void render(com.mojang.blaze3d.matrix.MatrixStack matrixStack,\n"
     "            net.minecraft.client.renderer.vertex.IVertexBuilder buffer,\n"
     "            int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {"),
    ("public void remove(RemovalReason reason) {\n        super.remove(reason);",
     "public void remove() {\n        super.remove();"),
    ("net.minecraft.network.chat.TranslatableComponent(", "net.minecraft.util.text.TranslationTextComponent("),
    ("net.minecraft.network.chat.StringTextComponent(", "net.minecraft.util.text.StringTextComponent("),
    # 1.16.5 member names (official mappings): `level` is a public field.
    ("level()", "level"),
    # Temperature lookup: 1.16.5 Biome#getTemperature(BlockPos).
    ("getBiome(blockPosition()).value().getBaseTemperature()",
     "getBiome(blockPosition()).getTemperature(blockPosition())"),
    # 1.16.5 sendMessage takes the sender UUID.
    ("player.sendSystemMessage(new net.minecraft.util.text.StringTextComponent(msg));",
     "player.sendMessage(new net.minecraft.util.text.StringTextComponent(msg), player.getUUID());"),
    ("player.sendSystemMessage(new net.minecraft.util.text.TranslatableComponent(",
     "player.sendMessage(new net.minecraft.util.text.TranslatableComponent("),
    ("vanilla.getBaseTemperature()",
     "vanilla.getTemperature(new net.minecraft.util.math.BlockPos(x << 2, 0, z << 2))"),
]

# Text components: Component.literal/translatable statics appeared in 1.18.2.
TEXT_REWRITES = [
    ("net.minecraft.network.chat.Component.literal(", "new net.minecraft.network.chat.StringTextComponent("),
    ("net.minecraft.network.chat.Component.translatable(", "new net.minecraft.network.chat.TranslatableComponent("),
    ("Component.literal(", "new net.minecraft.network.chat.StringTextComponent("),
    ("Component.translatable(", "new net.minecraft.network.chat.TranslatableComponent("),
]


def _walk_java(directory):
    for r, _d, files in os.walk(directory):
        for f in files:
            if f.endswith(".java"):
                yield os.path.join(r, f)


def postprocess(root, line_key):
    F = LINES[line_key]
    T = types_for(F)
    line_dir = os.path.join(root, "common/src/line-%s/java" % line_key)
    for path in _walk_java(line_dir):
        with open(path) as fh:
            text = fh.read()
        orig = text
        # Expand short type names to this line's simple class names
        # (ItemGroup -> CreativeModeTab on modern lines, Mob -> MobEntity on
        # legacy).  The lookbehind keeps fully-qualified names untouched.
        for short, full in T.items():
            simple = full.rsplit(".", 1)[-1]
            if simple != short:
                text = re.sub(r"(?<!\.)\b%s\b" % re.escape(short), simple, text)
        if F["expect"] == "dev":
            text = text.replace(
                "me.shedaniel.architectury.registry.DeferredRegister",
                "dev.architectury.registry.registries.DeferredRegister")
            text = text.replace(
                "me.shedaniel.architectury.registry.RegistrySupplier",
                "dev.architectury.registry.registries.RegistrySupplier")
            text = text.replace(
                "me.shedaniel.architectury.registry.EntityAttributeRegistry",
                "dev.architectury.registry.level.entity.EntityAttributeRegistry")
            text = text.replace(
                "me.shedaniel.architectury.registry.EntityRendererRegistry",
                "dev.architectury.registry.client.level.entity.EntityRendererRegistry")
            text = text.replace(
                "me.shedaniel.architectury.registry.ParticleProviderRegistry",
                "dev.architectury.registry.client.particle.ParticleProviderRegistry")
            text = text.replace(ARCH_PKG_OLD, ARCH_PKG_NEW)
        if F["text"] != "component":
            for a, b in TEXT_REWRITES:
                text = text.replace(a, b)
        if F["pkgs"] != "legacy":
            text = text.replace("RemovalReason",
                                "net.minecraft.world.entity.Entity.RemovalReason")
        if line_key in ("1.21", "1.21.2", "1.21.3", "1.21.4", "1.21.5", "1.21.9", "26"):
            text = text.replace(
                "int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {",
                "int packedLight, int packedOverlay, int packedColor) {")
            text = text.replace(
                "matrixStack, buffer, packedLight, packedOverlay, red, green, blue, alpha);",
                "matrixStack, buffer, packedLight, packedOverlay, packedColor);")
        if F["pkgs"] == "legacy":
            for a, b in LEGACY_REWRITES:
                text = text.replace(a, b)
            text = re.sub(
                r"player\.sendMessage\(new net\.minecraft\.util\.text\.TranslatableComponent\((.*?)\)\);",
                r"player.sendMessage(new net.minecraft.util.text.TranslatableComponent(\1), player.getUUID());",
                text)
        if text != orig:
            with open(path, "w") as fh:
                fh.write(text)


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..")
    root = os.path.abspath(root)
    print("Generating Biomes Unseen into", root)

    # Remove previously generated trees so renamed/deleted files never linger.
    import shutil
    generated = ["common", "build.gradle", "settings.gradle", "gradle.properties",
                 "gradlew", "gradlew.bat", "gradle", "README.md", "BUILD.md"]
    for name in os.listdir(root):
        if name.startswith(("fabric-", "forge-", "neoforge-", "data-")):
            generated.append(name)
    for name in generated:
        path = os.path.join(root, name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    print("  root build files ...")
    emit_root.emit(root)

    print("  common core ...")
    emit_common.emit(root)

    for line_key in LINES:
        print("  line %s ..." % line_key)
        emit_families.emit(root, line_key)
        emit_families2.emit_registries(root, line_key)
        emit_worldgen.emit_worldgen(root, line_key)
        emit_entities.emit_entities(root, line_key)
        emit_client_datagen.emit_client_datagen(root, line_key)
        postprocess(root, line_key)

    print("  assets ...")
    emit_assets.emit(root)

    print("  datapack data trees ...")
    emit_data.emit(root)

    print("  platform modules ...")
    emit_platforms.emit(root)

    n = sum(len(files) for r, _d, files in os.walk(root) if ".git" not in r)
    print("Done. Files in tree (excluding .git):", n)


if __name__ == "__main__":
    main()
