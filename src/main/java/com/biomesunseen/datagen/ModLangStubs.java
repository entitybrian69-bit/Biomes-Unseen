package com.biomesunseen.datagen;

import com.biomesunseen.BiomesUnseen;
import net.minecraft.data.PackOutput;
import net.minecraftforge.common.data.LanguageProvider;
import java.util.Map;

/** Curated translations for the Field Guide and core gameplay items. */
public class ModLangStubs extends LanguageProvider {
    public static final String[] LOCALES = {"es_es", "fr_fr", "de_de", "pt_br", "ru_ru", "zh_cn", "ja_jp"};
    private final String locale;
    private static final Map<String, Map<String, String>> TRANSLATIONS = Map.of(
            "es_es", Map.ofEntries(
                    Map.entry("itemGroup.biomesunseen.main", "Biomes Unseen"),
                    Map.entry("block.biomesunseen.hollow_portal", "Portal del Hollow Deep"),
                    Map.entry("item.biomesunseen.hollowite_ingot", "Lingote de Hollowite"),
                    Map.entry("item.biomesunseen.hollowite_sword", "Espada de Hollowite"),
                    Map.entry("item.biomesunseen.hollowite_battleaxe", "Hacha de batalla de Hollowite"),
                    Map.entry("item.biomesunseen.field_guide", "Guía de campo de Biomes Unseen"),
                    Map.entry("item.biomesunseen.hollow_sigil", "Sello del Hollow Deep"),
                    Map.entry("guide.biomesunseen.title", "BIOMES UNSEEN — GUÍA DE CAMPO"),
                    Map.entry("guide.biomesunseen.world", "Crea un mundo NUEVO para generar los biomas y estructuras. Los chunks antiguos no se regeneran."),
                    Map.entry("guide.biomesunseen.biomes", "Encuentra un bioma: /locate biome biomesunseen:amber_meadow"),
                    Map.entry("guide.biomesunseen.structures", "Encuentra una estructura: /locate structure biomesunseen:windmill_ruin"),
                    Map.entry("guide.biomesunseen.dimension", "Usa un Sello para ir y volver de Hollow Deep; te devuelve al punto de aparición del Mundo superior. Respaldo: /execute in biomesunseen:hollow_deep run tp @s 0 100 0"),
                    Map.entry("guide.biomesunseen.portal", "Fabrica un Portal del Hollow Deep con 4 obsidianas, 4 fragmentos de amatista y 1 ojo de ender; entra en él. Si el portal original sigue intacto, la salida te deja junto a él."),
                    Map.entry("guide.biomesunseen.weapons", "Fabrica espadas con su mineral y combina Hollowite con palos para crear un hacha de batalla."),
                    Map.entry("message.biomesunseen.hollow_travel.wrong_dimension", "El viaje solo conecta el Mundo superior y Hollow Deep."),
                    Map.entry("message.biomesunseen.hollow_travel.cooldown", "El viaje se está recargando. Espera un momento antes de intentarlo de nuevo."),
                    Map.entry("item.biomesunseen.hollow_sigil.wrong_dimension", "El sello solo funciona en el Mundo superior y Hollow Deep."),
                    Map.entry("item.biomesunseen.hollow_sigil.dimension_missing", "Hollow Deep no está cargado. Crea un mundo nuevo con Biomes Unseen instalado.")
            ),
            "fr_fr", Map.ofEntries(
                    Map.entry("itemGroup.biomesunseen.main", "Biomes Unseen"),
                    Map.entry("block.biomesunseen.hollow_portal", "Portail du Hollow Deep"),
                    Map.entry("item.biomesunseen.hollowite_ingot", "Lingot de Hollowite"),
                    Map.entry("item.biomesunseen.hollowite_sword", "Épée en Hollowite"),
                    Map.entry("item.biomesunseen.hollowite_battleaxe", "Hache de guerre en Hollowite"),
                    Map.entry("item.biomesunseen.field_guide", "Guide de terrain Biomes Unseen"),
                    Map.entry("item.biomesunseen.hollow_sigil", "Sceau du Hollow Deep"),
                    Map.entry("guide.biomesunseen.title", "BIOMES UNSEEN — GUIDE DE TERRAIN"),
                    Map.entry("guide.biomesunseen.world", "Créez un NOUVEAU monde pour générer les biomes et structures. Les anciens chunks ne sont pas régénérés."),
                    Map.entry("guide.biomesunseen.biomes", "Trouver un biome : /locate biome biomesunseen:amber_meadow"),
                    Map.entry("guide.biomesunseen.structures", "Trouver une structure : /locate structure biomesunseen:windmill_ruin"),
                    Map.entry("guide.biomesunseen.dimension", "Utilisez le Sceau pour voyager depuis Hollow Deep ; il vous ramène au point d’apparition de la Surface. Secours : /execute in biomesunseen:hollow_deep run tp @s 0 100 0"),
                    Map.entry("guide.biomesunseen.portal", "Fabriquez un Portail avec 4 obsidiennes, 4 éclats d’améthyste et 1 œil de l’End ; entrez dedans. Le retour vous dépose près du portail d’origine s’il existe encore."),
                    Map.entry("guide.biomesunseen.weapons", "Fabriquez les épées avec leur minerai ; combinez Hollowite et bâtons pour créer une hache de guerre."),
                    Map.entry("message.biomesunseen.hollow_travel.wrong_dimension", "Le trajet ne relie que la Surface et Hollow Deep."),
                    Map.entry("message.biomesunseen.hollow_travel.cooldown", "Le portail se recharge. Attendez un instant avant de repartir."),
                    Map.entry("item.biomesunseen.hollow_sigil.wrong_dimension", "Le sceau ne fonctionne que dans la Surface et Hollow Deep."),
                    Map.entry("item.biomesunseen.hollow_sigil.dimension_missing", "Hollow Deep n'est pas chargé. Créez un monde avec Biomes Unseen installé.")
            ),
            "de_de", Map.ofEntries(
                    Map.entry("itemGroup.biomesunseen.main", "Biomes Unseen"),
                    Map.entry("block.biomesunseen.hollow_portal", "Hollow-Deep-Portal"),
                    Map.entry("item.biomesunseen.hollowite_ingot", "Hollowitebarren"),
                    Map.entry("item.biomesunseen.hollowite_sword", "Hollowiteschwert"),
                    Map.entry("item.biomesunseen.hollowite_battleaxe", "Hollowite-Kampfaxt"),
                    Map.entry("item.biomesunseen.field_guide", "Biomes-Unseen-Feldführer"),
                    Map.entry("item.biomesunseen.hollow_sigil", "Hollow-Deep-Siegel"),
                    Map.entry("guide.biomesunseen.title", "BIOMES UNSEEN — FELDFÜHRER"),
                    Map.entry("guide.biomesunseen.world", "Erstelle eine NEUE Welt für die neuen Biome und Strukturen. Alte Chunks werden nicht neu generiert."),
                    Map.entry("guide.biomesunseen.biomes", "Biom finden: /locate biome biomesunseen:amber_meadow"),
                    Map.entry("guide.biomesunseen.structures", "Struktur finden: /locate structure biomesunseen:windmill_ruin"),
                    Map.entry("guide.biomesunseen.dimension", "Nutze das Siegel für Reisen nach Hollow Deep und zurück; es bringt dich zum Oberwelt-Spawn. Notfallbefehl: /execute in biomesunseen:hollow_deep run tp @s 0 100 0"),
                    Map.entry("guide.biomesunseen.portal", "Stelle ein Portal aus 4 Obsidian, 4 Amethystscherben und 1 Enderauge her und betrete es. Der Rückweg führt zum ursprünglichen Portal, falls es noch steht."),
                    Map.entry("guide.biomesunseen.weapons", "Schwerter aus dem passenden Erz herstellen; Hollowite und Stöcke ergeben eine Kampfaxt."),
                    Map.entry("message.biomesunseen.hollow_travel.wrong_dimension", "Diese Reiseverbindung führt nur zwischen Oberwelt und Hollow Deep."),
                    Map.entry("message.biomesunseen.hollow_travel.cooldown", "Das Portal lädt noch auf. Warte kurz, bevor du erneut reist."),
                    Map.entry("item.biomesunseen.hollow_sigil.wrong_dimension", "Das Siegel funktioniert nur in der Oberwelt und Hollow Deep."),
                    Map.entry("item.biomesunseen.hollow_sigil.dimension_missing", "Hollow Deep ist nicht geladen. Erstelle eine neue Welt mit Biomes Unseen.")
            ),
            "pt_br", Map.ofEntries(
                    Map.entry("itemGroup.biomesunseen.main", "Biomes Unseen"),
                    Map.entry("block.biomesunseen.hollow_portal", "Portal do Hollow Deep"),
                    Map.entry("item.biomesunseen.hollowite_ingot", "Barra de Hollowite"),
                    Map.entry("item.biomesunseen.hollowite_sword", "Espada de Hollowite"),
                    Map.entry("item.biomesunseen.hollowite_battleaxe", "Machado de batalha de Hollowite"),
                    Map.entry("item.biomesunseen.field_guide", "Guia de campo do Biomes Unseen"),
                    Map.entry("item.biomesunseen.hollow_sigil", "Selo do Hollow Deep"),
                    Map.entry("guide.biomesunseen.title", "BIOMES UNSEEN — GUIA DE CAMPO"),
                    Map.entry("guide.biomesunseen.world", "Crie um mundo NOVO para gerar os biomas e estruturas. Chunks antigos não são regenerados."),
                    Map.entry("guide.biomesunseen.biomes", "Encontre um bioma: /locate biome biomesunseen:amber_meadow"),
                    Map.entry("guide.biomesunseen.structures", "Encontre uma estrutura: /locate structure biomesunseen:windmill_ruin"),
                    Map.entry("guide.biomesunseen.dimension", "Use o Selo para ir e voltar do Hollow Deep; ele retorna você ao ponto de surgimento do Mundo Superior. Alternativa: /execute in biomesunseen:hollow_deep run tp @s 0 100 0"),
                    Map.entry("guide.biomesunseen.portal", "Fabrique um Portal com 4 obsidianas, 4 fragmentos de ametista e 1 olho do End; entre nele. A volta leva você ao portal original se ele ainda existir."),
                    Map.entry("guide.biomesunseen.weapons", "Fabrique espadas com seus minérios; combine Hollowite e gravetos para fazer um machado de batalha."),
                    Map.entry("message.biomesunseen.hollow_travel.wrong_dimension", "Essa viagem conecta apenas o Mundo Superior e o Hollow Deep."),
                    Map.entry("message.biomesunseen.hollow_travel.cooldown", "O portal ainda está recarregando. Aguarde um pouco antes de viajar novamente."),
                    Map.entry("item.biomesunseen.hollow_sigil.wrong_dimension", "O selo funciona apenas no Mundo Superior e no Hollow Deep."),
                    Map.entry("item.biomesunseen.hollow_sigil.dimension_missing", "Hollow Deep não está carregado. Crie um mundo com Biomes Unseen instalado.")
            ),
            "ru_ru", Map.ofEntries(
                    Map.entry("itemGroup.biomesunseen.main", "Biomes Unseen"),
                    Map.entry("block.biomesunseen.hollow_portal", "Портал в Hollow Deep"),
                    Map.entry("item.biomesunseen.hollowite_ingot", "Слиток холлоуита"),
                    Map.entry("item.biomesunseen.hollowite_sword", "Меч из холлоуита"),
                    Map.entry("item.biomesunseen.hollowite_battleaxe", "Боевой топор из холлоуита"),
                    Map.entry("item.biomesunseen.field_guide", "Полевой справочник Biomes Unseen"),
                    Map.entry("item.biomesunseen.hollow_sigil", "Печать Hollow Deep"),
                    Map.entry("guide.biomesunseen.title", "BIOMES UNSEEN — ПОЛЕВОЙ СПРАВОЧНИК"),
                    Map.entry("guide.biomesunseen.world", "Создайте НОВЫЙ мир, чтобы появились биомы и структуры. Старые чанки не обновляются."),
                    Map.entry("guide.biomesunseen.biomes", "Найти биом: /locate biome biomesunseen:amber_meadow"),
                    Map.entry("guide.biomesunseen.structures", "Найти структуру: /locate structure biomesunseen:windmill_ruin"),
                    Map.entry("guide.biomesunseen.dimension", "Используйте Печать для путешествий в Hollow Deep и обратно; она возвращает к точке возрождения Верхнего мира. Запасная команда: /execute in biomesunseen:hollow_deep run tp @s 0 100 0"),
                    Map.entry("guide.biomesunseen.portal", "Создайте портал из 4 обсидианов, 4 осколков аметиста и 1 ока Края и войдите в него. Обратный портал вернёт вас к исходному, если он цел."),
                    Map.entry("guide.biomesunseen.weapons", "Создавайте мечи из соответствующих руд; холлоуит и палки нужны для боевого топора."),
                    Map.entry("message.biomesunseen.hollow_travel.wrong_dimension", "Путешествие возможно только между Верхним миром и Hollow Deep."),
                    Map.entry("message.biomesunseen.hollow_travel.cooldown", "Портал перезаряжается. Подождите немного перед новым путешествием."),
                    Map.entry("item.biomesunseen.hollow_sigil.wrong_dimension", "Печать работает только в Верхнем мире и Hollow Deep."),
                    Map.entry("item.biomesunseen.hollow_sigil.dimension_missing", "Hollow Deep не загружен. Создайте новый мир с Biomes Unseen.")
            ),
            "zh_cn", Map.ofEntries(
                    Map.entry("itemGroup.biomesunseen.main", "Biomes Unseen"),
                    Map.entry("block.biomesunseen.hollow_portal", "Hollow Deep传送门"),
                    Map.entry("item.biomesunseen.hollowite_ingot", "Hollowite锭"),
                    Map.entry("item.biomesunseen.hollowite_sword", "Hollowite剑"),
                    Map.entry("item.biomesunseen.hollowite_battleaxe", "Hollowite战斧"),
                    Map.entry("item.biomesunseen.field_guide", "Biomes Unseen野外指南"),
                    Map.entry("item.biomesunseen.hollow_sigil", "Hollow Deep印记"),
                    Map.entry("guide.biomesunseen.title", "BIOMES UNSEEN — 野外指南"),
                    Map.entry("guide.biomesunseen.world", "请创建一个新世界以生成新生物群系和结构。旧区块不会重新生成。"),
                    Map.entry("guide.biomesunseen.biomes", "定位生物群系：/locate biome biomesunseen:amber_meadow"),
                    Map.entry("guide.biomesunseen.structures", "定位结构：/locate structure biomesunseen:windmill_ruin"),
                    Map.entry("guide.biomesunseen.dimension", "使用印记往返 Hollow Deep；印记会将你送回主世界出生点。备用命令：/execute in biomesunseen:hollow_deep run tp @s 0 100 0"),
                    Map.entry("guide.biomesunseen.portal", "用4块黑曜石、4个紫水晶碎片和1个末影之眼制作传送门并进入。原传送门仍存在时，返回门会将你送到它旁边。"),
                    Map.entry("guide.biomesunseen.weapons", "使用对应矿石制作剑；Hollowite和木棍可制作战斧。"),
                    Map.entry("message.biomesunseen.hollow_travel.wrong_dimension", "该旅行路线仅连接主世界和 Hollow Deep。"),
                    Map.entry("message.biomesunseen.hollow_travel.cooldown", "传送门仍在冷却，请稍等片刻再旅行。"),
                    Map.entry("item.biomesunseen.hollow_sigil.wrong_dimension", "印记只能在主世界和 Hollow Deep 使用。"),
                    Map.entry("item.biomesunseen.hollow_sigil.dimension_missing", "Hollow Deep尚未加载。请创建一个安装了Biomes Unseen的新世界。")
            ),
            "ja_jp", Map.ofEntries(
                    Map.entry("itemGroup.biomesunseen.main", "Biomes Unseen"),
                    Map.entry("block.biomesunseen.hollow_portal", "ホロウディープのポータル"),
                    Map.entry("item.biomesunseen.hollowite_ingot", "ホロウアイトインゴット"),
                    Map.entry("item.biomesunseen.hollowite_sword", "ホロウアイトの剣"),
                    Map.entry("item.biomesunseen.hollowite_battleaxe", "ホロウアイトのバトルアックス"),
                    Map.entry("item.biomesunseen.field_guide", "Biomes Unseenフィールドガイド"),
                    Map.entry("item.biomesunseen.hollow_sigil", "ホロウディープの印章"),
                    Map.entry("guide.biomesunseen.title", "BIOMES UNSEEN — フィールドガイド"),
                    Map.entry("guide.biomesunseen.world", "新しいバイオームと構造物には新規ワールドを作成してください。既存チャンクは再生成されません。"),
                    Map.entry("guide.biomesunseen.biomes", "バイオームを探す: /locate biome biomesunseen:amber_meadow"),
                    Map.entry("guide.biomesunseen.structures", "構造物を探す: /locate structure biomesunseen:windmill_ruin"),
                    Map.entry("guide.biomesunseen.dimension", "印章でHollow Deepへ往復できます。印章を使うとオーバーワールドのスポーン地点に戻ります。予備コマンド: /execute in biomesunseen:hollow_deep run tp @s 0 100 0"),
                    Map.entry("guide.biomesunseen.portal", "黒曜石4個、アメジストの欠片4個、エンダーアイ1個でポータルを作り、中へ入ります。元のポータルが残っていれば、戻り口はその隣へ送ります。"),
                    Map.entry("guide.biomesunseen.weapons", "対応する鉱石から剣を作成できます。Hollowiteと棒でバトルアックスを作れます。"),
                    Map.entry("message.biomesunseen.hollow_travel.wrong_dimension", "この移動手段はオーバーワールドとHollow Deepのみを接続します。"),
                    Map.entry("message.biomesunseen.hollow_travel.cooldown", "ポータルはまだ再使用できません。少し待ってからもう一度移動してください。"),
                    Map.entry("item.biomesunseen.hollow_sigil.wrong_dimension", "印章はオーバーワールドとHollow Deepでのみ使えます。"),
                    Map.entry("item.biomesunseen.hollow_sigil.dimension_missing", "Hollow Deepが読み込まれていません。Biomes Unseenを導入して新しいワールドを作成してください。")
            )
    );

    public ModLangStubs(PackOutput output, String locale) {
        super(output, BiomesUnseen.MOD_ID, locale);
        this.locale = locale;
    }

    @Override
    protected void addTranslations() {
        Map<String, String> localeTranslations = TRANSLATIONS.get(locale);
        if (localeTranslations != null) {
            localeTranslations.forEach(this::add);
        }
    }
}
