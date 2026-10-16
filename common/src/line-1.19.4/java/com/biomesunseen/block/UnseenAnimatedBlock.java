package com.biomesunseen.block;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;

import software.bernie.geckolib.animatable.GeoBlock;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animatable.manager.AnimatableManager;
import software.bernie.geckolib.animation.AnimatableManager.ControllerRegistrar;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Animated decorative block: the crystal shard block, glowcap and nullglass
 * all pulse/glow through their own GeckoLib animation clips so the world
 * feels alive even in stillness.
 */
public class UnseenAnimatedBlock extends Block implements GeoBlock {

    private final String animId;
    private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

    public UnseenAnimatedBlock(String animId, Block.Properties properties) {
        super(properties);
        this.animId = animId;
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.addAnimationController(new AnimationController<>(this, "pulse", 0, state -> {
            state.getController().setAnimation(RawAnimation.begin()
                    .thenLoop("animation." + animId + ".pulse"));
            return PlayState.CONTINUE;
        }));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return cache;
    }

    @Override
    public double getTick(Object object) {
        return 0;
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
