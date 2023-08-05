Install WinCUPL with default options.

The 5vcomp.bat batch file can be used to automate compiling of .PLD files with CUPL.EXE.
This eliminates the need to use WinCUPL directly. Use your favorite IDE or text editor.

Place 5vcomp.bat inside of C:\Wincupl\WinCupl\Fitters and it should end up in your path.

Adding context-menu-pld-5vcomp.reg to the registry will add the "compile" right-click
option to any .PLD files, which will simply call C:\Wincupl\WinCupl\Fitters\5vcomp.bat

This batch file will perform some basic checks (fitter version, etc.) and will perform
simulation only if the corresponding .SI file has been found.

This workflow has been tested to run properly on:
 - Windows XP 32-bit
 - Windows 7 64-bit

Todo:
* Impose character length limit on filenames (CSIM.EXE issues)
* Probably check to make sure find150x.exe files have been replaced with their corresponding fit150x.exe files
