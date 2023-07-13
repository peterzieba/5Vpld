# Overview
This repository centers around modern workflows for Atmel (Now Microchip) 5V GAL PLD and CPLD parts.

These parts are still active and highly worth considering wherever prototyping and 5V logic are a requirement. They can easily replace large numbers of TTL/CMOS logic gates and can be reprogrammed many times. Finally, the DIP parts are easy to solder, and the PQFP parts can be placed into a through-hole socket.

Ignored or briefly mentioned are parts which are NRND or inactive.

This repository aims to make it easier to work with the following parts:
* GAL Devices: ATF16V8, ATF22V10 (Require an EPROM Programmer)
  * Part number convention seems to be: "number of inputs" V "number of outputs/macrocells".
* CPLD Devices (JTAG Programmable): ATF1502AS (32 macrocell), ATF1504AS (64 macrocell), ATF1508AS (128 macrocells)
  * The devices ending in AS are commonly available.
  * The BE devices not covered here as they seem to be difficult to obtain and somewhat different.
  * Available in TQFP, PLCC, PQFP variants. PLCCs can be placed in through-hole sockets.
<details>
<summary>Expand here for details on how all of these compare to FPGAs</summary>
Such parts are the spiritual predecessors of more modern FPGAs. Key differences between FPGAs and PLDs:

* FPGAs are typically constructed from a large number of LUTs (Lookup tables). CPLDs use a sum-of-products structure.
* FPGAs typically expect to have their bitstream uploaded on powerup, requiring an external EEPROM. PLDs are typically non-volatile.
* FPGAs usually support standard JTAG for programming, whereas many PLDs required specialized device programmers.
* There are likely exceptions to all of the above in some parts. There are not hard rules.
</details>

# Terminology / Background
PLD - <a href="https://en.wikipedia.org/wiki/Programmable_logic_device">Programmable Logic Device</a><br />
GAL - <a href="https://en.wikipedia.org/wiki/Programmable_logic_device#GALs">Generic Array Logic</a><br />
CPLD - <a href="https://en.wikipedia.org/wiki/Programmable_logic_device#CPLDs">Complex Programmable Logic Device</a><br />
<a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">WinCUPL</a> - A Windows front-end/IDE to the CUPL compiler and related programs<br />
<a href="https://en.wikipedia.org/wiki/Macrocell_array">Macrocell</a> - A block of logic gates that is used multiple times within a PLD. Typically, there is one macrocell for each output, however, more complex devices can have more macrocells than outputs, allowing "buried" or "internal" logic.
CUPL - Compiler for Universal Programmable Logic. (A old programming language for logic. Modern examples would be Verilog/VHDL). WinCUPL ultimately uses CUPL.EXE to compile .PLD files into a .JED file. Assisted Technology released CUPL in September 1983.<br />
.TT2 - The Berkeley PLA netlist format which CUPL.EXE can generate that can be used by the Atmel fitters.<br />
EDIF - Another type of netlist format which also is usable by the Atmel fitters. Yosys is capable of generating this format, however, one will still need a techmap.<br />
FITTER - A fitter converts a netlist into the fusemap (.JED) file. Fitters are needed for the ATF150x CPLD devices. If my understanding is correct, this is basically place & route.<br />
.JED/JEDEC File - A fuse map intended to be "burned/programmed" into a logic device.<br />
.SVF File - Serial Vector Format. This file can be used by any JTAG programmer (vendor-independent) to program a device that has a JTAG interface.<br />
Wine - Wine is not an emulator. Allows running Windows programs under Linux.<br />

# Writing logic for these parts: Possible Workflows
Each of these subsections represents a potential workflow to design logic equations for these parts. The majority of the focus will be on modern methods.
## Old Approach: WinCUPL
While logic for these parts can be written via WinCUPL, the experience may be fraught with difficulty as it is somewhat unstable and requires Windows. While it does run under Linux via Wine, it is nonetheless not worth the trouble to use it for serious work considering the number of other options for setting up a workflow. It does however have value in the help files / documentation / examples. To get it working within Wine, you'll need winetricks so you can install mfc40 and mfc42. On Ubuntu, this would look something like:

<code>sudo apt-get install wine winetricks playonlinux
winetricks mfc40 mfc42
</code>


This diagram is from the help files built into WinCUPL:

![WinCUPL Data Flow Diagram](vendor-docs/WinCUPL-data-flow-diagram.png)

## Command line approach: CUPL & Your favorite text editor or IDE.
Since WinCUPL simply is a front-end / IDE on top of CUPL and related programs, one can write a CUPL .PLD file in their favorite editor and have CUPL compile it into a .JED file for a PLD. CPLD parts will require the additional step of using a fitter for the specific device.

