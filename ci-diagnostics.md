# CI build results

- build outcome: success
- production-server smoke outcome: success

## build log (errors + tail)
```
----- tail -----
 > Running 'merge'
 > Running 'listLibraries'
 > Running 'rename'
Stopping at requested step: /home/runner/.gradle/caches/forge_gradle/mcp_repo/de/oceanlabs/mcp/mcp_config/1.20.1-20230612.114412/joined/rename/output.jar
[10:46:12] [main/INFO]: Writing debug log file accesstransform.log
[10:46:12] [main/INFO]: Access Transformer processor running version 8.2.14
[10:46:12] [main/INFO]: Command line arguments [--inJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar, --outJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, --logFile, accesstransform.log, --atFile, /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg]
[10:46:12] [main/INFO]: Reading from /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar
[10:46:12] [main/INFO]: Writing to /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
[10:46:12] [main/INFO]: Transformer file /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg
[10:46:12] [main/WARN]: Found existing output jar /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, overwriting
[10:46:15] [main/INFO]: JAR transformation complete /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
Creating SRG -> MCP TSRG
Note: Some input files use or override a deprecated API.
Note: Recompile with -Xlint:deprecation for details.

> Task :processResources
> Task :classes
> Task :jar
> Task :downloadMcpConfig
> Task :extractSrg
> Task :createMcpToSrg
> Task :reobfJar
> Task :jarJar SKIPPED
> Task :reobfJarJar SKIPPED
> Task :assemble
> Task :compileTestJava NO-SOURCE
> Task :processTestResources NO-SOURCE
> Task :testClasses UP-TO-DATE
> Task :test NO-SOURCE
> Task :check UP-TO-DATE
> Task :build

BUILD SUCCESSFUL in 1m 45s
7 actionable tasks: 7 executed
```

## dedicated-server smoke log
```
176:[10:48:30] [Server thread/INFO] [minecraft/GenericThread]: Thread RCON Listener started
177:[10:48:30] [Server thread/INFO] [minecraft/RconThread]: RCON running on 0.0.0.0:25575
178-[10:48:30] [Server thread/INFO] [ne.mi.se.pe.PermissionAPI/]: Successfully initialized permission handler forge:default_handler
179:[10:48:30] [Server thread/INFO] [co.bi.BiomesUnseen/]: Biomes Unseen worldgen ready: 140 biomes, 115 structures, 23 structure sets; Hollow Deep, portal, guide, sigil, weapon items and core recipes loaded
180:[10:48:31] [Server thread/INFO] [co.bi.BiomesUnseen/]: Hollow travel smoke passed: portal round trip and sigil round trip
181:[10:48:32] [RCON Listener #1/INFO] [minecraft/GenericThread]: Thread RCON Client /127.0.0.1 started
182-[10:48:32] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:amber_meadow took 100 ms
183-[10:48:33] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:windmill_ruin took 1 ms
184-[10:48:33] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Changed the block at 128, 120, 128]
--
201:[10:48:53] [RCON Client /127.0.0.1 #2/INFO] [minecraft/RconClient]: Thread RCON Client /127.0.0.1 shutting down
202-[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: Saving players
203-[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: Saving worlds
204-[10:48:54] [Server thread/INFO] [minecraft/MinecraftServer]: Saving chunks for level 'ServerLevel[world]'/minecraft:overworld
--
213:[10:48:55] [Server thread/INFO] [minecraft/GenericThread]: Thread RCON Listener stopped
214-verified generated biome biomesunseen:amber_meadow in saved chunk (-33, -22)
215-verified naturally generated structure start biomesunseen:windmill_ruin in saved chunk (-17, -15)
----- tail -----
[10:48:32] [RCON Listener #1/INFO] [minecraft/GenericThread]: Thread RCON Client /127.0.0.1 started
[10:48:32] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:amber_meadow took 100 ms
[10:48:33] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:windmill_ruin took 1 ms
[10:48:33] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Changed the block at 128, 120, 128]
[10:48:33] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Changed the block at 129, 120, 128]
[10:48:33] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Changed the block at 128, 120, 128]
[10:48:33] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Changed the block at 129, 120, 128]
[10:48:35] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Marked chunk [-33, -22] in minecraft:overworld to be force loaded]
[10:48:35] [Server thread/WARN] [minecraft/MinecraftServer]: Can't keep up! Is the server overloaded? Running 3789ms or 75 ticks behind
[10:48:42] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Marked chunk [-16, -14] in minecraft:overworld to be force loaded]
[10:48:47] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Unmarked chunk [-33, -22] in minecraft:overworld for force loading]
[10:48:47] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Unmarked chunk [-16, -14] in minecraft:overworld for force loading]
[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (world): All chunks are saved
[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (DIM-1): All chunks are saved
[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (DIM1): All chunks are saved
[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (hollow_deep): All chunks are saved
[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage: All dimensions are saved
[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Saved the game]
[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Stopping the server]
[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: Stopping server
[10:48:53] [RCON Client /127.0.0.1 #2/INFO] [minecraft/RconClient]: Thread RCON Client /127.0.0.1 shutting down
[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: Saving players
[10:48:53] [Server thread/INFO] [minecraft/MinecraftServer]: Saving worlds
[10:48:54] [Server thread/INFO] [minecraft/MinecraftServer]: Saving chunks for level 'ServerLevel[world]'/minecraft:overworld
[10:48:55] [Server thread/INFO] [minecraft/MinecraftServer]: Saving chunks for level 'ServerLevel[world]'/minecraft:the_nether
[10:48:55] [Server thread/INFO] [minecraft/MinecraftServer]: Saving chunks for level 'ServerLevel[world]'/minecraft:the_end
[10:48:55] [Server thread/INFO] [minecraft/MinecraftServer]: Saving chunks for level 'ServerLevel[world]'/biomesunseen:hollow_deep
[10:48:55] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (world): All chunks are saved
[10:48:55] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (DIM-1): All chunks are saved
[10:48:55] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (DIM1): All chunks are saved
[10:48:55] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (hollow_deep): All chunks are saved
[10:48:55] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage: All dimensions are saved
[10:48:55] [Server thread/INFO] [minecraft/GenericThread]: Thread RCON Listener stopped
verified generated biome biomesunseen:amber_meadow in saved chunk (-33, -22)
verified naturally generated structure start biomesunseen:windmill_ruin in saved chunk (-17, -15)
```

## built jars
```
total 1352
drwxr-xr-x  2 runner runner    4096 Oct 24 10:46 .
drwxr-xr-x 19 runner runner    4096 Oct 24 10:46 ..
-rw-r--r--  1 runner runner 1372424 Oct 24 10:46 biomesunseen-1.1.0.jar
```
