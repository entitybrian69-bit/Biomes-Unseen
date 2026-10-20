package com.biomesunseen.world;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.init.BUBiomes;
import com.biomesunseen.init.BUContent;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.levelgen.SurfaceRules;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.ArrayList;
import java.util.List;

/**
 * Biome-gated surface rules for the Overworld biomes.
 *
 * <p>The three dimensions this mod adds carry their own surface rules inside
 * their noise_settings JSON, so they are already correct. The Overworld is
 * different: its rules come from vanilla's noise settings, which a datapack
 * cannot extend per biome. Without rules of our own, every Overworld biome would
 * grow a grass-and-dirt crust no matter what its authored surface material says
 * -- a biome of abyssal silt or sunbleached sand would still be green.
 *
 * <p>Each rule is gated on {@link SurfaceRules#isBiome}, which is the part that
 * matters for compatibility: our stones are applied only inside our own biomes.
 * An ungated rule would let hollowstone or voidstone bleed into plains and
 * forests across every other mod's biomes too, which is exactly the failure the
 * gate prevents.
 *
 * <p>Materials come from {@code BUContent.OVERWORLD_SURFACES}, generated from the
 * same authored table as everything else, so a surface can never disagree with
 * the biome it belongs to.
 */
public final class BUOverworldSurfaceRules {

    private BUOverworldSurfaceRules() {
    }

    /**
     * Build the rule sequence for every Overworld biome that has materials.
     *
     * A biome whose material cannot be resolved is skipped and logged rather than
     * allowed to throw: these rules are assembled during common setup, and an
     * exception here would abort mod loading for the whole pack over one bad id.
     */
    public static SurfaceRules.RuleSource makeRules() {
        List<SurfaceRules.RuleSource> rules = new ArrayList<>();
        int skipped = 0;

        for (Object[] row : BUContent.OVERWORLD_SURFACES) {
            String id = (String) row[0];
            ResourceKey<Biome> key = BUBiomes.get(id);
            if (key == null) {
                BiomesUnseen.LOGGER.warn("Surface rule for unknown biome {}", id);
                skipped++;
                continue;
            }
            Block top = resolve((String) row[1], id);
            Block filler = resolve((String) row[2], id);
            if (top == null || filler == null) {
                skipped++;
                continue;
            }

            rules.add(SurfaceRules.ifTrue(SurfaceRules.isBiome(key),
                    SurfaceRules.sequence(
                            // The exposed crust is the biome's authored top
                            // material, which is what the player actually sees.
                            SurfaceRules.ifTrue(SurfaceRules.ON_FLOOR,
                                    SurfaceRules.state(top.defaultBlockState())),
                            // A few blocks beneath, the filler takes over, so
                            // digging into a hillside shows the authored subsurface
                            // rather than vanilla dirt under an exotic crust.
                            //
                            // UNDER_FLOOR rather than stoneDepthCheck: in 1.20.1
                            // stoneDepthCheck takes a CaveSurface argument, and
                            // these two constants are exactly the floor /
                            // sub-floor pair vanilla's own Overworld rules are
                            // built from, so there is no signature to get wrong.
                            SurfaceRules.ifTrue(SurfaceRules.UNDER_FLOOR,
                                    SurfaceRules.state(filler.defaultBlockState())))));
        }

        if (skipped > 0) {
            BiomesUnseen.LOGGER.error(
                    "Biomes Unseen: {} Overworld biome(s) have unresolvable surface materials "
                            + "and will fall back to the vanilla crust", skipped);
        }
        BiomesUnseen.LOGGER.info(
                "Biomes Unseen: authored surface rules for {} Overworld biome(s)", rules.size());
        return SurfaceRules.sequence(rules.toArray(new SurfaceRules.RuleSource[0]));
    }

    /**
     * Resolve a namespaced block id, or null with a logged reason.
     *
     * Surface materials may be vanilla or ours, so the lookup goes through the
     * block registry rather than assuming our own namespace.
     */
    private static Block resolve(String id, String biomeId) {
        ResourceLocation location = ResourceLocation.tryParse(id);
        if (location == null) {
            BiomesUnseen.LOGGER.error(
                    "Biome {} has a malformed surface material id: {}", biomeId, id);
            return null;
        }
        Block block = ForgeRegistries.BLOCKS.getValue(location);
        if (block == null) {
            BiomesUnseen.LOGGER.error(
                    "Biome {} references unregistered surface material {}", biomeId, id);
        }
        return block;
    }
}
