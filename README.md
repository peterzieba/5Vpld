# Overview
This repository centers around documenting modern ways of developing logic for and programming Atmel (Now Microchip) 5V GAL PLD and CPLD parts under recent Linux (Ubuntu 22.04) and Windows 10 22H2 versions.
* ![ATF16V8](vendor-datasheets/Atmel-0425-PLD-ATF16V8C-Datasheet.pdf) (Modern/active equivalent of the PAL16V8 and GAL16V8 parts)
* ![ATF22V10](vendor-datasheets/doc0735.pdf) (Modern/active equivalent of the PAL22V10 and GAL22V10 parts)
* ![ATF1502](vendor-datasheets/Atmel-0995-CPLD-ATF1502AS(L)-Datasheet.pdf) (Active replacement for the EPM7032)
* ![ATF1504](vendor-datasheets/Atmel-0950-CPLD-ATF1504AS(L)-Datasheet.pdf) (Active replacement for the EPM7064)
* ![ATF1508](vendor-datasheets/doc0784.pdf) (Active replacement for the EPM7128)

These parts are still active and highly worth considering wherever:
* 5V logic is a requirement, avoiding level shifting, low latency (7ns), instant-on & non-volatile, and situations needing Hi-Z / Open-collector states.
* Prototyping / Iteration (reprogrammable)
* Learning about logic: Through-hole / soldering-friendly is desired: All 16V8 or 22V10 parts are available in DIP packages; ATF150x parts are available in PLCC packages that can be placed in through-hole PLCC sockets. SMD packages are available for any of the parts.
* Replacing large quantities of various TTL/CMOS Logic Gates (74-series logic)

In short, these chips work very well wherever the above requirements are necessary, however, the software (and device programming) experience can be incredibly challenging owing to outdated and buggy software.

This repository aims to make it easier to work with these parts and hopefully keep them active for years to come.

This is a "Choose your own adventure novel". Covered here are many approaches and tradeoffs:
* <a href="#old-approach-wincupl-16v8-22v10-and-atf150x">Using the WinCUPL IDE (Erratic, unreliable)</a>
* <a href="#5vcomp-the-cupl-compiler--your-favorite-text-editor-or-ide-16v8-22v10-and-atf150x">Using just the CUPL.EXE compiler from WinCUPL directly with some wrapper scripts here (5vcomp). Works in Windows/Linux. (recommended)</a>
* <a href="#quartus-free-verilog-vhdl-schematic-capture-indirect-support-for-atf150x-linux-or-windows">Using Quartus (only for the CPLD. Works by first targeting a similar Altera CPLD and then using the POF2JED utility to convert.) Windows/Linux</a>
* <a href="#absurd-approach-fusemaps-by-hand-16v8--22v10">Making your own fusemap / .JED file with nothing more than a datasheet and text editor. Maybe need some graph paper...</a>
* Experimental approaches with Yosys (Only for the CPLD parts. EDIF is fed into the [Atmel fitter](atmel-fitters/))
* Several Approaches to reverse-engineering a .JED file back into logic equations.

<details>
<summary>Scope: Expand here for why similar parts not covered</summary>

