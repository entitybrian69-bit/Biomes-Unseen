package com.biomesunseen.item;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;

import java.util.List;

/**
 * A written lore book.
 *
 * Every structure in the mod guarantees one of these in its chest pool, so the
 * lore is discoverable rather than being something a player has to look up on a
 * wiki. Right-clicking opens the vanilla written-book screen, which is the
 * cheapest way to present several pages of authored text without a custom GUI.
 *
 * The pages are resolved from the lang file at use time rather than baked into
 * the item, so a translator can rewrite the lore without regenerating loot
 * tables, and so a book found in a chest can carry the pages of the place it
 * came from.
 */
public class BULoreBookItem extends Item {

    /** Lang key prefix; the suffix is derived from the item's registry path. */
    private static final String LORE_KEY_PREFIX = "biomesunseen.lore.structure.";
    /** Maximum pages pulled from the lang file for one book. */
    private static final int MAX_PAGES = 6;

    public BULoreBookItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player,
                                                 InteractionHand hand) {
        ItemStack held = player.getItemInHand(hand);
        if (level.isClientSide()) {
            return InteractionResultHolder.success(held);
        }
        if (!(player instanceof ServerPlayer)) {
            return InteractionResultHolder.pass(held);
        }
        // Build a written book on the fly and open it. The lore item itself is
        // not consumed: a book is a record of a place, not a resource.
        ItemStack written = new ItemStack(Items.WRITTEN_BOOK);
        CompoundTag tag = written.getOrCreateTag();
        tag.putString("author", "Biomes Unseen");
        tag.putString("title", titleFor(held));

        List<String> pages = pagesFor(held);
        net.minecraft.nbt.ListTag pageList = new net.minecraft.nbt.ListTag();
        for (String page : pages) {
            // Written-book pages are stored as JSON text components.
            pageList.add(net.minecraft.nbt.StringTag.valueOf(
                    Component.Serializer.toJson(Component.literal(page))));
        }
        tag.put("pages", pageList);
        written.setTag(tag);

        player.openItemGui(written, hand);
        return InteractionResultHolder.success(held);
    }

    /** The book title, taken from the item's own translation key. */
    private String titleFor(ItemStack stack) {
        return stack.getHoverName().getString();
    }

    /**
     * The pages for this book.
     *
     * Looked up by registry path so each structure's book carries that
     * structure's lore. Pages that are not translated are skipped rather than
     * shown as a raw key, so a partially translated book still reads cleanly.
     */
    private List<String> pagesFor(ItemStack stack) {
        java.util.List<String> pages = new java.util.ArrayList<>();
        net.minecraft.resources.ResourceLocation key =
                net.minecraftforge.registries.ForgeRegistries.ITEMS.getKey(this);
        if (key == null) {
            pages.add("The pages are blank.");
            return pages;
        }
        String path = key.getPath();
        for (int i = 0; i < MAX_PAGES; i++) {
            String suffix = i == 0 ? "" : "." + i;
            String langKey = LORE_KEY_PREFIX + path + suffix;
            Component component = Component.translatable(langKey);
            // translatable() returns the key itself when no translation exists;
            // detecting that is how we stop at the last authored page.
            if (component.getString().equals(langKey)) {
                break;
            }
            pages.add(component.getString());
        }
        if (pages.isEmpty()) {
            pages.add("Whatever was written here has been torn out.");
        }
        return pages;
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level,
                               List<Component> tooltip,
                               net.minecraft.world.item.TooltipFlag flag) {
        // The lore is the point of the item, so say what it is on the tooltip
        // rather than making the player open it to find out.
        tooltip.add(Component.translatable("biomesunseen.tooltip.lore_book")
                .withStyle(net.minecraft.ChatFormatting.DARK_PURPLE,
                        net.minecraft.ChatFormatting.ITALIC));
    }
}
