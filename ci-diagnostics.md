# CI build results

- build outcome: success
- production-server smoke outcome: success

## build log (errors + tail)
```
----- tail -----
 > Running 'stripClient'
 > Running 'stripServer'
 > Running 'merge'
 > Running 'listLibraries'
 > Running 'rename'
Stopping at requested step: /home/runner/.gradle/caches/forge_gradle/mcp_repo/de/oceanlabs/mcp/mcp_config/1.20.1-20230612.114412/joined/rename/output.jar
[07:38:14] [main/INFO]: Writing debug log file accesstransform.log
[07:38:14] [main/INFO]: Access Transformer processor running version 8.2.14
[07:38:14] [main/INFO]: Command line arguments [--inJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar, --outJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, --logFile, accesstransform.log, --atFile, /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg]
[07:38:14] [main/INFO]: Reading from /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar
[07:38:14] [main/INFO]: Writing to /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
[07:38:14] [main/INFO]: Transformer file /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg
[07:38:14] [main/WARN]: Found existing output jar /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, overwriting
[07:38:17] [main/INFO]: JAR transformation complete /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
Creating SRG -> MCP TSRG

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

BUILD SUCCESSFUL in 2m 8s
7 actionable tasks: 7 executed
```

## dedicated-server smoke log
```
173:[07:40:30] [Server thread/INFO] [minecraft/GenericThread]: Thread RCON Listener started
174:[07:40:30] [Server thread/INFO] [minecraft/RconThread]: RCON running on 0.0.0.0:25575
175-[07:40:30] [Server thread/INFO] [ne.mi.se.pe.PermissionAPI/]: Successfully initialized permission handler forge:default_handler
176:[07:40:30] [Server thread/INFO] [co.bi.BiomesUnseen/]: Biomes Unseen worldgen ready: 140 biomes, 115 structures, 23 structure sets; Hollow Deep dimension loaded
177:[07:40:30] [RCON Listener #1/INFO] [minecraft/GenericThread]: Thread RCON Client /127.0.0.1 started
178-[07:40:30] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:amber_meadow took 98 ms
179-[07:40:30] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:windmill_ruin took 1 ms
180-[07:40:30] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Stopping the server]
--
182:[07:40:30] [RCON Client /127.0.0.1 #2/INFO] [minecraft/RconClient]: Thread RCON Client /127.0.0.1 shutting down
183-[07:40:30] [Server thread/INFO] [minecraft/MinecraftServer]: Saving players
184-[07:40:30] [Server thread/INFO] [minecraft/MinecraftServer]: Saving worlds
185-[07:40:32] [Server thread/INFO] [minecraft/MinecraftServer]: Saving chunks for level 'ServerLevel[world]'/minecraft:overworld
--
194:[07:40:33] [Server thread/INFO] [minecraft/GenericThread]: Thread RCON Listener stopped
----- tail -----
[07:40:25] [Worker-Main-2/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 89%
[07:40:25] [Worker-Main-2/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 90%
[07:40:26] [Worker-Main-2/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 91%
[07:40:26] [Worker-Main-2/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 92%
[07:40:27] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 93%
[07:40:27] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 94%
[07:40:28] [Worker-Main-1/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 95%
[07:40:28] [Worker-Main-2/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 96%
[07:40:29] [Worker-Main-2/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 98%
[07:40:29] [Worker-Main-1/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 98%
[07:40:30] [Server thread/INFO] [minecraft/LoggerChunkProgressListener]: Time elapsed: 59904 ms
[07:40:30] [Server thread/INFO] [minecraft/DedicatedServer]: Done (67.780s)! For help, type "help"
[07:40:30] [Server thread/INFO] [minecraft/DedicatedServer]: Starting remote control listener
[07:40:30] [Server thread/INFO] [minecraft/GenericThread]: Thread RCON Listener started
[07:40:30] [Server thread/INFO] [minecraft/RconThread]: RCON running on 0.0.0.0:25575
[07:40:30] [Server thread/INFO] [ne.mi.se.pe.PermissionAPI/]: Successfully initialized permission handler forge:default_handler
[07:40:30] [Server thread/INFO] [co.bi.BiomesUnseen/]: Biomes Unseen worldgen ready: 140 biomes, 115 structures, 23 structure sets; Hollow Deep dimension loaded
[07:40:30] [RCON Listener #1/INFO] [minecraft/GenericThread]: Thread RCON Client /127.0.0.1 started
[07:40:30] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:amber_meadow took 98 ms
[07:40:30] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:windmill_ruin took 1 ms
[07:40:30] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Stopping the server]
[07:40:30] [Server thread/INFO] [minecraft/MinecraftServer]: Stopping server
[07:40:30] [RCON Client /127.0.0.1 #2/INFO] [minecraft/RconClient]: Thread RCON Client /127.0.0.1 shutting down
[07:40:30] [Server thread/INFO] [minecraft/MinecraftServer]: Saving players
[07:40:30] [Server thread/INFO] [minecraft/MinecraftServer]: Saving worlds
[07:40:32] [Server thread/INFO] [minecraft/MinecraftServer]: Saving chunks for level 'ServerLevel[world]'/minecraft:overworld
[07:40:33] [Server thread/INFO] [minecraft/MinecraftServer]: Saving chunks for level 'ServerLevel[world]'/minecraft:the_end
[07:40:33] [Server thread/INFO] [minecraft/MinecraftServer]: Saving chunks for level 'ServerLevel[world]'/biomesunseen:hollow_deep
[07:40:33] [Server thread/INFO] [minecraft/MinecraftServer]: Saving chunks for level 'ServerLevel[world]'/minecraft:the_nether
[07:40:33] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (world): All chunks are saved
[07:40:33] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (DIM1): All chunks are saved
[07:40:33] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (hollow_deep): All chunks are saved
[07:40:33] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage (DIM-1): All chunks are saved
[07:40:33] [Server thread/INFO] [minecraft/MinecraftServer]: ThreadedAnvilChunkStorage: All dimensions are saved
[07:40:33] [Server thread/INFO] [minecraft/GenericThread]: Thread RCON Listener stopped
```

## built jars
```
total 1156
drwxr-xr-x  2 runner runner    4096 Oct 24 07:38 .
drwxr-xr-x 19 runner runner    4096 Oct 24 07:38 ..
-rw-r--r--  1 runner runner 1171924 Oct 24 07:38 biomesunseen-1.1.0.jar
```
