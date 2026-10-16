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
from lines import LINES, MC_TO_LINE, types_for
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
    ("net.minecraft.world.server.ServerWorld", "net.minecraft.server.level.ServerLevel"),
    ("net.minecraft.world.server.", "net.minecraft.server.level."),
    ("net.minecraft.entity.ai.attributes.AttributeModifierMap.MutableAttribute",
     "net.minecraft.world.entity.ai.attributes.AttributeSupplier.Builder"),
    ("net.minecraft.entity.ai.attributes.AttributeModifierMap",
     "net.minecraft.world.entity.ai.attributes.AttributeSupplier"),
    ("net.minecraft.network.chat.contents.LiteralContents", "net.minecraft.network.chat.TextComponent"),
    ("public void remove(RemovalReason reason)",
     "public void remove(net.minecraft.world.entity.Entity.RemovalReason reason)"),
    ("super.remove(reason);", "super.remove(reason);"),
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
    (r"\bServerWorld\b", "ServerLevel"),
    (r"\bAttributeModifierMap\.MutableAttribute\b", "AttributeSupplier.Builder"),
    (r"\bAttributeModifierMap\b", "AttributeSupplier"),
]

# net.minecraft.core.registries.Registries arrived in 1.19.3; older lines use
# net.minecraft.core.Registry with the *_REGISTRY constants.
NO_REGISTRIES_LINES = ("1.16.5", "1.17.1", "1.18", "1.18.1", "1.19", "1.19.1", "1.19.2")

# The jigsaw Structure class and StructureSeparationSettings arrived in 1.19;
# on 1.17.1/1.18.1 the legacy registrar works off StructureFeature instead.
NO_STRUCTURE_CLASS_LINES = ("1.17.1", "1.18.1")

# Text components: Component.literal/translatable statics appeared in 1.18.2.
TEXT_REWRITES = [
    ("net.minecraft.network.chat.Component.literal(", "new net.minecraft.network.chat.StringTextComponent("),
    ("net.minecraft.network.chat.Component.translatable(", "new net.minecraft.network.chat.TranslatableComponent("),
    ("Component.literal(", "new net.minecraft.network.chat.StringTextComponent("),
    ("Component.translatable(", "new net.minecraft.network.chat.TranslatableComponent("),
]


# ---------------------------------------------------------------------------
# API-drift layer
#
# Minecraft's Mojang-mapped API moves between releases.  The per-line templates
# emit one canonical spelling; this layer rewrites it to whatever the line's
# Minecraft version actually offers.  Every rule is taken from the javap probes
# committed in docs/api-probe, not from memory.
# ---------------------------------------------------------------------------

# Oldest -> newest, so "rank >= X" means "this API change has happened".
_LINE_ORDER = ["1.16.5", "1.17.1", "1.18.1", "1.18", "1.19.3", "1.19.4",
               "1.20.2", "1.20.5", "1.21", "1.21.2", "1.21.4", "1.21.5",
               "1.21.9", "26"]
LINE_RANK = {k: i for i, k in enumerate(_LINE_ORDER)}

# probe-fabric-1.21+: ResourceLocation(String,String) is private; the public
# entry points are the fromNamespaceAndPath/parse/withDefaultNamespace factories.
RL_PRIVATE_CTOR_FROM = "1.21"
# probe-fabric-1.21.2+: EntityType$Builder.build(ResourceKey<EntityType<?>>),
# ArmorMaterial/ArmorType live in net.minecraft.world.item.equipment, and
# Item.use returns InteractionResult (InteractionResultHolder was removed).
EQUIPMENT_FROM = "1.21.2"
# 1.19.3+: SoundEvents.* are Holder.Reference<SoundEvent>, not SoundEvent.
SOUND_HOLDER_FROM = "1.19.3"

_MOD_ID = "com.biomesunseen.core.ModConstants.MOD_ID"

# new ItemStack(ModItems.GEAR.get("x"))            -> ...get("x").get()
# new ItemStack(ModItems.TROPHIES.get("x"), 3)     -> ...get("x").get(), 3)
_RE_ITEMSTACK_SUPPLIER = re.compile(
    r'new ItemStack\((ModItems\.[A-Za-z_]+\.get\("[^"]*"\))((?:\s*,[^)]*)?)\)')