* <a href="https://www.qsl.net/bh1phl/CUPL_USERS_GUIDE.pdf">A detailed User's Guide to CUPL in PDF</a>


Run CUPL using the following command line format:

<code>cupl [-flags] [library] [device] source</code>


Examples run under Wine would look like this:

<code>wine c:/Wincupl/Shared/cupl.exe -m1lxfjnabep -u c:/Wincupl/Shared/cupl.dl your-code.PLD</code>

Additionally, if you are targeting a CPLD (ATF150x) for which CUPL.EXE does not have direct support, you will need to run:

<code>wine c:/Wincupl/WinCupl/Fitters/fit1502.exe -i your-code.tt2 -dev P1502T44 -DEBUG on -Verilog_sim VERILOG -Out_Edif ON</code>

The above example is for an ATF1502 in a TQFP-44 package. You will need to use the appropriate fitter and device type for your particular CPLD.

<details>
<summary>Expand here for details of the command line flags for CUPL.EXE</summary>
Run CUPL using the following command line format:
<code>cupl [-flags] [library] [device] source
where
-flags is the following set of compiler options:
-j JEDEC download format
-h ASCII-HEX download format
-i HL download format
-n use input filename for output file
-a create absolute file
-l create listing file
-e create expanded macro definition file
-x create expanded product-terms in documentation file
-f create fuse plot/chip diagram in documentation file
-p create PDIF database interchange format file
-b create Berkeley PLA format file
-c create PALASM format file
-d deactivate unused OR terms
-r disable product term merging
-g program security fuse
-o treat all state machines as “one-hot”
-u use specified library for compilation
-s perform logic simulation after compilation
-w perform simulation with waveform output (MS-DOS only)
-m0 no minimization
-m1 quick minimization (default)
-m2 Quine McCluskey
-m3 Presto
-m4 Expresso
-q MIcrosoft format for error messages
-zq QuickLogic’s QDIF file
-kb Optimize product term usage for pin or pinnode variables. This overrides the DEMORGAN statement if it appears in the source file
-kd DeMorganize all pin and pinnode variables. This overrides the DEMORGAN statement if it appears in the source file
-ks Force product term sharing during minimization. This is also referred to as group reduction
-kx Do not expand XOR to AND-OR equations. This is used for device independent designs or designs targeted for fitter-supported devices where the fitter supports XOR gates
</code>
</details>

Recently, two different extensions for VS Code for CUPL have been written:
* https://marketplace.visualstudio.com/items?itemName=tlgkccampbell.code-cupl
  * This one handles just syntax highlighting for CUPL .PLD files
* https://marketplace.visualstudio.com/items?itemName=VaynerSystems.VS-Cupl
  * This is an entire workflow, including syntax highlighting.

<details>
<summary>Expand here for a list of devices the version of CUPL provided with WinCUPL supports</summary>
* CBLD.EXE will allow you to see a list of devices that are supported within the CUPL.DL device library.
* WinCUPL is specifically restricted to Atmel devices, however, other versions of CUPL found elsewhere will likely have parts from a broader array of manufacturers.

<code>wine ./cbld.exe -l
CBLD(PM): CUPL Device Library Management Program
Version 5.0a
Copyright (c) 1983, 1998 Logical Devices, Inc.
C:\Wincupl\Shared\CUPL.DL  rev:DLIB-h

