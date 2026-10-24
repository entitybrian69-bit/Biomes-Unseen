package com.biomesunseen.datagen;

import com.biomesunseen.BiomesUnseen;
import net.minecraft.data.PackOutput;
import net.minecraftforge.common.data.LanguageProvider;

/** Stub locales: generated empty so the game falls back to en_us until translated. */
public class ModLangStubs extends LanguageProvider {
    public static final String[] LOCALES = {"es_es", "fr_fr", "de_de", "pt_br", "ru_ru", "zh_cn", "ja_jp"};

    public ModLangStubs(PackOutput output, String locale) {
        super(output, BiomesUnseen.MOD_ID, locale);
    }

    @Override
    protected void addTranslations() {
        // Intentionally empty: stub locale.
    }
}