# level.isClientSide -> level.isClientSide()
_RE_CLIENTSIDE = re.compile(r'(?<=\.)isClientSide(?![\w(])')
# playSound(SoundEvents.RAID_HORN, ...) -> playSound(SoundEvents.RAID_HORN.value(), ...)
_RE_SOUND_HOLDER = re.compile(r'playSound\(SoundEvents\.([A-Z_0-9]+)\s*,')
# new ResourceLocation(ns, path) / new ResourceLocation(single)
_RE_RL_TWO = re.compile(
    r'new (?:net\.minecraft\.resources\.)?ResourceLocation\(\s*([^()]*?)\s*,\s*([^()]*?)\s*\)')
_RE_RL_ONE = re.compile(
    r'new (?:net\.minecraft\.resources\.)?ResourceLocation\(\s*([^(),]*?)\s*\)')
# ArmorType used as a bare type name
_RE_ARMOR_TYPE = re.compile(r'(?<![.\w])ArmorType(?![\w])')
# EntityType builder: .build("siltstrider")
_RE_ENTITY_BUILD = re.compile(r'\.build\("([a-z0-9_/]+)"\)')
# Item.use return type and the InteractionResultHolder factories
_RE_IRH_TYPE = re.compile(r'InteractionResultHolder<\s*ItemStack\s*>')
_RE_IRH_FACTORY = re.compile(r'InteractionResultHolder\.(success|consume|pass|fail)\([^()]*\)')
# MeleeAttackGoal.checkAndPerformAttack lost its distance parameter in 1.20.2
# (probe-fabric-1.19.4: (LivingEntity,double); probe-fabric-1.20.4: (LivingEntity)).
CHECK_ATTACK_TWO_ARG_BEFORE = "1.20.2"
# 1.19.3+: SoundEvents.* are Holder.Reference<SoundEvent>.
# 1.20.5+: MobEffects.* are Holder<MobEffect> and MobEffectInstance takes one.
MOB_EFFECT_HOLDER_FROM = "1.20.5"

_RE_CHECK_ATTACK_DECL = re.compile(
    r'protected void checkAndPerformAttack\((LivingEntity|[A-Za-z.]*LivingEntity) (\w+)\) \{')
_RE_CHECK_ATTACK_SUPER = re.compile(
    r'super\.checkAndPerformAttack\((\w+)\);')
_RE_WRAP_AS_HOLDER = re.compile(
    r'BuiltInRegistries\.SOUND_EVENT\.wrapAsHolder\((SoundEvents\.[A-Z_0-9]+)\)')
_RE_EFFECT_FOR_TYPE = re.compile(
    r'net\.minecraft\.world\.effect\.MobEffect effectFor\(')
# probe-fabric-1.21.5: Entity.spawnAtLocation gained a leading ServerLevel
# parameter (all four overloads), so the item-drop calls need a server check.
SPAWN_AT_LOCATION_NEEDS_LEVEL_FROM = "1.21.5"

# probe-fabric-1.21.2: Entity.isInvulnerableTo gained a leading ServerLevel and
# Entity.hurt stopped returning boolean; both changed in the same release.
HURT_VOID_FROM = "1.21.2"

_HURT_BOOLEAN_IMPL = """    @Override
    public boolean hurt(DamageSource source, float amount) {
        boolean hurt = super.hurt(source, amount);
        if (hurt) {
            triggerAnim(\"hurt\");
        }
        return hurt;
    }"""

_HURT_VOID_IMPL = """    @Override
    public void hurt(DamageSource source, float amount) {
        float healthBefore = getHealth();
        super.hurt(source, amount);
        if (getHealth() < healthBefore) {
            triggerAnim(\"hurt\");
        }
    }"""

_INVULN_ONE_ARG = """    public boolean isInvulnerableTo(DamageSource source) {
        return phaseShiftTicks > 0 || super.isInvulnerableTo(source);"""
_INVULN_TWO_ARG = """    public boolean isInvulnerableTo(net.minecraft.server.level.ServerLevel level,
            DamageSource source) {
        return phaseShiftTicks > 0 || super.isInvulnerableTo(level, source);"""

