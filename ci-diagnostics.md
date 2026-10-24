# CI build results

- build outcome: success
- production-server smoke outcome: failure

## build log (errors + tail)
```
----- tail -----
 > Running 'merge'
 > Running 'listLibraries'
 > Running 'rename'
Stopping at requested step: /home/runner/.gradle/caches/forge_gradle/mcp_repo/de/oceanlabs/mcp/mcp_config/1.20.1-20230612.114412/joined/rename/output.jar
[10:33:16] [main/INFO]: Writing debug log file accesstransform.log
[10:33:16] [main/INFO]: Access Transformer processor running version 8.2.14
[10:33:16] [main/INFO]: Command line arguments [--inJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar, --outJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, --logFile, accesstransform.log, --atFile, /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg]
[10:33:16] [main/INFO]: Reading from /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar
[10:33:16] [main/INFO]: Writing to /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
[10:33:16] [main/INFO]: Transformer file /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg
[10:33:16] [main/WARN]: Found existing output jar /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, overwriting
[10:33:18] [main/INFO]: JAR transformation complete /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
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

BUILD SUCCESSFUL in 2m 34s
7 actionable tasks: 7 executed
```

## dedicated-server smoke log
```
151:[10:35:08] [Server thread/INFO] [minecraft/GenericThread]: Thread RCON Listener started
152:[10:35:08] [Server thread/INFO] [minecraft/RconThread]: RCON running on 0.0.0.0:25575
153-[10:35:08] [Server thread/INFO] [ne.mi.se.pe.PermissionAPI/]: Successfully initialized permission handler forge:default_handler
154:[10:35:08] [Server thread/INFO] [co.bi.BiomesUnseen/]: Biomes Unseen worldgen ready: 140 biomes, 115 structures, 23 structure sets; Hollow Deep, portal, guide, sigil, weapon items and core recipes loaded
155:[10:35:09] [RCON Listener #1/INFO] [minecraft/GenericThread]: Thread RCON Client /127.0.0.1 started
156-[10:35:09] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:amber_meadow took 66 ms
157-[10:35:09] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:windmill_ruin took 0 ms
158-[10:35:09] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Changed the block at 128, 120, 128]
--
160:[10:35:09] [RCON Client /127.0.0.1 #2/INFO] [minecraft/RconClient]: Thread RCON Client /127.0.0.1 shutting down
161-[10:35:09] [Server thread/INFO] [minecraft/MinecraftServer]: Stopping server
162-[10:35:09] [Server thread/INFO] [minecraft/MinecraftServer]: Saving players
163-[10:35:09] [Server thread/INFO] [minecraft/MinecraftServer]: Saving worlds
----- tail -----
[10:34:59] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 77%
[10:35:00] [Worker-Main-1/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 78%
[10:35:00] [Worker-Main-2/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 79%
[10:35:01] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 81%
[10:35:01] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 82%
[10:35:02] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 83%
[10:35:02] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 84%
[10:35:03] [Worker-Main-1/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 85%
[10:35:03] [Worker-Main-2/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 86%
[10:35:04] [Worker-Main-2/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 88%
[10:35:04] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 89%
[10:35:05] [Worker-Main-1/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 91%
[10:35:05] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 91%
[10:35:06] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 93%
[10:35:06] [Worker-Main-2/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 94%
[10:35:07] [Worker-Main-2/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 95%
[10:35:07] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 96%
[10:35:08] [Worker-Main-3/INFO] [minecraft/LoggerChunkProgressListener]: Preparing spawn area: 98%
[10:35:08] [Server thread/INFO] [minecraft/LoggerChunkProgressListener]: Time elapsed: 48972 ms
[10:35:08] [Server thread/INFO] [minecraft/DedicatedServer]: Done (55.129s)! For help, type "help"
[10:35:08] [Server thread/INFO] [minecraft/DedicatedServer]: Starting remote control listener
[10:35:08] [Server thread/INFO] [minecraft/GenericThread]: Thread RCON Listener started
[10:35:08] [Server thread/INFO] [minecraft/RconThread]: RCON running on 0.0.0.0:25575
[10:35:08] [Server thread/INFO] [ne.mi.se.pe.PermissionAPI/]: Successfully initialized permission handler forge:default_handler
[10:35:08] [Server thread/INFO] [co.bi.BiomesUnseen/]: Biomes Unseen worldgen ready: 140 biomes, 115 structures, 23 structure sets; Hollow Deep, portal, guide, sigil, weapon items and core recipes loaded
[10:35:09] [RCON Listener #1/INFO] [minecraft/GenericThread]: Thread RCON Client /127.0.0.1 started
[10:35:09] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:amber_meadow took 66 ms
[10:35:09] [Server thread/INFO] [minecraft/LocateCommand]: Locating element biomesunseen:windmill_ruin took 0 ms
[10:35:09] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Changed the block at 128, 120, 128]
[10:35:09] [Server thread/INFO] [minecraft/MinecraftServer]: [Rcon: Changed the block at 129, 120, 128]
[10:35:09] [RCON Client /127.0.0.1 #2/INFO] [minecraft/RconClient]: Thread RCON Client /127.0.0.1 shutting down
[10:35:09] [Server thread/INFO] [minecraft/MinecraftServer]: Stopping server
[10:35:09] [Server thread/INFO] [minecraft/MinecraftServer]: Saving players
[10:35:09] [Server thread/INFO] [minecraft/MinecraftServer]: Saving worlds
[10:35:10] [Server thread/INFO] [minecraft/MinecraftServer]: Saving chunks for level 'ServerLevel[world]'/minecraft:overworld
```

## built jars
```
total 1344
drwxr-xr-x  2 runner runner    4096 Oct 24 10:33 .
drwxr-xr-x 19 runner runner    4096 Oct 24 10:33 ..
-rw-r--r--  1 runner runner 1366815 Oct 24 10:33 biomesunseen-1.1.0.jar
```
