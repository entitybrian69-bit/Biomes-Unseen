package com.biomesunseen.item;

import com.biomesunseen.BiomesUnseen;
import com.biomesunseen.init.BUItems;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.player.ItemTooltipEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * The armour set bonuses, actually applied.
 *
 * <p>Each of the ten gear families authors a {@code set_bonus} and the lang file
 * names all ten for the player, but until this handler existed nothing ever
 * called {@link BUItems#completeSetBonus}. The bonuses were authored, exposed
 * through a public accessor, documented as "used by the armour tick handler" --
 * and wired to nothing, so wearing a full set did exactly what wearing four
 * unrelated pieces did. This is the handler that javadoc claimed existed.
 *
 * <p>A bonus applies only when all four pieces of one family are worn, and is
 * revoked the moment the set is broken rather than allowed to lapse on its own
 * timer, so taking a helmet off mid-fight has an immediate and readable effect.
 *
 * <p>Effects are applied hidden-particle with a HUD icon: a set bonus is a
 * persistent state, and vanilla-style particle spam every tick would obscure the
 * fight it is supposed to help with.
 */
@Mod.EventBusSubscriber(modid = BiomesUnseen.MODID)
public final class BUArmorSetEffects {

    /** How often the worn set is re-evaluated, in ticks. */
    private static final int CHECK_INTERVAL = 20;

    /**
     * Effect duration granted per check.
     *
     * Comfortably longer than the check interval so the effect never lapses
     * between refreshes, and short enough that the explicit revoke below is not
     * doing most of the work if a piece is lost.
     */
    private static final int DURATION = 60;

    /**
     * Night vision needs a longer grant than the others.
     *
     * Vanilla pulses the night-vision overlay once the remaining duration drops
     * below about 200 ticks, so a 60-tick grant would strobe constantly. Granting
     * past the threshold and refreshing on the same interval keeps the view
     * steady, and the explicit revoke on set loss still removes it immediately.
     */
    private static final int NIGHT_VISION_DURATION = 400;

    /** Radius in which the aura bonuses reach hostile mobs. */
    private static final double AURA_RADIUS = 8.0D;

    /** Every effect this handler can apply, so a broken set can be revoked cleanly. */
    private static final Map<String, MobEffect> BONUS_EFFECTS = new LinkedHashMap<>();

    static {
        BONUS_EFFECTS.put("lumenshade_glow", net.minecraft.world.effect.MobEffects.GLOWING);
        BONUS_EFFECTS.put("voidstone_phase", net.minecraft.world.effect.MobEffects.DAMAGE_RESISTANCE);
        BONUS_EFFECTS.put("aetherium_flight_assist", net.minecraft.world.effect.MobEffects.SLOW_FALLING);
        BONUS_EFFECTS.put("chronos_haste", net.minecraft.world.effect.MobEffects.DIG_SPEED);
        BONUS_EFFECTS.put("pyroclast_fire_aura", net.minecraft.world.effect.MobEffects.FIRE_RESISTANCE);
        BONUS_EFFECTS.put("hollowite_night_vision", net.minecraft.world.effect.MobEffects.NIGHT_VISION);
        BONUS_EFFECTS.put("rootiron_regeneration", net.minecraft.world.effect.MobEffects.REGENERATION);
        BONUS_EFFECTS.put("gloomsteel_invisibility", net.minecraft.world.effect.MobEffects.INVISIBILITY);
        BONUS_EFFECTS.put("starforged_luck", net.minecraft.world.effect.MobEffects.LUCK);
        // nullite_wither_aura has no self effect: it only afflicts attackers.
    }

    private BUArmorSetEffects() {
    }

    /**
     * Re-evaluate each player's worn set and apply or revoke the bonus.
     *
     * Runs on the server only. The client derives its own effect icons from the
     * synced effect data, so applying here is enough for both sides.
     */
    @SubscribeEvent
    public static void onPlayerTick(TickEvent.PlayerTickEvent event) {
        if (event.phase != TickEvent.Phase.END) {
            return;
        }
        if (!(event.player instanceof ServerPlayer player)) {
            return;
        }
        if (player.tickCount % CHECK_INTERVAL != 0) {
            return;
        }

        String bonus = BUItems.completeSetBonus(player);
        if (bonus == null) {
            revokeAll(player);
            return;
        }
        apply(bonus, player);
    }

    /** Apply one family's bonus to its wearer. */
    private static void apply(String bonus, ServerPlayer player) {
        MobEffect self = BONUS_EFFECTS.get(bonus);
        if (self != null) {
            int duration = self == net.minecraft.world.effect.MobEffects.NIGHT_VISION
                    ? NIGHT_VISION_DURATION
                    : DURATION;
            // Ambient + hidden particles: the HUD icon is the feedback, and a
            // per-tick particle trail would obscure the fight.
            player.addEffect(new MobEffectInstance(self, duration, 0, true, false, true));
        }

        // The three auras reach outward rather than inward.
        switch (bonus) {
            case "lumenshade_glow":
                // Reveals hostiles through walls -- the scouting half of a
                // light-themed set, and the reason its self-effect is Glowing
                // applied to them rather than to the wearer.
                afflictNearby(player, net.minecraft.world.effect.MobEffects.GLOWING, DURATION);
                break;
            case "nullite_wither_aura":
                afflictNearby(player, net.minecraft.world.effect.MobEffects.WITHER, DURATION);
                break;
            case "pyroclast_fire_aura":
                igniteNearby(player);
                break;
            default:
                break;
        }
    }

    /**
     * Remove every bonus effect this handler could have granted.
     *
     * Called when the set is no longer complete. Without it a broken set would
     * keep its bonus for up to the full grant duration -- and for night vision
     * that is twenty seconds, long enough to feel like the armour never came off.
     *
     * Only effects this handler owns are touched, so a potion the player drank is
     * left alone.
     */
    private static void revokeAll(ServerPlayer player) {
        for (MobEffect effect : BONUS_EFFECTS.values()) {
            MobEffectInstance instance = player.getEffect(effect);
            // isAmbient is the marker for a grant from this handler: potion and
            // beacon effects are not ambient, so they survive.
            if (instance != null && instance.isAmbient()) {
                player.removeEffect(effect);
            }
        }
    }

    /** Apply an effect to hostile mobs within the aura radius. */
    private static void afflictNearby(ServerPlayer player, MobEffect effect, int duration) {
        for (Monster mob : player.level().getEntitiesOfClass(Monster.class,
                player.getBoundingBox().inflate(AURA_RADIUS))) {
            if (!mob.isAlive()) {
                continue;
            }
            mob.addEffect(new MobEffectInstance(effect, duration, 0, true, false, true));
        }
    }

    /**
     * Set nearby hostiles alight.
     *
     * A short burn rather than a damage tick: it reads as an aura, it is legible
     * to the player being attacked, and it does not stack into free damage every
     * check the way a direct hurt call would.
     */
    private static void igniteNearby(ServerPlayer player) {
        for (Monster mob : player.level().getEntitiesOfClass(Monster.class,
                player.getBoundingBox().inflate(AURA_RADIUS / 2.0D))) {
            if (!mob.isAlive() || mob.isOnFire()) {
                continue;
            }
            mob.setSecondsOnFire(3);
        }
    }

    // ------------------------------------------------------------------ //
    //  Discoverability
    // ------------------------------------------------------------------ //

    /**
     * Name the set bonus on every piece of the set.
     *
     * A bonus that only exists once all four pieces are worn is invisible to a
     * player who has found one helmet in a chest. The tooltip is what turns it
     * from a hidden interaction into a reason to go looking for the rest, and the
     * lang file already carries a display name for all ten families -- so this
     * surfaces strings that were authored and otherwise unused.
     */
    @SubscribeEvent
    public static void onTooltip(ItemTooltipEvent event) {
        ItemStack stack = event.getItemStack();
        if (!(stack.getItem() instanceof ArmorItem)) {
            return;
        }
        String setId = BUItems.setIdOf(stack.getItem());
        if (setId == null) {
            return;
        }
        String bonus = BUItems.setBonus(setId);
        if (bonus == null) {
            return;
        }
        event.getToolTip().add(Component.translatable("biomesunseen.armor." + setId + ".bonus")
                .withStyle(net.minecraft.ChatFormatting.GOLD));
        event.getToolTip().add(Component.translatable("biomesunseen.armor.set_requirement")
                .withStyle(net.minecraft.ChatFormatting.DARK_GRAY,
                        net.minecraft.ChatFormatting.ITALIC));
    }
}
