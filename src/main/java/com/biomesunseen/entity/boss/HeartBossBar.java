package com.biomesunseen.entity.boss;

import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.world.BossEvent;

/** Phase-aware boss bar: colour, notch count and screen darkening change per phase. */
public class HeartBossBar extends ServerBossEvent {
    public HeartBossBar(Component name) {
        super(name, BossEvent.BossBarColor.GREEN, BossEvent.BossBarOverlay.NOTCHED_10);
        this.applyPhase(1);
    }

    public void applyPhase(int phase) {
        switch (phase) {
            case 1 -> {
                this.setColor(BossEvent.BossBarColor.GREEN);
                this.setOverlay(BossEvent.BossBarOverlay.NOTCHED_10);
                this.setDarkenScreen(false);
                this.setCreateWorldFog(false);
            }
            case 2 -> {
                this.setColor(BossEvent.BossBarColor.YELLOW);
                this.setOverlay(BossEvent.BossBarOverlay.NOTCHED_12);
                this.setDarkenScreen(false);
                this.setCreateWorldFog(false);
            }
            default -> {
                this.setColor(BossEvent.BossBarColor.RED);
                this.setOverlay(BossEvent.BossBarOverlay.NOTCHED_20);
                this.setDarkenScreen(true);
                this.setCreateWorldFog(true);
            }
        }
    }
}
