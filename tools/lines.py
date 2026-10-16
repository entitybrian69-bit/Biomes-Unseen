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
        text="component", material=True, sound_ctor="new", data_dirs="plural",
        biome_json="old", worldgen="noise", biome_add="mixin_legacy",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=False, features="placed", structures="legacy",
    ),
    "1.18": dict(
        line="1.18", mc="1.18.2", java=17, pkgs="modern", reg="core_registry",
        geckolib="none", tab="old", damage="old", synched="old",
        text="component", material=True, sound_ctor="new", data_dirs="plural",
        biome_json="old", worldgen="noise", biome_add="noise_list",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.19.3": dict(
        line="1.19.3", mc="1.19.3", java=17, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="old", synched="old",
        text="component", material=False, sound_ctor="factory", data_dirs="plural",
        biome_json="new", worldgen="noise", biome_add="noise_list",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.19.4": dict(
        line="1.19.4", mc="1.19.4", java=17, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="old",
        text="component", material=False, sound_ctor="factory", data_dirs="plural",
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
        geckolib="none", tab="new", damage="new", synched="old",
        text="component", material=False, sound_ctor="factory", data_dirs="plural",
        biome_json="new", worldgen="modern", biome_add="noise_list",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.21": dict(
        line="1.21", mc="1.21.1", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="old",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="new", worldgen="modern", biome_add="noise_list",
        item_def="model_only", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.21.2": dict(
        line="1.21.2", mc="1.21.3", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="new", worldgen="modern", biome_add="noise_list",
        item_def="items_dir", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.21.4": dict(
        line="1.21.4", mc="1.21.4", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="new", worldgen="modern", biome_add="noise_list",
        item_def="items_dir", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.21.5": dict(
        line="1.21.5", mc="1.21.8", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="new", worldgen="modern", biome_add="noise_list",
        item_def="items_dir", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "1.21.9": dict(
        line="1.21.9", mc="1.21.11", java=21, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="new", worldgen="modern", biome_add="noise_list",
        item_def="items_dir", expect="dev", entity_base="modern",
        tagkey=True, features="placed", structures="sets",
    ),
    "26": dict(
        line="26", mc="26.3", java=25, pkgs="modern", reg="registries",
        geckolib="none", tab="new", damage="new", synched="builder",
        text="component", material=False, sound_ctor="factory", data_dirs="flat",
        biome_json="new", worldgen="modern", biome_add="noise_list",
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
    "1.19": "1.18", "1.19.1": "1.18", "1.19.2": "1.18",
    "1.19.3": "1.19.3",
    "1.19.4": "1.19.4", "1.20": "1.19.4", "1.20.1": "1.19.4",
    "1.20.2": "1.20.2", "1.20.3": "1.20.2", "1.20.4": "1.20.2",
    "1.20.5": "1.20.5", "1.20.6": "1.20.5",
    "1.21": "1.21", "1.21.1": "1.21",
    "1.21.2": "1.21.2", "1.21.3": "1.21.2",
    "1.21.4": "1.21.4",
    "1.21.5": "1.21.5", "1.21.6": "1.21.5", "1.21.7": "1.21.5", "1.21.8": "1.21.5",
    "1.21.9": "1.21.9", "1.21.10": "1.21.9", "1.21.11": "1.21.9",
    "26.1": "26", "26.1.1": "26", "26.1.2": "26", "26.2": "26", "26.3": "26",
}

# Mojang-mapping type names per package generation.
LEGACY_TYPES = {
    "Block": "net.minecraft.block.Block",
    "BlockBehaviour": "net.minecraft.block.AbstractBlock",
    "Blocks": "net.minecraft.block.Blocks",
    "SoundType": "net.minecraft.block.SoundType",
    "BlockState": "net.minecraft.block.BlockState",
    "BlockPos": "net.minecraft.util.math.BlockPos",
    "Direction": "net.minecraft.util.Direction",
    "Item": "net.minecraft.item.Item",
    "BlockItem": "net.minecraft.item.BlockItem",
    "Items": "net.minecraft.item.Items",
    "ItemStack": "net.minecraft.item.ItemStack",
    "ItemGroup": "net.minecraft.item.ItemGroup",
    "SpawnEggItem": "net.minecraft.item.SpawnEggItem",
    "Tier": "net.minecraft.item.ItemTier",
    "SwordItem": "net.minecraft.item.SwordItem",
    "PickaxeItem": "net.minecraft.item.PickaxeItem",
    "ArmorItem": "net.minecraft.item.ArmorItem",
    "ArmorMaterial": "net.minecraft.item.ArmorMaterial",
    "EntityType": "net.minecraft.entity.EntityType",
    "MobCategory": "net.minecraft.entity.EntityClassification",
    "Entity": "net.minecraft.entity.Entity",
    "LivingEntity": "net.minecraft.entity.LivingEntity",
    "Mob": "net.minecraft.entity.MobEntity",
    "PathfinderMob": "net.minecraft.entity.CreatureEntity",
    "Monster": "net.minecraft.entity.MonsterEntity",
    "Player": "net.minecraft.entity.player.PlayerEntity",
    "Goal": "net.minecraft.entity.ai.goal.Goal",
    "Attributes": "net.minecraft.entity.ai.attributes.Attributes",
    "AttributeSupplier": "net.minecraft.entity.ai.attributes.AttributeModifierMap",
    "Level": "net.minecraft.world.World",
    "ServerLevel": "net.minecraft.world.server.ServerWorld",
    "WorldGenLevel": "net.minecraft.world.IWorld",
    "DamageSource": "net.minecraft.util.DamageSource",
    "ResourceLocation": "net.minecraft.util.ResourceLocation",
    "SoundEvent": "net.minecraft.util.SoundEvent",
    "SoundEvents": "net.minecraft.util.SoundEvents",
    "SoundCategory": "net.minecraft.util.SoundCategory",
    "ParticleType": "net.minecraft.particles.ParticleType",
    "SimpleParticleType": "net.minecraft.particles.BasicParticleType",
    "ParticleOptions": "net.minecraft.particles.IParticleData",
    "ParticleEngine": "net.minecraft.client.particle.ParticleManager",
    "AABB": "net.minecraft.util.math.AxisAlignedBB",
    "Vec3": "net.minecraft.util.math.vector.Vector3d",
    "InteractionHand": "net.minecraft.util.Hand",
    "InteractionResult": "net.minecraft.util.ActionResultType",
    "SynchedEntityData": "net.minecraft.network.datasync.EntityDataManager",
    "EntityDataAccessor": "net.minecraft.network.datasync.DataParameter",
    "EntityDataSerializers": "net.minecraft.network.datasync.DataSerializers",
    "CompoundTag": "net.minecraft.nbt.CompoundNBT",
    "Translation": "net.minecraft.util.text.TranslationTextComponent",
    "BuiltinRegistries": "net.minecraft.util.registry.BuiltinRegistries",
    "Registry": "net.minecraft.util.registry.Registry",
    "ConfiguredFeature": "net.minecraft.world.gen.feature.ConfiguredFeature",
    "Feature": "net.minecraft.world.gen.feature.Feature",
    "OreFeatureConfig": "net.minecraft.world.gen.feature.OreFeatureConfig",
    "ConfiguredSurfaceBuilder": "net.minecraft.world.gen.surfacebuilders.ConfiguredSurfaceBuilder",
    "SurfaceBuilder": "net.minecraft.world.gen.surfacebuilders.SurfaceBuilder",
    "SurfaceBuilderConfig": "net.minecraft.world.gen.surfacebuilders.SurfaceBuilderConfig",
    "Biome": "net.minecraft.world.biome.Biome",
    "BiomeAmbience": "net.minecraft.world.biome.BiomeAmbience",
    "MoodSoundAmbience": "net.minecraft.world.biome.MoodSoundAmbience",
    "BiomeGenerationSettings": "net.minecraft.world.biome.BiomeGenerationSettings",
    "MobSpawnInfo": "net.minecraft.world.biome.MobSpawnInfo",
    "BiomeCategory": "net.minecraft.world.biome.Biome.Category",
    "World": "net.minecraft.world.World",
    "EntityLookup": "net.minecraft.entity.Entity",
    "Predicate": "java.util.function.Predicate",
    "Flag": "net.minecraft.entity.ai.goal.Goal.Flag",
    "FollowOwnerGoal": "net.minecraft.entity.ai.goal.FollowOwnerGoal",
    "SitWhenOrderedToGoal": "net.minecraft.entity.ai.goal.SitWhenOrderedToGoal",
    "TemptGoal": "net.minecraft.entity.ai.goal.TemptGoal",
    "FollowParentGoal": "net.minecraft.entity.ai.goal.FollowParentGoal",
    "PanicGoal": "net.minecraft.entity.ai.goal.PanicGoal",
    "LookAtGoal": "net.minecraft.entity.ai.goal.LookAtGoal",
    "LookRandomlyGoal": "net.minecraft.entity.ai.goal.LookRandomlyGoal",
    "SwimGoal": "net.minecraft.entity.ai.goal.SwimGoal",
    "MeleeAttackGoal": "net.minecraft.entity.ai.goal.MeleeAttackGoal",
    "NearestAttackableTargetGoal": "net.minecraft.entity.ai.goal.NearestAttackableTargetGoal",
    "WaterAvoidingRandomStrollGoal": "net.minecraft.entity.ai.goal.WaterAvoidingRandomWalkingGoal",
    "RandomLookAroundGoal": "net.minecraft.entity.ai.goal.LookRandomlyGoal",
    "FloatGoal": "net.minecraft.entity.ai.goal.SwimGoal",
    "FleeEntityGoal": "net.minecraft.entity.ai.goal.FleeEntityGoal",
    "HurtByTargetGoal": "net.minecraft.entity.ai.goal.HurtByTargetGoal",
    "RangedAttackGoal": "net.minecraft.entity.ai.goal.RangedAttackGoal",
    "SpawnGroupData": "net.minecraft.entity.SpawnGroupData",
    "AgeableMob": "net.minecraft.entity.AgeableEntity",
    "MobSpawnType": "net.minecraft.entity.MobSpawnType",
}

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
        return "Registry." + (old or new)
    if flags["reg"] == "core_registry":
        return "Registry." + (old or new)
    return "Registries." + new


def line_source_root(line_key):
    return "common/src/line-%s/java" % line_key


def line_resource_root(line_key):
    return "common/src/line-%s/resources" % line_key
