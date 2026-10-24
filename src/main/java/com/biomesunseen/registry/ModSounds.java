package com.biomesunseen.registry;

import com.biomesunseen.BiomesUnseen;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.LinkedHashMap;
import java.util.Map;

public final class ModSounds {
    public static final DeferredRegister<SoundEvent> SOUNDS =
            DeferredRegister.create(ForgeRegistries.SOUND_EVENTS, BiomesUnseen.MOD_ID);

    /** Ambient / hurt / death trio used by every mob. */
    public record MobSet(RegistryObject<SoundEvent> ambient, RegistryObject<SoundEvent> hurt,
                         RegistryObject<SoundEvent> death) {
    }

    public static final MobSet STALKER = mob("hollow_stalker");
    public static final MobSet SPORELING = mob("sporeling");
    public static final MobSet CRAWLER = mob("gloom_crawler");
    public static final MobSet GOLEM = mob("crystal_golem");
    public static final MobSet WRAITH = mob("mire_wraith");
    public static final MobSet HEART = mob("heart_of_the_forest");
    public static final RegistryObject<SoundEvent> HEART_SHOOT = reg("heart_of_the_forest.shoot");
    public static final RegistryObject<SoundEvent> HEART_PHASE = reg("heart_of_the_forest.phase_shift");

    /** Shared sound sets for the generated spec mobs, keyed by archetype. */
    public static final Map<String, MobSet> GENERIC = new LinkedHashMap<>();

    static {
        for (String archetype : new String[]{"biped", "brute", "crawler", "quad", "floater", "blob", "serpent"}) {
            GENERIC.put(archetype, mob("generic_" + archetype));
        }
    }

    private ModSounds() {
    }

    private static MobSet mob(String name) {
        return new MobSet(reg(name + ".ambient"), reg(name + ".hurt"), reg(name + ".death"));
    }

    private static RegistryObject<SoundEvent> reg(String name) {
        return SOUNDS.register(name, () ->
                SoundEvent.createVariableRangeEvent(new ResourceLocation(BiomesUnseen.MOD_ID, name)));
    }

    public static void register(IEventBus bus) {
        SOUNDS.register(bus);
    }
}
