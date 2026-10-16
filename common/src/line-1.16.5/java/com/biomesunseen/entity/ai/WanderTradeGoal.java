package com.biomesunseen.entity.ai;

import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.player.Player;


import com.biomesunseen.entity.BiomesUnseenMob;
import com.biomesunseen.registry.ModItems;

import net.minecraft.world.item.ItemStack;

/**
 * Wandering barter: periodically offers a small trade to nearby players
 * (mob trophy for an ore mineral), playing the trade animation.
 */
public class WanderTradeGoal extends ThrottledGoal {

    private final double speed;
    private int tradeCooldown = 200;
    private Player customer;

    public WanderTradeGoal(PathfinderMob mob, double speed) {
        super(mob);
        this.speed = speed;
        this.setFlags(java.util.EnumSet.of(Flag.MOVE, Flag.LOOK));
    }

    @Override
    protected boolean throttledCanUse() {
        if (!(mob instanceof BiomesUnseenMob) || !((BiomesUnseenMob) mob).mobDef().tradable) {
            return false;
        }
        customer = com.biomesunseen.util.EntityLevels.of(mob).getNearestPlayer(mob, 6.0D);
        return customer != null && tradeCooldown <= 0;
    }

    @Override
    public void start() {
        tradeCooldown = 400;
        ((BiomesUnseenMob) mob).triggerAnim("trade");
        mob.getLookControl().setLookAt(customer, 30.0F, 30.0F);
    }

    @Override
    public boolean canContinueToUse() {
        return customer != null && customer.isAlive() && mob.distanceTo(customer) < 8.0D
                && tradeCooldown > 380;
    }

    @Override
    public void tick() {
        tradeCooldown--;
        if (customer != null && tradeCooldown == 390 && !com.biomesunseen.util.EntityLevels.of(mob).isClientSide()) {
            // Simple barter: trophy from the mob, mineral to the player.
            java.util.List<me.shedaniel.architectury.registry.RegistrySupplier<net.minecraft.world.item.Item>> minerals =
                    new java.util.ArrayList<>(ModItems.MINERALS.values());
            if (!minerals.isEmpty()) {
                ItemStack gift = new ItemStack(minerals.get(mob.getRandom().nextInt(minerals.size())).get());
                if (!customer.addItem(gift)) {
                    customer.drop(gift, false);
                }
                if (!customer.getInventory().items.stream().anyMatch(s -> !s.isEmpty())) {
                    // No payment expected: this is ambient life, not a villager UI.
                }
            }
        }
    }

    @Override
    public void stop() {
        customer = null;
    }

    @Override
    public boolean requiresUpdateEveryTick() {
        return true;
    }
}
