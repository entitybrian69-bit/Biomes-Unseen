# CI build results

- build outcome: success
- production-server smoke outcome: failure

## build log (errors + tail)
```
----- tail -----
 > Running 'stripClient'
 > Running 'stripServer'
 > Running 'merge'
 > Running 'listLibraries'
 > Running 'rename'
Stopping at requested step: /home/runner/.gradle/caches/forge_gradle/mcp_repo/de/oceanlabs/mcp/mcp_config/1.20.1-20230612.114412/joined/rename/output.jar
[07:29:19] [main/INFO]: Writing debug log file accesstransform.log
[07:29:19] [main/INFO]: Access Transformer processor running version 8.2.14
[07:29:19] [main/INFO]: Command line arguments [--inJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar, --outJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, --logFile, accesstransform.log, --atFile, /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg]
[07:29:19] [main/INFO]: Reading from /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar
[07:29:19] [main/INFO]: Writing to /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
[07:29:19] [main/INFO]: Transformer file /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg
[07:29:19] [main/WARN]: Found existing output jar /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, overwriting
[07:29:22] [main/INFO]: JAR transformation complete /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
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

BUILD SUCCESSFUL in 1m 46s
7 actionable tasks: 7 executed
```

## dedicated-server smoke log
```
159-	at net.minecraft.world.level.biome.FeatureSorter.m_220603_(FeatureSorter.java:100) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
160-	at net.minecraft.world.level.chunk.ChunkGenerator.m_223094_(ChunkGenerator.java:102) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
161-	at com.google.common.base.Suppliers$NonSerializableMemoizingSupplier.get(Suppliers.java:183) ~[guava-31.1-jre.jar%2374!/:?] {}
--
181:[07:30:20] [Server thread/ERROR] [minecraft/BlockableEventLoop]: Error executing task on Chunk source main thread executor for minecraft:overworld
182:net.minecraft.ReportedException: Exception generating new chunk
183-	at net.minecraft.server.level.ChunkMap.m_214912_(ChunkMap.java:658) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
184-	at net.minecraft.util.thread.BlockableEventLoop.m_6367_(BlockableEventLoop.java:156) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading,pl:accesstransformer:B}
185-	at net.minecraft.server.level.ServerChunkCache$MainThreadExecutor.m_6367_(ServerChunkCache.java:541) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
--
202:Caused by: java.lang.IllegalStateException: Feature order cycle found, involved sources: [Reference{ResourceKey[minecraft:worldgen/biome / minecraft:deep_dark]=net.minecraft.world.level.biome.Biome@2b452bc7}, Reference{ResourceKey[minecraft:worldgen/biome / biomesunseen:dreamwisp_dell]=net.minecraft.world.level.biome.Biome@c6610a9}]
203-	at net.minecraft.world.level.biome.FeatureSorter.m_220603_(FeatureSorter.java:100) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
204-	at net.minecraft.world.level.chunk.ChunkGenerator.m_223094_(ChunkGenerator.java:102) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
205-	at com.google.common.base.Suppliers$NonSerializableMemoizingSupplier.get(Suppliers.java:183) ~[guava-31.1-jre.jar%2374!/:?] {}
--
225:[07:30:21] [Server thread/ERROR] [minecraft/BlockableEventLoop]: Error executing task on Chunk source main thread executor for minecraft:overworld
226:net.minecraft.ReportedException: Exception generating new chunk
227-	at net.minecraft.server.level.ChunkMap.m_214912_(ChunkMap.java:658) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
228-	at net.minecraft.util.thread.BlockableEventLoop.m_6367_(BlockableEventLoop.java:156) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading,pl:accesstransformer:B}
229-	at net.minecraft.server.level.ServerChunkCache$MainThreadExecutor.m_6367_(ServerChunkCache.java:541) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
--
246:Caused by: java.lang.IllegalStateException: Feature order cycle found, involved sources: [Reference{ResourceKey[minecraft:worldgen/biome / minecraft:deep_dark]=net.minecraft.world.level.biome.Biome@2b452bc7}, Reference{ResourceKey[minecraft:worldgen/biome / biomesunseen:dreamwisp_dell]=net.minecraft.world.level.biome.Biome@c6610a9}]
247-	at net.minecraft.world.level.biome.FeatureSorter.m_220603_(FeatureSorter.java:100) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
248-	at net.minecraft.world.level.chunk.ChunkGenerator.m_223094_(ChunkGenerator.java:102) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
249-	at com.google.common.base.Suppliers$NonSerializableMemoizingSupplier.get(Suppliers.java:183) ~[guava-31.1-jre.jar%2374!/:?] {}
--
269:[07:30:21] [Server thread/ERROR] [minecraft/BlockableEventLoop]: Error executing task on Chunk source main thread executor for minecraft:overworld
270:net.minecraft.ReportedException: Exception generating new chunk
271-	at net.minecraft.server.level.ChunkMap.m_214912_(ChunkMap.java:658) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
272-	at net.minecraft.util.thread.BlockableEventLoop.m_6367_(BlockableEventLoop.java:156) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading,pl:accesstransformer:B}
273-	at net.minecraft.server.level.ServerChunkCache$MainThreadExecutor.m_6367_(ServerChunkCache.java:541) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
--
290:Caused by: java.lang.IllegalStateException: Feature order cycle found, involved sources: [Reference{ResourceKey[minecraft:worldgen/biome / minecraft:deep_dark]=net.minecraft.world.level.biome.Biome@2b452bc7}, Reference{ResourceKey[minecraft:worldgen/biome / biomesunseen:dreamwisp_dell]=net.minecraft.world.level.biome.Biome@c6610a9}]
291-	at net.minecraft.world.level.biome.FeatureSorter.m_220603_(FeatureSorter.java:100) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
292-	at net.minecraft.world.level.chunk.ChunkGenerator.m_223094_(ChunkGenerator.java:102) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
293-	at com.google.common.base.Suppliers$NonSerializableMemoizingSupplier.get(Suppliers.java:183) ~[guava-31.1-jre.jar%2374!/:?] {}
--
313:[07:30:22] [Server thread/ERROR] [minecraft/BlockableEventLoop]: Error executing task on Chunk source main thread executor for minecraft:overworld
314:net.minecraft.ReportedException: Exception generating new chunk
315-	at net.minecraft.server.level.ChunkMap.m_214912_(ChunkMap.java:658) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
316-	at net.minecraft.util.thread.BlockableEventLoop.m_6367_(BlockableEventLoop.java:156) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading,pl:accesstransformer:B}
317-	at net.minecraft.server.level.ServerChunkCache$MainThreadExecutor.m_6367_(ServerChunkCache.java:541) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
--
334:Caused by: java.lang.IllegalStateException: Feature order cycle found, involved sources: [Reference{ResourceKey[minecraft:worldgen/biome / minecraft:deep_dark]=net.minecraft.world.level.biome.Biome@2b452bc7}, Reference{ResourceKey[minecraft:worldgen/biome / biomesunseen:dreamwisp_dell]=net.minecraft.world.level.biome.Biome@c6610a9}]
335-	at net.minecraft.world.level.biome.FeatureSorter.m_220603_(FeatureSorter.java:100) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
336-	at net.minecraft.world.level.chunk.ChunkGenerator.m_223094_(ChunkGenerator.java:102) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
337-	at com.google.common.base.Suppliers$NonSerializableMemoizingSupplier.get(Suppliers.java:183) ~[guava-31.1-jre.jar%2374!/:?] {}
--
357:[07:30:22] [Server thread/ERROR] [minecraft/BlockableEventLoop]: Error executing task on Chunk source main thread executor for minecraft:overworld
358:net.minecraft.ReportedException: Exception generating new chunk
359-	at net.minecraft.server.level.ChunkMap.m_214912_(ChunkMap.java:658) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
360-	at net.minecraft.util.thread.BlockableEventLoop.m_6367_(BlockableEventLoop.java:156) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading,pl:accesstransformer:B}
361-	at net.minecraft.server.level.ServerChunkCache$MainThreadExecutor.m_6367_(ServerChunkCache.java:541) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
--
378:Caused by: java.lang.IllegalStateException: Feature order cycle found, involved sources: [Reference{ResourceKey[minecraft:worldgen/biome / minecraft:deep_dark]=net.minecraft.world.level.biome.Biome@2b452bc7}, Reference{ResourceKey[minecraft:worldgen/biome / biomesunseen:dreamwisp_dell]=net.minecraft.world.level.biome.Biome@c6610a9}]
379-	at net.minecraft.world.level.biome.FeatureSorter.m_220603_(FeatureSorter.java:100) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
380-	at net.minecraft.world.level.chunk.ChunkGenerator.m_223094_(ChunkGenerator.java:102) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
381-	at com.google.common.base.Suppliers$NonSerializableMemoizingSupplier.get(Suppliers.java:183) ~[guava-31.1-jre.jar%2374!/:?] {}
--
401:[07:30:23] [Server thread/ERROR] [minecraft/BlockableEventLoop]: Error executing task on Chunk source main thread executor for minecraft:overworld
402:net.minecraft.ReportedException: Exception generating new chunk
403-	at net.minecraft.server.level.ChunkMap.m_214912_(ChunkMap.java:658) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
404-	at net.minecraft.util.thread.BlockableEventLoop.m_6367_(BlockableEventLoop.java:156) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading,pl:accesstransformer:B}
405-	at net.minecraft.server.level.ServerChunkCache$MainThreadExecutor.m_6367_(ServerChunkCache.java:541) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
--
422:Caused by: java.lang.IllegalStateException: Feature order cycle found, involved sources: [Reference{ResourceKey[minecraft:worldgen/biome / minecraft:deep_dark]=net.minecraft.world.level.biome.Biome@2b452bc7}, Reference{ResourceKey[minecraft:worldgen/biome / biomesunseen:dreamwisp_dell]=net.minecraft.world.level.biome.Biome@c6610a9}]
423-	at net.minecraft.world.level.biome.FeatureSorter.m_220603_(FeatureSorter.java:100) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
424-	at net.minecraft.world.level.chunk.ChunkGenerator.m_223094_(ChunkGenerator.java:102) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
425-	at com.google.common.base.Suppliers$NonSerializableMemoizingSupplier.get(Suppliers.java:183) ~[guava-31.1-jre.jar%2374!/:?] {}
--
445:[07:30:23] [Server thread/ERROR] [minecraft/MinecraftServer]: Encountered an unexpected exception
446:net.minecraft.ReportedException: Exception generating new chunk
447-	at net.minecraft.server.MinecraftServer.m_129815_(MinecraftServer.java:359) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading,pl:accesstransformer:B}
448-	at net.minecraft.server.MinecraftServer.m_130006_(MinecraftServer.java:308) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading,pl:accesstransformer:B}
449-	at net.minecraft.server.dedicated.DedicatedServer.m_7038_(DedicatedServer.java:164) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading,pl:accesstransformer:B}
--
453:Caused by: java.lang.IllegalStateException: Feature order cycle found, involved sources: [Reference{ResourceKey[minecraft:worldgen/biome / minecraft:deep_dark]=net.minecraft.world.level.biome.Biome@2b452bc7}, Reference{ResourceKey[minecraft:worldgen/biome / biomesunseen:dreamwisp_dell]=net.minecraft.world.level.biome.Biome@c6610a9}]
454-	at net.minecraft.world.level.biome.FeatureSorter.m_220603_(FeatureSorter.java:100) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
455-	at net.minecraft.world.level.chunk.ChunkGenerator.m_223094_(ChunkGenerator.java:102) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
456-	at com.google.common.base.Suppliers$NonSerializableMemoizingSupplier.get(Suppliers.java:183) ~[guava-31.1-jre.jar%2374!/:?] {}
--
477:[07:30:23] [Server thread/ERROR] [minecraft/MinecraftServer]: This crash report has been saved to: /home/runner/work/Biomes-Unseen/Biomes-Unseen/smoke/server/./crash-reports/crash-2026-10-24_07.30.23-server.txt
478-[07:30:23] [Server thread/INFO] [minecraft/MinecraftServer]: Stopping server
479-[07:30:23] [Server thread/INFO] [minecraft/MinecraftServer]: Saving players
480-[07:30:23] [Server thread/INFO] [minecraft/MinecraftServer]: Saving worlds
481:[07:30:23] [Server thread/ERROR] [minecraft/MinecraftServer]: Exception stopping the server
482:java.util.concurrent.CompletionException: net.minecraft.ReportedException: Exception generating new chunk
483-	at java.util.concurrent.CompletableFuture.encodeThrowable(CompletableFuture.java:315) ~[?:?] {}
484-	at java.util.concurrent.CompletableFuture.completeThrowable(CompletableFuture.java:320) ~[?:?] {}
485-	at java.util.concurrent.CompletableFuture$UniCompose.tryFire(CompletableFuture.java:1159) ~[?:?] {}
--
497:Caused by: net.minecraft.ReportedException: Exception generating new chunk
498-	at net.minecraft.server.level.ChunkMap.lambda$scheduleChunkGeneration$27(ChunkMap.java:660) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
499-	at com.mojang.datafixers.util.Either$Left.map(Either.java:38) ~[datafixerupper-6.0.8.jar%2377!/:?] {}
500-	at net.minecraft.server.level.ChunkMap.lambda$scheduleChunkGeneration$29(ChunkMap.java:634) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
--
503:Caused by: java.lang.IllegalStateException: Feature order cycle found, involved sources: [Reference{ResourceKey[minecraft:worldgen/biome / minecraft:deep_dark]=net.minecraft.world.level.biome.Biome@2b452bc7}, Reference{ResourceKey[minecraft:worldgen/biome / biomesunseen:dreamwisp_dell]=net.minecraft.world.level.biome.Biome@c6610a9}]
504-	at net.minecraft.world.level.biome.FeatureSorter.m_220603_(FeatureSorter.java:100) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
505-	at net.minecraft.world.level.chunk.ChunkGenerator.m_223094_(ChunkGenerator.java:102) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
506-	at com.google.common.base.Suppliers$NonSerializableMemoizingSupplier.get(Suppliers.java:183) ~[guava-31.1-jre.jar%2374!/:?] {}
----- tail -----
[07:30:23] [Server thread/ERROR] [minecraft/MinecraftServer]: Exception stopping the server
java.util.concurrent.CompletionException: net.minecraft.ReportedException: Exception generating new chunk
	at java.util.concurrent.CompletableFuture.encodeThrowable(CompletableFuture.java:315) ~[?:?] {}
	at java.util.concurrent.CompletableFuture.completeThrowable(CompletableFuture.java:320) ~[?:?] {}
	at java.util.concurrent.CompletableFuture$UniCompose.tryFire(CompletableFuture.java:1159) ~[?:?] {}
	at java.util.concurrent.CompletableFuture$Completion.run(CompletableFuture.java:482) ~[?:?] {}
	at net.minecraft.server.level.ChunkTaskPriorityQueueSorter.m_143188_(ChunkTaskPriorityQueueSorter.java:62) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at net.minecraft.util.thread.ProcessorMailbox.m_18759_(ProcessorMailbox.java:91) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at net.minecraft.util.thread.ProcessorMailbox.m_18747_(ProcessorMailbox.java:146) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at net.minecraft.util.thread.ProcessorMailbox.run(ProcessorMailbox.java:102) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at java.util.concurrent.ForkJoinTask$RunnableExecuteAction.exec(ForkJoinTask.java:1395) ~[?:?] {}
	at java.util.concurrent.ForkJoinTask.doExec(ForkJoinTask.java:373) ~[?:?] {}
	at java.util.concurrent.ForkJoinPool$WorkQueue.topLevelExec(ForkJoinPool.java:1182) ~[?:?] {}
	at java.util.concurrent.ForkJoinPool.scan(ForkJoinPool.java:1655) ~[?:?] {}
	at java.util.concurrent.ForkJoinPool.runWorker(ForkJoinPool.java:1622) ~[?:?] {}
	at java.util.concurrent.ForkJoinWorkerThread.run(ForkJoinWorkerThread.java:165) ~[?:?] {}
Caused by: net.minecraft.ReportedException: Exception generating new chunk
	at net.minecraft.server.level.ChunkMap.lambda$scheduleChunkGeneration$27(ChunkMap.java:660) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at com.mojang.datafixers.util.Either$Left.map(Either.java:38) ~[datafixerupper-6.0.8.jar%2377!/:?] {}
	at net.minecraft.server.level.ChunkMap.lambda$scheduleChunkGeneration$29(ChunkMap.java:634) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at java.util.concurrent.CompletableFuture$UniCompose.tryFire(CompletableFuture.java:1150) ~[?:?] {}
	... 11 more
Caused by: java.lang.IllegalStateException: Feature order cycle found, involved sources: [Reference{ResourceKey[minecraft:worldgen/biome / minecraft:deep_dark]=net.minecraft.world.level.biome.Biome@2b452bc7}, Reference{ResourceKey[minecraft:worldgen/biome / biomesunseen:dreamwisp_dell]=net.minecraft.world.level.biome.Biome@c6610a9}]
	at net.minecraft.world.level.biome.FeatureSorter.m_220603_(FeatureSorter.java:100) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at net.minecraft.world.level.chunk.ChunkGenerator.m_223094_(ChunkGenerator.java:102) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at com.google.common.base.Suppliers$NonSerializableMemoizingSupplier.get(Suppliers.java:183) ~[guava-31.1-jre.jar%2374!/:?] {}
	at net.minecraft.world.level.chunk.ChunkGenerator.m_213609_(ChunkGenerator.java:288) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at net.minecraft.world.level.chunk.ChunkStatus.m_279978_(ChunkStatus.java:108) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading,pl:accesstransformer:B}
	at net.minecraft.world.level.chunk.ChunkStatus$SimpleGenerationTask.m_214024_(ChunkStatus.java:309) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at net.minecraft.world.level.chunk.ChunkStatus.m_280308_(ChunkStatus.java:252) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading,pl:accesstransformer:B}
	at net.minecraft.server.level.ChunkMap.lambda$scheduleChunkGeneration$27(ChunkMap.java:643) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at com.mojang.datafixers.util.Either$Left.map(Either.java:38) ~[datafixerupper-6.0.8.jar%2377!/:?] {}
	at net.minecraft.server.level.ChunkMap.lambda$scheduleChunkGeneration$29(ChunkMap.java:634) ~[server-1.20.1-20230612.114412-srg.jar%23107!/:?] {re:classloading}
	at java.util.concurrent.CompletableFuture$UniCompose.tryFire(CompletableFuture.java:1150) ~[?:?] {}
	... 11 more
```

## built jars
```
total 1156
drwxr-xr-x  2 runner runner    4096 Oct 24 07:29 .
drwxr-xr-x 19 runner runner    4096 Oct 24 07:29 ..
-rw-r--r--  1 runner runner 1171963 Oct 24 07:29 biomesunseen-1.1.0.jar
```
