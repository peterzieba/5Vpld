Install WinCUPL with default options.
* <a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">Download WinCUPL from here</a>.

The 5vcomp.bat batch file can be used to automate compiling of .PLD files with CUPL.EXE.
This eliminates the need to use WinCUPL directly. Use your favorite IDE or text editor.

Place 5vcomp.bat inside of C:\Wincupl\WinCupl\Fitters and it should end up in your path so you can run it from anywhere.

WinCUPL is nonetheless a requirement as it provides:
* The CUPL.EXE compiler
* The Atmel.dl device library (which CUPL.EXE uses)
* The fitters for the ATF150x CPLD parts (though this utility will refuse to work with the ones provided by Atmel WinCUPL -- please replace them with the newer ones from the Atmel Prochip package)

Adding context-menu-pld-5vcomp.reg to the registry will add the "compile" right-click
option to any .PLD files, which will simply call C:\Wincupl\WinCupl\Fitters\5vcomp.bat [your-cupl-project.PLD]

This script isn't anything too sophisticated. It merely checks for a bunch of common but esoteric gotchas and provides a working example on how to go from a .PLD to a .JED

Basic customizations (compiler flags, device library) are broken out into variables at the top of the script.

This batch file will also refuse to run until you replace the installed fitters with those from Atmel Prochip
* <a href="https://ww1.microchip.com/downloads/en/DeviceDoc/ProChip5.0.1.zip">Download Atmel Prochip from here</a>

This workflow has been tested to run properly on:
 - Windows XP 32-bit
 - Windows 7 64-bit

Todo:
* Impose character length limit on filenames (CSIM.EXE issues)
* Probably check to make sure find150x.exe files have been replaced with their corresponding fit150x.exe files
