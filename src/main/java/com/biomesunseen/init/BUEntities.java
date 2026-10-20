package com.biomesunseen.init;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.entity.BUBoss;
import com.biomesunseen.entity.BUCreature;
import com.biomesunseen.entity.BossData;
import com.biomesunseen.entity.MobData;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundSource;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraftforge.event.entity.EntityAttributeCreationEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/**
 * All 85 entity types: 80 creatures plus 5 bosses.
 *
 * Two classes back the whole roster. Every species is its own
 * {@link EntityType} -- so it has its own id, its own spawn egg, its own
 * attributes and its own loot table -- but they share {@link BUCreature} or
 * {@link BUBoss} and are parameterised by the generated {@link MobData} /
 * {@link BossData} rows. That is what makes 85 entities maintainable: adding a
 * species is a data change in tools/content/mobs.py, not a new Java file.
 *
 * The {@code speciesFor} / {@code bossFor} lookups are the bridge between an
 * EntityType instance and its data row, resolved once at registration so the
 * hot path is a map read.
 */
public final class BUEntities {

    public static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(ForgeRegistries.ENTITY_TYPES, BUContent.MODID);

    private static final Map<String, RegistryObject<EntityType<?>>> BY_PATH = new LinkedHashMap<>();
    private static final Map<EntityType<?>, MobData> SPECIES = new LinkedHashMap<>();
    private static final Map<EntityType<?>, BossData> BOSSES = new LinkedHashMap<>();
    /** Boss id -> BossData, for the artefact items and the arena triggers. */
    private static final Map<String, BossData> BOSS_BY_ID = new LinkedHashMap<>();
    /** Mob id -> MobData, for spawn placement and the creative tab icons. */
    private static final Map<String, MobData> MOB_BY_ID = new LinkedHashMap<>();

    private BUEntities() {
    }

    public static void register(IEventBus bus) {
        registerCreatures();
        registerBosses();
        ENTITIES.register(bus);
    }

    // ------------------------------------------------------------------ //
    //  Registration
    // ------------------------------------------------------------------ //

    private static void registerCreatures() {
        for (MobData data : BUContent.MOBS) {
            MOB_BY_ID.put(data.id, data);
            RegistryObject<EntityType<?>> holder = ENTITIES.register(data.id, () -> {
                EntityType<BUCreature> type = EntityType.Builder
                        .<BUCreature>of(BUCreature::new, categoryFor(data.spawnCategory))
                        // The authored collision box, unscaled. getDimensions applies
                        // species.scale once on top; folding scale in here too compounded
                        // it, so the 50 species whose scale is not 1.0 were sized by scale
                        // squared -- a 2.6 came out at 6.76x, a 0.5 at a quarter size. The
                        // 0.9F was also a constant standing in for the per-species
                        // model_width / model_height the content tables author.
                        .sized(data.modelWidth, data.modelHeight)
                        .clientTrackingRange(data.hostile ? 10 : 8)
                        .updateInterval(3)
                        .build(new ResourceLocation(BUContent.MODID, data.id).toString());
                SPECIES.put(type, data);
                return type;
            });
            BY_PATH.put(data.id, holder);
        }
    }

    private static void registerBosses() {
        for (BossData data : BUContent.BOSSES) {
            BOSS_BY_ID.put(data.id, data);
            MOB_BY_ID.put(data.id, mobDataFor(data));
            RegistryObject<EntityType<?>> holder = ENTITIES.register(data.id, () -> {
                // Bosses are always in the monster category and always tracked
                // far: they are the reason a player entered the arena.
                EntityType<BUBoss> type = EntityType.Builder
                        .<BUBoss>of(BUBoss::new, MobCategory.MONSTER)
                        // As for creatures: the authored box, with scale applied once by
                        // getDimensions. The five bosses author widths from 1.6 to 3.4,
                        // which a shared 2.4F constant discarded entirely -- the Warden and
                        // the Unraveling were the same size.
                        .sized(data.modelWidth, data.modelHeight)
                        .fireImmune()
                        .clientTrackingRange(16)
                        .updateInterval(3)
                        .build(new ResourceLocation(BUContent.MODID, data.id).toString());
                BOSSES.put(type, data);
                SPECIES.put(type, mobDataFor(data));
                return type;
            });
            BY_PATH.put(data.id, holder);
        }
    }

    /**
     * The MobData a boss's own body uses.
     *
     * BossData does not repeat the mob row; the generator inlines it, so this
     * finds the matching entry in the creature table by id. Bosses are not in
     * BUContent.MOBS (they are their own roster), so a synthesised row is built
     * from the boss's own numbers when there is no match.
     */
    public static MobData mobDataFor(BossData boss) {
        if (boss == null) {
            return fallbackSpecies("unknown_boss");
        }
        for (MobData candidate : BUContent.MOBS) {
            if (candidate.id.equals(boss.id)) {
                return candidate;
            }
        }
        return new MobData(boss.id, "boss", boss.dimension, true,
                400.0F, 0.30F, 12.0F, 2.0F, 64.0F, 10.0F, boss.scale,
                true, false, "cutout", 1.2F, boss.textureSize, boss.textureHeight,
                new String[]{"melee_attack", "hurt_by_target",
                        "nearest_attackable_target_player", "float",
                        "look_at_player", "water_avoiding_random_stroll"},
                new String[]{"minecraft:player"},
                "monster", 1, 1, 1, 500, BOSS_ANIMATIONS,
                boss.modelWidth, boss.modelHeight);
    }

