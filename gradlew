#!/bin/sh

#
# Gradle start up script for POSIX.  Bootstraps the Gradle wrapper when the
# wrapper jar is present, otherwise falls back to a system Gradle install so
# the project can be bootstrapped with `gradle wrapper --gradle-version 8.14.3`.
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
        ( cd "$APP_HOME" && exec gradle wrapper --gradle-version 8.14.3 ) || exit 1
    else
        echo "ERROR: gradle/wrapper/gradle-wrapper.jar is missing and no system Gradle was found." >&2
        echo "Install Gradle 8.14.3+ (https://gradle.org) and run:  gradle wrapper --gradle-version 8.14.3" >&2
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
