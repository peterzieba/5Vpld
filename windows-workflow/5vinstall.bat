echo off
cls

echo This batch file replaces the WinCUPL installed fitters with those from Atmel Prochip.

rem This batch file is aims to be compatible across as many Windows Versions as possible, but is not thoroughly tested.
rem Care has been taken not to utilize functionality that might be missing in older versions.

echo.
if not exist C:\Wincupl\WinCupl\Fitters\fit1502.exe goto :missingwincupl
if not exist C:\ATMEL_PLS_Tools\Prochip\pldfit\fit1502.exe goto :missingprochip

pause

rem Skip backup up old fitters if a backup has already has been made before.
if exist C:\Wincupl\WinCupl\Fitters\atmel.std.old goto :copyfitters

echo Backing up old fitters in WinCUPL to *.old
ren C:\Wincupl\WinCupl\Fitters\atmel.std atmel.std.old
ren C:\Wincupl\WinCupl\Fitters\find1502.exe find1502.exe.old
ren C:\Wincupl\WinCupl\Fitters\find1504.exe find1504.exe.old
ren C:\Wincupl\WinCupl\Fitters\find1508.exe find1508.exe.old
ren C:\Wincupl\WinCupl\Fitters\fit1502.exe fit1502.exe.old
ren C:\Wincupl\WinCupl\Fitters\fit1504.exe fit1504.exe.old
ren C:\Wincupl\WinCupl\Fitters\fit1508.exe fit1508.exe.old


:copyfitters
echo Copying fitters from Atmel Prochip to C:\Wincupl\WinCupl\Fitters
copy C:\ATMEL_PLS_Tools\Prochip\pldfit\atmel.std C:\Wincupl\WinCupl\Fitters\
copy C:\ATMEL_PLS_Tools\Prochip\pldfit\fit1502.exe C:\Wincupl\WinCupl\Fitters\
copy C:\ATMEL_PLS_Tools\Prochip\pldfit\fit1504.exe C:\Wincupl\WinCupl\Fitters\
copy C:\ATMEL_PLS_Tools\Prochip\pldfit\fit1508.exe C:\Wincupl\WinCupl\Fitters\
copy C:\ATMEL_PLS_Tools\Prochip\pldfit\fit1502.exe C:\Wincupl\WinCupl\Fitters\find1502.exe
copy C:\ATMEL_PLS_Tools\Prochip\pldfit\fit1504.exe C:\Wincupl\WinCupl\Fitters\find1504.exe
copy C:\ATMEL_PLS_Tools\Prochip\pldfit\fit1508.exe C:\Wincupl\WinCupl\Fitters\find1508.exe
if not exist 5vcomp.bat goto :skipcomp
echo Installing 5vcomp.bat to C:\Wincupl\WinCupl\Fitters\
copy 5vcomp.bat C:\Wincupl\WinCupl\Fitters\
goto :done

:skipcomp
echo 5vcomp.bat not found. Copy 5vcomp.bat manually into C:\Wincupl\WinCupl\Fitters\
goto :done

:missingprochip
rem Expected install directory is C:\ATMEL_PLS_Tools
echo ERROR: Atmel Prochip is not installed or is not in the default installation directory.
echo You can download Atmel Prochip from:
echo https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources
echo https://ww1.microchip.com/downloads/en/DeviceDoc/ProChip5.0.1.zip
pause
exit /B 3

:missingwincupl
echo ERROR: WinCUPL is not installed or is not in the default installation directory.
echo You can download WinCUPL from:
echo https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources
echo https://ww1.microchip.com/downloads/en/DeviceDoc/awincupl.exe.zip
echo Serial Number: 60008009
pause
exit /B 2

:done
echo Done.
echo If everything went well, the old Atmel fitters have been renamed to .old and replaced with those from Atmel Prochip.
echo You should now be able to use 5vcomp to compile .PLD files.
echo.
echo Additionally, if you import context-menu-pld-5vcomp.reg, this will allow you to right-click and compile a .PLD file without opening a command prompt first.
rem reg import context-menu-pld-5vcomp.reg
rem FIXME: import registry stuff across windows versions
rem We don't do this automatically because it requires privilege elevation and it's probably different across Windows versions.
pause