    /**
     * Every animation a boss model must define: the shared creature set plus a
     * loop and entry clip per phase.
     *
     * The GeckoLib animation JSON generated for each boss implements exactly
     * this list, so the model controller never asks for a clip that is absent.
     */
    public static final String[] BOSS_ANIMATIONS = {
            "animation.idle", "animation.walk", "animation.attack",
            "animation.hurt", "animation.death", "animation.spawn",
            "animation.phase.1", "animation.phase.2", "animation.phase.3",
            "animation.phase.4",
    };

    /**
     * The species data for an EntityType, never null.
     *
     * The entity constructors read this immediately -- a creature sets its
     * experience reward from it before anything else runs -- so a miss here is an
     * NullPointerException during world load with no indication which species
     * caused it. Falling back to a synthesised row turns that into a logged error
     * and a mob that still spawns, which is survivable in a way a crashed world is
     * not.
     */
    public static MobData speciesOrDefault(EntityType<?> type) {
        MobData data = SPECIES.get(type);
        if (data != null) {
            return data;
        }
        String id = registryPath(type);
        data = MOB_BY_ID.get(id);
        if (data != null) {
            return data;
        }
        BiomesUnseen.LOGGER.error(
                "No species data for entity type {}; using a placeholder. The entity will "
                        + "spawn but its authored stats, AI and animation set are missing.", id);
        return fallbackSpecies(id);
    }

    /**
     * The boss definition for an EntityType, never null.
     *
     * Same reasoning as {@link #speciesOrDefault}: the boss constructor reads the
     * phase list and the boss-bar styling from this before it can do anything
     * else, and a phase machine with no phases would throw on the first tick.
     */
    public static BossData bossOrDefault(EntityType<?> type) {
        BossData data = BOSSES.get(type);
        if (data != null) {
            return data;
        }
        String id = registryPath(type);
        data = BOSS_BY_ID.get(id);
        if (data != null) {
            return data;
        }
        BiomesUnseen.LOGGER.error(
                "No boss data for entity type {}; using a single-phase placeholder.", id);
        return new BossData(id, id, "overworld", "", "purple", "progress",
                2.0F, BOSS_TEX_SIZE, BOSS_TEX_SIZE, "", "entities/" + id, "",
                new BossData.PhaseData[]{fallbackPhase()},
                FALLBACK_BOSS_WIDTH, FALLBACK_BOSS_HEIGHT);
    }

    /** Boss atlas edge length; every boss atlas is authored square at this size. */
    private static final int BOSS_TEX_SIZE = 64;

    /** The registry path of an EntityType, or a placeholder if it is unregistered. */
    private static String registryPath(EntityType<?> type) {
        ResourceLocation key = ForgeRegistries.ENTITY_TYPES.getKey(type);
        return key == null ? "unknown" : key.getPath();
    }

    /**
     * A neutral species row.
     *
     * Deliberately passive and slow: a placeholder that cannot fight back is
     * safer than one that inherits combat goals it has no animation for.
     */
    private static MobData fallbackSpecies(String id) {
        return new MobData(id, "quadruped", "overworld", false,
                10.0F, 0.25F, 0.0F, 0.0F, 16.0F, 0.0F, 1.0F,
                false, false, "cutout", 0.5F, MOB_TEX_SIZE, MOB_TEX_SIZE,
                new String[]{"float", "water_avoiding_random_stroll",
                        "look_at_player", "random_look_around"},
                new String[0],
                "creature", 1, 1, 1, 0, FALLBACK_ANIMATIONS,
                FALLBACK_MODEL_WIDTH, FALLBACK_MODEL_HEIGHT);
    }

    /** Creature atlas edge lengths, matching the authored 64x64 family atlases. */
    private static final int MOB_TEX_SIZE = 64;

    /**
     * Collision box for a placeholder species.
     *
     * Roughly a block wide and tall, which is what 78 of the 80 authored species
     * use, so a fallback is not conspicuously wrong in world.
     */
    private static final float FALLBACK_MODEL_WIDTH = 0.9F;
    private static final float FALLBACK_MODEL_HEIGHT = 0.9F;

    /** Collision box for a placeholder boss: mid-range of the authored 1.6..3.4. */
    private static final float FALLBACK_BOSS_WIDTH = 2.4F;
    private static final float FALLBACK_BOSS_HEIGHT = 2.4F;

    /** The clips every family rig defines, so a placeholder still animates. */
    private static final String[] FALLBACK_ANIMATIONS = {
            "animation.idle", "animation.walk", "animation.attack",
            "animation.hurt", "animation.death",
    };

    /** A single phase that never triggers a transition. */
    public static BossData.PhaseData fallbackPhase() {
        return new BossData.PhaseData(1, "default", 0.0F, "animation.spawn",
                new String[0], new String[0], false, 0);
    }

