# CI build results

- datagen outcome: success
- build outcome: success

## data generation log (tail)
```
[04:46:19] [main/DEBUG] [mixin/]: Selecting config geckolib.mixins.json
[04:46:19] [main/DEBUG] [mixin/]: Preparing terrablender.mixins.json (7)
[04:46:19] [main/DEBUG] [mixin/]: Preparing terrablender_forge.mixins.json (0)
[04:46:19] [main/DEBUG] [mixin/]: Preparing geckolib.mixins.json (1)
[04:46:19] [main/DEBUG] [mixin/]: Registering new injector for @Inject with org.spongepowered.asm.mixin.injection.struct.CallbackInjectionInfo
[04:46:19] [main/DEBUG] [mixin/]: Registering new injector for @ModifyArg with org.spongepowered.asm.mixin.injection.struct.ModifyArgInjectionInfo
[04:46:19] [main/DEBUG] [mixin/]: Registering new injector for @ModifyArgs with org.spongepowered.asm.mixin.injection.struct.ModifyArgsInjectionInfo
[04:46:19] [main/DEBUG] [mixin/]: Registering new injector for @Redirect with org.spongepowered.asm.mixin.injection.struct.RedirectInjectionInfo
[04:46:19] [main/DEBUG] [mixin/]: Registering new injector for @ModifyVariable with org.spongepowered.asm.mixin.injection.struct.ModifyVariableInjectionInfo
[04:46:19] [main/DEBUG] [mixin/]: Registering new injector for @ModifyConstant with org.spongepowered.asm.mixin.injection.struct.ModifyConstantInjectionInfo
[04:46:19] [main/DEBUG] [io.ne.ut.in.lo.InternalLoggerFactory/]: Using SLF4J as the default logging framework
[04:46:19] [main/DEBUG] [io.ne.ut.ResourceLeakDetector/]: -Dio.netty.leakDetection.level: simple
[04:46:19] [main/DEBUG] [io.ne.ut.ResourceLeakDetector/]: -Dio.netty.leakDetection.targetRecords: 4
[04:46:19] [main/INFO] [ne.mi.da.lo.DatagenModLoader/]: Initializing Data Gatherer for mods [biomesunseen]
[04:46:19] [main/DEBUG] [mixin/]: Mixing MixinBuiltInRegistries from terrablender.mixins.json into net.minecraft.core.registries.BuiltInRegistries
[04:46:19] [main/DEBUG] [mixin/]: Renaming synthetic method lambda$registerSimple$0(Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;Lnet/minecraft/core/Registry;)Ljava/lang/Object; to md856c5b$lambda$registerSimple$0$0 in terrablender.mixins.json:MixinBuiltInRegistries
[04:46:19] [main/FATAL] [mixin/]: Mixin apply failed terrablender.mixins.json:MixinBuiltInRegistries -> net.minecraft.core.registries.BuiltInRegistries: org.spongepowered.asm.mixin.injection.throwables.InvalidInjectionException Critical injection failure: @Inject annotation on registerSimple could not find any targets matching 'Lnet/minecraft/core/registries/BuiltInRegistries;m_258002_(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;)Lnet/minecraft/core/Registry;' in net.minecraft.core.registries.BuiltInRegistries. Using refmap terrablender.refmap.json [PREINJECT Applicator Phase -> terrablender.mixins.json:MixinBuiltInRegistries -> Prepare Injections ->  -> handler$zza000$registerSimple(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V -> Parse]
org.spongepowered.asm.mixin.injection.throwables.InvalidInjectionException: Critical injection failure: @Inject annotation on registerSimple could not find any targets matching 'Lnet/minecraft/core/registries/BuiltInRegistries;m_258002_(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;)Lnet/minecraft/core/Registry;' in net.minecraft.core.registries.BuiltInRegistries. Using refmap terrablender.refmap.json [PREINJECT Applicator Phase -> terrablender.mixins.json:MixinBuiltInRegistries -> Prepare Injections ->  -> handler$zza000$registerSimple(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V -> Parse]
	at org.spongepowered.asm.mixin.injection.struct.InjectionInfo.validateTargets(InjectionInfo.java:656) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.injection.struct.InjectionInfo.findTargets(InjectionInfo.java:587) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.injection.struct.InjectionInfo.readAnnotation(InjectionInfo.java:330) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.injection.struct.InjectionInfo.<init>(InjectionInfo.java:316) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.injection.struct.InjectionInfo.<init>(InjectionInfo.java:308) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.injection.struct.CallbackInjectionInfo.<init>(CallbackInjectionInfo.java:46) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method) ~[?:?] {}
	at jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:77) ~[?:?] {}
	at jdk.internal.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45) ~[?:?] {}
	at java.lang.reflect.Constructor.newInstanceWithCaller(Constructor.java:500) ~[?:?] {}
	at java.lang.reflect.Constructor.newInstance(Constructor.java:481) ~[?:?] {}
	at org.spongepowered.asm.mixin.injection.struct.InjectionInfo$InjectorEntry.create(InjectionInfo.java:149) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.injection.struct.InjectionInfo.parse(InjectionInfo.java:708) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.transformer.MixinTargetContext.prepareInjections(MixinTargetContext.java:1311) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.transformer.MixinApplicatorStandard.prepareInjections(MixinApplicatorStandard.java:1042) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.transformer.MixinApplicatorStandard.applyMixin(MixinApplicatorStandard.java:393) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.transformer.MixinApplicatorStandard.apply(MixinApplicatorStandard.java:325) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.transformer.TargetClassContext.apply(TargetClassContext.java:383) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.transformer.TargetClassContext.applyMixins(TargetClassContext.java:365) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.transformer.MixinProcessor.applyMixins(MixinProcessor.java:363) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.mixin.transformer.MixinTransformer.transformClass(MixinTransformer.java:250) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.service.modlauncher.MixinTransformationHandler.processClass(MixinTransformationHandler.java:131) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at org.spongepowered.asm.launch.MixinLaunchPluginLegacy.processClass(MixinLaunchPluginLegacy.java:131) ~[mixin-0.8.5.jar:0.8.5+Jenkins-b310.git-155314e6e91465dad727e621a569906a410cd6f4] {}
	at cpw.mods.modlauncher.serviceapi.ILaunchPluginService.processClassWithFlags(ILaunchPluginService.java:156) ~[modlauncher-10.0.9.jar:10.0.9+10.0.9+main.dcd20f30] {}
	at cpw.mods.modlauncher.LaunchPluginHandler.offerClassNodeToPlugins(LaunchPluginHandler.java:88) ~[modlauncher-10.0.9.jar:?] {}
	at cpw.mods.modlauncher.ClassTransformer.transform(ClassTransformer.java:120) ~[modlauncher-10.0.9.jar:?] {}
	at cpw.mods.modlauncher.TransformingClassLoader.maybeTransformClassBytes(TransformingClassLoader.java:50) ~[modlauncher-10.0.9.jar:?] {}
	at cpw.mods.cl.ModuleClassLoader.readerToClass(ModuleClassLoader.java:113) ~[securejarhandler-2.1.10.jar:?] {}
	at cpw.mods.cl.ModuleClassLoader.lambda$findClass$15(ModuleClassLoader.java:219) ~[securejarhandler-2.1.10.jar:?] {}
	at cpw.mods.cl.ModuleClassLoader.loadFromModule(ModuleClassLoader.java:229) ~[securejarhandler-2.1.10.jar:?] {}
	at cpw.mods.cl.ModuleClassLoader.findClass(ModuleClassLoader.java:219) ~[securejarhandler-2.1.10.jar:?] {}
	at cpw.mods.cl.ModuleClassLoader.loadClass(ModuleClassLoader.java:135) ~[securejarhandler-2.1.10.jar:?] {}
	at java.lang.ClassLoader.loadClass(ClassLoader.java:525) ~[?:?] {}
	at net.minecraft.server.Bootstrap.bootStrap(Bootstrap.java:43) ~[forge-1.20.1-47.3.0_mapped_official_1.20.1.jar:?] {re:classloading}
	at net.minecraftforge.data.loading.DatagenModLoader.begin(DatagenModLoader.java:42) ~[forge-1.20.1-47.3.0_mapped_official_1.20.1.jar:?] {re:classloading}
	at net.minecraft.data.Main.main(Main.java:90) ~[forge-1.20.1-47.3.0_mapped_official_1.20.1.jar:?] {re:classloading}
	at jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method) ~[?:?] {}
	at jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77) ~[?:?] {}
	at jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43) ~[?:?] {}
	at java.lang.reflect.Method.invoke(Method.java:569) ~[?:?] {}
	at net.minecraftforge.fml.loading.targets.CommonLaunchHandler.runTarget(CommonLaunchHandler.java:111) ~[fmlloader-1.20.1-47.3.0.jar:?] {}
	at net.minecraftforge.fml.loading.targets.CommonLaunchHandler.dataService(CommonLaunchHandler.java:107) ~[fmlloader-1.20.1-47.3.0.jar:?] {}
	at net.minecraftforge.fml.loading.targets.ForgeDataUserdevLaunchHandler.devService(ForgeDataUserdevLaunchHandler.java:22) ~[fmlloader-1.20.1-47.3.0.jar:?] {}
	at net.minecraftforge.fml.loading.targets.CommonDevLaunchHandler.lambda$makeService$7(CommonDevLaunchHandler.java:135) ~[fmlloader-1.20.1-47.3.0.jar:?] {}
	at cpw.mods.modlauncher.LaunchServiceHandlerDecorator.launch(LaunchServiceHandlerDecorator.java:30) ~[modlauncher-10.0.9.jar:?] {}
	at cpw.mods.modlauncher.LaunchServiceHandler.launch(LaunchServiceHandler.java:53) ~[modlauncher-10.0.9.jar:?] {}
	at cpw.mods.modlauncher.LaunchServiceHandler.launch(LaunchServiceHandler.java:71) ~[modlauncher-10.0.9.jar:?] {}
	at cpw.mods.modlauncher.Launcher.run(Launcher.java:108) ~[modlauncher-10.0.9.jar:?] {}
	at cpw.mods.modlauncher.Launcher.main(Launcher.java:78) ~[modlauncher-10.0.9.jar:?] {}
	at cpw.mods.modlauncher.BootstrapLaunchConsumer.accept(BootstrapLaunchConsumer.java:26) ~[modlauncher-10.0.9.jar:?] {}
	at cpw.mods.modlauncher.BootstrapLaunchConsumer.accept(BootstrapLaunchConsumer.java:23) ~[modlauncher-10.0.9.jar:?] {}
	at cpw.mods.bootstraplauncher.BootstrapLauncher.main(BootstrapLauncher.java:141) ~[bootstraplauncher-1.1.2.jar:?] {}
Exception in thread "main" java.lang.RuntimeException: java.lang.reflect.InvocationTargetException
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.LaunchServiceHandlerDecorator.launch(LaunchServiceHandlerDecorator.java:32)
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.LaunchServiceHandler.launch(LaunchServiceHandler.java:53)
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.LaunchServiceHandler.launch(LaunchServiceHandler.java:71)
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.Launcher.run(Launcher.java:108)
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.Launcher.main(Launcher.java:78)
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.BootstrapLaunchConsumer.accept(BootstrapLaunchConsumer.java:26)
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.BootstrapLaunchConsumer.accept(BootstrapLaunchConsumer.java:23)
	at cpw.mods.bootstraplauncher@1.1.2/cpw.mods.bootstraplauncher.BootstrapLauncher.main(BootstrapLauncher.java:141)
Caused by: java.lang.reflect.InvocationTargetException
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:569)
	at MC-BOOTSTRAP/fmlloader@1.20.1-47.3.0/net.minecraftforge.fml.loading.targets.CommonLaunchHandler.runTarget(CommonLaunchHandler.java:111)
	at MC-BOOTSTRAP/fmlloader@1.20.1-47.3.0/net.minecraftforge.fml.loading.targets.CommonLaunchHandler.dataService(CommonLaunchHandler.java:107)
	at MC-BOOTSTRAP/fmlloader@1.20.1-47.3.0/net.minecraftforge.fml.loading.targets.ForgeDataUserdevLaunchHandler.devService(ForgeDataUserdevLaunchHandler.java:22)
	at MC-BOOTSTRAP/fmlloader@1.20.1-47.3.0/net.minecraftforge.fml.loading.targets.CommonDevLaunchHandler.lambda$makeService$7(CommonDevLaunchHandler.java:135)
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.LaunchServiceHandlerDecorator.launch(LaunchServiceHandlerDecorator.java:30)
	... 7 more
Caused by: org.spongepowered.asm.mixin.transformer.throwables.MixinTransformerError: An unexpected critical error was encountered
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.MixinProcessor.applyMixins(MixinProcessor.java:392)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.MixinTransformer.transformClass(MixinTransformer.java:250)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.service.modlauncher.MixinTransformationHandler.processClass(MixinTransformationHandler.java:131)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.launch.MixinLaunchPluginLegacy.processClass(MixinLaunchPluginLegacy.java:131)
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.serviceapi.ILaunchPluginService.processClassWithFlags(ILaunchPluginService.java:156)
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.LaunchPluginHandler.offerClassNodeToPlugins(LaunchPluginHandler.java:88)
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.ClassTransformer.transform(ClassTransformer.java:120)
	at MC-BOOTSTRAP/cpw.mods.modlauncher@10.0.9/cpw.mods.modlauncher.TransformingClassLoader.maybeTransformClassBytes(TransformingClassLoader.java:50)
	at cpw.mods.securejarhandler/cpw.mods.cl.ModuleClassLoader.readerToClass(ModuleClassLoader.java:113)
	at cpw.mods.securejarhandler/cpw.mods.cl.ModuleClassLoader.lambda$findClass$15(ModuleClassLoader.java:219)
	at cpw.mods.securejarhandler/cpw.mods.cl.ModuleClassLoader.loadFromModule(ModuleClassLoader.java:229)
	at cpw.mods.securejarhandler/cpw.mods.cl.ModuleClassLoader.findClass(ModuleClassLoader.java:219)
	at cpw.mods.securejarhandler/cpw.mods.cl.ModuleClassLoader.loadClass(ModuleClassLoader.java:135)
	at java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:525)
	at TRANSFORMER/minecraft@1.20.1/net.minecraft.server.Bootstrap.bootStrap(Bootstrap.java:43)
	at TRANSFORMER/forge@47.3.0/net.minecraftforge.data.loading.DatagenModLoader.begin(DatagenModLoader.java:42)
	at TRANSFORMER/minecraft@1.20.1/net.minecraft.data.Main.main(Main.java:90)
	... 16 more
Caused by: org.spongepowered.asm.mixin.throwables.MixinApplyError: Mixin [terrablender.mixins.json:MixinBuiltInRegistries] from phase [DEFAULT] in config [terrablender.mixins.json] FAILED during APPLY
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.MixinProcessor.handleMixinError(MixinProcessor.java:636)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.MixinProcessor.handleMixinApplyError(MixinProcessor.java:588)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.transformer.MixinProcessor.applyMixins(MixinProcessor.java:379)
	... 32 more
Caused by: org.spongepowered.asm.mixin.injection.throwables.InvalidInjectionException: Critical injection failure: @Inject annotation on registerSimple could not find any targets matching 'Lnet/minecraft/core/registries/BuiltInRegistries;m_258002_(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;)Lnet/minecraft/core/Registry;' in net.minecraft.core.registries.BuiltInRegistries. Using refmap terrablender.refmap.json [PREINJECT Applicator Phase -> terrablender.mixins.json:MixinBuiltInRegistries -> Prepare Injections ->  -> handler$zza000$registerSimple(Lnet/minecraft/resources/ResourceKey;Lnet/minecraft/core/registries/BuiltInRegistries$RegistryBootstrap;Lorg/spongepowered/asm/mixin/injection/callback/CallbackInfoReturnable;)V -> Parse]
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.injection.struct.InjectionInfo.validateTargets(InjectionInfo.java:656)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.injection.struct.InjectionInfo.findTargets(InjectionInfo.java:587)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.injection.struct.InjectionInfo.readAnnotation(InjectionInfo.java:330)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.injection.struct.InjectionInfo.<init>(InjectionInfo.java:316)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.injection.struct.InjectionInfo.<init>(InjectionInfo.java:308)
	at MC-BOOTSTRAP/org.spongepowered.mixin/org.spongepowered.asm.mixin.injection.struct.CallbackInjectionInfo.<init>(CallbackInjectionInfo.java:46)
	at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:77)
	at java.base/jdk.internal.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at java.base/java.lang.reflect.Constructor.newInstanceWithCaller(Constructor.java:500)
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
	... 32 more

> Task :runData FAILED

FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':runData'.
> Process 'command '/usr/lib/jvm/temurin-17-jdk-amd64/bin/java'' finished with non-zero exit value 1

* Try:
> Run with --stacktrace option to get the stack trace.
> Run with --info or --debug option to get more log output.
> Run with --scan to get full insights.

* Get more help at https://help.gradle.org

Deprecated Gradle features were used in this build, making it incompatible with Gradle 9.0.

You can use '--warning-mode all' to show the individual deprecation warnings and determine if they come from your own scripts or plugins.

See https://docs.gradle.org/8.1.1/userguide/command_line_interface.html#sec:command_line_warnings

BUILD FAILED in 1m 47s
10 actionable tasks: 10 executed
```

