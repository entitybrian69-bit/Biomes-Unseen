package com.biomesunseen.util;

import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;

import java.lang.reflect.Field;

/**
 * Single accessor for the {@code level} field of an entity.
 *
 * <p>The field is public on 1.19.4, private from 1.20, and the {@code level()}
 * accessor is removed altogether from 1.20.5 on, so one reflective lookup -
 * cached after the first call - is the only form that compiles and runs on
 * every line from 1.19.4 through 26.x.
 */
public final class EntityLevels {

    private static Field levelField;
    private static boolean resolved;

    private EntityLevels() {
    }

    /** @return the Level the given entity is currently ticking in. */
    public static Level of(Entity entity) {
        if (!resolved) {
            resolved = true;
            try {
                levelField = Entity.class.getDeclaredField("level");
                levelField.setAccessible(true);
            } catch (ReflectiveOperationException e) {
                throw new IllegalStateException("Cannot reach Entity#level", e);
            }
        }
        try {
            return (Level) levelField.get(entity);
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException("Cannot read Entity#level", e);
        }
    }
}
