# -*- coding: utf-8 -*-
"""Minecraft version 'lines' - API-homogeneous groups sharing one source tree.

Each line gets its own complete common source tree (Java + data resources) so
every module compiles against the exact API generation of its Minecraft
version.  Flags drive the template in emit_families.py / emit_data.py.
"""

# pkgs:       "legacy" (1.16.5 class packages) | "modern" (1.17+ world.level packages)
# reg:        registry constant generation
# geckolib:   "none" | "g3" | "g4"
# data:       static datapack resource style
# tab:        "old" (ItemGroup) | "new" (CreativeModeTab.builder)
# damage:     "old" (DamageSource.GENERIC) | "new" (level.damageSources())
# synched:    "old" (defineSynchedData()) | "builder" (defineSynchedData(Builder))
# text:       "legacy" | "translatable_class" | "component"
# material:   whether Material exists in BlockBehaviour.Properties
# sound_ctor: "new" (new SoundEvent(rl)) | "factory" (SoundEvent.createVariableRangeEvent)
# data_dirs:  "plural" (loot_tables/, recipes/) | "flat" (loot_table/, recipe/)
# biome_json: "old" (precipitation) | "new" (has_precipitation)
# worldgen:   "legacy" (no placed_feature) | "noise" | "modern" (structure_set era)
# biome_add:  how biomes enter the overworld
# item_def:   "model_only" | "items_dir" (assets/<ns>/items/*.json)
# expect:     ExpectPlatform annotation package