>* The intention is primarily to make it easier to work with parts that are still active so they do not go NRND and eventually disappear from the market. While there are gems here for other related historical parts, this is not the focus of this repository.
>* The ATF1500 is not covered because it is a more expensive part and does not support JTAG programming. It is fundamentally different from the ATF1502, ATF1504, and ATF1508
>* The ATF750 and ATF2500 are also not covered for similar reasons. Other chips are almost certainly a better choice.
>   * The ATF2500C might be worth examining in spite of the somewhat high cost due to being available in a DIP-40 package and thus breadboard friendly. Without understanding the programming algorithm however, it would be of use to very few people as no recent/affordable device programmers support this chip.
>* We only consider true 5V parts (not merely parts with 5V tolerant inputs, of which there are many more).
>   * 3.3V parts cannot supply the minimum of 3.6V to drive the input of a 5V CMOS part high, so 5V tolerant parts are not enough in many cases. Even the parts covered here may not necessarily be capable of the required VoH as their output voltage drops off quickly under load. In these cases, pullup resistors can be considered.[^2]
>   * Notably, however, driving 5V TTL inputs from a 3.3V part, on the other hand, is not a problem. A 5V TTL input has a threshold of 2V.
>* 3.3V parts are not considered: There are simply better choices that are well documented. Also, the CPLD parts have VccIO inputs, so you can technically use them in 3.3V designs just as well.
>* The following 5V IO capable parts probably should be covered, but they're already well supported, documented, modern tools, etc.
>   * The Greekpak devices
>   * The Cypress PSoC5LP (An ARM Cortex M3 with CPLD-like logic blocks), available in 68-pin QFN, 100-pin TQFP
>* Any parts that are NRND or inactive are not covered, as we consider what can be reliably and sensibly purchased.
>* Since all of the parts considered here are still in full production (as of 2023), they can be used in production designs.
>* For the ATF150x CPLD parts specifically:
>   * The parts ending in 'BE' are not covered here as they seem to be very expensive. In principle these are interesting because they have multiple IO bank voltages.
>   * The parts ending in 'ASV' are 3.3V only, however, these are supported just fine in the workflows discussed here. Incidentally, the 'AS' devices can be operated at 3.3V IO through the VccIO pins. The lower pincount (44-pin) devices to not show VccIO pins in their datasheet, but it does seem to be the case that two pins are Vcc and two are VccIO, so this is possible as well.
>* For applications where 5-Volt tolerant operation is acceptable, it might be worth considering the ispMACH4000 series. Parts such as the LC4032ZE are available in a somewhat soldering friendly TQFP, however there are likely similar challenges with software.
>   * Vendor Tools:
>      * ispLEVER v3.1 (2003)
>      * ispLEVER v4.0 (2004)
>      * ispLEVER Classic v1.8 (2014)
>      * ispLEVER Classic v2.0 (2015)
>   * Open source paths for these parts:
>      * https://github.com/bcrist/re4k
>      * https://github.com/bcrist/Zig-LC4k
>      * Vendor Fitter: `C:\ispLEVER_Classic2_1\ispcpld\bin\lpf4k.exe`
</details>

# Background on digital logic.
This repository isn't intended to be an introduction to digital logic, but a brief review and compare/contrast to similar things is provided here.

<details>
<summary>Expand here for tutorials on Digital Logic</summary>

 >Ben Eater does a series of <a href="https://www.youtube.com/watch?v=KM0DdEaY5sY&list=PLowKtXNTBypGqImE405J2565dvjafglHU&index=6">Videos on Digital Logic</a> that are a really excellent introduction to some of the concepts here.
</details>

<details>
<summary>Expand here for a description of how these parts compare to ladder logic on a PLC</summary>

>* Each rung's output in ladder-logic can be thought of as a single macrocell.
>* The inputs on a rung can be "normally open" or "normally closed" (active high or low), and can consist of any number of inputs (or even the state of another macrocell). The inputs defined on a single rung are basically equivalent to a single product-term belonging to a macrocell. There can be multiple product terms defined that activate a given macrocell.
</details>

<details>
<summary>Expand here for details on how all of these compare to FPGAs</summary>

>Such parts are the spiritual predecessors of more modern FPGAs. Key differences between FPGAs and PLDs:

>* FPGAs are typically constructed from a large number of LUTs (Lookup tables). CPLDs use a sum-of-products structure.
>* FPGAs typically expect to have their bitstream uploaded on powerup, requiring an external EEPROM. PLDs are typically non-volatile and instantly ready upon powerup.
>* FPGAs usually support more standard means of programming, whereas many PLDs required specialized device programmers.
>* From input to output, CPLDs can be thought of as shallow but wide, theoretically having lower propagation delays (in practice, if we're talking about 5V logic, don't expect better than 7ns). FPGA have much deeper internal logic but are composed of LUTs with relatively tiny input widths (LUT4, LUT5, etc.).
>* There are likely exceptions to all of the above in some parts. These are not hard rules.
</details>

# Requirements
A high-level overview of what is required:
* Basic understanding of digital logic.
* The actual PLD/CPLD chip you'd like to work with from the usual suppliers (Mouser, Digikey, Octopart)
* A software workflow covered here. Highly recommended is using the 5vcomp script from here to call the CUPL.EXE compiler. This works on Linux and even Windows 10 22H2 x64!
* An EPROM/Device programmer if you wish to use the ATF16V8 or ATF22V10 parts.
* An EPROM or JTAG programmer for the ATF150x parts
![See PROGRAMMING.md](PROGRAMMING.md) for details on what it takes to program these parts in detail.

# Terminology & File Formats
<a href="https://en.wikipedia.org/wiki/Programmable_logic_device">**PLD/GAL**</a> - Programmable Logic Device. Small, generally DIP-package 5V programmable Logic.<br />
<a href="https://en.wikipedia.org/wiki/Programmable_logic_device#CPLDs">**CPLD**</a> - Complex Programmable Logic Device. Larger packages, many pins, much more complex.<br />

**5vcomp** - A utility in this repository ([batch file for Windows](windows-workflow/) / [shell script for linux](linux-workflow)) that is a wrapper around the CUPL.EXE compiler.<br />

