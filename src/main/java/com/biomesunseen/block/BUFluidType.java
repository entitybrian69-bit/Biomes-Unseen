package com.biomesunseen.block;

import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.client.extensions.common.IClientFluidTypeExtensions;
import net.minecraftforge.fluids.FluidType;

import java.util.function.Consumer;

/**
 * A {@link FluidType} whose still and flowing sprites are our own authored
 * textures rather than the vanilla water sheets.
 *
 * Without this override Forge falls back to {@code block/water_still} and
 * {@code block/water_flow}, so the hand-painted hollow_water, lumen_water,
 * void_fluid and aether_essence art would never be seen in game.
 *
 * {@code initializeClient} is only ever invoked on the physical client, so
 * referencing the client-only extensions interface here is safe on a dedicated
 * server.
 */
public class BUFluidType extends FluidType {

    private final ResourceLocation stillTexture;
    private final ResourceLocation flowingTexture;
    private final int tint;

    public BUFluidType(Properties properties, String name, int tint) {
        super(properties);
        this.stillTexture = new ResourceLocation("biomesunseen", "block/" + name);
        this.flowingTexture = new ResourceLocation("biomesunseen", "block/" + name + "_flow");
        this.tint = tint;
    }

    @Override
    public void initializeClient(Consumer<IClientFluidTypeExtensions> consumer) {
        consumer.accept(new IClientFluidTypeExtensions() {
            @Override
            public ResourceLocation getStillTexture() {
                return stillTexture;
            }

            @Override
            public ResourceLocation getFlowingTexture() {
                return flowingTexture;
            }

            @Override
            public int getTintColor() {
                return tint;
            }
        });
    }
}
