# CI build results

- build outcome: success

## build log (errors + tail)
```
----- tail -----
 > Running 'stripClient'
 > Running 'stripServer'
 > Running 'merge'
 > Running 'listLibraries'
 > Running 'rename'
Stopping at requested step: /home/runner/.gradle/caches/forge_gradle/mcp_repo/de/oceanlabs/mcp/mcp_config/1.20.1-20230612.114412/joined/rename/output.jar
[05:11:16] [main/INFO]: Writing debug log file accesstransform.log
[05:11:16] [main/INFO]: Access Transformer processor running version 8.2.14
[05:11:16] [main/INFO]: Command line arguments [--inJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar, --outJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, --logFile, accesstransform.log, --atFile, /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg]
[05:11:16] [main/INFO]: Reading from /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar
[05:11:16] [main/INFO]: Writing to /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
[05:11:16] [main/INFO]: Transformer file /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg
[05:11:16] [main/WARN]: Found existing output jar /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, overwriting
[05:11:19] [main/INFO]: JAR transformation complete /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
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

BUILD SUCCESSFUL in 1m 42s
7 actionable tasks: 7 executed
```

## built jars
```
total 1100
drwxr-xr-x  2 runner runner    4096 Oct 24 05:11 .
drwxr-xr-x 18 runner runner    4096 Oct 24 05:11 ..
-rw-r--r--  1 runner runner 1117203 Oct 24 05:11 biomesunseen-1.0.0.jar
```
