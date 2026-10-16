package com.biomesunseen.client.render;

import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;

import software.bernie.geckolib3.renderers.geo.GeoBlockRenderer;

import com.biomesunseen.block.UnseenAnimatedBlock;

/**
 * Renderer for animated decorative blocks (crystal shards, glowcaps,
 * nullglass) so their pulse animations display in-world.
 */
public class AnimatedBlockRenderer extends GeoBlockRenderer<UnseenAnimatedBlock> {

    public AnimatedBlockRenderer(BlockEntityRendererProvider.Context context) {
        super(context);
    }
}
