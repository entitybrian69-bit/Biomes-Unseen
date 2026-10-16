package com.biomesunseen.block;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;

import software.bernie.geckolib3.core.IAnimatable;
import software.bernie.geckolib3.core.PlayState;
import software.bernie.geckolib3.core.builder.AnimationBuilder;
import software.bernie.geckolib3.core.controller.AnimationController;
import software.bernie.geckolib3.core.event.predicate.AnimationState;
import software.bernie.geckolib3.core.manager.AnimationData;
import software.bernie.geckolib3.core.manager.AnimationFactory;

/**
 * Animated decorative block: the crystal shard block, glowcap and nullglass
 * all pulse/glow through their own GeckoLib animation clips so the world
 * feels alive even in stillness.
 */
public class UnseenAnimatedBlock extends Block implements IAnimatable {

    private final String animId;
    private final AnimationFactory factory = new AnimationFactory(this);

    public UnseenAnimatedBlock(String animId, Block.Properties properties) {
        super(properties);
        this.animId = animId;
    }

    @Override
    public void registerControllers(AnimationData data) {
        data.addAnimationController(new AnimationController<>(this, "pulse", 0, state -> {
            state.getController().setAnimation(new AnimationBuilder()
                    .addAnimation("animation." + animId + ".pulse", true));
            return PlayState.CONTINUE;
        }));
    }

    @Override
    public AnimationFactory getFactory() {
        return factory;
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, java.util.Random random) {
        super.animateTick(state, level, pos, random);
        if (random.nextInt(24) == 0) {
            level.addParticle(com.biomesunseen.registry.ModParticles.BY_ID.get("crystal_spark").get(),
                    pos.getX() + random.nextDouble(), pos.getY() + random.nextDouble(),
                    pos.getZ() + random.nextDouble(), 0.0D, 0.02D, 0.0D);
        }
    }
}
