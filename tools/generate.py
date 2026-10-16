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
    # Minecraft 1.16.5's *official Mojang* mappings already use the modern
    # layout - verified with javap against the real 1.16.5 jar:
    #   net.minecraft.world.entity.Mob / EntityType / MobCategory
    #   net.minecraft.world.entity.player.Player
    #   net.minecraft.world.level.Level, world.InteractionResult,
    #   world.InteractionHand, network.syncher.EntityDataAccessor,
    #   core.particles.SimpleParticleType, world.item.CreativeModeTab,
    #   client.model.geom.ModelPart, client.renderer.entity.MobRenderer
    # all exist there.  The legacy templates were written with MCP names, so
    # they are translated to Mojang names instead of the other way round.
]

# MCP (Forge 1.16.5) name -> official Mojang mapping name.
LEGACY_MOJANG_FQN = [
    ("net.minecraft.entity.ai.goal.", "net.minecraft.world.entity.ai.goal."),
    ("net.minecraft.entity.ai.attributes.EntityAttributes",
     "net.minecraft.world.entity.ai.attributes.Attributes"),
    ("net.minecraft.entity.ai.attributes.", "net.minecraft.world.entity.ai.attributes."),
    ("net.minecraft.entity.player.PlayerEntity", "net.minecraft.world.entity.player.Player"),
    ("net.minecraft.entity.player.", "net.minecraft.world.entity.player."),
    ("net.minecraft.entity.MobEntity", "net.minecraft.world.entity.Mob"),
    ("net.minecraft.entity.LivingEntity", "net.minecraft.world.entity.LivingEntity"),
    ("net.minecraft.entity.EntityType", "net.minecraft.world.entity.EntityType"),
    ("net.minecraft.entity.MobCategory", "net.minecraft.world.entity.MobCategory"),
    ("net.minecraft.entity.Entity", "net.minecraft.world.entity.Entity"),
    ("net.minecraft.world.World", "net.minecraft.world.level.Level"),
    ("net.minecraft.util.ActionResultType", "net.minecraft.world.InteractionResult"),
    ("net.minecraft.util.Hand", "net.minecraft.world.InteractionHand"),
    ("net.minecraft.util.DamageSource", "net.minecraft.world.damagesource.DamageSource"),
    ("net.minecraft.util.SoundEvent", "net.minecraft.sounds.SoundEvent"),
    ("net.minecraft.util.math.BlockPos", "net.minecraft.core.BlockPos"),
    ("net.minecraft.util.math.Vec3d", "net.minecraft.world.phys.Vec3"),
    ("net.minecraft.util.registry.Registry", "net.minecraft.core.Registry"),
    ("net.minecraft.util.Identifier", "net.minecraft.resources.ResourceLocation"),
    ("net.minecraft.network.datasync.DataParameter",
     "net.minecraft.network.syncher.EntityDataAccessor"),
    ("net.minecraft.network.datasync.", "net.minecraft.network.syncher."),
    ("net.minecraft.particles.BasicParticleType",
     "net.minecraft.core.particles.SimpleParticleType"),
    ("net.minecraft.item.ItemGroup", "net.minecraft.world.item.CreativeModeTab"),
    ("net.minecraft.item.", "net.minecraft.world.item."),
    ("net.minecraft.block.", "net.minecraft.world.level.block."),
    ("net.minecraft.inventory.EquipmentSlotType", "net.minecraft.world.entity.EquipmentSlot"),
    ("net.minecraft.nbt.CompoundNBT", "net.minecraft.nbt.CompoundTag"),
    ("net.minecraft.client.renderer.entity.MobEntityRenderer",
     "net.minecraft.client.renderer.entity.MobRenderer"),

("net.minecraft.entity.CreatureEntity", "net.minecraft.world.entity.PathfinderMob"),
    ("net.minecraft.entity.PathfinderEntity", "net.minecraft.world.entity.PathfinderMob"),
    ("net.minecraft.entity.AgeableEntity", "net.minecraft.world.entity.AgeableMob"),
    ("net.minecraft.entity.monster.", "net.minecraft.world.entity.monster."),
    ("net.minecraft.entity.animal.", "net.minecraft.world.entity.animal."),
    ("net.minecraft.entity.passive.", "net.minecraft.world.entity.animal."),
    ("net.minecraft.util.ResourceLocation", "net.minecraft.resources.ResourceLocation"),
    ("net.minecraft.util.Identifier", "net.minecraft.resources.ResourceLocation"),
    ("net.minecraft.util.RegistryKey", "net.minecraft.resources.ResourceKey"),
    ("net.minecraft.util.math.AxisAlignedBB", "net.minecraft.world.phys.AABB"),
    ("net.minecraft.util.math.ChunkPos", "net.minecraft.world.level.ChunkPos"),
    ("net.minecraft.util.text.TranslationTextComponent",
     "net.minecraft.network.chat.TranslatableComponent"),
    ("net.minecraft.util.text.StringTextComponent", "net.minecraft.network.chat.TextComponent"),
    ("net.minecraft.network.syncher.DataSerializers", "net.minecraft.network.syncher.EntityDataSerializers"),
    ("net.minecraft.network.syncher.EntityDataManager", "net.minecraft.network.syncher.SynchedEntityData"),
    ("net.minecraft.network.chat.StringTextComponent", "net.minecraft.network.chat.TextComponent"),
    ("net.minecraft.network.chat.contents.LiteralContents", "net.minecraft.network.chat.TextComponent"),
    ("Component.literal(", "new net.minecraft.network.chat.TextComponent("),
    ("Component.translatable(", "new net.minecraft.network.chat.TranslatableComponent("),
]

