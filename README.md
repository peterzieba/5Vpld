# Overview
This repository centers around modern workflows for Atmel (Now Microchip) 5V GAL PLD and CPLD parts.

These parts are still active and highly worth considering wherever prototyping and 5V logic are a requirement. They can easily replace large numbers of TTL/CMOS logic gates and can be reprogrammed many times.

This repository aims to make it easier to work with the following parts:
* ATF1502, ATF1504, ATF1508 (programmable via JTAG)
* ATF16V8, ATF22V10 (Require an EPROM Programmer)

# Terminology
CPLD - <a href="https://en.wikipedia.org/wiki/Programmable_logic_device">Complex Programmable Logic Device</a><br />
GAL - <a href="https://en.wikipedia.org/wiki/Programmable_logic_device">Generic Array Logic</a><br />
WinCUPL - A Windows front-end to the CUPL compiler and related programs<br />
CUPL - Compiler for Universal Programmable Logic (A old programming language for logic. Modern examples would be Verilog/VHDL)<br />
FITTER - A fitter converts a netlist into the fusemap (.JED) file. Fitters are needed for the CPLD devices. If my understanding is correct, this is basically place & route.<br />
.JED/JEDEC File - A fuse map intended to be "burned/programmed" into a logic device.<br />
.SVF File - Serial Vector Format. This file can be used by any JTAG programmer (vendor-independent) to program a device that has a JTAG interface.<br />
Wine - Wine is not an emulator. Allows running Windows programs under Linux.<br />


# Writing logic for these parts: Possible Workflows
Each of these subsections represents a potential workflow.
## CUPL / WinCUPL
While logic for these parts can be written via WinCUPL, the experience may be fraught with difficulty as it is somewhat unstable and requires Windows. While it does run under Linux via Wine, it is nonetheless not worth the trouble to use it for serious work considering the number of other options for setting up a workflow. It is worth installing simply to use its help files / documentation / examples, however. To get it working within Wine, you'll need winetricks so you can install mfc40 and mfc42. On Ubuntu, this would look something like:
<code>
sudo apt-get install wine winetricks playonlinux
winetricks mfc40 mfc42
</code>

## Atmel Prochip
Atmel Prochip is not free, however, you may be able to get a trial license from Microchip. It is nonetheless worth installing regardless because there are newer fitters for the ATF150x devices that can be extracted from this package. These can be used with other workflows and so having these is pretty useful. The newer versions of the fitters should be from 
<details open>
<summary>MD5 sums for the newer version of fitters</summary>

</details>

## CUPL via VS Code (or just a text editor)

The good news is that WinCUPL is really just a front-end / IDE for the command-line compiler CUPL.EXE, which can process a .PLD file and turn it into a .JED file ready for programming (in the case of PLD devices), or produce a netlist which can then be passed to the appropriate fitter for the particular CPLD. As of this writing, there are two extensions that have been created for VS Code which support CUPL:
* https://marketplace.visualstudio.com/items?itemName=tlgkccampbell.code-cupl
  * This handles just syntax highlighting
* https://marketplace.visualstudio.com/items?itemName=VaynerSystems.VS-Cupl
  * This is an entire workflow

The secret to getting CUPL.EXE to turn a .PLD into a .JED is the following:
<code>
wine c:/Wincupl/Shared/cupl.exe -m1lxfjnabep -u c:/Wincupl/Shared/cupl.dl your-code.PLD
</code>
Additionally, if you are targeting a CPLD (ATF150x) for which CUPL.EXE does not have direct support, you will need to run:
<code>
wine c:/Wincupl/WinCupl/Fitters/fit1502.exe -i your-code.tt2 -dev P1502T44 -DEBUG on -Verilog_sim VERILOG -Out_Edif ON
</code>
The above example is for an ATF1502 in a TQFP-44 package. You will need to use the appropriate fitter and device type for your particular CPLD.

## Quartus via POF2JED
* It turns out that the Altera (Now Intel) <a href="https://www.intel.com/content/www/us/en/software-kit/711791/intel-quartus-ii-web-edition-design-software-version-13-0sp1-for-windows.html?">Quartus 13.0sp1</a> can be used to produce a .POF file targeting various EPM series CPLDs from Altera.
* The resulting .POF file can be converted using a utility called <a href="http://ww1.microchip.com/downloads/archive/pof2jed.zip">POF2JED</a> from Atmel (Now Microchip). This is further detailed in <a href="http://ww1.microchip.com/downloads/en/AppNotes/DOC0916.PDF">this application note.
* Important!: Newer versions will not work. v13.0sp1 last version that had support for the MAX EPM3K/EPM7K chips. Support for these chips has been removed from newer versions. You MUST use the old version.

## Digital
"Digital is an easy-to-use digital logic designer and circuit simulator designed for educational purposes." This is an interesting option as one can create a schematic and have a .JED file generated for a GAL16V8 or GAL22V10. If one provides the fitters to Digital, it can produce .JED files for the ATF150x series as well.
https://github.com/hneemann/Digital

## Yosys
One can use Yosys Open SYnthesis Suite (Yosys) with the help of the Atmel Fitters a specific CPLD and a techmap to produce .JED files. This allows an almost entirely open-source workflow using Verilog. A good place to start would be using the <a href="https://github.com/YosysHQ/oss-cad-suite-build">OSS CAD Suite</a> to get the

# Programming / Burning
There are a few choices on how the part can actually be programmed depending on whether it support JTAG.

## PLD Devices (ATF16V8, ATF22V10)
These parts require an EPROM programmer. <span style="color: red;">Additionally, an important gotcha' is that there are many variants and manufacturers of these parts. While the fusemap may be compatible across variants (GAL16V8 from Lattice vs. the ATF16V8 from Atmel/Microchip), THE PROGRAMMING ALGORITHMS ARE NOT! You will need an EPROM programmer with support for the EXACT manufacturer and part number of the device you have.</span>

## CPLD Devices (ATF1502, ATF1504, ATF1508)
These parts can be programmed via JTAG, so there are a few options.
* Official programmer: https://www.kanda.com/CPLD-Programmers.175.html
  * Software: https://www.microchip.com/en-us/development-tool/ATMISP
* OpenOCD: https://openocd.org/
  * You will need an SVF file to program a device via OpenOCD. This can be created by converting the .JED file using either ATMISP, or fuseconv.py from whitequark/prjbureau

* To generate a .JED file for these devices, you will need the fitters. While WinCUPL has fitters within it, a much more updated version of the fitters is available inside of Atmel Prochip from <a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">Microchip's website</a>

## Other CPLD Parts (ATF750, ATF1500)
* These parts do not support JTAG and are a bit more expensive, so they haven't been tried.
* In theory the ATF1500 fitter should work fine under Wine and so if fed with a netlist it should work. This means either CUPL.EXE or in theory Yosys with the right techmap could work.
* I believe CUPL should be able to generate a .JED directly for the ATF750 without a fitter.