<a href="https://en.wikipedia.org/wiki/Combinational_logic">**Combinatorial Logic**</a> - Simple logic (AND, OR, NOT, gates, etc.) that does not use flip-flops / registers / clocks. Such logic could technically be implemented with an EPROM/Memory, where a series of inputs always maps to a known set of outputs.<br>
<a href="https://en.wikipedia.org/wiki/Sequential_logic">**Registered Logic**</a> - Logic that uses registers (flip-flops), and can thus hold state. On the GAL16V8 and GAL22V10, each macrocell can be configured as a D-Flip-Flop, and all flip-flops share the same clock pin. On the ATF150x, much more complex types of registered logic and clocking options are available.

<a href="https://en.wikipedia.org/wiki/Macrocell_array">**Macrocell**</a> - Each output has a macrocell associated with it. These can often be configured as active high, active low, flip-flops, etc.<br />
<a href="https://en.wikipedia.org/wiki/Programmable_logic_device#/media/File:Programmable_Logic_Device.svg">**Product Term**</a> - Each macrocell has a number of product terms associated with it (typically around 5). A single product term is essentially a giant AND gate with inputs to each pin on the device. Burning away fuses allows selecting which inputs are fed into this AND gate, ultimately selecting the conditions required for a product term to be activated. Multiple product terms belonging to the same output macrocell are then combined into an OR gate before being fed into the macrocell. This means that there can be several combination of inputs that allow a given macrocell to be triggered. This architecture is called a Sum-of-Products logic array.

