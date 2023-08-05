5vcomp is a Linux Shell Script that is a light wrapper around the CUPL.EXE

The CUPL.EXE compiler runs well under Linux using Wine and enables one to use a command-line/scripted approach to compilation.

This allows you to avoid the WinCUPL IDE and use your favorite IDE/Text editor instead to develop .PLD files.

WinCUPL is nonetheless a requirement as it provides:
* The CUPL.EXE compiler
* The Atmel.dl device library (which CUPL.EXE uses)
* The fitters for the ATF150x CPLD parts (though this utility will refuse to work with the ones provided by Atmel WinCUPL -- please use the newer ones from the Atmel Prochip package)

This script isn't anything too sophisticated. It merely checks for a bunch of common but esoteric gotchas and provides a working example on how to go from a .PLD to a .JED

Basic customizations (compiler flags, device library) are broken out into variables at the top of the script.

To get Wine working on Ubuntu Linux, this would look something like:

<code>sudo apt-get install wine winetricks playonlinux
winetricks mfc40 mfc42
</code>

From there, you can install WinCUPL:
* <a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">Download WinCUPL from here</a>.
* <a href="https://ww1.microchip.com/downloads/en/DeviceDoc/ProChip5.0.1.zip">Download Atmel Prochip from here</a>
