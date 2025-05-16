# Overview
5vcomp is a Linux Shell Script that is a light wrapper around the CUPL.EXE compiler.

The CUPL.EXE compiler runs well under Linux using Wine and enables one to use a command-line/scripted approach to compilation.

This allows you to avoid the WinCUPL IDE and use your favorite IDE/Text editor instead to develop .PLD files.

If you are not already familiar with Wine, you might want to consider using the [windows workflow](../windows-workflow/) as it might be easier to get started.

Installing WinCUPL is required to get the compiler, but you'll never have to open WinCUPL itself. Installing it provides:
* The CUPL.EXE compiler
* The Atmel.dl device library (which CUPL.EXE uses)
* The fitters for the ATF150x CPLD parts (though this script/workflow will refuse to work with the ones provided by Atmel WinCUPL -- please replace them with the newer ones from the Atmel Prochip package)

This script isn't anything too sophisticated. It merely checks for a bunch of common but esoteric gotchas and provides a working example on how to go from a .PLD to a .JED

Basic customizations (compiler flags, device library) are broken out into variables at the top of the script.

# Installation

To get Wine working on Ubuntu Linux, this could look something like:

```
dpkg --add-architecture i386
sudo apt-get install wine wine32:i386 winetricks playonlinux innoextract
WINEARCH=win32 WINEPREFIX=~/.wine wine wineboot
winetricks mfc40 mfc42
```
* Alternately, you may want to consider installing Wine from <a href="https://wiki.winehq.org/Download">WineHQ</a> (more frequently updated than distro packages. Better file association defaults (.HLP files, etc.))


From there, you can install WinCUPL and Atmel Prochip:
* <a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">Download WinCUPL from here</a>.
  * `unzip awincupl.exe.zip`
  * `wine awincupl.exe`
  * Serial Number freely provided by Microchip is `60008009`
* <a href="https://ww1.microchip.com/downloads/en/DeviceDoc/ProChip5.0.1.zip">Download Atmel Prochip from here</a>
  * You only need to select the "ProChip Designer 5.0" option if you do not want the all parts of Prochip.
  * Alternately, you can extract the fitters from the installer using innoextract:
    * <code>innoextract -I app/Prochip/pldfit/aprim.lib -I app/Prochip/pldfit/atmel.std -I app/Prochip/pldfit/fit1502.exe -I app/Prochip/pldfit/fit1504.exe -I app/Prochip/pldfit/fit1508.exe ProChip5_setup.exe</code>

* Copy the new fitters as well as `aprim.lib` and `atmel.std` over to C:\Wincupl\WinCupl\Fitters:
  * Overwrite the ATF150x.EXE fitters in `C:\Wincupl\WinCupl\Fitters\` <br>with those from Atmel Prochip `C:\ATMEL_PLS_Tools\Prochip\pldfit\`
  * Also delete all three of the FIND150x.EXE files in C:\Wincupl\WinCupl\Fitters\ and copy each of the corresponding FIT150x.EXE in their place.
```
cp fit1502.exe find1502.exe
cp fit1504.exe find1504.exe
cp fit1508.exe find1508.exe
```
* Once you have everything installed, you can download and place 5vcomp somewhere like `/usr/local/bin/` or `~/.local/bin/` where it will be conveniently in your path.


# Usage
From the command line run:<br>
`5vcomp your-project.PLD`

Alternately, you can use <code>5vpld.xml</code> and <code>5vcomp.desktop</code> as templates, modifying them to suit your paths so that you can simply right-click on your .PLD file to have it open with 5vcomp.

This should generate a bunch of files and most crucially, a .JED file if everything works properly.<br>
If a .SI file is detected, it will pass additional flags to the compiler to run simulation as well, producing a .SO file and many others.

See the [examples folder](../examples) for some very simple (buffer, inverter) .PLD files to make sure everything is working properly.

See also `C:\Wincupl\Examples\Atmel` for a bunch of more elaborate vendor included examples, demonstrating the language as well as what is possible to build using these devices.

# Misc
These files make it easier to handle file associations and their usual actions when using a GUI filemanager:
* <code>5vpld.xml</code> (work in progress) provides Mime Types for the most common files (.JED, .PLD, etc.).
  * Can be placed inside of `~/.local/share/mime/packages`
* <code>5vcomp.desktop</code> provides a .desktop shortcut to make launching 5vcomp easier.