# Inventory.items went private; isEmpty() is public on every version and means
# exactly "no non-empty stack", which is what the trade goal was testing.
_INVENTORY_ITEMS = ("!customer.getInventory().items.stream().anyMatch(s -> !s.isEmpty())",
                    "customer.getInventory().isEmpty()")

# "net.minecraft.world.phys.AABB box = new AABB(...)" - the declaration is
# qualified but the constructor is not, and nothing imports the short name.
_RE_NEW_AABB = re.compile(r'(?<![.\w])new AABB\(')

_RE_PACKAGE_LINE = re.compile(r'^(package [^\n]+\n)', re.M)


def _ensure_import(text, fqn):
    """Insert an import right after the package statement if not already there."""
    stmt = "import %s;" % fqn
    if stmt in text:
        return text
    return _RE_PACKAGE_LINE.sub(r'\1\n' + stmt + "\n", text, count=1)


def _rewrite_spawn_at_location(text):
    """Wrap bare spawnAtLocation(stack) calls in a ServerLevel guard.

    From 1.21.5 every Entity.spawnAtLocation overload takes the ServerLevel as
    its first argument.  The call sites are statements inside entity classes, so
    each one becomes a block that resolves the level and drops only server-side.
    Arguments are matched with a paren/quote-aware scan because they nest
    (new ItemStack(minerals.get(getRandom().nextInt(...)).get(), 3 + ...)).
    """
    out = []
    i = 0
    needle = "spawnAtLocation("
    while True:
        j = text.find(needle, i)
        if j < 0:
            out.append(text[i:])
            break
        # A qualified call (x.spawnAtLocation) targets another entity, and an
        # already-guarded one starts with our own dropServer parameter: skip both
        # so the rewrite stays idempotent.
        rest = text[j + len(needle):]
        if text[max(0, j - 1):j] == "." or rest.startswith("(net.minecraft.server.level.ServerLevel) dropLevel"):
            out.append(text[i:j + len(needle)])
            i = j + len(needle)
            continue
        k = j + len(needle)
        depth = 1
        in_str = False
        while k < len(text) and depth:
            c = text[k]
            if in_str:
                if c == "\\":
                    k += 2
                    continue
                if c == '"':
                    in_str = False
            elif c == '"':
                in_str = True
            elif c in "([{":
                depth += 1
            elif c in ")]}":
                depth -= 1
            k += 1
        args = text[j + len(needle):k - 1]
        # Swallow the statement's own semicolon; the guard block supplies its own.
        if k < len(text) and text[k] == ";":
            k += 1
        out.append(text[i:j])
        # Classic instanceof + cast rather than a Java 16 pattern binding: it is
        # valid on every toolchain in the matrix and keeps the generated tree
        # parseable by the pre-flight syntax check in tools/.
        out.append(
            "{\n"
            "                net.minecraft.world.level.Level dropLevel =\n"
            "                        com.biomesunseen.util.EntityLevels.of(this);\n"
            "                if (dropLevel instanceof net.minecraft.server.level.ServerLevel) {\n"
            "                    spawnAtLocation((net.minecraft.server.level.ServerLevel) dropLevel,\n"
            "                            " + args + ");\n"
            "                }\n"
            "            }")
        i = k
    return "".join(out)


