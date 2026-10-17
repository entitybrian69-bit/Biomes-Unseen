package com.biomesunseen.item;

import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionHand;
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
    public InteractionResult use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!level.isClientSide()) {
            UnseenTravel.travel(level, player, dimensionId);
        }
        return InteractionResult.SUCCESS;
    }
}
