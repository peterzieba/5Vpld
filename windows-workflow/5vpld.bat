echo off
rem This batch file compiles a .PLD file using CUPL.EXE, all in an effort to avoid using WinCUPL directly.
rem It does some basic checks to make sure that the fitters exist and that they are the latest known version.

if "%~1" == "" GOTO noargs

if not exist C:\Wincupl\WinCupl\Fitters\fit1502.exe goto :missingfitter
if not exist C:\Wincupl\WinCupl\Fitters\fit1504.exe goto :missingfitter
if not exist C:\Wincupl\WinCupl\Fitters\fit1508.exe goto :missingfitter

rem Check for the latest version of the fitters.
rem Because we can't assume a file hashing program exists on Windows
rem (we're aiming for Windows 2000 and up compatability)
rem we rely on filesize instead.

set size=0
call :filesize C:\Wincupl\WinCupl\Fitters\fit1502.exe
if %size% NEQ 520192 goto :oldversion

set size=0
call :filesize C:\Wincupl\WinCupl\Fitters\fit1504.exe
if %size% NEQ 548864 goto :oldversion

set size=0
call :filesize C:\Wincupl\WinCupl\Fitters\fit1508.exe
if %size% NEQ 565248 goto :oldversion

rem Basic checks seem OK. Go to compilation step.
goto :compile

rem Set filesize of first argument in %size% variable, and return
:filesize
  set size=%~z1
  exit /b 0

:oldversion
cls
echo You appear to be running an old version of the atmel fitters.
echo.
echo The fitters for the ATF1502, ATF1504, and ATF1508 chips
echo Should report Version 1918 (3-21-07)
echo These are the expected file sizes:
echo FIT1502.EXE 520,192
echo FIT1504.EXE 548,864
echo FIT1508.EXE 565,248
echo One or more of the fitters failed the file size comparison.
echo The newer fitters can be obtained from the Atmel Prochip package:
echo https://ww1.microchip.com/downloads/en/DeviceDoc/ProChip5.0.1.zip
echo.
echo Place the files in C:\Wincupl\WinCupl\Fitters\
pause
exit /B 1

:missingfitter
cls
echo You appear to be missing one or more of the ATMEL fitters.
echo These should be present c:\Wincupl\WinCupl\Fitters directory.
pause
exit /B 2

:noargs
cls
echo This batch file compiles a CUPL .PLD file
echo It requires a single argument:
echo the name of the .PLD file you'd like compiled
echo.
echo It will place all resulting files in the same directory.
pause
exit /B 3

:compile
rem See CUPL documentation for full command line options. The following are used here:
rem -m1 quick minimization (default)
rem -j JEDEC download format
rem -n use input filename for output file
rem -s perform logic simulation after compilation
rem -w perform simulation with waveform output (MS-DOS only)
rem It seems the -a option to create an absolute file is implied when -s or -w are specified.

rem cupl.exe -m1lxfjnabeps z:\tim_cnt\tim_cnt.pld
cupl.exe -m1jnsw %1