Device        Rev   Pins  Fuses  Pterms
------------  ---   ----  -----  ------
v750           03    24   14394    171
v750b          02    24   14435    171
v750c          02    24   14504    171
v750cext       02    24   14504    171
v750cextppk    02    24   14504    171
v750cppk       02    24   14504    171
v2500          07    40   71648    416
v2500b         04    40   71745    416
v2500c         04    40   71816    416
v2500cppk      04    40   71816    416
f1500          01    44   15360    320
f1500t         01    44   15360    320
f1500a         01    44   15360    320
f1500at        01    44   15360    320
f1502plcc44    01    44   15360    320
f1502ispplcc44   01    44   15360    320
f1502tqfp44    01    44   15360    320
f1502isptqfp44   01    44   15360    320
f1504plcc44    01    44   15360    320
f1504ispplcc44   01    44   15360    320
f1504tqfp44    01    44   15360    320
f1504isptqfp44   01    44   15360    320
f1504plcc68    02    68   15360    320
f1504ispplcc68   02    68   15360    320
f1504plcc84    02    84   15360    320
f1504ispplcc84   02    84   15360    320
f1504qfp100    02   100   15360    320
f1504ispqfp100   02   100   15360    320
f1504tqfp100   02   100   15360    320
f1504isptqfp100   02   100   15360    320
f1508plcc84    02    84   15360    320
f1508ispplcc84   02    84   15360    320
f1508qfp100    02   100   15360    320
f1508ispqfp100   02   100   15360    320
f1508tqfp100   02   100   15360    320
f1508isptqfp100   02   100   15360    320
f1508pqfp160   01   160   15360    320
f1508isppqfp160   01   160   15360    320
atfvirtual     01    44   99999   5000
g16v8          09    20    2194     64
g16v8ma        08    20    2194     64
g16v8ms        11    20    2194     64
g16v8a         03    20    2194     64
g16v8as        02    20    2194     64
g16v8s         09    20    2194     64
g16v8cpms      01    20    2195     64
g16v8cp        01    20    2195     64
g16v8cpas      01    20    2195     64
g16v8cpma      01    20    2195     64
g20v8          03    24    2706     64
g20v8ma        03    24    2706     64
g20v8ms        03    24    2706     64
g20v8a         02    24    2706     64
g20v8as        01    24    2706     64
g20v8cp        02    24    2707     64
g20v8cps       01    24    2707     64
g20v8cpma      03    24    2707     64
g20v8cpms      03    24    2707     64
g22v10         01    24    5892    132
g22v10cp       01    24    5893    132
p22v10         17    24    5828    132
virtual        01   200   99999   5000
v750lcc        07    28   14394    171
v750blcc       02    28   14435    171
v750clcc       02    28   14504    171
v750cextlcc    02    28   14504    171
v750cextppklcc   02    28   14504    171
v750cppklcc    02    28   14504    171
v2500lcc       08    44   71648    416
v2500blcc      04    44   71745    416
v2500clcc      04    44   71816    416
v2500cppklcc   04    44   71816    416
g20v8lcc       03    28    2706     64
g20v8alcc      02    28    2706     64
g20v8aslcc     01    28    2706     64
g20v8malcc     03    28    2706     64
g20v8mslcc     03    28    2706     64
g20v8slcc      03    28    2706     64
g20v8cplcc     02    28    2707     64
g20v8cpslcc    01    28    2707     64
g20v8cpmalcc   03    28    2707     64
g20v8cpmslcc   03    28    2707     64
g22v10lcc      02    28    5892    132
g22v10cplcc    01    28    5893    132
p22v10lcc      17    28    5828    132
</code>
</details>


