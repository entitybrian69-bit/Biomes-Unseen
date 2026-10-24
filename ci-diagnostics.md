# CI build results

- build outcome: success
- dedicated-server smoke outcome: failure

## build log (errors + tail)
```
----- tail -----
 > Running 'stripClient'
 > Running 'stripServer'
 > Running 'merge'
 > Running 'listLibraries'
 > Running 'rename'
Stopping at requested step: /home/runner/.gradle/caches/forge_gradle/mcp_repo/de/oceanlabs/mcp/mcp_config/1.20.1-20230612.114412/joined/rename/output.jar
[07:17:49] [main/INFO]: Writing debug log file accesstransform.log
[07:17:49] [main/INFO]: Access Transformer processor running version 8.2.14
[07:17:49] [main/INFO]: Command line arguments [--inJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar, --outJar, /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, --logFile, accesstransform.log, --atFile, /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg]
[07:17:49] [main/INFO]: Reading from /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-injected.jar
[07:17:49] [main/INFO]: Writing to /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
[07:17:49] [main/INFO]: Transformer file /home/runner/work/Biomes-Unseen/Biomes-Unseen/build/_atJar_4/parent_at.cfg
[07:17:49] [main/WARN]: Found existing output jar /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar, overwriting
[07:17:52] [main/INFO]: JAR transformation complete /home/runner/.gradle/caches/forge_gradle/minecraft_user_repo/net/minecraftforge/forge/1.20.1-47.3.0_mapped_official_1.20.1/forge-1.20.1-47.3.0_mapped_official_1.20.1.jar
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

BUILD SUCCESSFUL in 1m 51s
7 actionable tasks: 7 executed
```

## dedicated-server smoke log
```
3892:[07:18:40] [main/FATAL] [mixin/]: Mixin apply failed terrablender.mixins.json:MixinBuiltInRegistries -> net.minecraft.core.registries.BuiltInRegistries: org.spongepowered.asm.mixin.injection.throwables.InvalidInjectionException Critical injection failure: @Inject annotation on registerSimple could not find any targets matching 'Lnet/minecraft/core/registries/BuiltInRegistries;m_258002_(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;)Lnet/minecraft/core/Registry;' in net.minecraft.core.registries.BuiltInRegistries. Using refmap terrablender.refmap.json [PREINJECT Applicator Phase -> terrablender.mixins.json:MixinBuiltInRegistries -> Prepare Injections ->  -> handler$zza000$registerSimple(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V -> Parse]
3893:org.spongepowered.asm.mixin.injection.throwables.InvalidInjectionException: Critical injection failure: @Inject annotation on registerSimple could not find any targets matching 'Lnet/minecraft/core/registries/BuiltInRegistries;m_258002_(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;)Lnet/minecraft/core/Registry;' in net.minecraft.core.registries.BuiltInRegistries. Using refmap terrablender.refmap.json [PREINJECT Applicator Phase -> terrablender.mixins.json:MixinBuiltInRegistries -> Prepare Injections ->  -> handler$zza000$registerSimple(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V -> Parse]
3894-	at org.spongepowered.asm.mixin.injection.struct.InjectionInfo.validateTargets(InjectionInfo.java:656) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
3895-	at org.spongepowered.asm.mixin.injection.struct.InjectionInfo.findTargets(InjectionInfo.java:587) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
3896-	at org.spongepowered.asm.mixin.injection.struct.InjectionInfo.readAnnotation(InjectionInfo.java:330) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
--
3945:Exception in thread "main" java.lang.RuntimeException: java.lang.reflect.InvocationTargetException
3946-	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.LaunchServiceHandlerDecorator.launch(LaunchServiceHandlerDecorator.java:32)
3947-	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.LaunchServiceHandler.launch(LaunchServiceHandler.java:53)
3948-	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.LaunchServiceHandler.launch(LaunchServiceHandler.java:71)
--
3954:Caused by: java.lang.reflect.InvocationTargetException
3955-	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
3956-	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
3957-	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
--
3988:Caused by: org.spongepowered.asm.mixin.injection.throwables.InvalidInjectionException: Critical injection failure: @Inject annotation on registerSimple could not find any targets matching 'Lnet/minecraft/core/registries/BuiltInRegistries;m_258002_(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;)Lnet/minecraft/core/Registry;' in net.minecraft.core.registries.BuiltInRegistries. Using refmap terrablender.refmap.json [PREINJECT Applicator Phase -> terrablender.mixins.json:MixinBuiltInRegistries -> Prepare Injections ->  -> handler$zza000$registerSimple(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V -> Parse]
3989-	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.injection.struct.InjectionInfo.validateTargets(InjectionInfo.java:656)
3990-	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.injection.struct.InjectionInfo.findTargets(InjectionInfo.java:587)
3991-	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.injection.struct.InjectionInfo.readAnnotation(InjectionInfo.java:330)
----- tail -----
	at java.base/java.lang.reflect.Constructor.newInstance(Constructor.java:481)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.injection.struct.InjectionInfo$InjectorEntry.create(InjectionInfo.java:149)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.injection.struct.InjectionInfo.parse(InjectionInfo.java:708)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.MixinTargetContext.prepareInjections(MixinTargetContext.java:1311)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.MixinApplicatorStandard.prepareInjections(MixinApplicatorStandard.java:1042)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.MixinApplicatorStandard.applyMixin(MixinApplicatorStandard.java:393)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.MixinApplicatorStandard.apply(MixinApplicatorStandard.java:325)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.TargetClassContext.apply(TargetClassContext.java:383)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.TargetClassContext.applyMixins(TargetClassContext.java:365)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.MixinProcessor.applyMixins(MixinProcessor.java:363)
	... 31 more

> Task :runServer FAILED

FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':runServer'.
> Process 'command '/usr/lib/jvm/temurin-17-jdk-amd64/bin/java'' finished with non-zero exit value 1

* Try:
> Run with --stacktrace option to get the stack trace.
> Run with --info or --debug option to get more log output.
> Run with --scan to get full insights.

* Get more help at https://help.gradle.org

Deprecated Gradle features were used in this build, making it incompatible with Gradle 9.0.

You can use '--warning-mode all' to show the individual deprecation warnings and determine if they come from your own scripts or plugins.

See https://docs.gradle.org/8.1.1/userguide/command_line_interface.html#sec:command_line_warnings

BUILD FAILED in 21s
10 actionable tasks: 7 executed, 3 up-to-date
```

## built jars
```
total 1156
drwxr-xr-x  2 runner runner    4096 Oct 24 07:18 .
drwxr-xr-x 21 runner runner    4096 Oct 24 07:18 ..
-rw-r--r--  1 runner runner 1171947 Oct 24 07:18 biomesunseen-1.1.0.jar
```