<a href="https://en.wikipedia.org/wiki/Programmable_Array_Logic#CUPL">**CUPL**</a> - A early (1983) programming language by [Assisted Technology, Inc.](https://deramp.com/swtpc.com/PLD_History/ABEL_project/CUPL_Data_Sheet_1983_ocr.pdf) used to define the behavior of programmable digital logic. "Compiler for Universal Programmable Logic.", is essentially a predecessor to languages like Verilog/VHDL. CUPL.EXE is the compiler which is used to compile .PLD files written in CUPL, ultimately to be burned into programmable logic devices.<br />
**.PLD** file - A logic design source file written in the CUPL language. See [examples/](examples) for a basic idea of what this looks like.<br />
<a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">**WinCUPL**</a> - A Windows front-end/IDE to the CUPL compiler and related programs. WinCUPL itself is best avoided but installing it is necessary to get the CUPL compiler and device libraries.<br />
**Variable Extensions** (such as .D or .OE) can be added to variable names to indicate specific functions associated with the major nodes inside a programmable device, including such capabilities as flip-flop description and programmable tri-state enables.<br />
[**.dl File**](device-library/) - A Device Library file is a binary file used by the CUPL compiler which provides support for the various devices CUPL has the ability to compile logic for. This should not be confused with the Device/Primitive Libraries that are part of the [Atmel fitter](atmel-fitters/).<br>

<a href="https://en.wikipedia.org/wiki/Netlist">**Netlist**</a> - A netlist is essentially an electrical schematic in a text file which defines connections. For the purposes here, it is an intermediary file format (Either EDIF or Berkeley PLA), which is used to describe the behavior of logic ultimately fed into the [Atmel fitter](atmel-fitters/).<br />
<a href="">**.TT2**</a> - The Berkeley PLA file format. An intermediary file which CUPL.EXE can generate that can be used by the [Atmel fitter](atmel-fitters/). Notably, one can use [berkeley-abc](https://github.com/berkeley-abc/abc) to work with these files.<br />
<a href="https://en.wikipedia.org/wiki/EDIF">**.EDF / .EDN**</a> - EDIF is another type of netlist format. The [Atmel fitter](atmel-fitters/) can use this as both an input, as well as an output. Yosys is capable of generating this format, however, one will still need a techmap for this to work.<br />
<a href="https://en.wikipedia.org/wiki/Place_and_route">**Fitter**</a> - A fitter converts a netlist into the fusemap (.JED) file. It is specific to the device in question and provided by the device manufacturer (Atmel in this case). Fitters are needed only for the ATF150x CPLD devices, whereas the PLD devices can go straight from a .PLD to a .JED file. In more modern parlance the fitter is basically the place & route stage.<br />
**ATMEL.STD File** - Part of the Atmel ATF150x fitter, the primitive/device library for PLA.[^1]<br />
**APRIM.LIB File** - Part of the Atmel ATF150x fitter, the primitive/device library for EDIF.[^1]

**.JED/JEDEC File** - A fuse map intended to be "burned/programmed" into a logic device. A JEDEC file is a text file formatted specifically to the <a href="https://archive.org/details/JEDECJESD3C/mode/2up">JESD3 standard</a>. If you have a device programmer that has support for the exact device you are interested in programming this file is all that is needed. If your device supports JTAG programming (Most CPLDs) and you have a more generic JTAG programmer that does not know of your device, you will probably need to convert the .JED file to an .SVF or .XSVF file first.<br />

[**.SVF File**](https://en.wikipedia.org/wiki/Serial_Vector_Format) - Serial Vector Format. Generated from the .JED file, the .SVF can be used by any JTAG programmer (vendor-independent) to program a device that has a JTAG interface (So, the ATF150x CPLDs). The Windows <a href="https://ww1.microchip.com/downloads/en/DeviceDoc/ATMISP67.zip">**ATMISP v6.7**</a> or <a href="https://ww1.microchip.com/downloads/en/DeviceDoc/ATMISP7.zip">ATMISP v7</a> tools can be used to generate an .SVF from a .JED file, as well as the <a href="https://github.com/whitequark/prjbureau/blob/main/util/fuseconv.py">fuseconv.py</a> utility by whitequark. Once you have an .SVF, you can use tools like OpenOCD or [Afterburner](https://github.com/ole00/afterburner) to program a CPLD with a JTAG interface.<br>
[**.XSVF File**](http://www.jtagtest.com/pdf/xapp503_svf_xsvf.pdf) - A compressed variant of an .SVF file created by Xilinx. This normally never shows up in the tools mentioned here with the exception of the [Open-Source 'Afterburner' Device Programmer](https://github.com/ole00/afterburner/) project, where it is the format that it accepts when programming a JTAG device.
<br><br>
**Security bit** - Aka Security Fuse. When enabled, this prevents copying of a device by disabling readout. This does not prevent reprogramming of the device -- if the device is eraseable, the security bit is returned to disabled status when erased. After programming, verification of the device becomes impossible if the security bit is set, so this bit should be set last if verification is desired. The CUPL compiler will produce a .JED file with the security bit set if the 'g' flag is passed. Within the JESD3 standard, the G1 command enables device security. The ATMISP programmer supports setting this in the interface, and other device programmers may have this option as well, so it need not be set within the .JED file. Finally, the Atmel fitters also have a parameter to set this.
<br><br>
**CSIM.EXE** - Part of WinCUPL. A tool for [simulating](simulation/) the behavior of logic. This takes an .SI file (test vectors) and an `.ABS file`. Given these it produces an .SO file. Only provides functional simulation (so, logic states but not timing)

<a href="https://www.winehq.org/">**Wine**</a> - "Wine Is Not an Emulator". Allows running Windows programs under Linux. This guide assumes enough familiarity with Linux & Wine. If these are new topics, consider running everything under Windows to keep things simple in the beginning.<br />
**Wine Prefix** - Just as with an emulator, you can have multiple virtual machines. In Wine, though it is not an emulator, you can have multiple virtual environments. The location of the 'default' wine prefix is ```~/.wine```. The 5vcomp scripts assume the default the default prefix, which might be annoying for advanced users.

# Writing logic for these parts: Possible Workflows
Each of the subsections here represents a potential workflow to design logic equations for these parts. The majority of the focus will be on methods that avoid using the WinCUPL frontend/IDE directly (unreliable), but which do use the underlying CUPL.EXE command-line compiler which is fairly robust.

Finally, a word on preferred approach, given the options: Using the CUPL.EXE compiler via command line or avoiding CUPL altogether and using Quartus are probably the best ways, especially if you are interested in using Hi-Z states. Neither Yosys nor Digital seem to have robust support for 'inout' ports, Tristate/Hi-Z states, open collector outputs, etc. If these are important to you, it may be worth considering tools and workflows which are less experimental.

## Old Approach: WinCUPL (16V8, 22V10, and ATF150x)
WinCUPL is basically an IDE. While logic for these parts can be written within WinCUPL's editor, the experience may be fraught with difficulty as it is a quirky and often unstable Windows application (While it does run great under Wine, this doesn't really change things much). I've seen the editor itself crash just for looking at it sideways, and its copy-paste functionality behave in bewildering ways.
It does however have value in the help files / documentation / examples. It should emphasized that the CUPL compiler itself is actually pretty solid/stable, and so the troubles of WinCUPL shouldn't be equated with CUPL itself.
So, the recommended approach is to start here regardless and use it for documentation/examples/compiler/device-library and then simply avoid it for serious work by using the command line CUPL.EXE (perhaps through the 5vcomp helper scripts in this repository as in the next section). 

You can <a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">Download WinCUPL from here</a>.

To get it working under Linux with Wine, you'll need winetricks so you can install mfc40 and mfc42. On Ubuntu Linux, this would look something like:

<code>dpkg --add-architecture i386
sudo apt-get install wine wine32:i386 winetricks playonlinux innoextract
WINEARCH=win32 WINEPREFIX=~/.wine wine wineboot
winetricks mfc40 mfc42
wine awincupl.exe
</code>

Furthermore, if you are intending on working with the ATF150x parts, you should probably grab the newer fitters out of the Atmel Prochip package. The utilities in this repository will refuse to work with the old fitters.

## 5vcomp: The CUPL compiler & Your favorite text editor or IDE (16V8, 22V10, and ATF150x)
Since WinCUPL simply is a front-end / IDE on top of the CUPL.EXE compiler and related programs, one can write the desired logic in the CUPL language, save it in a .PLD file using their favorite editor and have CUPL.EXE compile it into a .JED file for programming into a PLD.

5vcomp is a simple wrapper around the CUPL compiler.
This is probably the most solid approach assuming you are OK with using CUPL as a language. You should start with the WinCUPL approach as a prerequisite since it installs the CUPL compiler and has examples/help files.
The workflows here simply make it easier/convenient to get started with CUPL by catching a lot of common issues and providing reasonable defaults to the compiler. It intentionally tries to be as simple as possible so that it may be easily understood, modified, and stand the tests of time across operating system versions. It also tries to catch any errors that might arise so that they are obvious and actionable. Using 5vcomp with example .PLD files (from here or those included with WinCUPL) and modifying them to suit is probably the easiest way of getting started with CUPL that avoids a lot of the quirks of WinCUPL itself.:

* ![Linux Workflow (point 5vcomp at your .PLD file from a command line)](linux-workflow/)
* ![Windows Workflow (right-click on a .PLD to compile with 5vcomp.bat)](windows-workflow/)

## Guide to the CUPL Language and Compiler
Assuming you're using CUPL either through WinCUPL or 5vcomp, this section has a general reference to the language.

An overview of how things work which shows how one can go from a CUPL .PLD into the .JED file needed to program a device. Note that the Atmel Fitter (place and route) stage is only used when working with the ATF150x CPLD parts. For most simpler parts, CUPL is capable of generating a .JED directly.

![WinCUPL Data Flow Diagram](vendor-docs/WinCUPL-data-flow-diagram.png)
(diagram from built-in WinCUPL help)

* ![A detailed User's Guide to the CUPL compiler and language reference in PDF](vendor-docs/CUPL_USERS_GUIDE.pdf)
* ![Atmel WinCUPL User's Manual](vendor-docs/doc0737.pdf)
* ![CUPL Device Libraries in Detail (This determines the chips the compiler supports)](device-library/)

<details>
<summary>Expand here for details of the command line flags for the CUPL.EXE compiler</summary>
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

>[!IMPORTANT]
>**Compiler Mode Selection**
>
>A word of warning is that the <code>Device:</code> keyword in the header section at the top of a .PLD file is not quite the part number you are interested in programming -- it is actually a device mnemonic which selects different macrocell configuration modes and these mnemonics should be mentioned in the datasheet for your device.
>
>So, if you're having trouble getting a flip-flop to work on a 16V8, it might be because you have selected the mnemonic for "simple mode".<br>
>As an example, the compiler can be set to four different modes for the ATF16V8 (similar considerations apply to the 22V10 parts, etc):<br>
>Registered - <code>G16V8MS</code><br>
>Complex - <code>G16V8MA</code><br>
>Simple - <code>G16V8AS</code><br>
>Auto - <code>G16V8</code>

<details>
<summary>Expand Here for a list of mnemonic prefixes</summary>
<code>
EP	Erasable Programmable Logic Device (EPLD)
G	Generic Array Logic (GAL)
F	Field Programmable Logic Array (FPLA)
F	Field Programmable Gate Array (FPGA)
F	Field Programmable Logic Sequencer (FPLS)
F	Field Programmable Sequence Generator (FPSG)
P	Programmable Logic Array (PAL)
P	Programmable Logic Device (PLD)
P	Programmable Electrically Erasable Logic (PEEL)
PLD	Pseudo Logical Device
RA	Bipolar Programmable Read Only Memory (PROM)
</code>
</details>

### Atmel ATF150x CPLD Fitters
While CUPL is self-sufficient to generate the final .JED files for most simple devices, the ATF150x CPLD parts rely on a fitter executable (essentially place and route) that was supplied by Atmel. These fitters work with the CUPL compiler, but the fitters _can in theory_ be made to work with anything that can supply a netlist in the correct EDIF or PLA TT2 format to them. Yosys, Berkeley-ABC, and SpyDrNet might all be able to do this in different ways.

* ![ATF15xx Family Device Fitter User's Manual](vendor-docs/fitter.pdf)

<details>
<summary>Expand for command line options for the latest known version of the ATF1502.EXE fitter. Output is similar for ATF1504 and ATF1508 devices.</summary>
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

Advanced help options:
<code>
Atmel ATF1502 Fitter Version 1918 (3-21-07)
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

### Other CUPL workflows:
* https://github.com/willie68/WCPLD
* https://github.com/Manawyrm/PAL-GAL-CI
  * This uses Github Actions to run CUPL under Wine to compile .PLD files.
* Recently, two different extensions for VS Code for CUPL have been written:
  * https://marketplace.visualstudio.com/items?itemName=tlgkccampbell.code-cupl
    * This one handles just syntax highlighting for CUPL .PLD files
  * https://marketplace.visualstudio.com/items?itemName=VaynerSystems.VS-Cupl
    * This is an entire workflow, which has a bit more functionality beyond just syntax highlighting.
 * Dockerized CUPL workflow https://github.com/dinoboards/cpld-toolchain/tree/main

## Absurd approach: Fusemaps by hand (16V8 / 22V10)
One can literally create a fusemap by hand for a PLD.
* See this <a href="https://blog.frankdecaire.com/2017/01/22/generic-array-logic-devices/">blog post</a> by Frank DeCaire, where he documents his journey of doing so.

While not the easiest approach, just as one can write G-Code in notepad or Assembly code in a hex editor, manually creating a fusemap is technically possible. This assumes that you have a datasheet for your device which has a description of the fusemap and the details of how the macrocells work. With this in hand, one could write a JEDEC file with the desired functionality and a text editor. This would be non-trivial and error-prone (if double-negatives confuse you, this is even more exciting), but it demonstrates that such a thing could be done, at least with the older PLDs (16V8, 22V10), and even with the ATF750 (some datasheets actually had the fusemap for this part).

It is worth noting that the fusemap for the ATF150x parts has been recently documented in <a href="https://github.com/whitequark/prjbureau">prjbureau</a>. Given the complexity of these devices over PLDs, writing a fusemap by hand for these parts would probably be a bad idea.

## Other languages / Software: ABEL, PALASM
These will only be covered very briefly:
* ABEL: "Advanced Boolean Expression Language" was created in 1983 by Data I/O Corporation. [Bit of Abel (and CUPL) history](https://deramp.com/swtpc.com/PLD_History/ABEL_project/ABEL_Memos.htm)
* PALASM: Introduced by Monolithic Memories, Inc. (MMI) in the 1980's
  * A modern version of this is called <a href="https://github.com/daveho/GALasm">GALASM</a> which is a continuation of something called GALer. This might be worth considering if you are happy with just PLDs.
* Atmel-Synario: A 1999-era ABEL-HDL and Schematic PLD/CPLD design tool.
* Viewlogic's Workview/ProPLD: 90's-era software.
* Atmel-ProPLD: (possibly Atmel's bundled version of the above?)

## Galette / GALasm (Free, 16V8, 22V10)
Useful for simpler PLD devices. Less expressive than CUPL as a language and uses different operators (AND is *, OR is +, NEGATION is /), but gets the job done if you just want to write some logic for some PLDs.<br>CUPL has the advantage that if you are making things like [address decoders](https://github.com/dbuchwald/6502/blob/d1194eb0162b50493e9f32f2d46c190da779da66/WinCUPL/DB6502.PLD#), you can clearly express the ranges in the language at a high level: `RAM       = Address:[0000..7FFF]`
* https://github.com/simon-frankau/galette
  * Actively maintained, written in rust.
* https://github.com/daveho/GALasm
* https://github.com/dwery/galasm

## Atmel Prochip (Not Free, Verilog/VHDL support for ATF150x)
![PDF: Example Verilog Design flows with using ProChip 5.0.1](vendor-docs/CPLD_Mentor_Verilog_tutorial[1].pdf)<br />
Atmel Prochip is not free, however, you can <a href="https://ww1.microchip.com/downloads/en/DeviceDoc/ProChip5.0.1.zip">download it from here</a>, and may be able to <a href="https://www.microchip.com/prochiplicensing/#/">request a trial license from Microchip</a>. This workflow supports Verilog/VHDL, which is great if one wants to move away from CUPL entirely and can afford to purchase a license.

Prochip should be downloaded regardless because there are newer fitters for the ATF150x devices that can be extracted from this installation, and these fitters are required in every other approach mentioned here. The newer versions of the fitters should mention version 1918 (3-21-07) when invoked from a command line. (The fitters that come with WinCUPL are old and should be replaced with the ones from this package).

In essence, Prochip is the Atmel fitter bundled with:
* "Precision® RTL Synthesis" from Mentor Graphics for Verilog/VHDL synthesis.
* (optionally) "ModelSim®" from Mentor Graphics for Functional/Timing Simulation
* (optionally) "Protel Design Explorer 99SE" for Schematic/CUPL design entry.

## Quartus (Free, Verilog, VHDL, Schematic Capture). Indirect support for ATF150x. Linux or Windows.
* It turns out that the Altera (Now Intel) Quartus II 13.0sp1 Web Edition can be used to produce a .POF file targeting various CPLD chips made by Altera in the MAX EPM3K/EPM7K series, which can be converted to target an ATF150x CPLD.
  * <a href="https://www.intel.com/content/www/us/en/software-kit/711791/intel-quartus-ii-web-edition-design-software-version-13-0sp1-for-windows.html?">Intel® Quartus&reg; II Web Edition Design Software Version 13.0sp1 for Windows</a>
  * <a href="https://www.intel.com/content/www/us/en/software-kit/711790/intel-quartus-ii-web-edition-design-software-version-13-0sp1-for-linux.html?">Intel® Quartus&reg; II Web Edition Design Software Version 13.0sp1 for Linux</a>
  * When installing, you only need "MAX II/V, MAX3000/7000" under device support. Unchecking the other devices can save ~2GB.
  * You may have trouble running it as libpng12.so.0 may be required. See <a href="https://silverdrs.wordpress.com/2020/11/24/running-older-altera-quartus-on-modern-64bit-gnu-linux/">here</a>.
  * Quartus frequently crashes and can even crash your whole desktop session. Fix that by <a href="https://zkre.xyz/posts/quartus/">replacing the bundled libtbb</a>.
  * You can move the .desktop shortcut into ~/.local/share/applications/Quartus II 13.0sp1 (64-bit) Web Edition.desktop
    * I found I had to set Terminal=true for it to work.
* The resulting .POF file can be converted using a utility called <a href="http://ww1.microchip.com/downloads/archive/pof2jed.zip">POF2JED</a> from Atmel (Now Microchip). This is further detailed in <a href="http://ww1.microchip.com/downloads/en/AppNotes/DOC0916.PDF">this application note.
* Important!: Newer versions of Quartus will not work. v13.0sp1 is the last version that had support for the MAX EPM3K/EPM7K chips. Support for these chips has been removed from newer versions of Quartus. You MUST use the old version.

## Digital (free, use schematics instead of logic equations / programming)
"Digital is an easy-to-use digital logic designer and circuit simulator designed for educational purposes."

This is an interesting option as one can create a schematic and have a .JED file generated for a GAL16V8 or GAL22V10. If one provides the [Atmel fitter](atmel-fitters/) to Digital, it can produce .JED files for the ATF150x series as well. Note that this is more of an educational tool for learning about logic. You may have trouble if you expect fullly featured support of these devices (Tri-state pins, Bi-directional IO, etc.)
* https://github.com/hneemann/Digital
If this appeals to you, you might be interested in similar software (though no support for the Atmel parts):
* <a href="http://www.cburch.com/logisim/">Logisim</a>
* <a href="https://github.com/logisim-evolution/logisim-evolution">Logisim Evolution</a>

## Yosys (Open Source with Atmel Fitters for ATF150x, experimental)
In theory, one can use Yosys Open SYnthesis Suite (Yosys) with the help of the [Atmel fitter](atmel-fitters/) a specific CPLD and a techmap to produce .JED files. This is a bit more experimental, but some have managed to make this work. This allows an almost entirely open-source workflow using Verilog, and probably <a href="https://icestudio.io/">Icestudio</a> if one prefers schematic capture as well. A good place to start would be using the <a href="https://github.com/YosysHQ/oss-cad-suite-build">OSS CAD Suite</a> to get the big parts of the suite set up. After that, there are two approaches to making this work:
* https://github.com/whitequark/prjbureau
  * prjbureau demonstrates going from RTLIL to a .JED file
* https://github.com/hoglet67/atf15xx_yosys/
  * This example goes from plain old verilog into a .JED file by implementing a techmap.
* https://github.com/michaelhunsberger/JsonToCupl/
  * This is an example of how to use Yosys to generate CUPL code.
  * Potentially interesting as one could use this to generate a .PLD even for the simpler 16V8 or 22V10 devices
  * http://forum.6502.org/viewtopic.php?f=10&t=7601
* https://github.com/annoyatron255/yosys4gal Verilog Flow for the GAL16V8 and GAL22V10
  * A Verilog flow for GAL16V8 and GAL22V10 logic chips (and pin-compatible alternatives like the ATF16V8 and ATF22V10). It leverages [Yosys](https://www.github.com/YosysHQ/yosys) and [Galette](https://www.github.com/simon-frankau/galette).


Finally, since yosys is extremely complex, a section on understanding the basics is in order especially from the context of these devices. For the moment, however, others have written guides for different parts:
* https://github.com/Ravenslofty/yosys-cookbook
  * https://github.com/Ravenslofty/74xx-liberty/
  * https://github.com/Ravenslofty/74xx-liberty/tree/master/kicad

## Protel 99SE
This was a ~1999/2000 era circuit board design tool made by Altium that worked in Windows and which had support for the SPLD and CPLD parts mentioned here. It is mentioned here for completeness sake, but the author has no direct experience with it. It is said to have supported CUPL and Schematic entry for development of logic but not Verilog nor VHDL.

## Berkeley ABC
Berkeley ABC can be made to read and write verilog and the PLA format used by the [Atmel fitter](atmel-fitters/). If this works, it could potentially eliminate the need to use the CUPL language altogether and instead have a path from verilog to the Atmel CPLDs without the need for expensive software. This remains to be tested.

## BYU's SpyDrNet
SpyDrNet is capable of generating an EDIF netlist which could in theory be fed into the [Atmel fitter](atmel-fitters/).
* https://github.com/byuccl/spydrnet
* https://byuccl.github.io/spydrnet/docs/stable/index.html

# Programming / Burning and Device Information
There are a few choices on how a PLD/CPLD part can be programmed depending on whether it supports JTAG. If using JTAG, be mindful of making sure you are using a programmer with the correct voltage levels and not to unintentionally programatically disable the JTAG interface.

![A detailed overview of ways to program a given device.](PROGRAMMING.md)


# Reversing a JED file back into logic equations
Finally, if one is able to read a .JED out of a device, this can sometimes be reversed back into equations, provided the security fuse on the device has not been set. Given a .JED file, the following approaches can be taken to arrive at the equations:
* By hand, comparing the .JED file to the fusemap / macrocells in the datasheet. See this <a href="https://blog.frankdecaire.com/2017/01/22/generic-array-logic-devices/">blog post</a> by Frank DeCaire.
* `JED2EQN.EXE` - A DOS utility floating around on the internet.
* `jedutil` - MAME can be compiled with a utility called jedutil which does something similar. Sometimes it is broken out into a seperate package "mame-tools"
* Finally, brute force can be used on a PLD that is strictly combonatorial: it can be read out as though it is an EPROM by stepping through all combinations of possible inputs. In this approach, security fuses do not matter because one is not trying to read out the fusemap directly. Once state/registers are involved, this becomes much more challenging.

# Simulation
The behavior of logic equations to be programmed into a device (or even a virtual device) can be simulated with a utility called WinSim which is part of WinCUPL.

Just like WinCUPL, WinSim is an erratic front-end. Thankfully however, the simulation itself is actually performed by the CUPL compiler and this underlying functionality is solid.

Note that this is only a 'functional simulation' and not a 'timing simulation' and covered here are primarily details on WinSim/CSIM.EXE. Functional simulation is achieved using what are essentially JEDEC-style test vectors.

See the "[simulation/](simulation/)" folder for further information.

# Acknowledgments
This repository is merely a bunch of tips, tricks, helper scripts and documentation. The real work comes from:
* Whitequark for putting together <a href="https://github.com/whitequark/prjbureau">Prjbureau</a>, which documents the fusemap for these devices, provides an ability to go from a .JED file to an .SVF, documentation and more.
* Yosys
* hoglet67 for putting together <a href="https://github.com/hoglet67/atf15xx_yosys">atf15xx_yosys</a>, which shows a workflow using yosys and provides a techmap.
* ole00 for putting together [Afterburner](https://github.com/ole00/afterburner/) a modern, open-source device programmer that supports a majority of these devices
* Countless other tips, tools, contributions and from all over the web and plenty of trial-and-error working around the quirks of WinCUPL and the fitters themselves.

# References
[^1]: From the Readme.txt of fit5_0.zip (an older version of the Atmel Fitters) found here: http://ebook.pldworld.com/_semiconductors/Atmel/Databook%20CDROM/Atmel/prod147.htm
[^2]: https://www.eevblog.com/forum/beginners/5v-pal-or-gal-with-cmos-outputs/