If one is trying to utilize the ATF150X devices, using the appropriate fitter is required.
* ![ATF15xx Family Device Fitter User's Manual](vendor-docs/fitter.pdf)

<details>
<summary>Expand for command line options for the newer ATF1502.EXE fitter.</summary>
<code>Atmel ATF1502 Fitter Version 1918 (3-21-07)
Copyright 1999,2000 Atmel Corporation
 Usage: FIT1502.EXE [-i] input_file[.tt2] {options}
 Options:
   -help
   -o output_file_name (for *.tt3 and *.jed)
   -device package_type (PLCC44/TQFP44)
   -tech tech_name (ATF1502AS/ATF1502ASV/ATF1502BE)
   -module module_name
   -preassign TRY|keep|ignore (pin preassignment options)
   -silent (no message on screen)
   -h2 (advanced help option)
   -has (advanced help option for AS)
   -hbe (advanced help option for BE)
</code>
<code>Atmel ATF1502 Fitter Version 1918 (3-21-07)
Copyright 1999,2000 Atmel Corporation
   -strategy c [command file name]
   -strategy ifmt (input file format) [TT | edif]
   -strategy lib (library file name for edif input)
   -strategy open_collector = [   OFF |   on  | = pin_name1 pin_name2...]
   -strategy JTAG = [   off |   ON ]
   -strategy pd1 [   OFF |   on ] (power down 1)
   -strategy pd2 [   OFF |   on ] (power down 2)
   -strategy TDI_pullup = [   OFF |   on ]
   -strategy TMS_pullup = [   OFF |   on ]
   -strategy DEBUG = [   on |   OFF ]
   -strategy output_fast [on | OFF | = pin_name1 pin_name2...]
   -strategy pin_keep [ off | = pin_name1 pin_name2...]
   -strategy ues [value ] (2 ASCII characters)
   -strategy security [ OFF | on ]
   -strategy tPD = [ 5 | 7 ]
   -strategy voltage_level_A [ 1.8 | 2.5 | 3.3]
   -strategy voltage_level_B [ 1.8 | 2.5 | 3.3]
   -strategy fast_inlatch [ OFF | on | = pin_name1 pin_name2...]
   -strategy schmitt_trigger [ OFF | = pin_name1 pin_name2...]
   -strategy pull_up [ OFF | = pin_name1 pin_name2...]
   -strategy unused_To_PinKeeper [ off | ON ]
   -strategy pull_up_unused [ OFF | on]
   -strategy unused_To_Ground [ OFF | on]
   -strategy pull_down [ OFF | = dedicated_pin1 dedicated_pin2...]
   -strategy Latch_Synthesis [ON | off ]
   -strategy Optimize [ON | off]
   -strategy Cascade_Logic [ON | off |= pin_name1 ..pin_nameN]
   -strategy Foldback_Logic [ON | off |= node_name1 ..node_nameN]
   -strategy Soft_Buffer [on | OFF |= node_name1 ..node_nameN]
   -strategy XOR_Synthesis [on | OFF |= pin_name1 ..pin_nameN]
   -strategy Push_Gate [on | OFF]
   -strategy Verilog_sim [sdf | Verilog | OFF]
   -strategy Vhdl_sim [sdf | vhdl | OFF]
   -strategy Out_Edif [on | OFF]
   -strategy Global_Fold [node_name1 ..node_nameN]
   -strategy Global_OE [node_name1 ..node_nameN]
   -strategy OE_node [node_Number1..node_NumberN]
   -strategy logic_doubling [on | OFF]
   -strategy twoclock [clockname]
   -strategy pinfile
</code>
</details>

## Absurd approach: Fusemaps by hand
* See this <a href="https://blog.frankdecaire.com/2017/01/22/generic-array-logic-devices/">blog post</a> by Frank DeCaire.


While not the easiest approach, just as one can write G-Code in notepad or Assembly code in a hex editor, manually creating a fusemap is technically possible. This assumes that you have a datasheet for your device which has a description of the fusemap and the details of how the macrocells work. With this in hand, one could write a JEDEC file with the desired functionality and a text editor. This would be non-trivial and error-prone, but it demonstrates that such a thing could be done, at least with the older PLDs (16V8, 22V10), and even with the ATF750 (some datasheets actually had the fusemap for this part).


It is worth noting that the fusemap for the ATF150x parts has been recently documented in <a href="https://github.com/whitequark/prjbureau">prjbureau</a>. Given the complexity of these devices over PLDs, writing a fusemap by hand for these parts would probably be a bad idea.

## Other languages: ABEL, PALASM (ancient)
Since we're mostly covering modern approaches to these devices here, these will only be covered very briefly:
* ABEL: "Advanced Boolean Expression Language" was created in 1983 by Data I/O Corporation.
* PALASM: Introduced by Monolithic Memories, Inc. (MMI) in the 1980's
  * A modern version of this called <a href="https://github.com/daveho/GALasm">GALASM</a>

## Atmel Prochip (not free)
Atmel Prochip is not free, however, you may be able to get a trial license from Microchip. It is nonetheless worth installing regardless because there are newer fitters for the ATF150x devices that can be extracted from this installation. These can be used with other workflows and so having these is pretty useful. The newer versions of the fitters should mention version 1918 (3-21-07) when invoked from a command line.

## Quartus (free) via POF2JED
* It turns out that the Altera (Now Intel) <a href="https://www.intel.com/content/www/us/en/software-kit/711791/intel-quartus-ii-web-edition-design-software-version-13-0sp1-for-windows.html?">Quartus 13.0sp1</a> can be used to produce a .POF file targeting various CPLD chips made by Altera in the MAX EPM3K/EPM7K series.
* The resulting .POF file can be converted using a utility called <a href="http://ww1.microchip.com/downloads/archive/pof2jed.zip">POF2JED</a> from Atmel (Now Microchip). This is further detailed in <a href="http://ww1.microchip.com/downloads/en/AppNotes/DOC0916.PDF">this application note.
* Important!: Newer versions will not work. v13.0sp1 last version that had support for the MAX EPM3K/EPM7K chips. Support for these chips has been removed from newer versions of Quartus. You MUST use the old version.

## Digital (free, use schematics instead of logic equations / programming)
"Digital is an easy-to-use digital logic designer and circuit simulator designed for educational purposes." This is an interesting option as one can create a schematic and have a .JED file generated for a GAL16V8 or GAL22V10. If one provides the fitters to Digital, it can produce .JED files for the ATF150x series as well.
https://github.com/hneemann/Digital

## Yosys (Open Source + Atmel Fitters, experimental)
In theory, one can use Yosys Open SYnthesis Suite (Yosys) with the help of the Atmel Fitters a specific CPLD and a techmap to produce .JED files. This is a bit more experimental, but some have managed to make this work. This allows an almost entirely open-source workflow using Verilog, and probably <a href="https://icestudio.io/">Icestudio</a> if one prefers schematic capture as well. A good place to start would be using the <a href="https://github.com/YosysHQ/oss-cad-suite-build">OSS CAD Suite</a> to get the big parts of the suite set up. After that, there are two approaches to making this work:
* https://github.com/whitequark/prjbureau
** prjbureau demonstrates going from RTLIL to a .JED file
* https://github.com/hoglet67/atf15xx_yosys/
** This example goes from plain old verilog into a .JED file by implementing a techmap.

# Programming / Burning
There are a few choices on how the part can actually be programmed depending on whether it supports JTAG.

A word on programming algorithms:
Programming algorithms were seldom documented on datasheets for a part. Usually, these were behind NDA and only the companies producing Device Programmers had them (Data I/O, Logical Devices, Hi-Lo Systems, BP Microsystems, Wellon). Furthermore, some parts supporting JTAG (which in theory is much more open/universal), can nonetheless be programmed to repurpose the JTAG pins, at which point a dedicated device programmer or specialized knowledge of blanking the device is required.

## PLD Devices (ATF16V8, ATF22V10)
These parts require an EPROM programmer. <span style="color: red;">Additionally, an important gotcha' is that there are many manufacturers of these parts as well as variants within a manufacturer. While the fusemap may be compatible across variants (GAL16V8 from Lattice vs. the ATF16V8 from Atmel/Microchip), THE PROGRAMMING ALGORITHMS ARE NOT! You will need an EPROM programmer with support for the EXACT manufacturer and EXACT part number of the device you have.</span>

## CPLD Devices (ATF1502, ATF1504, ATF1508)
These parts can be programmed via JTAG, so there are a few options.
* Official programmer: https://www.kanda.com/CPLD-Programmers.175.html
  * Software: https://www.microchip.com/en-us/development-tool/ATMISP
* OpenOCD: https://openocd.org/
  * You will need an SVF file to program a device via OpenOCD. This can be created by converting the .JED file using either ATMISP, or fuseconv.py from whitequark/prjbureau

* To generate a .JED file for these devices, you will need the fitters. While WinCUPL has fitters within it, a much more updated version of the fitters is available inside of Atmel Prochip from <a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">Microchip's website</a>

* Finally, it is worth pointing out that the JTAG pins on these devices can be repurposed for user I/O in a design. However, if one does this, the devices will no longer be reprogrammable via JTAG. One then requires a universal device programmer (and requisite adapters) to blank the device. Some information is out there concerning a trick of applying 12V Vpp to the OE1 pin in order to unlock the device, and some unofficial documentation exists for this.

## Other Atmel CPLD Parts (ATF750, ATF1500)
* These parts do not support JTAG and are a bit more expensive, so they haven't been tried. You'll need an EPROM programmer that supports these.
* In theory the ATF1500 fitter should work fine under Wine and so if fed with a netlist it should work. This means either CUPL.EXE or in theory Yosys with the right techmap could work.
* I believe CUPL should be able to generate a .JED directly for the ATF750 without a fitter.

## Altera EPM3X and EPM7X parts
I believe these parts are no longer produced, or possibly NRND, at least as far are true 5V devices are concerned (and not merely 5V tolerant), so I would recommend moving toward the ATF150x parts. However, since a large number of people seem to really like these parts and seek them out on used markets I will say this:

The Altera EPM3X/EPM7X parts when purchased used might not be blank, and some of these parts do not support JTAG. It is possible to program them in such a way that they cannot be reprogrammed via JTAG, and the programming algorithms in almost any PLD is not actually part of the datasheet. Nonetheless, if one has a universal device programmer, or if one knows the trick of applying 12V VPP on the JTAG-supporting devices, they can be blanked. Finally, there are simply counterfeit / remarked devices out there are well, and no amount of hardware or ingenuity will solve this problem.

# Reversing a JED file back into logic equations
Finally, if one is able to read a .JED out of a device, this can sometimes be reversed back into equations. These devices all have security fuses, however, which can disable any ability to read out the device. Given a .JED file, the following approaches can be taken to arrive at the equations:
* By hand, comparing the .JED file to the fusemap / macrocells in the datasheet. See this <a href="https://blog.frankdecaire.com/2017/01/22/generic-array-logic-devices/">blog post</a> by Frank DeCaire.
* JED2EQN.EXE - A DOS utility floating around on the internet.
* MAME can be compiled with a utility called jedutil