LINES = {
    "1.16.5": dict(
        line="1.16.5", mc="1.16.5", java=8, pkgs="legacy", reg="util_registry",
        geckolib="none", tab="old", damage="old", synched="old",
        text="legacy", material=True, sound_ctor="new", data_dirs="plural",
        biome_json="old", worldgen="legacy", biome_add="mixin_legacy",
        item_def="model_only", expect="me.shedaniel", entity_base="legacy",
        tagkey=False, features="legacy", structures="legacy",
    ),
    "1.17.1": dict(
        line="1.17.1", mc="1.17.1", java=16, pkgs="modern", reg="core_registry",
        geckolib="none", tab="old", damage="old", synched="old",
        text="translatable_class", material=True, sound_ctor="new",
        data_dirs="plural", biome_json="old", worldgen="legacy",
        biome_add="mixin_legacy", item_def="model_only", expect="dev",
        entity_base="modern", tagkey=False, features="legacy", structures="legacy",
    ),
    "1.18.1": dict(
        line="1.18.1", mc="1.18.1", java=17, pkgs="modern", reg="core_registry",
        geckolib="none", tab="old", damage="old", synched="old",
        text="translatable_class", material=True, sound_ctor="new", data_dirs="plural",
        biome_json="old", worldgen="noise", biome_add="mixin_legacy",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=False, features="placed", structures="legacy",
    ),
    "1.18": dict(
        line="1.18", mc="1.18.2", java=17, pkgs="modern", reg="core_registry",
        geckolib="none", tab="old", damage="old", synched="old",
        text="translatable_class", material=True, sound_ctor="new", data_dirs="plural",
        biome_json="old", worldgen="noise", biome_add="noise_list",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.19": dict(
        line="1.19", mc="1.19", java=17, pkgs="modern", reg="core_registry",
        geckolib="none", tab="old", damage="old", synched="old",
        text="component", material=True, sound_ctor="new", data_dirs="plural",
        biome_json="old", worldgen="noise", biome_add="noise_list",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.20": dict(
        line="1.20", mc="1.20.1", java=17, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="old",
        text="component", material=False, sound_ctor="factory",
        data_dirs="plural", biome_json="new", worldgen="modern",
        biome_add="noise_list", item_def="model_only", expect="dev",
        entity_base="modern", tagkey=True, features="placed", structures="sets",
    ),
    "1.19.3": dict(
        line="1.19.3", mc="1.19.3", java=17, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="old", synched="old",
        text="component", material=True, sound_ctor="factory", data_dirs="plural",
        biome_json="new", worldgen="noise", biome_add="noise_list",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.19.4": dict(
        line="1.19.4", mc="1.19.4", java=17, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="old",
        text="component", material=True, sound_ctor="factory", data_dirs="plural",
        biome_json="new", worldgen="modern", biome_add="noise_list",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.20.2": dict(
        line="1.20.2", mc="1.20.4", java=17, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="old",
        text="component", material=False, sound_ctor="factory", data_dirs="plural",
        biome_json="new", worldgen="modern", biome_add="noise_list",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.20.5": dict(
        line="1.20.5", mc="1.20.6", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="plural",
        biome_json="new", worldgen="modern", biome_add="noise_list",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.21": dict(
        line="1.21", mc="1.21.1", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="new", worldgen="modern", biome_add="noise_list",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.21.2": dict(
        line="1.21.2", mc="1.21.3", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="list", worldgen="modern", biome_add="noise_list",
        item_def="items_dir", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.21.4": dict(
        line="1.21.4", mc="1.21.4", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="list", worldgen="modern", biome_add="noise_list",
        item_def="items_dir", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.21.5": dict(
        line="1.21.5", mc="1.21.8", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="list", worldgen="modern", biome_add="noise_list",
        item_def="items_dir", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.21.9": dict(
        line="1.21.9", mc="1.21.11", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="list", worldgen="modern", biome_add="noise_list",
        item_def="items_dir", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.21.11": dict(
        line="1.21.11", mc="1.21.11", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory",
        data_dirs="flat", biome_json="list", worldgen="modern",
        biome_add="noise_list", item_def="items_dir", expect="dev",
        entity_base="modern", tagkey=True, features="placed", structures="sets",
    ),
    "26": dict(
        line="26", mc="26.3", java=25, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="attrs", worldgen="modern", biome_add="noise_list",
        item_def="items_dir", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
}

# Which line serves each target Minecraft version.
MC_TO_LINE = {
    "1.16.5": "1.16.5",
    "1.17.1": "1.17.1",
    "1.18.1": "1.18.1",
    "1.18.2": "1.18",
    "1.19": "1.19", "1.19.1": "1.19", "1.19.2": "1.19",
    "1.19.3": "1.19.3",
    "1.19.4": "1.19.4", "1.20": "1.20", "1.20.1": "1.20",
    "1.20.2": "1.20.2", "1.20.3": "1.20.2", "1.20.4": "1.20.2",
    "1.20.5": "1.20.5", "1.20.6": "1.20.5",
    "1.21": "1.21", "1.21.1": "1.21",
    "1.21.2": "1.21.2", "1.21.3": "1.21.2",
    "1.21.4": "1.21.4",
    "1.21.5": "1.21.5", "1.21.6": "1.21.5", "1.21.7": "1.21.5", "1.21.8": "1.21.5",
    "1.21.9": "1.21.9", "1.21.10": "1.21.9",
    "1.21.11": "1.21.11",
    "26.1": "26", "26.1.1": "26", "26.1.2": "26", "26.2": "26", "26.3": "26",
}

# Mojang-mapping type names per package generation.
MODERN_TYPES = {
    "Block": "net.minecraft.world.level.block.Block",
    "BlockBehaviour": "net.minecraft.world.level.block.state.BlockBehaviour",
    "Blocks": "net.minecraft.world.level.block.Blocks",
    "SoundType": "net.minecraft.world.level.block.SoundType",
    "BlockState": "net.minecraft.world.level.block.state.BlockState",
    "BlockPos": "net.minecraft.core.BlockPos",
    "Direction": "net.minecraft.core.Direction",
    "Item": "net.minecraft.world.item.Item",
    "BlockItem": "net.minecraft.world.item.BlockItem",
    "Items": "net.minecraft.world.item.Items",
    "ItemStack": "net.minecraft.world.item.ItemStack",
    "ItemGroup": "net.minecraft.world.item.CreativeModeTab",
    "SpawnEggItem": "net.minecraft.world.item.SpawnEggItem",
    "Tier": "net.minecraft.world.item.Tier",
    "SwordItem": "net.minecraft.world.item.SwordItem",
    "PickaxeItem": "net.minecraft.world.item.PickaxeItem",
    "ArmorItem": "net.minecraft.world.item.ArmorItem",
    "ArmorMaterial": "net.minecraft.world.item.ArmorMaterial",
    "EntityType": "net.minecraft.world.entity.EntityType",
    "MobCategory": "net.minecraft.world.entity.MobCategory",
    "Entity": "net.minecraft.world.entity.Entity",
    "LivingEntity": "net.minecraft.world.entity.LivingEntity",
    "Mob": "net.minecraft.world.entity.Mob",
    "PathfinderMob": "net.minecraft.world.entity.PathfinderMob",
    "Monster": "net.minecraft.world.entity.Monster",
    "Player": "net.minecraft.world.entity.player.Player",
    "Goal": "net.minecraft.world.entity.ai.goal.Goal",
    "Attributes": "net.minecraft.world.entity.ai.attributes.Attributes",
    "AttributeSupplier": "net.minecraft.world.entity.ai.attributes.AttributeSupplier",
    "Level": "net.minecraft.world.level.Level",
    "ServerLevel": "net.minecraft.server.level.ServerLevel",
    "WorldGenLevel": "net.minecraft.world.level.WorldGenLevel",
    "DamageSource": "net.minecraft.world.damagesource.DamageSource",
    "ResourceLocation": "net.minecraft.resources.ResourceLocation",
    "SoundEvent": "net.minecraft.sounds.SoundEvent",
    "SoundEvents": "net.minecraft.sounds.SoundEvents",
    "SoundCategory": "net.minecraft.sounds.SoundSource",
    "ParticleType": "net.minecraft.core.particles.ParticleType",
    "SimpleParticleType": "net.minecraft.core.particles.SimpleParticleType",
    "ParticleOptions": "net.minecraft.core.particles.ParticleOptions",
    "ParticleEngine": "net.minecraft.client.particle.ParticleEngine",
    "AABB": "net.minecraft.world.phys.AABB",
    "Vec3": "net.minecraft.world.phys.Vec3",
    "InteractionHand": "net.minecraft.world.InteractionHand",
    "InteractionResult": "net.minecraft.world.InteractionResult",
    "SynchedEntityData": "net.minecraft.network.syncher.SynchedEntityData",
    "EntityDataAccessor": "net.minecraft.network.syncher.EntityDataAccessor",
    "EntityDataSerializers": "net.minecraft.network.syncher.EntityDataSerializers",
    "CompoundTag": "net.minecraft.nbt.CompoundTag",
    "Translation": "net.minecraft.network.chat.Component",
    "BuiltinRegistries": "net.minecraft.core.Registry",
    "Registry": "net.minecraft.core.Registry",
    "ConfiguredFeature": "net.minecraft.world.level.levelgen.feature.ConfiguredFeature",
    "Feature": "net.minecraft.world.level.levelgen.feature.Feature",
    "OreFeatureConfig": "net.minecraft.world.level.levelgen.feature.configurations.OreConfiguration",
    "ConfiguredSurfaceBuilder": "net.minecraft.world.level.levelgen.surfacebuilders.ConfiguredSurfaceBuilder",
    "SurfaceBuilder": "net.minecraft.world.level.levelgen.surfacebuilders.SurfaceBuilder",
    "SurfaceBuilderConfig": "net.minecraft.world.level.levelgen.surfacebuilders.SurfaceBuilderConfig",
    "Biome": "net.minecraft.world.level.biome.Biome",
    "BiomeAmbience": "net.minecraft.world.level.biome.BiomeSpecialEffects",
    "MoodSoundAmbience": "net.minecraft.world.level.biome.AmbientMoodSettings",
    "BiomeGenerationSettings": "net.minecraft.world.level.biome.BiomeGenerationSettings",
    "MobSpawnInfo": "net.minecraft.world.level.biome.MobSpawnSettings",
    "BiomeCategory": "net.minecraft.world.level.biome.Biome$BiomeCategory",
    "World": "net.minecraft.world.level.Level",
    "Flag": "net.minecraft.world.entity.ai.goal.Goal.Flag",
    "FollowOwnerGoal": "net.minecraft.world.entity.ai.goal.FollowOwnerGoal",
    "SitWhenOrderedToGoal": "net.minecraft.world.entity.ai.goal.SitWhenOrderedToGoal",
    "TemptGoal": "net.minecraft.world.entity.ai.goal.TemptGoal",
    "FollowParentGoal": "net.minecraft.world.entity.ai.goal.FollowParentGoal",
    "PanicGoal": "net.minecraft.world.entity.ai.goal.PanicGoal",
    "LookAtGoal": "net.minecraft.world.entity.ai.goal.LookAtPlayerGoal",
    "LookRandomlyGoal": "net.minecraft.world.entity.ai.goal.RandomLookAroundGoal",
    "SwimGoal": "net.minecraft.world.entity.ai.goal.SwimGoal",
    "MeleeAttackGoal": "net.minecraft.world.entity.ai.goal.MeleeAttackGoal",
    "NearestAttackableTargetGoal": "net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal",
    "WaterAvoidingRandomStrollGoal": "net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal",
    "RandomLookAroundGoal": "net.minecraft.world.entity.ai.goal.RandomLookAroundGoal",
    "FloatGoal": "net.minecraft.world.entity.ai.goal.FloatGoal",
    "FleeEntityGoal": "net.minecraft.world.entity.ai.goal.FleeEntityGoal",
    "HurtByTargetGoal": "net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal",
    "RangedAttackGoal": "net.minecraft.world.entity.ai.goal.RangedAttackGoal",
    "SpawnGroupData": "net.minecraft.world.entity.SpawnGroupData",
    "AgeableMob": "net.minecraft.world.entity.AgeableMob",
    "MobSpawnType": "net.minecraft.world.entity.MobSpawnType",
}

# The 1.16.5 line builds against the *official Mojang* mappings, which already
# use the modern class layout.  Verified against the target's own class index
# (docs/api-probe/probe-fabric-1.16.5.txt ### ALL-CLASSES): MobCategory,
# EntityType, Player, Level, InteractionResult, InteractionHand,
# EntityDataAccessor, SimpleParticleType, CreativeModeTab, ModelPart,
# MobRenderer, Tier, ArmorMaterial, PathfinderMob, StructureFeature and
# StructureFeatureConfiguration are all present there, while every MCP name
# (EntityClassification, World, ActionResultType, ...) is absent.  The legacy
# line therefore shares the modern table, plus the two legacy-only helpers.
LEGACY_TYPES = dict(MODERN_TYPES)
LEGACY_TYPES.update({
    "EntityLookup": "net.minecraft.world.entity.Entity",
    "Predicate": "java.util.function.Predicate",
})



def types_for(flags):
    return LEGACY_TYPES if flags["pkgs"] == "legacy" else MODERN_TYPES


def imports_for(flags, names):
    """Build an import block for the requested short type names."""
    t = types_for(flags)
    lines = []
    for n in names:
        full = t[n]
        if full.startswith("java."):
            continue
        lines.append("import %s;" % full)
    return "\n".join(lines)


def registry_constant(flags, kind):
    """Registry constant expression for BLOCK/ITEM/ENTITY_TYPE/..."""
    names = {
        "BLOCK": ("BLOCK", "BLOCK"),
        "ITEM": ("ITEM", "ITEM"),
        "ENTITY_TYPE": ("ENTITY_TYPE", "ENTITY_TYPE"),
        "SOUND_EVENT": ("SOUND_EVENT", "SOUND_EVENT"),
        "PARTICLE_TYPE": ("PARTICLE_TYPE", "PARTICLE_TYPE"),
        "CREATIVE_MODE_TAB": (None, "CREATIVE_MODE_TAB"),
        "BIOME": ("BIOME", "BIOME"),
    }
    old, new = names[kind]
    if flags["reg"] == "util_registry":
        # 1.16.5 keeps the ResourceKey<Registry<T>> constants on Registry; the
        # bare Registry.BLOCK/ITEM/... constants are Registry<Block> values and
        # do not match DeferredRegister.create(String, ResourceKey<Registry<T>>).
        return "Registry." + (old or new) + "_REGISTRY"
    if flags["reg"] == "core_registry":
        return ("net.minecraft.resources.ResourceKey.createRegistryKey("
                "new net.minecraft.resources.ResourceLocation(\"minecraft\", \"%s\"))"
                % (old or new).lower())
    return "Registries." + new


def line_source_root(line_key):
    return "common/src/line-%s/java" % line_key


def line_resource_root(line_key):
    return "common/src/line-%s/resources" % line_key


# ---------------------------------------------------------------------------
# Cross-dimension teleport API generation.
#
# javap over the 33 API probes shows exactly three shapes for the call that
# moves a player into another ServerLevel (see docs/api-probe):
#   * "legacy": Entity#changeDimension(ServerLevel)               ... 1.16.5-1.20.6
#   * "set":    Entity#teleportTo(ServerLevel, x, y, z, Set, f, f) ... 1.21, 1.21.1
#   * "set8":   same + trailing boolean (setCamera)               ... 1.21.2+
# The boolean form replaced the Set-only form in 1.21.2; changeDimension lost
# its ServerLevel overload in 1.21 when DimensionTransition was introduced.
# ---------------------------------------------------------------------------

_TRAVEL_SET = ("1.21", "1.21.1")


def _version_tuple(mc):
    parts = []
    for chunk in str(mc).split("."):
        try:
            parts.append(int(chunk))
        except ValueError:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def travel_api(mc):
    """Return the teleport code shape for an exact Minecraft version."""
    if str(mc) in _TRAVEL_SET:
        return "set"
    if _version_tuple(mc) >= (1, 21, 2):
        return "set8"
    return "legacy"


def travel_api_for_line(line_key):
    return travel_api(LINES[line_key]["mc"])
