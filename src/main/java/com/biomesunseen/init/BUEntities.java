package com.biomesunseen.init;

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
                        .sized(0.9F * data.scale, 0.9F * data.scale)
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
                        .sized(2.4F * data.scale, 2.4F * data.scale)
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
    private static MobData mobDataFor(BossData boss) {
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
                "monster", 1, 1, 1, 500, BOSS_ANIMATIONS);
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
        net.minecraft.sounds.SoundEvent sound = BUSounds.get(data.music);
        if (sound == null) {
            return;
        }
        player.connection.send(new net.minecraft.network.protocol.game.ClientboundStopSoundPacket(
                null, SoundSource.MUSIC));
        player.connection.send(new net.minecraft.network.protocol.game.ClientboundSoundPacket(
                net.minecraftforge.registries.ForgeRegistries.SOUND_EVENTS.getDelegateOrThrow(sound),
                SoundSource.MUSIC, boss.getX(), boss.getY(), boss.getZ(),
                1.6F, 1.0F, player.level().getRandom().nextLong()));
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