def apply_api_drift(text, line_key):
    rank = LINE_RANK[line_key]

    # Level.isClientSide went private in 1.21.9; isClientSide() exists on every
    # version, so the accessor is always the safe spelling.
    text = _RE_CLIENTSIDE.sub('isClientSide()', text)

    # RegistrySupplier is not an ItemLike - unwrap it before new ItemStack().
    text = _RE_ITEMSTACK_SUPPLIER.sub(r'new ItemStack(\1.get()\2)', text)

    if rank >= LINE_RANK[SOUND_HOLDER_FROM]:
        text = _RE_SOUND_HOLDER.sub(r'playSound(SoundEvents.\1.value(),', text)

    if rank >= LINE_RANK[RL_PRIVATE_CTOR_FROM]:
        text = _RE_RL_TWO.sub(
            r'net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(\1, \2)',
            text)
        text = _RE_RL_ONE.sub(
            r'net.minecraft.resources.ResourceLocation.parse(\1)', text)

    if rank >= LINE_RANK[EQUIPMENT_FROM]:
        # ArmorItem.Type moved out to net.minecraft.world.item.equipment.ArmorType.
        if "ArmorItem.Type" in text:
            text = text.replace("ArmorItem.Type", "ArmorType")
        if _RE_ARMOR_TYPE.search(text):
            text = _ensure_import(text, "net.minecraft.world.item.equipment.ArmorType")

        # EntityType.Builder.build now wants a ResourceKey, not a String id.
        text = _RE_ENTITY_BUILD.sub(
            '.build(net.minecraft.resources.ResourceKey.create('
            'net.minecraft.core.registries.Registries.ENTITY_TYPE, '
            'net.minecraft.resources.ResourceLocation.fromNamespaceAndPath('
            + _MOD_ID + r', "\1")))',
            text)

        # Item.use returns InteractionResult; InteractionResultHolder is gone.
        text = text.replace("import net.minecraft.world.InteractionResultHolder;\n", "")
        text = _RE_IRH_TYPE.sub('InteractionResult', text)
        text = _RE_IRH_FACTORY.sub(
            lambda m: "InteractionResult." + m.group(1).upper(), text)

    # -- SoundEvents.X has been a Holder since 1.19.3, so wrapAsHolder() on it
    #    is a type error; pass the holder straight through.
    if rank >= LINE_RANK[SOUND_HOLDER_FROM]:
        text = _RE_WRAP_AS_HOLDER.sub(r'\1', text)

    # -- 1.20.5+: MobEffects.* are Holder<MobEffect> and MobEffectInstance takes
    #    the holder, so effectFor() must return the holder too.
    if rank >= LINE_RANK[MOB_EFFECT_HOLDER_FROM]:
        text = _RE_EFFECT_FOR_TYPE.sub(
            'net.minecraft.core.Holder<net.minecraft.world.effect.MobEffect> effectFor(',
            text)

    # -- Before 1.20.2 checkAndPerformAttack still takes the attack distance.
    if rank < LINE_RANK[CHECK_ATTACK_TWO_ARG_BEFORE]:
        text = _RE_CHECK_ATTACK_DECL.sub(
            r'protected void checkAndPerformAttack(\1 \2, double distance) {', text)
        text = _RE_CHECK_ATTACK_SUPER.sub(
            r'super.checkAndPerformAttack(\1, distance);', text)

    # -- 1.21.5+: spawnAtLocation takes the ServerLevel first.
    if rank >= LINE_RANK[SPAWN_AT_LOCATION_NEEDS_LEVEL_FROM]:
        text = _rewrite_spawn_at_location(text)

    # -- 1.21.2+: Entity.hurt returns void, isInvulnerableTo takes the ServerLevel.
    if rank >= LINE_RANK[HURT_VOID_FROM]:
        text = text.replace(_HURT_BOOLEAN_IMPL, _HURT_VOID_IMPL)
        text = text.replace(_INVULN_ONE_ARG, _INVULN_TWO_ARG)

    # -- Inventory.items is private; isEmpty() says the same thing publicly.
    text = text.replace(_INVENTORY_ITEMS[0], _INVENTORY_ITEMS[1])

    text = _RE_NEW_AABB.sub('new net.minecraft.world.phys.AABB(', text)

    # -- Particle declares render(VertexConsumer,Camera,float) abstract and has
    #    no setSpriteFromAge(); TextureSheetParticle is the sprite-particle base
    #    that supplies both on every version.
    text = text.replace("public class UnseenParticle extends Particle {",
                        "public class UnseenParticle extends TextureSheetParticle {")
    text = text.replace("import net.minecraft.client.particle.Particle;\n"
                        "import net.minecraft.client.particle.ParticleProvider;",
                        "import net.minecraft.client.particle.Particle;\n"
                        "import net.minecraft.client.particle.ParticleProvider;\n"
                        "import net.minecraft.client.particle.TextureSheetParticle;")

    return text


def _walk_java(directory):
    for r, _d, files in os.walk(directory):
        for f in files:
            if f.endswith(".java"):
                yield os.path.join(r, f)


