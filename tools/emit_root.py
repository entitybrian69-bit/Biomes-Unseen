# -*- coding: utf-8 -*-
"""Emits root build files, wrapper, README, BUILD.md, LICENSE."""

import os

from content import (MOD_ID, MOD_NAME, MOD_VERSION, MOD_GROUP, MOD_DESCRIPTION,
                     MOD_LICENSE, MOD_AUTHORS, TARGETS, LOOM_VERSION,
                     GRADLE_VERSION, FABRIC_LOADER_VERSION)


def _w(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return rel


SETTINGS_GRADLE = '''pluginManagement {
    repositories {
        maven { url = "https://maven.fabricmc.net/" }
        maven { url = "https://maven.architectury.dev/" }
        maven { url = "https://maven.minecraftforge.net/" }
        maven { url = "https://maven.neoforged.net/releases" }
        maven { url = "https://maven.geckolib.com/" }
        maven { url = "https://maven.shedaniel.me/" }
        gradlePluginPortal()
        mavenCentral()
    }
}

rootProject.name = "biomes-unseen"

include(
%(includes)s
)
'''

BUILD_GRADLE = '''// Biomes Unseen - root build script.
// Each subproject (fabric-*, forge-*, neoforge-*) is a standalone Architectury
// Loom module targeting one Minecraft version and one loader.  The shared
// content lives in common/ and is compiled into every module as extra sources.

allprojects {
    group = project.mod_group
    version = project.mod_version

    repositories {
        mavenCentral()
        maven { url = "https://maven.fabricmc.net/" }
        maven { url = "https://maven.architectury.dev/" }
        maven { url = "https://maven.minecraftforge.net/" }
        maven { url = "https://maven.neoforged.net/releases" }
        maven { url = "https://maven.geckolib.com/" }
        maven { url = "https://maven.shedaniel.me/" }
        maven { url = "https://maven.terraformersmc.com/releases" }
        maven { url = "https://oss.sonatype.org/content/repositories/snapshots/" }
    }
}

subprojects {
    apply plugin: "java"

    java {
        toolchain {
            languageVersion = JavaLanguageVersion.of(Integer.parseInt(project.target_java))
        }
        withSourcesJar()
    }

    tasks.withType(JavaCompile).configureEach {
        options.encoding = "UTF-8"
        options.release = Integer.parseInt(project.target_java)
    }

    tasks.withType(ProcessResources).configureEach {
        def props = [
                mod_version      : project.mod_version,
                mod_id           : project.mod_id,
                mod_name         : project.mod_name,
                minecraft_version: project.minecraft_version
        ]
        inputs.properties props
        filesMatching(["META-INF/mods.toml", "META-INF/neoforge.mods.toml", "fabric.mod.json"]) {
            expand props
        }
    }
}
'''

GRADLE_PROPERTIES = '''# ---------------------------------------------------------------------------
# Global project coordinates
# ---------------------------------------------------------------------------
mod_id=biomesunseen
mod_name=Biomes Unseen
mod_version=1.0.0
mod_group=com.biomesunseen
mod_description=A massive world-generation, adventure, biome, structure, ore, mob and boss mod.
mod_license=MIT
mod_authors=Biomes Unseen Team
mod_url=https://github.com/entitybrian69-bit/Biomes-Unseen

# ---------------------------------------------------------------------------
# Build tooling
# ---------------------------------------------------------------------------
org.gradle.jvmargs=-Xmx3G
org.gradle.daemon=true
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=false

# Architectury Loom plugin version used by every subproject
loom_version=%(loom)s
gradle_version=%(gradle)s

# ---------------------------------------------------------------------------
# Common dependency versions (per-module gradle.properties may override)
# ---------------------------------------------------------------------------
fabric_loader_version=%(loader)s
''' % {"loom": LOOM_VERSION, "gradle": GRADLE_VERSION, "loader": FABRIC_LOADER_VERSION}

GITIGNORE = '''# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar
out/
run/
runs/
remappedSrc/
.classpath
.project
.settings/
bin/
eclipse/
.idea/
*.iml
*.ipr
*.iws
.vscode/
*.launch
.classpath
metals.sbt
.bloop/
.kotlin/
*.log
.DS_Store
'''


def _gradlew_sh():
    return r'''#!/bin/sh

#
# Gradle start up script for POSIX.  Bootstraps the Gradle wrapper when the
# wrapper jar is present, otherwise falls back to a system Gradle install so
# the project can be bootstrapped with `gradle wrapper --gradle-version %(g)s`.
#

app_path=$0
while [ -h "$app_path" ]; do
    ls=$(ls -ld "$app_path")
    link=${ls#*' -> '}
    case $link in
        /*) app_path=$link ;;
        *) app_path=$(dirname "$app_path")/$link ;;
    esac
done
APP_HOME=$(cd "$(dirname "$app_path")" && pwd -P) || exit 1

CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar

if [ ! -f "$CLASSPATH" ]; then
    if command -v gradle >/dev/null 2>&1; then
        echo "gradle-wrapper.jar missing - bootstrapping with system Gradle."
        ( cd "$APP_HOME" && exec gradle wrapper --gradle-version %(g)s ) || exit 1
    else
        echo "ERROR: gradle/wrapper/gradle-wrapper.jar is missing and no system Gradle was found." >&2
        echo "Install Gradle %(g)s+ (https://gradle.org) and run:  gradle wrapper --gradle-version %(g)s" >&2
        exit 1
    fi
fi

DEFAULT_JVM_OPTS='"-Xmx64m" "-Xms64m"'

if [ -n "$JAVA_HOME" ]; then
    JAVACMD=$JAVA_HOME/bin/java
else
    JAVACMD=java
fi

exec "$JAVACMD" $DEFAULT_JVM_OPTS -classpath "$CLASSPATH" org.gradle.wrapper.GradleWrapperMain "$@"
''' % {"g": GRADLE_VERSION}


def _gradlew_bat():
    return r'''@rem Gradle startup script for Windows
@if "%%DEBUG%%"=="" @echo off
setlocal

set DIRNAME=%%~dp0
if "%%DIRNAME%%"=="" set DIRNAME=.
set APP_HOME=%%DIRNAME%%

set CLASSPATH=%%APP_HOME%%gradle\wrapper\gradle-wrapper.jar

if not exist "%%CLASSPATH%%" (
    where gradle >nul 2>nul
    if %%ERRORLEVEL%%==0 (
        echo gradle-wrapper.jar missing - bootstrapping with system Gradle.
        pushd "%%APP_HOME%%"
        call gradle wrapper --gradle-version %(g)s
        popd
    ) else (
        echo ERROR: gradle\wrapper\gradle-wrapper.jar is missing and no system Gradle was found. 1>&2
        echo Install Gradle %(g)s+ and run:  gradle wrapper --gradle-version %(g)s 1>&2
        exit /b 1
    )
)

set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"

if defined JAVA_HOME (
    set JAVA_EXE=%%JAVA_HOME%%\bin\java.exe
) else (
    set JAVA_EXE=java.exe
)

"%%JAVA_EXE%%" %%DEFAULT_JVM_OPTS%% -classpath "%%CLASSPATH%%" org.gradle.wrapper.GradleWrapperMain %%*
endlocal
''' % {"g": GRADLE_VERSION}


WRAPPER_PROPERTIES = '''distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-%(g)s-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
''' % {"g": GRADLE_VERSION}

LICENSE = '''MIT License

Copyright (c) 2026 Biomes Unseen Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


def _readme():
    lines = []
    a = lines.append
    a("# %s" % MOD_NAME)
    a("")
    a("> %s" % MOD_DESCRIPTION)
    a("")
    a("**Mod id:** `%s` &nbsp;|&nbsp; **Version:** %s &nbsp;|&nbsp; **License:** %s"
      % (MOD_ID, MOD_VERSION, MOD_LICENSE))
    a("")
    a("## Content")
    a("")
    a("- **80** unique biomes (8 families: Crystal, Ember, Verdant, Frost, Storm, Mire, Sky, Void)")
    a("- **20** ores with unique textures, particles, mining sounds, tool/armor/material tiers and worldgen conditions")
    a("- **30** jigsaw structures including 2 massive boss arenas, lore books, journals and murals")
    a("- **25** mobs with GeckoLib animations, goal-based AI, herding, taming, trading, fleeing, pack tactics and terrain use")
    a("- **2** multi-phase bosses: *The Heart of the Forest* and *The Void Serpent*")
    a("- Full tag support (wood, stone, ores, plants, mobs) for inter-mod compatibility")
    a("- Cloth Config integration: biome rarity, ore rates, structure spacing, mob caps, feature toggles")
    a("- DataGen for blockstates, models, loot tables, recipes, tags, worldgen, biome, structure and spawn data")
    a("")
    a("## Project layout")
    a("")
    a("```")
    a("common/            shared content definitions, registries, worldgen, datagen, assets")
    a("fabric-<mc>/       Fabric entrypoint for Minecraft <mc>")
    a("forge-<mc>/        Forge entrypoint (1.16.5 - 1.20.1)")
    a("neoforge-<mc>/     NeoForge entrypoint (1.20.2+)")
    a("tools/             the project generator that stamps every module")
    a("```")
    a("")
    a("Every target in the 1.16.5 - 26.3 matrix exists as its own Gradle subproject.")
    a("The shared code under `common/` is compiled into each module against that")
    a("module's exact Minecraft/loader toolchain (Architectury Loom, Mojang mappings).")
    a("")
    a("## Requirements")
    a("")
    a("- **JDK** matching the target (8 for 1.16.5, 16 for 1.17.1, 17 for 1.18-1.20.4,")
    a("  21 for 1.20.5-1.21.11, 25 for 26.x). Gradle toolchains download missing JDKs automatically.")
    a("- **Gradle %s** (or run `gradle wrapper --gradle-version %s` once; `gradlew` does this automatically if a system Gradle is on PATH)." % (GRADLE_VERSION, GRADLE_VERSION))
    a("- Internet access to Fabric / Forge / NeoForge / Architectury / GeckoLib / Shedaniel maven hosts.")
    a("")
    a("## Building")
    a("")
    a("Build **one** target (recommended):")
    a("")
    a("```bash")
    a("./gradlew :fabric-1.21.1:build          # Fabric for Minecraft 1.21.1")
    a("./gradlew :neoforge-1.21.1:build       # NeoForge for Minecraft 1.21.1")
    a("./gradlew :forge-1.20.1:build          # Forge for Minecraft 1.20.1")
    a("```")
    a("")
    a("The jar lands in `<module>/build/libs/`.")
    a("")
    a("Build **all** targets (slow, resolves every Minecraft version):")
    a("")
    a("```bash")
    a("./gradlew build")
    a("```")
    a("")
    a("Run datagen for a target (regenerates blockstates/models/loot/recipes/tags/worldgen):")
    a("")
    a("```bash")
    a("./gradlew :fabric-1.21.1:runDatagen")
    a("```")
    a("")
    a("See **BUILD.md** for the full per-target build matrix, output paths and")
    a("dependency-bump instructions.")
    a("")
    a("## Configuration")
    a("")
    a("Everything (biome rarity, ore rates, structure spacing, mob caps, per-feature")
    a("toggles) is configurable through Cloth Config (`Config` -> `Biomes Unseen`) or")
    a("by editing `config/biomesunseen.json`. Defaults generate all content in the world.")
    a("")
    a("## Credits")
    a("")
    a("%s. Licensed under %s." % (MOD_AUTHORS, MOD_LICENSE))
    a("")
    return "\n".join(lines)


def _build_md():
    lines = []
    a = lines.append
    a("# BUILD.md - exact build instructions")
    a("")
    a("## 0. Bootstrap")
    a("")
    a("1. Install a JDK for your target (see matrix below). Gradle toolchains will")
    a("   auto-download missing JDKs when `foojay-resolver` is available, otherwise")
    a("   install manually and set `JAVA_HOME`.")
    a("2. Install Gradle %s or newer (https://gradle.org), **or** let the included" % GRADLE_VERSION)
    a("   `gradlew` script bootstrap the wrapper with `gradle wrapper --gradle-version %s`." % GRADLE_VERSION)
    a("3. First run needs internet access to the Fabric, Architectury, Forge/NeoForge,")
    a("   GeckoLib and Shedaniel (Cloth) maven repositories.")
    a("")
    a("## 1. Build one target")
    a("")
    a("```bash")
    a("cd Biomes-Unseen")
    a("./gradlew :<module>:build")
    a("```")
    a("")
    a("Output jar: `<module>/build/libs/biomesunseen-<mc>-<loader>-1.0.0.jar`")
    a("")
    a("## 2. Full target matrix")
    a("")
    a("| Module | Minecraft | Java | Loader | Loader version |")
    a("|---|---|---|---|---|")
    for mc, java, loaders, family in TARGETS:
        for loader in loaders:
            from content import FORGE_VERSIONS, NEOFORGE_VERSIONS, FABRIC_LOADER_VERSION
            if loader == "fabric":
                lv = "Fabric Loader " + FABRIC_LOADER_VERSION
            elif loader == "forge":
                lv = "Forge " + FORGE_VERSIONS[mc]
            else:
                lv = "NeoForge " + NEOFORGE_VERSIONS[mc]
            a("| `%s-%s` | %s | %s | %s | %s |" % (loader, mc, mc, java, loader.capitalize(), lv))
    a("")
    a("## 3. Where jars land")
    a("")
    a("```")
    a("<module>/build/libs/")
    a("  biomesunseen-<mc>-<loader>-1.0.0.jar        <- drop into mods/")
    a("  biomesunseen-<mc>-<loader>-1.0.0-sources.jar <- sources (not needed at runtime)")
    a("```")
    a("")
    a("## 4. Datagen")
    a("")
    a("Each module exposes `runDatagen`:")
    a("")
    a("```bash")
    a("./gradlew :fabric-1.21.1:runDatagen")
    a("```")
    a("")
    a("Generated resources are written to the module's `src/generated/resources` and")
    a("are automatically added to the jar. The repository also ships the complete")
    a("pre-generated resource tree under `common/src/main/resources` so the mod works")
    a("without running datagen first.")
    a("")
    a("## 5. Bumping dependency versions")
    a("")
    a("All dependency versions live in `tools/content.py` and are stamped into every")
    a("module's `gradle.properties`. To bump e.g. Fabric API for 1.21.1:")
    a("")
    a("1. Edit `fabric-1.21.1/gradle.properties` (`fabric_api_version=...`) **or**")
    a("   edit `FABRIC_API_VERSIONS` in `tools/content.py` and re-run")
    a("   `python3 tools/generate.py`.")
    a("2. Re-run `./gradlew :fabric-1.21.1:build`.")
    a("")
    a("## 6. Troubleshooting")
    a("")
    a("- **`gradle-wrapper.jar` missing**: run `gradle wrapper --gradle-version %s` once." % GRADLE_VERSION)
    a("- **Dependency resolution failure**: the pinned Fabric API / GeckoLib / Architectury")
    a("  version string for that Minecraft line needs a bump (see section 5).")
    a("- **Wrong JDK**: set `org.gradle.java.home` or install the toolchain JDK the")
    a("  matrix lists for that target.")
    a("- **26.x targets** need a JDK 25 toolchain; Gradle %s downloads it automatically." % GRADLE_VERSION)
    a("")
    return "\n".join(lines)


def emit(root):
    modules = []
    for mc, java, loaders, family in TARGETS:
        for loader in loaders:
            modules.append("%s-%s" % (loader, mc))
    includes = ",\n".join('    "%s"' % m for m in modules)
    _w(root, "settings.gradle", SETTINGS_GRADLE % {"includes": includes})
    _w(root, "build.gradle", BUILD_GRADLE)
    _w(root, "gradle.properties", GRADLE_PROPERTIES)
    _w(root, ".gitignore", GITIGNORE)
    _w(root, "gradlew", _gradlew_sh())
    _w(root, "gradlew.bat", _gradlew_bat())
    _w(root, "gradle/wrapper/gradle-wrapper.properties", WRAPPER_PROPERTIES)
    _w(root, "LICENSE", LICENSE)
    _w(root, "README.md", _readme())
    _w(root, "BUILD.md", _build_md())
    os.chmod(os.path.join(root, "gradlew"), 0o755)
