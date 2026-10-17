# -*- coding: utf-8 -*-
"""Emits registry + worldgen Java for one API line."""

import os

from content import (MOD_ID, ALL_ORE_ROWS as ORE_ROWS,
                     ALL_DECOR_ROWS as DECOR_ROWS, ALL_PLANT_ROWS as PLANT_ROWS,
                     ALL_MOB_ROWS as MOB_ROWS, ALL_BOSS_ROWS as BOSS_ROWS,
                     ALL_STRUCTURE_ROWS as STRUCTURE_ROWS, SOUND_EVENTS,
                     PARTICLE_TYPES, BIOME_GROUPS, PORTAL_ROWS, DIMENSION_DEFS)
from lines import LINES, types_for, registry_constant
from emit_families import _w, _s, _camel, _imports, _sound_event_expr, _reg


def emit_registries(root, line_key):
    F = LINES[line_key]
    portal_rows = "".join(
        '            {"%s", "%s"},\n' % (p[0], p[4]) for p in PORTAL_ROWS)
    portal_key_loop = (
        "        String[][] portalKeys = {\n"
        + portal_rows +
        "        };\n"
        "        for (final String[] portal : portalKeys) {\n"
        "            PORTAL_KEYS.put(portal[1], track(ModRegistries.ITEMS.register(portal[1],\n"
        "                    () -> new com.biomesunseen.item.UnseenPortalKeyItem(portal[0],\n"
        "                            new Item.Properties()))));\n"
        "        }\n")
    T = types_for(F)
    base = "common/src/line-%s/java/com/biomesunseen" % line_key
    legacy = F["pkgs"] == "legacy"

    reg_block = _reg(F, "BLOCK")
    reg_item = _reg(F, "ITEM")
    reg_entity = _reg(F, "ENTITY_TYPE")
    reg_sound = _reg(F, "SOUND_EVENT")
    reg_particle = _reg(F, "PARTICLE_TYPE")
    if F["reg"] == "registries":
        reg_imports = ("import net.minecraft.core.Registry;\n"
                       "import net.minecraft.core.registries.Registries;\n"
                       "import net.minecraft.core.registries.BuiltInRegistries;")
    elif legacy:
        reg_imports = "import net.minecraft.util.registry.Registry;"
    else:
        reg_imports = "import net.minecraft.core.Registry;"

    # ------------------------------------------------------------------ #
    _w(root, base + "/registry/ModRegistries.java", '''package com.biomesunseen.registry;

%(reg_imports)s

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.core.ModConstants;

import me.shedaniel.architectury.registry.DeferredRegister;

/**
 * Every Architectury DeferredRegister used by Biomes Unseen.  Registration
 * order matters: entities before items so spawn eggs can resolve their
 * EntityType at construction time.
 */
public final class ModRegistries {

    public static final String MOD_ID = ModConstants.MOD_ID;

    public static final DeferredRegister<net.minecraft.world.level.block.Block> BLOCKS =
            DeferredRegister.create(MOD_ID, %(reg_block)s);
    public static final DeferredRegister<net.minecraft.world.item.Item> ITEMS =
            DeferredRegister.create(MOD_ID, %(reg_item)s);
    public static final DeferredRegister<net.minecraft.world.entity.EntityType<?>> ENTITIES =
            DeferredRegister.create(MOD_ID, %(reg_entity)s);
    public static final DeferredRegister<net.minecraft.sounds.SoundEvent> SOUNDS =
            DeferredRegister.create(MOD_ID, %(reg_sound)s);
    public static final DeferredRegister<net.minecraft.core.particles.ParticleType<?>> PARTICLES =
            DeferredRegister.create(MOD_ID, %(reg_particle)s);

    private ModRegistries() {
    }

    /** Kick every deferred register, then populate the content holders. */
    public static void registerAll() {
        ENTITIES.register();
        BLOCKS.register();
        ITEMS.register();
        SOUNDS.register();
        PARTICLES.register();
        ModEntities.registerContent();
        ModBlocks.registerContent();
        ModItems.registerContent();
        ModSounds.registerContent();
        ModParticles.registerContent();
    }
}
''' % {
        "reg_imports": reg_imports,
        "reg_block": reg_block,
        "reg_item": reg_item,
        "reg_entity": reg_entity,
        "reg_sound": reg_sound,
        "reg_particle": reg_particle,
    })

    # Strip the modern-only full package names in generic args for legacy:
    # Registries above use fully-qualified generics so they work on every line
    # (net.minecraft.world.level.block.Block exists 1.17+; for the legacy line
    # we rewrite the file below).
    if legacy:
        _w(root, base + "/registry/ModRegistries.java", '''package com.biomesunseen.registry;

import net.minecraft.block.Block;
import net.minecraft.entity.EntityType;
import net.minecraft.item.Item;
import net.minecraft.particles.ParticleType;
import net.minecraft.util.SoundEvent;
import net.minecraft.util.registry.Registry;

import com.biomesunseen.core.ModConstants;

import me.shedaniel.architectury.registry.DeferredRegister;

/**
 * Every Architectury DeferredRegister used by Biomes Unseen.  Registration
 * order matters: entities before items so spawn eggs can resolve their
 * EntityType at construction time.
 */
public final class ModRegistries {

    public static final String MOD_ID = ModConstants.MOD_ID;

    public static final DeferredRegister<Block> BLOCKS =
            DeferredRegister.create(MOD_ID, Registry.BLOCK);
    public static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(MOD_ID, Registry.ITEM);
    public static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(MOD_ID, Registry.ENTITY_TYPE);
    public static final DeferredRegister<SoundEvent> SOUNDS =
            DeferredRegister.create(MOD_ID, Registry.SOUND_EVENT);
    public static final DeferredRegister<ParticleType<?>> PARTICLES =
            DeferredRegister.create(MOD_ID, Registry.PARTICLE_TYPE);

    private ModRegistries() {
    }

    /** Kick every deferred register, then populate the content holders. */
    public static void registerAll() {
        ENTITIES.register();
        BLOCKS.register();
        ITEMS.register();
        SOUNDS.register();
        PARTICLES.register();
        ModEntities.registerContent();
        ModBlocks.registerContent();
        ModItems.registerContent();
        ModSounds.registerContent();
        ModParticles.registerContent();
    }
}
''')

    # ------------------------------------------------------------------ #
    # ModBlocks.java
    # ------------------------------------------------------------------ #
    block_extra = "BlockBehaviour" if not legacy else "AbstractBlock"
    _w(root, base + "/registry/ModBlocks.java", '''package com.biomesunseen.registry;

%(imports)s

import com.biomesunseen.block.UnseenDecorBlock;
import com.biomesunseen.block.UnseenOreBlock;
import com.biomesunseen.block.UnseenPlantBlock;
import com.biomesunseen.core.Content;
import com.biomesunseen.core.DecorDef;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.core.PlantDef;

import me.shedaniel.architectury.registry.RegistrySupplier;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * All %(n_blocks)s blocks: %(n_ores)s ores, %(n_decor)s palette blocks and
 %(n_plants_line)s
 */
public final class ModBlocks {

    /** ore id (e.g. "azurethril") -> "<id>_ore" block */
    public static final Map<String, RegistrySupplier<Block>> ORES =
            new LinkedHashMap<String, RegistrySupplier<Block>>();
    /** decor id -> block */
    public static final Map<String, RegistrySupplier<Block>> DECOR =
            new LinkedHashMap<String, RegistrySupplier<Block>>();
    /** plant id -> block */
    public static final Map<String, RegistrySupplier<Block>> PLANTS =
            new LinkedHashMap<String, RegistrySupplier<Block>>();

    static {
        for (int i = 0; i < Content.ORES.size(); i++) {
            OreDef ore = Content.ORES.get(i);
            ORES.put(ore.id, ModRegistries.BLOCKS.register(ore.id + "_ore",
                    () -> new UnseenOreBlock(ore)));
        }
        for (int i = 0; i < Content.DECOR.size(); i++) {
            DecorDef decor = Content.DECOR.get(i);
            DECOR.put(decor.id, ModRegistries.BLOCKS.register(decor.id,
                    () -> new UnseenDecorBlock(decor)));
        }
        for (int i = 0; i < Content.PLANTS.size(); i++) {
            PlantDef plant = Content.PLANTS.get(i);
            PLANTS.put(plant.id, ModRegistries.BLOCKS.register(plant.id,
                    () -> new UnseenPlantBlock(plant)));
        }
    }

    private ModBlocks() {
    }

    /** Triggers static initialization (called by ModRegistries). */
    public static void registerContent() {
        // Static initializers populate the maps above.
    }

    public static RegistrySupplier<Block> oreBlock(String oreId) {
        return ORES.get(oreId);
    }

    public static Map<String, RegistrySupplier<Block>> allOres() {
        return Collections.unmodifiableMap(ORES);
    }

    public static Map<String, RegistrySupplier<Block>> allDecor() {
        return Collections.unmodifiableMap(DECOR);
    }

    public static Map<String, RegistrySupplier<Block>> allPlants() {
        return Collections.unmodifiableMap(PLANTS);
    }
}
''' % {
        "imports": _imports(F, ["Block", "BlockBehaviour"] if not legacy
                            else ["Block", "BlockBehaviour"]),
        "n_blocks": len(ORE_ROWS) + len(DECOR_ROWS) + len(PLANT_ROWS),
        "n_ores": len(ORE_ROWS),
        "n_decor": len(DECOR_ROWS),
        "n_plants_line": "          %s plants." % len(PLANT_ROWS),
    })
    if legacy:
        _w(root, base + "/registry/ModBlocks.java",
           open(os.path.join(root, base + "/registry/ModBlocks.java"))
           .read().replace("import net.minecraft.block.BlockBehaviour;",
                           "import net.minecraft.block.AbstractBlock;"))

    # ------------------------------------------------------------------ #
    # ModSounds.java / ModParticles.java
    # ------------------------------------------------------------------ #
    sound_expr = _sound_event_expr(F, "new ResourceLocation(ModConstants.MOD_ID, id)")
    _w(root, base + "/registry/ModSounds.java", '''package com.biomesunseen.registry;

%(imports)s

import com.biomesunseen.core.CoreRegistries;
import com.biomesunseen.core.ModConstants;

import me.shedaniel.architectury.registry.RegistrySupplier;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * All %(n)s sound events: biome ambience, music, mob calls and block sounds.
 */
public final class ModSounds {

    public static final Map<String, RegistrySupplier<SoundEvent>> BY_ID =
            new LinkedHashMap<String, RegistrySupplier<SoundEvent>>();

    static {
        for (int i = 0; i < CoreRegistries.SOUND_EVENT_IDS.size(); i++) {
            String id = CoreRegistries.SOUND_EVENT_IDS.get(i);
            BY_ID.put(id, ModRegistries.SOUNDS.register(id, () -> %(expr)s));
        }
    }

    private ModSounds() {
    }

    public static void registerContent() {
        // Static initializers populate BY_ID.
    }

    /** Resolve a sound event by its sounds.json key (e.g. "music.biomesunseen.boss_heart"). */
    public static SoundEvent byId(String id) {
        RegistrySupplier<SoundEvent> supplier = BY_ID.get(id);
        return supplier == null ? null : supplier.get();
    }

    public static java.util.Set<String> allIds() {
        return Collections.unmodifiableSet(BY_ID.keySet());
    }
}
''' % {
        "imports": _imports(F, ["SoundEvent", "ResourceLocation"]),
        "n": len(SOUND_EVENTS),
        "expr": sound_expr,
    })

    particle_simple = "BasicParticleType" if legacy else "SimpleParticleType"
    particle_import = ("net.minecraft.particles.BasicParticleType" if legacy
                       else "net.minecraft.core.particles.SimpleParticleType")
    _w(root, base + "/registry/ModParticles.java", '''package com.biomesunseen.registry;

import %(ptype)s;
%(rl_import)s

import com.biomesunseen.core.CoreRegistries;
import com.biomesunseen.core.ModConstants;

import me.shedaniel.architectury.registry.RegistrySupplier;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * All %(n)s custom particle types (crystal sparks, embers, void motes, ...).
 */
public final class ModParticles {

    public static final Map<String, RegistrySupplier<ParticleType<%(simple)s>>> BY_ID =
            new LinkedHashMap<String, RegistrySupplier<ParticleType<%(simple)s>>>();

    static {
        for (int i = 0; i < CoreRegistries.PARTICLE_IDS.size(); i++) {
            String id = CoreRegistries.PARTICLE_IDS.get(i);
            BY_ID.put(id, narrow(ModRegistries.PARTICLES.register(id, () -> newSimple())));
        }
    }

    /**
     * The vanilla simple particle type keeps its constructor protected, so the
     * eight Biomes Unseen types are instantiated reflectively - this keeps the
     * registration code identical on every API line.
     */
    private static %(simple)s newSimple() {
        try {
            java.lang.reflect.Constructor<%(simple)s> ctor =
                    %(simple)s.class.getDeclaredConstructor(boolean.class);
            ctor.setAccessible(true);
            return ctor.newInstance(Boolean.TRUE);
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException("Cannot build particle type", e);
        }
    }

    private ModParticles() {
    }

    public static void registerContent() {
        // Static initializers populate BY_ID.
    }

    /** The particle register is declared with a wildcard; narrow it for typed lookups. */
    @SuppressWarnings("unchecked")
    private static RegistrySupplier<ParticleType<%(simple)s>> narrow(RegistrySupplier<?> supplier) {
        return (RegistrySupplier) supplier;
    }

    public static ParticleType<?> byId(String id) {
        RegistrySupplier<ParticleType<%(simple)s>> supplier = BY_ID.get(id);
        return supplier == null ? null : supplier.get();
    }

    public static java.util.Set<String> allIds() {
        return Collections.unmodifiableSet(BY_ID.keySet());
    }
}
''' % {
        "ptype": particle_import,
        "rl_import": ("import net.minecraft.particles.ParticleType;" if legacy
                      else "import net.minecraft.core.particles.ParticleType;"),
        "simple": particle_simple,
        "n": len(PARTICLE_TYPES),
    })

    # ------------------------------------------------------------------ #
    # ModEntities.java (holders + attributes; entity classes in entity/)
    # ------------------------------------------------------------------ #
    reg_entries = []
    attr_entries = []
    egg_entries = []
    for (mid, display, cat, hp, spd, atk, defn, w, h, behaviors, tame, trade,
         pack, herd, flees, terrain, bg, weight, night, anims, color, glow) in MOB_ROWS:
        cls = _camel(mid) + "Entity"
        mob_cat = "MobCategory.CREATURE" if cat == "creature" else "MobCategory.MONSTER"
        reg_entries.append(
            '        %s = ModRegistries.ENTITIES.register("%s", () -> EntityType.Builder.of(%s::new, %s)\n'
            '                .sized(%sF, %sF).clientTrackingRange(8).updateInterval(3)\n'
            '                .build("%s"));'
            % (_camel(mid).upper() if False else _camel(mid), mid, cls, mob_cat,
               w, h, mid))
        attr_entries.append(
            '        EntityAttributeRegistry.register(() -> %s.get(), () -> Mob.createMobAttributes()\n'
            '                .add(Attributes.MAX_HEALTH, %sD)\n'
            '                .add(Attributes.MOVEMENT_SPEED, %sD)\n'
            '                .add(Attributes.ATTACK_DAMAGE, %sD)\n'
            '                .add(Attributes.ARMOR, %sD)\n'
            '                .add(Attributes.FOLLOW_RANGE, 48D));'
            % (_camel(mid), hp, spd, atk, defn))
    for (bid, display, hp, spd, atk, w, h, arena, music, phases, attacks, loot,
         grp, color, glow) in BOSS_ROWS:
        cls = _camel(bid) + "Entity"
        reg_entries.append(
            '        %s = ModRegistries.ENTITIES.register("%s", () -> EntityType.Builder.of(%s::new, MobCategory.MONSTER)\n'
            '                .sized(%sF, %sF).clientTrackingRange(12).updateInterval(2)\n'
            '                .fireImmune().build("%s"));'
            % (_camel(bid), bid, cls, w, h, bid))
        attr_entries.append(
            '        EntityAttributeRegistry.register(() -> %s.get(), () -> Mob.createMobAttributes()\n'
            '                .add(Attributes.MAX_HEALTH, %sD)\n'
            '                .add(Attributes.MOVEMENT_SPEED, %sD)\n'
            '                .add(Attributes.ATTACK_DAMAGE, %sD)\n'
            '                .add(Attributes.ARMOR, 8D)\n'
            '                .add(Attributes.FOLLOW_RANGE, 96D)\n'
            '                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0D));'
            % (_camel(bid), hp, spd, atk))

    fields = []
    for (mid, *_rest) in MOB_ROWS:
        fields.append(
            "    public static RegistrySupplier<EntityType<%sEntity>> %s;"
            % (_camel(mid), _camel(mid)))
    for (bid, *_rest) in BOSS_ROWS:
        fields.append(
            "    public static RegistrySupplier<EntityType<%sEntity>> %s;"
            % (_camel(bid), _camel(bid)))

    _w(root, base + "/registry/ModEntities.java", '''package com.biomesunseen.registry;

%(imports)s

import com.biomesunseen.entity.boss.*;
import com.biomesunseen.entity.mobs.*;

import me.shedaniel.architectury.registry.EntityAttributeRegistry;
import me.shedaniel.architectury.registry.RegistrySupplier;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * All %(n_mobs)s mobs and %(n_bosses)s bosses with their spawn attributes.
 * Spawn eggs are created in ModItems after these types exist.
 */
public final class ModEntities {

%(fields)s

    /** mob id -> entity type supplier (excludes bosses) */
    public static final Map<String, RegistrySupplier<EntityType<?>>> MOB_TYPES =
            new LinkedHashMap<String, RegistrySupplier<EntityType<?>>>();
    /** boss id -> entity type supplier */
    public static final Map<String, RegistrySupplier<EntityType<?>>> BOSS_TYPES =
            new LinkedHashMap<String, RegistrySupplier<EntityType<?>>>();

    private ModEntities() {
    }

    @SuppressWarnings("unchecked")
    public static void registerContent() {
%(registrations)s

%(attributes)s

        for (int i = 0; i < com.biomesunseen.core.Content.MOBS.size(); i++) {
            String id = com.biomesunseen.core.Content.MOBS.get(i).id;
            MOB_TYPES.put(id, (RegistrySupplier<EntityType<?>>) (RegistrySupplier<?>) byMobId(id));
        }
        for (int i = 0; i < com.biomesunseen.core.Content.BOSSES.size(); i++) {
            String id = com.biomesunseen.core.Content.BOSSES.get(i).id;
            BOSS_TYPES.put(id, (RegistrySupplier<EntityType<?>>) (RegistrySupplier<?>) byBossId(id));
        }
    }

    private static RegistrySupplier<EntityType<?>> byMobId(String id) {
%(mob_switch)s
        return null;
    }

    private static RegistrySupplier<EntityType<?>> byBossId(String id) {
%(boss_switch)s
        return null;
    }
}
''' % {
        "imports": _imports(F, ["EntityType", "MobCategory", "Attributes", "Mob"]),
        "mobcls": ("MobEntity" if legacy else "Mob"),
        "n_mobs": len(MOB_ROWS),
        "n_bosses": len(BOSS_ROWS),
        "fields": "\n".join(fields),
        "registrations": "\n".join(reg_entries),
        "attributes": "\n".join(attr_entries).replace("Mob.createMobAttributes",
                                          ("MobEntity" if legacy else "Mob") + ".createMobAttributes"),
        "mob_switch": "\n".join(
            '        if ("%s".equals(id)) {\n            return (RegistrySupplier) %s;\n        }' % (mid, _camel(mid))
            for (mid, *_r) in MOB_ROWS),
        "boss_switch": "\n".join(
            '        if ("%s".equals(id)) {\n            return (RegistrySupplier) %s;\n        }' % (bid, _camel(bid))
            for (bid, *_r) in BOSS_ROWS),
    })

    # ------------------------------------------------------------------ #
    # ModItems.java
    # ------------------------------------------------------------------ #
    if F["tab"] == "old":
        tab_field = "public static ItemGroup MAIN;"
        tab_setup = ('        MAIN = new ItemGroup("biomesunseen") {\n'
                     '            @Override\n'
                     '            public ItemStack makeIcon() {\n'
                     '                return new ItemStack(UNSEEN_SIGIL.get());\n'
                     '            }\n'
                     '        };')
        props16 = ".stacksTo(16).tab(MAIN)"
        props_plain = ".tab(MAIN)"
        props_one = ".stacksTo(1).tab(MAIN)"
    else:
        tab_field = "public static RegistrySupplier<ItemGroup> MAIN;"
        tab_setup = '''        MAIN = TABS.register("main", () -> CreativeModeTab.builder()
                .title(Component.translatable("itemGroup.biomesunseen"))
                .icon(() -> new ItemStack(UNSEEN_SIGIL.get()))
                .displayItems((params, output) -> {
                    for (RegistrySupplier<Item> supplier : ALL_ITEMS) {
                        output.accept(supplier.get());
                    }
                })
                .build());'''
        props16 = ".stacksTo(16)"
        props_plain = ""
        props_one = ".stacksTo(1)"

    # The creative-mode tab API changed on nearly every Minecraft line, so the
    # tab is created reflectively by the platform entrypoint instead of here.
    tab_field = ""
    tab_setup = ""
    props16 = ".stacksTo(16)"
    props_plain = ""
    props_one = ".stacksTo(1)"

    if legacy:
        items_imports = ("import net.minecraft.block.Block;\n"
                         "import net.minecraft.item.Item;\n"
                         "import net.minecraft.item.ItemStack;\n"
                         "import net.minecraft.item.BlockItem;\n"
                         "import net.minecraft.item.ItemGroup;\n"
                         "import net.minecraft.item.SpawnEggItem;\n"
                         "import net.minecraft.item.crafting.Ingredient;\n"
                         "import net.minecraft.entity.EntityType;\n"
                         "import net.minecraft.entity.MobEntity;")
    else:
        items_imports = ("import net.minecraft.world.level.block.Block;\n"
                         "import net.minecraft.world.item.Item;\n"
                         "import net.minecraft.world.item.ItemStack;\n"
                         "import net.minecraft.world.item.BlockItem;\n"
                         "import net.minecraft.world.item.CreativeModeTab;\n"
                         "import net.minecraft.world.item.SpawnEggItem;\n"
                         "import net.minecraft.world.item.crafting.Ingredient;\n"
                         "import net.minecraft.world.entity.EntityType;\n"
                         "import net.minecraft.world.entity.Mob;\n"
                         "import net.minecraft.network.chat.Component;")

    tabs_import = ""
    tabs_register = ""

    _w(root, base + "/registry/ModItems.java", '''package com.biomesunseen.registry;

%(imports)s

import com.biomesunseen.core.Content;
import com.biomesunseen.core.ModConstants;
import com.biomesunseen.core.OreDef;
import com.biomesunseen.item.UnseenArmorMaterial;
import com.biomesunseen.item.UnseenGearItems;
import com.biomesunseen.item.UnseenToolTier;

import me.shedaniel.architectury.registry.DeferredRegister;
import me.shedaniel.architectury.registry.RegistrySupplier;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;

/**
 * All items: %(n_minerals)s ore minerals, %(n_gear)s gear pieces, %(n_tonics)s
 * tonics, %(n_core)s machine cores, %(n_eggs)s spawn eggs, %(n_lore)s lore
 * books, %(n_trophies)s mob trophies and the tab sigil.  Everything is
 * created from the shared Content catalog so items can never drift from
 * worldgen.
 */
public final class ModItems {

    public static final String MOD_ID = ModConstants.MOD_ID;

%(tabs_import)s    %(tab_field)s

    /** Every registered item, in creative-tab order. */
    public static final List<RegistrySupplier<Item>> ALL_ITEMS =
            new ArrayList<RegistrySupplier<Item>>();

    public static RegistrySupplier<Item> UNSEEN_SIGIL;

    /** ore id -> mineral item */
    public static final Map<String, RegistrySupplier<Item>> MINERALS =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** ore id -> tool tier */
    public static final Map<String, UnseenToolTier> TOOL_TIERS =
            new LinkedHashMap<String, UnseenToolTier>();
    /** ore id -> armor material */
    public static final Map<String, UnseenArmorMaterial> ARMOR_MATERIALS =
            new LinkedHashMap<String, UnseenArmorMaterial>();
    /** "<ore_id>_<slot>" -> gear item (pickaxe|sword|helmet|chestplate|leggings|boots) */
    public static final Map<String, RegistrySupplier<Item>> GEAR =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** ore id -> tonic item (applies the ore's potion effect) */
    public static final Map<String, RegistrySupplier<Item>> TONICS =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** tier number -> machine core item */
    public static final Map<Integer, RegistrySupplier<Item>> MACHINE_CORES =
            new LinkedHashMap<Integer, RegistrySupplier<Item>>();
    /** mob id -> spawn egg */
    public static final Map<String, RegistrySupplier<Item>> SPAWN_EGGS =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** lore theme -> journal item */
    public static final Map<String, RegistrySupplier<Item>> LORE_BOOKS =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** mob id -> trophy drop item */
    public static final Map<String, RegistrySupplier<Item>> TROPHIES =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** dimension id -> portal key item */
    public static final Map<String, RegistrySupplier<Item>> PORTAL_KEYS =
            new LinkedHashMap<String, RegistrySupplier<Item>>();
    /** boss id -> unique relic drop */
    public static final Map<String, RegistrySupplier<Item>> BOSS_RELICS =
            new LinkedHashMap<String, RegistrySupplier<Item>>();

    private static RegistrySupplier<Item> track(RegistrySupplier<Item> supplier) {
        ALL_ITEMS.add(supplier);
        return supplier;
    }

    private ModItems() {
    }

    public static void registerContent() {
%(tabs_register)s%(tab_setup)s
        UNSEEN_SIGIL = track(ModRegistries.ITEMS.register("unseen_sigil",
                () -> new Item(new Item.Properties()%(props16)s)));

        // Block items for every registered block.
        for (RegistrySupplier<Block> block : ModBlocks.allOres().values()) {
            track(ModRegistries.ITEMS.register(block.getId().getPath(),
                    () -> new BlockItem(block.get(), new Item.Properties()%(props_plain)s)));
        }
        for (RegistrySupplier<Block> block : ModBlocks.allDecor().values()) {
            track(ModRegistries.ITEMS.register(block.getId().getPath(),
                    () -> new BlockItem(block.get(), new Item.Properties()%(props_plain)s)));
        }
        for (RegistrySupplier<Block> block : ModBlocks.allPlants().values()) {
            track(ModRegistries.ITEMS.register(block.getId().getPath(),
                    () -> new BlockItem(block.get(), new Item.Properties()%(props_plain)s)));
        }

        // Ore minerals, tool tiers, armor materials, gear and tonics.
        for (int i = 0; i < Content.ORES.size(); i++) {
            final OreDef ore = Content.ORES.get(i);
            RegistrySupplier<Item> mineral = track(ModRegistries.ITEMS.register(ore.id,
                    () -> new Item(new Item.Properties()%(props_plain)s)));
            MINERALS.put(ore.id, mineral);
            TOOL_TIERS.put(ore.id, new UnseenToolTier(ore,
                    () -> Ingredient.of(mineral.get())));
            ARMOR_MATERIALS.put(ore.id, new UnseenArmorMaterial(ore,
                    () -> Ingredient.of(mineral.get())));
            GEAR.put(ore.id + "_pickaxe", track(ModRegistries.ITEMS.register(
                    ore.id + "_pickaxe",
                    () -> UnseenGearItems.pickaxe(ore, TOOL_TIERS.get(ore.id),
                            new Item.Properties()%(props_plain)s))));
            GEAR.put(ore.id + "_sword", track(ModRegistries.ITEMS.register(
                    ore.id + "_sword",
                    () -> UnseenGearItems.sword(ore, TOOL_TIERS.get(ore.id),
                            new Item.Properties()%(props_plain)s))));
            GEAR.put(ore.id + "_helmet", track(ModRegistries.ITEMS.register(
                    ore.id + "_helmet",
                    () -> UnseenGearItems.helmet(ore, ARMOR_MATERIALS.get(ore.id),
                            new Item.Properties()%(props_plain)s))));
            GEAR.put(ore.id + "_chestplate", track(ModRegistries.ITEMS.register(
                    ore.id + "_chestplate",
                    () -> UnseenGearItems.chestplate(ore, ARMOR_MATERIALS.get(ore.id),
                            new Item.Properties()%(props_plain)s))));
            GEAR.put(ore.id + "_leggings", track(ModRegistries.ITEMS.register(
                    ore.id + "_leggings",
                    () -> UnseenGearItems.leggings(ore, ARMOR_MATERIALS.get(ore.id),
                            new Item.Properties()%(props_plain)s))));
            GEAR.put(ore.id + "_boots", track(ModRegistries.ITEMS.register(
                    ore.id + "_boots",
                    () -> UnseenGearItems.boots(ore, ARMOR_MATERIALS.get(ore.id),
                            new Item.Properties()%(props_plain)s))));
            TONICS.put(ore.id, track(ModRegistries.ITEMS.register(
                    ore.id + "_tonic",
                    () -> new com.biomesunseen.item.UnseenTonicItem(ore,
                            new Item.Properties()%(props16)s))));
        }

        // Machine cores, one per machine tier used by the ore catalog.
        for (int tier = 1; tier <= 4; tier++) {
            MACHINE_CORES.put(tier, track(ModRegistries.ITEMS.register(
                    "machine_core_t" + tier,
                    () -> new Item(new Item.Properties()%(props16)s))));
        }

        // Spawn eggs for every mob and boss.
        for (int i = 0; i < Content.MOBS.size(); i++) {
            final String mobId = Content.MOBS.get(i).id;
            final int color = Content.MOBS.get(i).baseColor;
            final int accent = com.biomesunseen.core.ColorUtil.shade(color, 0.55D);
            SPAWN_EGGS.put(mobId, track(ModRegistries.ITEMS.register(
                    mobId + "_spawn_egg",
                    () -> new SpawnEggItem((EntityType<? extends MobEntityLike>) (EntityType<?>) ModEntities.MOB_TYPES.get(mobId).get(),
                            color, accent, new Item.Properties()%(props_plain)s))));
        }
        for (int i = 0; i < Content.BOSSES.size(); i++) {
            final String bossId = Content.BOSSES.get(i).id;
            final int color = Content.BOSSES.get(i).color;
            final int accent = com.biomesunseen.core.ColorUtil.shade(color, 0.5D);
            SPAWN_EGGS.put(bossId, track(ModRegistries.ITEMS.register(
                    bossId + "_spawn_egg",
                    () -> new SpawnEggItem((EntityType<? extends MobEntityLike>) (EntityType<?>) ModEntities.BOSS_TYPES.get(bossId).get(),
                            color, accent, new Item.Properties()%(props_plain)s))));
        }

        // Lore journals: one per structure lore theme.
        LinkedHashSet<String> themes = new LinkedHashSet<String>();
        for (int i = 0; i < Content.STRUCTURES.size(); i++) {
            themes.add(Content.STRUCTURES.get(i).loreTheme);
        }
        for (final String theme : themes) {
            LORE_BOOKS.put(theme, track(ModRegistries.ITEMS.register(
                    "lore_journal_" + theme,
                    () -> new com.biomesunseen.item.LoreBookItem(theme,
                            new Item.Properties()%(props_one)s))));
        }

        // Mob trophies used in crafting and structure decor.
        for (int i = 0; i < Content.MOBS.size(); i++) {
            final String mobId = Content.MOBS.get(i).id;
            TROPHIES.put(mobId, track(ModRegistries.ITEMS.register(
                    mobId + "_trophy",
                    () -> new Item(new Item.Properties()%(props_plain)s))));
        }

        // Dimension keys: right-click to enter the dimension, or to return to
        // the overworld when standing inside it.
%(portal_key_loop)s
        // Unique relic dropped by every boss (guaranteed, one per kill).
        for (int i = 0; i < Content.BOSSES.size(); i++) {
            final String bossId = Content.BOSSES.get(i).id;
            BOSS_RELICS.put(bossId, track(ModRegistries.ITEMS.register(
                    bossId + "_relic",
                    () -> new Item(new Item.Properties()%(props_plain)s))));
        }
    }

    public static RegistrySupplier<Item> mineral(String oreId) {
        return MINERALS.get(oreId);
    }
}
''' % {
        "imports": items_imports,
        "tabs_import": tabs_import,
        "tab_field": tab_field,
        "tabs_register": tabs_register,
        "tab_setup": tab_setup,
        "props16": props16,
        "portal_key_loop": portal_key_loop,
        "props_plain": props_plain,
        "props_one": props_one,
        "n_minerals": len(ORE_ROWS),
        "n_gear": len(ORE_ROWS) * 6,
        "n_tonics": len(ORE_ROWS),
        "n_core": 4,
        "n_eggs": len(MOB_ROWS) + len(BOSS_ROWS),
        "n_lore": len({row[13] for row in STRUCTURE_ROWS}),
        "n_trophies": len(MOB_ROWS),
    })

    # Spawn egg casts need the era's Mob base type name.
    items_path = os.path.join(root, base + "/registry/ModItems.java")
    with open(items_path) as fh:
        text = fh.read()
    mob_like = "MobEntity" if legacy else "Mob"
    text = text.replace("MobEntityLike", mob_like)
    with open(items_path, "w") as fh:
        fh.write(text)

    # ------------------------------------------------------------------ #
    # ModTags.java
    # ------------------------------------------------------------------ #
    if F.get("tagkey"):
        tags_body = '''package com.biomesunseen.registry;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.item.Item;
import net.minecraft.world.entity.EntityType;

/**
 * Interop tags (common "c" namespace plus mod-private tags) for wood, stone,
 * ores, plants and mobs so other mods can consume Biomes Unseen content.
 */
public final class ModTags {

    public static final TagKey<Block> ORES = TagKey.create(Registries.BLOCK, new ResourceLocation("c", "ores"));
    public static final TagKey<Block> ORES_IN_GROUND_STONE = TagKey.create(Registries.BLOCK, new ResourceLocation("c", "ores_in_ground/stone"));
    public static final TagKey<Block> ORES_IN_GROUND_DEEPSLATE = TagKey.create(Registries.BLOCK, new ResourceLocation("c", "ores_in_ground/deepslate"));
    public static final TagKey<Block> STONES = TagKey.create(Registries.BLOCK, new ResourceLocation("c", "stones"));
    public static final TagKey<Block> WOODS = TagKey.create(Registries.BLOCK, new ResourceLocation("c", "woods"));
    public static final TagKey<Block> PLANTS = TagKey.create(Registries.BLOCK, new ResourceLocation("c", "plants"));
    public static final TagKey<Block> UNSEEN_ORES = TagKey.create(Registries.BLOCK, new ResourceLocation("biomesunseen", "ores"));
    public static final TagKey<Block> UNSEEN_TERRAIN = TagKey.create(Registries.BLOCK, new ResourceLocation("biomesunseen", "terrain"));
    public static final TagKey<Block> UNSEEN_PLANTS = TagKey.create(Registries.BLOCK, new ResourceLocation("biomesunseen", "plants"));

    public static final TagKey<Item> ITEM_ORES = TagKey.create(Registries.ITEM, new ResourceLocation("c", "ores"));
    public static final TagKey<Item> ITEM_DUSTS = TagKey.create(Registries.ITEM, new ResourceLocation("c", "dusts"));
    public static final TagKey<Item> ITEM_GEMS = TagKey.create(Registries.ITEM, new ResourceLocation("c", "gems"));
    public static final TagKey<Item> ITEM_INGOTS = TagKey.create(Registries.ITEM, new ResourceLocation("c", "ingots"));
    public static final TagKey<Item> UNSEEN_ITEM_ORES = TagKey.create(Registries.ITEM, new ResourceLocation("biomesunseen", "ores"));

    public static final TagKey<EntityType<?>> UNSEEN_MOBS = TagKey.create(Registries.ENTITY_TYPE, new ResourceLocation("biomesunseen", "mobs"));
    public static final TagKey<EntityType<?>> UNSEEN_BOSSES = TagKey.create(Registries.ENTITY_TYPE, new ResourceLocation("biomesunseen", "bosses"));
    public static final TagKey<EntityType<?>> TAMEABLE = TagKey.create(Registries.ENTITY_TYPE, new ResourceLocation("biomesunseen", "tameable"));
    public static final TagKey<EntityType<?>> PACK_MOBS = TagKey.create(Registries.ENTITY_TYPE, new ResourceLocation("biomesunseen", "pack_mobs"));

    private ModTags() {
    }
}
'''
    else:
        tags_body = '''package com.biomesunseen.registry;

/**
 * Tag id strings for the pre-TagKey Minecraft lines.  Data generation writes
 * the same tag JSON documents; runtime code can resolve ids through these
 * constants.
 */
public final class ModTags {

    public static final String ORES = "c:ores";
    public static final String ORES_IN_GROUND_STONE = "c:ores_in_ground/stone";
    public static final String ORES_IN_GROUND_DEEPSLATE = "c:ores_in_ground/deepslate";
    public static final String STONES = "c:stones";
    public static final String WOODS = "c:woods";
    public static final String PLANTS = "c:plants";
    public static final String UNSEEN_ORES = "biomesunseen:ores";
    public static final String UNSEEN_TERRAIN = "biomesunseen:terrain";
    public static final String UNSEEN_PLANTS = "biomesunseen:plants";
    public static final String UNSEEN_MOBS = "biomesunseen:mobs";
    public static final String UNSEEN_BOSSES = "biomesunseen:bosses";
    public static final String TAMEABLE = "biomesunseen:tameable";
    public static final String PACK_MOBS = "biomesunseen:pack_mobs";

    private ModTags() {
    }
}
'''
    _w(root, base + "/registry/ModTags.java", tags_body)

    # ------------------------------------------------------------------ #
    # item/UnseenTonicItem.java + LoreBookItem.java
    # ----------------------------------------------------------------= #
    if legacy:
        use_imports = ("import net.minecraft.entity.player.PlayerEntity;\n"
                       "import net.minecraft.item.Item;\n"
                       "import net.minecraft.item.ItemStack;\n"
                       "import net.minecraft.potion.EffectInstance;\n"
                       "import net.minecraft.potion.Effects;\n"
                       "import net.minecraft.util.ActionResultType;\n"
                       "import net.minecraft.util.Hand;\n"
                       "import net.minecraft.world.World;")
        player_t = "PlayerEntity"
        world_t = "World"
        result_ok = "ActionResultType.SUCCESS"
    else:
        use_imports = ("import net.minecraft.world.entity.player.Player;\n"
                       "import net.minecraft.world.item.Item;\n"
                       "import net.minecraft.world.item.ItemStack;\n"
                       "import net.minecraft.world.item.ItemUtils;\n"
                       "import net.minecraft.world.effect.MobEffectInstance;\n"
                       "import net.minecraft.world.effect.MobEffects;\n"
                       "import net.minecraft.world.InteractionResultHolder;\n"
                       "import net.minecraft.world.InteractionHand;\n"
                       "import net.minecraft.world.level.Level;")
        player_t = "Player"
        world_t = "Level"
        result_ok = "InteractionResultHolder.success(stack)"

    if legacy:
        tonic_use = '''    @Override
    public ActionResultType use(World world, %(player)s player, Hand hand) {
        ItemStack stack = player.getItemInHand(hand);
        player.addEffect(new EffectInstance(effectFor(ore), 20 * 60, 0));
        if (!player.abilities.instabuild) {
            stack.shrink(1);
        }
        return ActionResultType.SUCCESS;
    }
''' % {"player": player_t}
    else:
        tonic_use = '''    @Override
    public InteractionResultHolder<ItemStack> use(Level level, %(player)s player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        player.addEffect(new MobEffectInstance(effectFor(ore), 20 * 60, 0));
        if (!player.getAbilities().instabuild) {
            stack.shrink(1);
        }
        return InteractionResultHolder.success(stack);
    }
''' % {"player": player_t}

    if legacy:
        effect_return = "net.minecraft.potion.Effect"
        effect_method = '''    private static net.minecraft.potion.Effect effectFor(OreDef ore) {
        if ("fire_resistance".equals(ore.potionEffect)) {
            return Effects.FIRE_RESISTANCE;
        }
        if ("swiftness".equals(ore.potionEffect)) {
            return Effects.MOVEMENT_SPEED;
        }
        if ("strength".equals(ore.potionEffect)) {
            return Effects.DAMAGE_BOOST;
        }
        if ("regeneration".equals(ore.potionEffect)) {
            return Effects.REGENERATION;
        }
        if ("invisibility".equals(ore.potionEffect)) {
            return Effects.INVISIBILITY;
        }
        if ("night_vision".equals(ore.potionEffect)) {
            return Effects.NIGHT_VISION;
        }
        if ("water_breathing".equals(ore.potionEffect)) {
            return Effects.WATER_BREATHING;
        }
        if ("poison".equals(ore.potionEffect)) {
            return Effects.POISON;
        }
        if ("slowness".equals(ore.potionEffect)) {
            return Effects.MOVEMENT_SLOWDOWN;
        }
        if ("haste".equals(ore.potionEffect)) {
            return Effects.DIG_SPEED;
        }
        if ("levitation".equals(ore.potionEffect)) {
            return Effects.LEVITATION;
        }
        if ("absorption".equals(ore.potionEffect)) {
            return Effects.ABSORPTION;
        }
        return Effects.DAMAGE_RESISTANCE;
    }
'''
    else:
        effect_method = '''    private static net.minecraft.world.effect.MobEffect effectFor(OreDef ore) {
        if ("fire_resistance".equals(ore.potionEffect)) {
            return MobEffects.FIRE_RESISTANCE;
        }
        if ("swiftness".equals(ore.potionEffect)) {
            return MobEffects.MOVEMENT_SPEED;
        }
        if ("strength".equals(ore.potionEffect)) {
            return MobEffects.DAMAGE_BOOST;
        }
        if ("regeneration".equals(ore.potionEffect)) {
            return MobEffects.REGENERATION;
        }
        if ("invisibility".equals(ore.potionEffect)) {
            return MobEffects.INVISIBILITY;
        }
        if ("night_vision".equals(ore.potionEffect)) {
            return MobEffects.NIGHT_VISION;
        }
        if ("water_breathing".equals(ore.potionEffect)) {
            return MobEffects.WATER_BREATHING;
        }
        if ("poison".equals(ore.potionEffect)) {
            return MobEffects.POISON;
        }
        if ("slowness".equals(ore.potionEffect)) {
            return MobEffects.MOVEMENT_SLOWDOWN;
        }
        if ("haste".equals(ore.potionEffect)) {
            return MobEffects.DIG_SPEED;
        }
        if ("levitation".equals(ore.potionEffect)) {
            return MobEffects.LEVITATION;
        }
        if ("absorption".equals(ore.potionEffect)) {
            return MobEffects.ABSORPTION;
        }
        return MobEffects.DAMAGE_RESISTANCE;
    }
'''
    _w(root, base + "/item/UnseenTonicItem.java", '''package com.biomesunseen.item;

%(use_imports)s

import com.biomesunseen.core.OreDef;

/**
 * Potion-effect tonic distilled from an ore.  Each ore maps to its potion
 * effect from the ore catalog ("use in potions").
 */
public class UnseenTonicItem extends Item {

    private final OreDef ore;

    public UnseenTonicItem(OreDef ore, Item.Properties properties) {
        super(properties);
        this.ore = ore;
    }

    public OreDef ore() {
        return ore;
    }

%(tonic_use)s
%(effect_method)s
}
''' % {"use_imports": use_imports, "tonic_use": tonic_use, "effect_method": effect_method})

    if legacy:
        lore_use = '''    @Override
    public ActionResultType use(World world, PlayerEntity player, Hand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (world.isClientSide) {
            return ActionResultType.SUCCESS;
        }
        player.sendMessage(new net.minecraft.util.text.TranslationTextComponent(
                "book.biomesunseen." + theme), player.getUUID());
        return ActionResultType.SUCCESS;
    }
'''
    else:
        lore_use = '''    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide) {
            return InteractionResultHolder.success(stack);
        }
        player.sendSystemMessage(net.minecraft.network.chat.Component.translatable(
                "book.biomesunseen." + theme));
        return InteractionResultHolder.success(stack);
    }
'''
    _w(root, base + "/item/UnseenPortalKeyItem.java",
       '''package com.biomesunseen.item;

import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

import com.biomesunseen.worldgen.UnseenTravel;

/**
 * Dimension key.  Right-clicking with it either opens the way into the key's
 * dimension or, when already inside, carries the player back to the overworld
 * spawn.  The destination is looked up by dimension id at use time so the same
 * item works before and after the dimension is registered.
 */
public class UnseenPortalKeyItem extends Item {

    private final String dimensionId;

    public UnseenPortalKeyItem(String dimensionId, Item.Properties properties) {
        super(properties);
        this.dimensionId = dimensionId;
    }

    public String dimensionId() {
        return dimensionId;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!level.isClientSide) {
            UnseenTravel.travel(level, player, dimensionId);
        }
        return InteractionResultHolder.success(stack);
    }
}
''')

    _w(root, base + "/item/LoreBookItem.java", '''package com.biomesunseen.item;

%(use_imports)s

/**
 * Lore journal found in structures.  Reading it surfaces the theme's journal
 * text (written into en_us.json) and unlocks structure advancements.
 */
public class LoreBookItem extends Item {

    private final String theme;

    public LoreBookItem(String theme, Item.Properties properties) {
        super(properties);
        this.theme = theme;
    }

    public String theme() {
        return theme;
    }

%(lore_use)s
}
''' % {"use_imports": use_imports, "lore_use": lore_use})