def _rewrite_text(text, F, T, line_key):
    """Shared line-specific source rewrite, used for common/src/line-* and for
    the per-loader platform modules so both trees see identical names."""
    for short, full in T.items():
        simple = full.rsplit(".", 1)[-1]
        if simple != short:
            text = re.sub(r"(?<!\.)\b%s\b" % re.escape(short), simple, text)
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
            # Word-boundary + lookbehind: a bare "Registries.ITEM" is the vanilla
            # registry constant, but "ModRegistries.ITEMS" is our own DeferredRegister
            # holder. The old str.replace() matched inside it and produced
            # "ModRegistry.ITEM_REGISTRYS" -> "package ModRegistry does not exist".
            text = re.sub(r"(?<![A-Za-z])Registries\." + name + r"(?![A-Za-z])",
                          "Registry." + name + "_REGISTRY", text)
    text = apply_api_drift(text, line_key)
    return text


def postprocess_platforms(root):
    """The per-loader modules (fabric-*/forge-*/neoforge-*) compile their own
    sources alongside common/src/line-*, so they must get the very same
    MCP -> Mojang translation.  Skipping them is what produced
    'PlatformExpectImpl.java:36: package net.minecraft.entity does not exist'
    on fabric-1.16.5 while common/src/line-1.16.5 was already clean."""
    for name in sorted(os.listdir(root)):
        m = re.match(r"^(?:fabric|forge|neoforge)-(.+)$", name)
        if not m:
            continue
        line_key = MC_TO_LINE.get(m.group(1))
        if not line_key:
            continue
        F = LINES[line_key]
        T = types_for(F)
        src = os.path.join(root, name, "src", "main", "java")
        if not os.path.isdir(src):
            continue
        for path in _walk_java(src):
            with open(path) as fh:
                text = fh.read()
            new = _rewrite_text(text, F, T, line_key)
            if new != text:
                with open(path, "w") as fh:
                    fh.write(new)


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
        if line_key in ("1.21.5", "1.21.9", "26"):
            # 1.21.5 removed net.minecraft.world.item.ArmorItem alongside
            # SwordItem/PickaxeItem, and ArmorItem$Type became
            # net.minecraft.world.item.equipment.ArmorType from 1.21.2.
            text = text.replace("import net.minecraft.world.item.ArmorItem;\n", "")
            text = text.replace("extends ArmorItem {", "extends Item {")
            text = text.replace("ArmorItem.Type", "ArmorType")
            text = text.replace("material.holder(), slot, properties", "properties")
            if "import net.minecraft.world.item.equipment.ArmorType;" not in text \
                    and "ArmorType" in text:
                text = text.replace("import net.minecraft.world.item.equipment.ArmorMaterial;",
                                    "import net.minecraft.world.item.equipment.ArmorMaterial;\n"
                                    "import net.minecraft.world.item.equipment.ArmorType;", 1)
        if line_key in NO_REGISTRIES_LINES:
            text = text.replace("import net.minecraft.core.registries.Registries;",
                                "import net.minecraft.core.Registry;")
            for name in ("BLOCK", "ITEM", "ENTITY_TYPE", "FLUID"):
                # Word-boundary + lookbehind: a bare "Registries.ITEM" is the vanilla
                # registry constant, but "ModRegistries.ITEMS" is our own DeferredRegister
                # holder. The old str.replace() matched inside it and produced
                # "ModRegistry.ITEM_REGISTRYS" -> "package ModRegistry does not exist".
                text = re.sub(r"(?<![A-Za-z])Registries\." + name + r"(?![A-Za-z])",
                              "Registry." + name + "_REGISTRY", text)
            text = re.sub(
                r"player\.sendMessage\(new net\.minecraft\.util\.text\.TranslatableComponent\((.*?)\)\);",
                r"player.sendMessage(new net.minecraft.util.text.TranslatableComponent(\1), player.getUUID());",
                text)
        text = apply_api_drift(text, line_key)
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

    print("  platform sources ...")
    postprocess_platforms(root)

    n = sum(len(files) for r, _d, files in os.walk(root) if ".git" not in r)
    print("Done. Files in tree (excluding .git):", n)


if __name__ == "__main__":
    main()
