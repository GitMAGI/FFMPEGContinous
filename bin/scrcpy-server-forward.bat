adb -s 07ea9707 push "scrcpy-server.jar" "/data/local/tmp/scrcpy-server.jar"
adb -s 07ea9707 forward tcp:27183 localabstract:scrcpy
::adb -s 07ea9707 shell CLASSPATH=/data/local/tmp/scrcpy-server.jar app_process / com.genymobile.scrcpy.Server 0 8000000 true - false
adb -s 07ea9707 shell CLASSPATH=/data/local/tmp/scrcpy-server.jar app_process / com.genymobile.scrcpy.Server 0 8000000 true - false
adb -s 07ea9707 forward --remove tcp:27183