# Bare MCP identifiers -> Mojang identifiers (word-boundary safe).
LEGACY_MOJANG_ID = [
    (r"\bMobEntity\b", "Mob"),
    (r"\bPlayerEntity\b", "Player"),
    (r"\bActionResultType\b", "InteractionResult"),
    (r"\bDataParameter\b", "EntityDataAccessor"),
    (r"\bBasicParticleType\b", "SimpleParticleType"),
    (r"\bItemGroup\b", "CreativeModeTab"),
    (r"\bEquipmentSlotType\b", "EquipmentSlot"),
    (r"\bEntityAttributes\b", "Attributes"),
    (r"\bSwimGoal\b", "FloatGoal"),
    (r"\bWaterAvoidingRandomWalkingGoal\b", "WaterAvoidingRandomStrollGoal"),
    (r"\bCompoundNBT\b", "CompoundTag"),
    (r"(?<![.\w])World(?![.\w])", "Level"),
    (r"(?<![.\w])Hand(?![.\w])", "InteractionHand"),

(r"\bCreatureEntity\b", "PathfinderMob"),
    (r"\bAgeableEntity\b", "AgeableMob"),
    (r"\bDataSerializers\b", "EntityDataSerializers"),
    (r"\bEntityDataManager\b", "SynchedEntityData"),
    (r"\bAxisAlignedBB\b", "AABB"),
    (r"\bRegistryKey\b", "ResourceKey"),
    (r"\bTranslationTextComponent\b", "TranslatableComponent"),
    (r"\bStringTextComponent\b", "TextComponent"),
]

# net.minecraft.core.registries.Registries arrived in 1.19.3; older lines use
# net.minecraft.core.Registry with the *_REGISTRY constants.
NO_REGISTRIES_LINES = ("1.16.5", "1.17.1", "1.18", "1.18.1", "1.19", "1.19.1", "1.19.2")

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
            for a, b in LEGACY_MOJANG_FQN:
                text = text.replace(a, b)
            for pat, rep in LEGACY_MOJANG_ID:
                text = re.sub(pat, rep, text)
        if line_key in NO_REGISTRIES_LINES:
            text = text.replace("import net.minecraft.core.registries.Registries;",
                                "import net.minecraft.core.Registry;")
            for name in ("BLOCK", "ITEM", "ENTITY_TYPE", "FLUID"):
                text = text.replace("Registries." + name, "Registry." + name + "_REGISTRY")
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
