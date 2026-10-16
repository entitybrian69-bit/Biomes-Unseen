@rem Gradle startup script for Windows
@if "%DEBUG%"=="" @echo off
setlocal

set DIRNAME=%~dp0
if "%DIRNAME%"=="" set DIRNAME=.
set APP_HOME=%DIRNAME%

set CLASSPATH=%APP_HOME%gradle\wrapper\gradle-wrapper.jar

if not exist "%CLASSPATH%" (
    where gradle >nul 2>nul
    if %ERRORLEVEL%==0 (
        echo gradle-wrapper.jar missing - bootstrapping with system Gradle.
        pushd "%APP_HOME%"
        call gradle wrapper --gradle-version 9.8.1
        popd
    ) else (
        echo ERROR: gradle\wrapper\gradle-wrapper.jar is missing and no system Gradle was found. 1>&2
        echo Install Gradle 9.8.1+ and run:  gradle wrapper --gradle-version 9.8.1 1>&2
        exit /b 1
    )
)

set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"

if defined JAVA_HOME (
    set JAVA_EXE=%JAVA_HOME%\bin\java.exe
) else (
    set JAVA_EXE=java.exe
)

"%JAVA_EXE%" %DEFAULT_JVM_OPTS% -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
endlocal