## build log (errors + tail)
```
----- build log tail -----
To honour the JVM settings for this build a single-use Daemon process will be forked. See https://docs.gradle.org/8.1.1/userguide/gradle_daemon.html#sec:disabling_the_daemon.
Daemon will be stopped at the end of the build 

> Configure project :
Directory '/home/runner/.gradle/daemon/8.1.1/${env.JAVA_HOME_11_X64}' (Maven Toolchains) used for java installations does not exist
Directory '/home/runner/.gradle/daemon/8.1.1/${env.JAVA_HOME_21_X64}' (Maven Toolchains) used for java installations does not exist
Directory '/home/runner/.gradle/daemon/8.1.1/${env.JAVA_HOME_8_X64}' (Maven Toolchains) used for java installations does not exist
Directory '/home/runner/.gradle/daemon/8.1.1/${env.JAVA_HOME_17_X64}' (Maven Toolchains) used for java installations does not exist
Directory '/home/runner/.gradle/daemon/8.1.1/${env.JAVA_HOME_25_X64}' (Maven Toolchains) used for java installations does not exist

> Task :compileJava UP-TO-DATE
> Task :processResources UP-TO-DATE
> Task :classes UP-TO-DATE
> Task :jar
> Task :downloadMcpConfig
> Task :extractSrg UP-TO-DATE
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

BUILD SUCCESSFUL in 11s
7 actionable tasks: 4 executed, 3 up-to-date
```

## generated resources
```
count: 0
```

## built jars
```
total 968
drwxr-xr-x  2 runner runner   4096 Oct 24 04:46 .
drwxr-xr-x 21 runner runner   4096 Oct 24 04:46 ..
-rw-r--r--  1 runner runner 980044 Oct 24 04:46 biomesunseen-1.0.0.jar
```
