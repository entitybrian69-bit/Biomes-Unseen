# BUILD.md - exact build instructions

## 0. Bootstrap

1. Install a JDK for your target (see matrix below). Gradle toolchains will
   auto-download missing JDKs when `foojay-resolver` is available, otherwise
   install manually and set `JAVA_HOME`.
2. Install Gradle 9.8.1 or newer (https://gradle.org), **or** let the included
   `gradlew` script bootstrap the wrapper with `gradle wrapper --gradle-version 9.8.1`.
3. First run needs internet access to the Fabric, Architectury, Forge/NeoForge,
   GeckoLib and Shedaniel (Cloth) maven repositories.

## 1. Build one target

```bash
cd Biomes-Unseen
./gradlew :<module>:build
```

Output jar: `<module>/build/libs/biomesunseen-<mc>-<loader>-1.0.0.jar`

## 2. Full target matrix

| Module | Minecraft | Java | Loader | Loader version |
|---|---|---|---|---|
| `fabric-1.16.5` | 1.16.5 | 8 | Fabric | Fabric Loader 0.16.9 |
| `forge-1.16.5` | 1.16.5 | 8 | Forge | Forge 1.16.5-36.2.42 |
| `fabric-1.17.1` | 1.17.1 | 16 | Fabric | Fabric Loader 0.16.9 |
| `forge-1.17.1` | 1.17.1 | 16 | Forge | Forge 1.17.1-37.1.1 |
| `fabric-1.18.1` | 1.18.1 | 17 | Fabric | Fabric Loader 0.16.9 |
| `forge-1.18.1` | 1.18.1 | 17 | Forge | Forge 1.18.1-39.1.2 |
| `fabric-1.18.2` | 1.18.2 | 17 | Fabric | Fabric Loader 0.16.9 |
| `forge-1.18.2` | 1.18.2 | 17 | Forge | Forge 1.18.2-40.2.21 |
| `fabric-1.19` | 1.19 | 17 | Fabric | Fabric Loader 0.16.9 |
| `forge-1.19` | 1.19 | 17 | Forge | Forge 1.19-41.1.0 |
| `fabric-1.19.1` | 1.19.1 | 17 | Fabric | Fabric Loader 0.16.9 |
| `forge-1.19.1` | 1.19.1 | 17 | Forge | Forge 1.19.1-42.0.9 |
| `fabric-1.19.2` | 1.19.2 | 17 | Fabric | Fabric Loader 0.16.9 |
| `forge-1.19.2` | 1.19.2 | 17 | Forge | Forge 1.19.2-43.4.2 |
| `fabric-1.19.3` | 1.19.3 | 17 | Fabric | Fabric Loader 0.16.9 |
| `forge-1.19.3` | 1.19.3 | 17 | Forge | Forge 1.19.3-44.1.23 |
| `fabric-1.19.4` | 1.19.4 | 17 | Fabric | Fabric Loader 0.16.9 |
| `forge-1.19.4` | 1.19.4 | 17 | Forge | Forge 1.19.4-45.2.0 |
| `fabric-1.20` | 1.20 | 17 | Fabric | Fabric Loader 0.16.9 |
| `forge-1.20` | 1.20 | 17 | Forge | Forge 1.20-46.0.14 |
| `fabric-1.20.1` | 1.20.1 | 17 | Fabric | Fabric Loader 0.16.9 |
| `forge-1.20.1` | 1.20.1 | 17 | Forge | Forge 1.20.1-47.3.12 |
| `fabric-1.20.2` | 1.20.2 | 17 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.20.2` | 1.20.2 | 17 | Neoforge | NeoForge 20.2.88 |
| `fabric-1.20.3` | 1.20.3 | 17 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.20.3` | 1.20.3 | 17 | Neoforge | NeoForge 20.3.113 |
| `fabric-1.20.4` | 1.20.4 | 17 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.20.4` | 1.20.4 | 17 | Neoforge | NeoForge 20.4.237 |
| `fabric-1.20.5` | 1.20.5 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.20.5` | 1.20.5 | 21 | Neoforge | NeoForge 20.5.27 |
| `fabric-1.20.6` | 1.20.6 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.20.6` | 1.20.6 | 21 | Neoforge | NeoForge 20.6.119 |
| `fabric-1.21` | 1.21 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21` | 1.21 | 21 | Neoforge | NeoForge 21.0.167 |
| `fabric-1.21.1` | 1.21.1 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21.1` | 1.21.1 | 21 | Neoforge | NeoForge 21.1.172 |
| `fabric-1.21.2` | 1.21.2 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21.2` | 1.21.2 | 21 | Neoforge | NeoForge 21.2.91 |
| `fabric-1.21.3` | 1.21.3 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21.3` | 1.21.3 | 21 | Neoforge | NeoForge 21.3.63 |
| `fabric-1.21.4` | 1.21.4 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21.4` | 1.21.4 | 21 | Neoforge | NeoForge 21.4.135 |
| `fabric-1.21.5` | 1.21.5 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21.5` | 1.21.5 | 21 | Neoforge | NeoForge 21.5.75 |
| `fabric-1.21.6` | 1.21.6 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21.6` | 1.21.6 | 21 | Neoforge | NeoForge 21.6.28 |
| `fabric-1.21.7` | 1.21.7 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21.7` | 1.21.7 | 21 | Neoforge | NeoForge 21.7.28 |
| `fabric-1.21.8` | 1.21.8 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21.8` | 1.21.8 | 21 | Neoforge | NeoForge 21.8.31 |
| `fabric-1.21.9` | 1.21.9 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21.9` | 1.21.9 | 21 | Neoforge | NeoForge 21.9.33 |
| `fabric-1.21.10` | 1.21.10 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21.10` | 1.21.10 | 21 | Neoforge | NeoForge 21.10.31 |
| `fabric-1.21.11` | 1.21.11 | 21 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-1.21.11` | 1.21.11 | 21 | Neoforge | NeoForge 21.11.1 |
| `fabric-26.1` | 26.1 | 25 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-26.1` | 26.1 | 25 | Neoforge | NeoForge 26.1.3 |
| `fabric-26.1.1` | 26.1.1 | 25 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-26.1.1` | 26.1.1 | 25 | Neoforge | NeoForge 26.1.1.3 |
| `fabric-26.1.2` | 26.1.2 | 25 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-26.1.2` | 26.1.2 | 25 | Neoforge | NeoForge 26.1.2.3 |
| `fabric-26.2` | 26.2 | 25 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-26.2` | 26.2 | 25 | Neoforge | NeoForge 26.2.1 |
| `fabric-26.3` | 26.3 | 25 | Fabric | Fabric Loader 0.16.9 |
| `neoforge-26.3` | 26.3 | 25 | Neoforge | NeoForge 26.3.1 |

## 3. Where jars land

```
<module>/build/libs/
  biomesunseen-<mc>-<loader>-1.0.0.jar        <- drop into mods/
  biomesunseen-<mc>-<loader>-1.0.0-sources.jar <- sources (not needed at runtime)
```

## 4. Datagen

Each module exposes `runDatagen`:

```bash
./gradlew :fabric-1.21.1:runDatagen
```

Generated resources are written to the module's `src/generated/resources` and
are automatically added to the jar. The repository also ships the complete
pre-generated resource tree under `common/src/main/resources` so the mod works
without running datagen first.

## 5. Bumping dependency versions

All dependency versions live in `tools/content.py` and are stamped into every
module's `gradle.properties`. To bump e.g. Fabric API for 1.21.1:

1. Edit `fabric-1.21.1/gradle.properties` (`fabric_api_version=...`) **or**
   edit `FABRIC_API_VERSIONS` in `tools/content.py` and re-run
   `python3 tools/generate.py`.
2. Re-run `./gradlew :fabric-1.21.1:build`.

## 6. Troubleshooting

- **`gradle-wrapper.jar` missing**: run `gradle wrapper --gradle-version 9.8.1` once.
- **Dependency resolution failure**: the pinned Fabric API / GeckoLib / Architectury
  version string for that Minecraft line needs a bump (see section 5).
- **Wrong JDK**: set `org.gradle.java.home` or install the toolchain JDK the
  matrix lists for that target.
- **26.x targets** need a JDK 25 toolchain; Gradle 9.8.1 downloads it automatically.
