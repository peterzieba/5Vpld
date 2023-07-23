The 5vpld.bat batch file can be used to automate compiling of .PLD files with CUPL.EXE.
This eliminates the need to use WinCUPL directly. Use your favorite IDE or text editor.

Place 5vpld.bat somewhere in the system's path.

WinCUPL has been tested to run inside of Windows 7 64-bit.

Todo:
* Maybe add right-click context menu for .PLD files to be compiled with this batch file.
* Test on different versions of Windows
* Add checks for .SI file presence. Only add simulation options for CUPL.EXE if found.