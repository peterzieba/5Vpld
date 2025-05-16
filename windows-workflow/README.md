# Overview
The `5vcomp.bat` batch file can be used to automate compiling of `.PLD` files with `CUPL.EXE`.
This eliminates the need to use WinCUPL directly. Use your favorite IDE or text editor.

WinCUPL is nonetheless a requirement as it provides:
* The CUPL.EXE compiler
* The Atmel.dl device library (which CUPL.EXE uses)
* The fitters for the ATF150x CPLD parts (though this utility will refuse to work with the ones provided by Atmel WinCUPL -- please replace them with the newer ones from the Atmel Prochip package)

This script isn't anything too sophisticated. It merely checks for a bunch of common but esoteric gotchas and provides a working example on how to go from a .PLD to a .JED

Basic customizations (compiler flags, device library) are broken out into variables at the top of the script.

The Linux equivalent version of 5vcomp is probably a bit ahead of this and more elaborate, but it is trying to do the same thing in essence.

# Installation

* Install WinCUPL with default options and default installation path.
  * <a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">Download WinCUPL from here</a>.
  * Serial Number is `60008009`

* Install Atmel Prochip to the default install path: `C:\ATMEL_PLS_Tools`
  * <a href="https://ww1.microchip.com/downloads/en/DeviceDoc/ProChip5.0.1.zip">Download Atmel Prochip from here</a>
  * You only need to select the "ProChip Designer 5.0" option if you do not want the additional software.

* Set up 5vpld:
  * Download this whole [repository as a .zip](https://github.com/peterzieba/5Vpld/archive/refs/heads/main.zip), Extract
  * From the windows-workflow folder, run `5vinstall.bat`
    * Hopefully everything just works.
  * Double-click on `context-menu-pld-5vcomp.reg` to import it to the registry.

* WinCUPLs built-in help does not work on newer versions of Windows (Vista, 7, 8, 8.1).
  * The built-in help has lots of very useful information, however, Windows removed support for .HLP files starting with Vista.
  * Install the WinHelp viewer (KB917607) for your specific version of Windows
  * https://archive.org/download/kb917607
  * https://www.helpscribble.com/KB917607.html
  * WinHelp viewer either does not seem to be available or is limited in functionality on Windows 10/11.
    * Maybe it is worth trying to install Windows6.1-KB917607-x64.msu ?

## Manual Installation (this is done automatically by 5vinstall.bat)
After WinCUPL and Atmel Prochip is installed, the following needs to be done.
Place `5vcomp.bat` inside of `C:\Wincupl\WinCupl\Fitters` and it should end up in your path so you can run it from anywhere.

Adding `context-menu-pld-5vcomp.reg` to the registry will add the "compile" right-click
option to any `.PLD` files, which will simply call `C:\Wincupl\WinCupl\Fitters\5vcomp.bat` [your-cupl-project.PLD]

`5vcomp.bat` will refuse to run until you replace the installed fitters with those from Atmel Prochip
* You can use `5vinstall.bat` to replace these for you, or you can do the following manually:
* Overwrite all three of the FIT150x.EXE fitters in C:\Wincupl\WinCupl\Fitters\ with those that have been installed from Atmel Prochip.
  * The prochip files are inside of C:\ATMEL_PLS_Tools\Prochip\pldfit\
  * Also delete all three of the FIND150x.EXE files in C:\Wincupl\WinCupl\Fitters\ and copy each of the corresponding FIT150x.EXE in their place.
    * FIT1502.EXE is Copied to FIND1502.EXE
    * FIT1504.EXE is Copied to FIND1504.EXE
    * FIT1508.EXE is Copied to FIND1508.EXE
* It's simply not worth using the old fitters -- too many variables of things that can go wrong.

# Usage
From command line, run:<br>
`5vcomp your-project.PLD`

Alternately, if you have imported `context-menu-pld-5vcomp.reg`, you can simply right-click on your .PLD file and select "Compile PLD"

![demonstration](rt-click-compile-pld.gif)

This should generate a bunch of files and most crucially, a .JED file if everything works properly.<br>
If a .SI file is detected, it will pass additional flags to the compiler to run simulation as well, producing a .SO file and many others.

See the [examples folder](../examples) for some very simple (buffer, inverter) .PLD files to make sure everything is working properly.

See also `C:\Wincupl\Examples\Atmel` for a bunch of more elaborate vendor included examples, demonstrating the language as well as what is possible to build using these devices.

Sensible compiler defaults are used, but can be changed inside of 5vcomp.bat.

# Notes

This workflow has been tested to run properly on:
 - Windows XP 32-bit
 - Windows 7 64-bit
 - Windows 10 64-bit 22H2

Todo:
* Impose character length limit on filenames (CSIM.EXE issues)
* Maybe automatically import `context-menu-pld-5vcomp.reg`
* Probably check to make sure find150x.exe files have been replaced with their corresponding fit150x.exe files. **If you don't do this, the fitter will not be automatically run and you won't get a .JED file for the CPLD parts.**

Bugs:
* Probably. Please report as limited testing has been performed.