    /** Maps the authored spawn-category string onto the vanilla enum. */
    private static MobCategory categoryFor(String spawnCategory) {
        if (spawnCategory == null) {
            return MobCategory.CREATURE;
        }
        switch (spawnCategory.toLowerCase(Locale.ROOT)) {
            case "monster":
                return MobCategory.MONSTER;
            case "ambient":
                return MobCategory.AMBIENT;
            case "axolotls":
                return MobCategory.AXOLOTLS;
            case "underground_water_creature":
                return MobCategory.UNDERGROUND_WATER_CREATURE;
            case "water_creature":
                return MobCategory.WATER_CREATURE;
            case "water_ambient":
                return MobCategory.WATER_AMBIENT;
            case "misc":
                return MobCategory.MISC;
            case "creature":
            default:
                return MobCategory.CREATURE;
        }
    }

    // ------------------------------------------------------------------ //
    //  Attributes
    // ------------------------------------------------------------------ //

    /**
     * Declare attributes for every registered entity.
     *
     * Forge requires this during {@link EntityAttributeCreationEvent} on the mod
     * bus; an entity with no attribute supplier throws the moment it spawns, so
     * this loop is what makes all 85 entities actually spawnable.
     */
    public static void registerAttributes(EntityAttributeCreationEvent event) {
        for (MobData data : BUContent.MOBS) {
            putAttributes(event, raw(data.id), BUCreature.attributesFor(data));
        }
        for (BossData data : BUContent.BOSSES) {
            putAttributes(event, raw(data.id), BUBoss.attributesFor(data));
        }
    }

    /**
     * Register one attribute supplier.
     *
     * {@code EntityAttributeCreationEvent.put} is generic over
     * {@code EntityType<T extends LivingEntity>}, and the registry hands back
     * {@code EntityType<?>}, which does not satisfy that bound. The raw cast is
     * confined to this one method instead of being repeated per entity; every
     * type registered here is a LivingEntity by construction.
     */
    @SuppressWarnings({"unchecked", "rawtypes"})
    private static void putAttributes(EntityAttributeCreationEvent event,
                                     EntityType<?> type,
                                     AttributeSupplier.Builder builder) {
        if (type != null) {
            event.put((EntityType) type, builder.build());
        }
    }

    // ------------------------------------------------------------------ //
    //  Boss music
    // ------------------------------------------------------------------ //

    /**
     * Start the boss's authored theme for one player.
     *
     * Played on the MUSIC source so it ducks the biome track the way vanilla
     * boss music does, rather than layering over it.
     */
    public static void playBossMusic(BUBoss boss, ServerPlayer player) {
        BossData data = boss.boss();
        // Checked before the SoundEvent lookup: an id can be registered and still
        // have no audio behind it, and starting one logs a client-side warning on
        // every boss sighting.
        if (!BUSounds.hasAudio(data.music)) {
            return;
        }
        net.minecraft.sounds.SoundEvent sound = BUSounds.get(data.music);
        if (sound == null) {
            return;
        }
        stopBossMusic(boss, player);
        // Played through the level on the MUSIC source rather than as a raw
        // packet: it takes a SoundEvent directly, so no registry-holder lookup
        // is needed, and it still ducks the biome track the way vanilla boss
        // music does.
        boss.level().playSound(null, boss.getX(), boss.getY(), boss.getZ(),
                sound, SoundSource.MUSIC, 1.6F, 1.0F);
    }

    /** Stop the boss theme when the fight ends or the player leaves. */
    public static void stopBossMusic(BUBoss boss, ServerPlayer player) {
        player.connection.send(new net.minecraft.network.protocol.game.ClientboundStopSoundPacket(
                null, SoundSource.MUSIC));
    }

    // ------------------------------------------------------------------ //
    //  Accessors
    // ------------------------------------------------------------------ //

    /** The data row for a creature EntityType, or null if it is not ours. */
    public static MobData speciesFor(EntityType<?> type) {
        return SPECIES.get(type);
    }

    /** The boss definition for a boss EntityType, or null for creatures. */
    public static BossData bossFor(EntityType<?> type) {
        return BOSSES.get(type);
    }

    public static MobData mobById(String id) {
        return MOB_BY_ID.get(id);
    }

    public static BossData bossById(String id) {
        return BOSS_BY_ID.get(id);
    }

    /** The registered EntityType for a path, or null if the mod does not add it. */
    @SuppressWarnings("unchecked")
    public static <T extends Entity> EntityType<T> entityType(String path) {
        RegistryObject<EntityType<?>> holder = BY_PATH.get(path);
        return holder == null ? null : (EntityType<T>) holder.get();
    }

    private static EntityType<?> raw(String path) {
        RegistryObject<EntityType<?>> holder = BY_PATH.get(path);
        return holder == null ? null : holder.get();
    }

    public static RegistryObject<EntityType<?>> holder(String path) {
        return BY_PATH.get(path);
    }

    public static boolean contains(String path) {
        return BY_PATH.containsKey(path);
    }

    public static java.util.Collection<RegistryObject<EntityType<?>>> all() {
        return BY_PATH.values();
    }
}
