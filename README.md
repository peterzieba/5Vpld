# Overview
This repository centers around documenting Linux and Windows workflows for Atmel (Now Microchip) 5V GAL PLD and CPLD parts:
* ATF16V8 (Modern/active equivalent of the PAL16V8 and GAL16V8 parts)
* ![ATF22V10](vendor-datasheets/doc0735.pdf) (Modern/active equivalent of the PAL22V10 and GAL22V10 parts)
* ATF1502
* ATF1504
* ATF1508

These parts are still active and highly worth considering wherever:
* 5V logic is a requirement / avoiding level shifting
* Prototyping (reprogrammable) / Learning about Logic.
* Through-hole / soldering-friendly is desired: All parts have DIP packages or can be placed in through-hole PLCC sockets.
* Replacing large quantities of various TTL/CMOS

This is mostly a collection of documentation, but some small scripts are here that help make things easier and provide examples on how to avoid WinCUPL while still utilizing these parts:
* ![Linux Workflow (5vcomp command-line utility pointed at a .PLD file)](linux-workflow/)
* ![Windows Workflow (right-click a .PLD file and get compiled/synthesized .JED files).](windows-workflow/)

<details>
<summary>Scope: Expand here for why similar parts not covered</summary>

* 3.3V parts are not considered: There are simply better choices that are well documented. Also, the CPLD parts have VccIO inputs, so you can technically use them in 3.3V designs just as well.
* The Greekpak devices probably should be covered here, but, they're reasonably well documented with modern tools.
* Any parts that are NRND or inactive. Because there are 5V parts that are still considered active, we only consider these.
* For the ATF150x CPLD parts specifically:
  * The BE and ASV devices not covered here as they seem to be difficult to obtain and are not 5V devices. If you need 3.3V or lower, there are probably better parts suited to your needs.
</details>

<details>
<summary>Expand here for a description of how these parts compare to ladder logic on a PLC</summary>

* Each rung's output in ladder-logic can be thought of as a single macrocell.
* The inputs on a rung can be "normally open" or "normally closed" (active high or low), and can consist of any number of inputs (or even the state of another macrocell). The inputs defined on a single rung are basically equivalent to a single product-term belonging to a macrocell. There can be multiple product terms defined that activate a given macrocell.
</details>


<details>
<summary>Expand here for details on how all of these compare to FPGAs</summary>
Such parts are the spiritual predecessors of more modern FPGAs. Key differences between FPGAs and PLDs:

* FPGAs are typically constructed from a large number of LUTs (Lookup tables). CPLDs use a sum-of-products structure.
* FPGAs typically expect to have their bitstream uploaded on powerup, requiring an external EEPROM. PLDs are typically non-volatile.
* FPGAs usually support standard JTAG for programming, whereas many PLDs required specialized device programmers.
* There are likely exceptions to all of the above in some parts. These are not hard rules.
</details>

# Requirements
![See PROGRAMMING.md](PROGRAMMING.md). TL;DR:
* An EPROM/Device programmer if you wish to use the ATF16V8 or ATF22V10 parts
* A JTAG programmer for the ATF150x parts

# Terminology / Background
<a href="https://en.wikipedia.org/wiki/Programmable_logic_device">PLD/GAL</a> - Programmable Logic Device. Small, generally DIP-package 5V programmable Logic.<br />
<a href="https://en.wikipedia.org/wiki/Programmable_logic_device#CPLDs">CPLD - </a>Complex Programmable Logic Device. Larger packages, many pins, much more complex.<br />

<a href="https://en.wikipedia.org/wiki/Macrocell_array">Macrocell</a> - Each output has a macrocell associated with it. These can often be configured as active high, active low, flip-flops, etc.<br />
Product Term - Each macrocell has a number of product terms associated with it (typically around 5). A product term is essentially a giant AND gate with inputs to each pin on the device. Burning away fuses allows selecting which inputs are fed into this AND gate, ultimately selecting the conditions required for a product term to be activated. Product terms belonging to the same output macrocell are then combined into an OR gate before being fed into the macrocell. This means that there can be several combination of inputs that allow a given macrocell to be triggered. This architecture is called a Sum-of-Products logic array.

<a href="https://en.wikipedia.org/wiki/Programmable_Array_Logic#CUPL">CUPL</a> - A early (1983) programming language used to define the behavior of digital logic gates. "Compiler for Universal Programmable Logic.", is essentially a predecessor to languages like Verilog/VHDL. CUPL.EXE is the compiler which is used to compile .PLD files written in CUPL, ultimately to be burned into programmable logic devices.<br />
<a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">WinCUPL</a> - A Windows front-end/IDE to the CUPL compiler and related programs. It is still part specifically that we are trying to avoid, while keeping everything else underneath/around it as it is buggy.<br />
.dl File - Device Library File. This file determines what devices CUPL has the ability to compile for.<br>
.cat File - A text file corresponding to a .dl device library file with the same name and containing a list of supported devices by CUPL.

<a href="https://en.wikipedia.org/wiki/Netlist">Netlist</a> - A netlist is essentially an electrical schematic in a text file which defines connections. For the purposes here, it is an intermediary file format (Either EDIF or Berkeley PLA), which is used to describe the behavior of logic ultimately fed into the fitter.<br />
<a href="">.TT2</a> - The Berkeley PLA file format. An intermediary file which CUPL.EXE can generate that can be used by the Atmel fitters.<br />
<a href="https://en.wikipedia.org/wiki/EDIF">EDIF</a> - Another type of netlist format which is also usable by the Atmel fitters. Yosys is capable of generating this format, however, one will still need a techmap.<br />
<a href="https://en.wikipedia.org/wiki/Place_and_route">Fitter</a> - A fitter converts a netlist into the fusemap (.JED) file. Fitters are needed for the ATF150x CPLD devices. In more modern parlance, this is basically place & route.<br />
.STD File - In the context of a fitter, the primitive/device library for PLA. This file is part of the Atmel ATF150x fitters.<br />
.LIB File - In the context of a fitter, the primitive/device library for EDIF. This file is part of the Atmel ATF150x fitters.

<a href="https://archive.org/details/JEDECJESD3C/mode/2up">.JED/JEDEC File</a> - A fuse map intended to be "burned/programmed" into a logic device.


.SVF File - Serial Vector Format. Generated from the .JED file, the .SVF can be used by any JTAG programmer (vendor-independent) to program a device that has a JTAG interface.<br />
CSIM - A tool for simulating the behavior of logic. This takes an .SI file and produces an .SO file. This is not concerned with timing, but simply logic states.


<a href="https://www.winehq.org/">Wine</a> - Wine is not an emulator. Allows running Windows programs under Linux.<br />


# Writing logic for these parts: Possible Workflows
Each of the subsections here represents a potential workflow to design logic equations for these parts. The majority of the focus will be on methods that avoid WinCUPL (which is ultimately just an IDE/text-editor that calls CUPL.EXE).

Some of the other approaches covered here also avoid the CUPL compiler as well and instead generate netlists provided directly to the device fitter.

Finally, a word on preferred approach, given the options: Using the CUPL.EXE compiler via command line or Quartus are probably the best ways, especially if you are interested in using Hi-Z states. Neither Yosys nor Digital seemed to have robust support for Hi-Z states (important for Bidirectional I/O). If that is important to you, you may want to stick with either Quartus or the CUPL command line methods.

This diagram is from the help files built into WinCUPL which shows how one can go from a CUPL .PLD into the .JED files needed to program a device.

![WinCUPL Data Flow Diagram](vendor-docs/WinCUPL-data-flow-diagram.png)

## Old Approach: WinCUPL
While logic for these parts can be written using the WinCUPL IDE, the experience may be fraught with difficulty as it is somewhat unstable and requires Windows. It does however have value in the help files / documentation / examples. Furthermore, it should be noted that the CUPL compiler itself is actually pretty solid/stable. So, the recommended approach is to install and use it for documentation/examples and then simply avoid it for serious work by using the command line CUPL.EXE (perhaps through the helper scripts in this repository).

You can <a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">Download WinCUPL from here</a>.

To get it working under Linux with Wine, you'll need winetricks so you can install mfc40 and mfc42. On Ubuntu Linux, this would look something like:

<code>sudo apt-get install wine winetricks playonlinux
winetricks mfc40 mfc42
</code>

Furthermore, if you are intending on working with the ATF150x parts, you should probably grab the newer fitters out of the Atmel Prochip package. The utilities in this repository will refuse to work without them.

## Command line approach: CUPL & Your favorite text editor or IDE.
This is probably the most solid approach assuming you are OK with using CUPL as a language. This approach can operate on both Linux and Windows without trouble. You should start with the WinCUPL approach as a prerequisite to getting the CUPL compiler and the examples/help files.
Since WinCUPL simply is a front-end / IDE on top of the CUPL.EXE compiler and related programs, one can write the desired logic in CUPL, save it in a .PLD file using their favorite editor and have CUPL.EXE compile it into a .JED file for programming into a PLD. CPLD parts will require the additional step of using a fitter for the specific device to produce the .JED file.

![A detailed User's Guide to CUPL in PDF](vendor-docs/CUPL_USERS_GUIDE.pdf)


Run CUPL using the following command line format:

<code>cupl [-flags] [library] [device] source</code>


Examples run under Wine would look like this:

<code>wine c:/Wincupl/Shared/cupl.exe -m1jn -u c:/Wincupl/Shared/cupl.dl your-code.PLD</code>

WARNING: Limit your the length of your filenames to 15 characters before the file extension (19 characters total) and do not allow multiple periods in the filename. Otherwise, CSIM.EXE seems to throw an error in the .SO file along the lines of <code>[0001sa] could not open:  terrible-long-fn....H.jed</code>

Additionally, if you are targeting a CPLD (ATF150x) for which CUPL.EXE does not have direct support, you will need to run:

<code>wine c:/Wincupl/WinCupl/Fitters/fit1502.exe -i your-code.tt2 -dev P1502T44 -DEBUG on -Verilog_sim VERILOG -Out_Edif ON</code>

The above example is for an ATF1502 in a TQFP-44 package. You will need to use the appropriate fitter and device type for your particular CPLD.

Additionally, you may want to explore the following environment variables:<br />
<code>FITTERDIR=C:\Wincupl\Wincupl\Fitters
LIBCUPL=c:\Wincupl\Shared\atmel.dl
</code>

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

<details>
<summary>Expand here if you are interested in using VS Code as an IDE</summary>
 
Recently, two different extensions for VS Code for CUPL have been written:
* https://marketplace.visualstudio.com/items?itemName=tlgkccampbell.code-cupl
  * This one handles just syntax highlighting for CUPL .PLD files
* https://marketplace.visualstudio.com/items?itemName=VaynerSystems.VS-Cupl
  * This is an entire workflow, which has a bit more functionality beyond just syntax highlighting.
</details>

<details>
<summary>Expand here for a list of devices Atmel WinCUPL supports</summary>
 
* CBLD.EXE will allow you to see a list of devices that are supported within the CUPL.DL device library.
* Atmel WinCUPL is limited Atmel devices, however, other versions of CUPL found elsewhere will have parts from a broader array of manufacturers.

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
<summary>Expand for command line options for the latest known version of the ATF1502.EXE fitter.</summary>
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

<details>
<summary>Expand here for a list of devices the version of CUPL provided by PLDmaster of Logical Devices, Inc. supports</summary>

<code>

wine ./cbld.exe -l -u pldmstr.dl
CBLD(PM): CUPL Device Library Management Program
Version 5.0a
Copyright (c) 1983, 1998 Logical Devices, Inc.
pldmstr.dl  rev:DLIB-h

Device        Rev   Pins  Fuses  Pterms
------------  ---   ----  -----  ------
ep300          21    20    2720     74
ep320          02    20    2916     72
ep312          07    24   13713    200
ep600          14    24    6482    160
27c64dip       01    28       0   8192
27c64plcc      01    32       0   8192
27c128dip      01    28       0   16384
27c128plcc     01    32       0   16384
27c256dip      01    28       0   32768
27c256plcc     01    32       0   32768
g16v8          09    20    2194     64
g16v8a         03    20    2194     64
g16v8as        02    20    2194     64
g16v8ma        08    20    2194     64
g16v8ms        11    20    2194     64
g16v8s         09    20    2194     64
g20v8          03    24    2706     64
g20v8s         02    24    2706     64
g20v8ma        03    24    2706     64
g20v8ms        03    24    2706     64
g20v8a         02    24    2706     64
g20v8as        01    24    2706     64
g22v10         01    24    5892    132
p10h8          07    20     320     16
p10l8          07    20     320     16
p10p8          07    20     328     16
p10p8v         01    20     664     32
p12h6          09    20     384     16
p12l6          07    20     384     16
p12p6          07    20     390     16
p12p6v         01    20     786     32
p12l10         07    24     480     20
p12p10         07    24     490     20
p14h4          07    20     448     16
p14l4          07    20     448     16
p14p4          07    20     452     16
p14p4v         01    20     908     32
p14l8          07    24     560     20
p14p8          09    24     568     20
p16c1          07    20     512     16
p16h2          07    20     512     16
p16l2          07    20     512     16
p16p2          07    20     514     16
p16p2v         01    20    1030     32
p16r4          11    20    2048     64
p16rp4         15    20    2056     64
p16rp4v        01    20    2072     64
p16l6          07    24     640     20
p16p6          07    24     646     20
p16r6          14    20    2048     64
p16rp6         15    20    2056     64
p16rp6v        01    20    2072     64
p16h8          08    20    2048     64
p16hd8         06    20    2048     64
p16l8          08    20    2048     64
p16ld8         06    20    2048     64
p16n8          01    20     512     16
p16p8          08    20    2056     64
p16p8h         07    20    2056     64
p16p8v         01    20    2072     64
p16r8          10    20    2048     64
p16rp8         14    20    2056     64
p16rp8v        01    20    2072     64
p18l4          07    24     720     20
p18p4          07    24     724     20
p20c1          07    24     640     16
p20l2          07    24     640     16
p20p2          07    24     642     16
p20r4          10    24    2560     64
p20rs4         21    24    3330     80
p20r6          10    24    2560     64
p20l8          08    24    2560     64
p20p8          01    24    2568     64
p20r8          09    24    2560     64
p20rs8         19    24    3338     80
p20l10         06    24    1600     40
p20rs10        19    24    3338     80
p20s10         17    24    3322     80
p22v10         17    24    5828    132
ra5p8          04    16     256     32
ra5p16         02    24     512     32
ra6p16         02    24    1024     64
ra8p4          04    16    1024    256
ra8p8          04    20    2048    256
ra9p4          04    16    2048    512
ra9p8          04    20    4096    512
ra10p4         04    18    4096   1024
ra10p8         04    24    8192   1024
ra11p4         04    18    8192   2048
ra11p8         04    24   16384   2048
ra12p4         04    20   16384   4096
ra12p8         04    24   32768   4096
ra13p8         04    24   65536   8192
virtual        01   200   99999   5000
ep312lcc       01    28   13713    200
ep600lcc       14    28    6482    160
g20v8lcc       03    28    2706     64
g20v8malcc     03    28    2706     64
g20v8mslcc     03    28    2706     64
g20v8slcc      03    28    2706     64
g20v8alcc      02    28    2706     64
g20v8aslcc     01    28    2706     64
g22v10lcc      02    28    5892    132
p12l10lcc      07    28     480     20
p12p10lcc      07    28     490     20
p12l10mlcc     08    28     480     20
p14l8lcc       07    28     560     20
p14p8lcc       09    28     568     20
p14l8mlcc      08    28     560     20
p16r4alcc      02    28    2048     64
p16l6lcc       07    28     640     20
p16p6lcc       07    28     646     20
p16l6mlcc      08    28     640     20
p16l8alcc      01    28    2048     64
p16r6alcc      01    28    2048     64
p16l8          08    20    2048     64
p16r8alcc      01    28    2048     64
p18l4lcc       07    28     720     20
p18p4lcc       07    28     724     20
p18l4mlcc      08    28     720     20
p20c1lcc       07    28     640     16
p20c1mlcc      08    28     640     16
p20l2lcc       07    28     640     16
p20r4lcc       11    28    2560     64
p20rs4lcc      21    28    3330     80
p20r4mlcc      11    28    2560     64
p20rs4mlcc     22    28    3338     80
p20r6lcc       11    28    2560     64
p20r6mlcc      11    28    2560     64
p20l8lcc       09    28    2560     64
p20p8lcc       01    28    2568     64
p20r8lcc       10    28    2560     64
p20l8mlcc      09    28    2560     64
p20l10lcc      06    28    1600     40
p20rs10lcc     19    28    3338     80
p20s10lcc      17    28    3322     80
p20rs10mlcc    20    28    3338     80
p20s10mlcc     17    28    3322     80
p22v10lcc      17    28    5828    132
v750           03    24   14394    171
v750b          02    24   14435    171
v750c          02    24   14504    171
v750cext       02    24   14504    171
v750cextppk    02    24   14504    171
v750cppk       02    24   14504    171
v2500          07    40   71648    416
v2500b         04    40   71745    416
v5000          02    68   163164   1232
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
f1508plcc68    02    68   15360    320
f1508ispplcc68   02    68   15360    320
f1508ispplcc84   02    84   15360    320
f1508plcc84    02    84   15360    320
f1508ispqfp100   02   100   15360    320
f1508qfp100    02   100   15360    320
f1508tqfp100   02   100   15360    320
f1508isptqfp100   02   100   15360    320
f1508pqfp160   01   160   15360    320
f1508isppqfp160   01   160   15360    320
ep324          05    40   47493    394
ep900          07    40   17402    240
ep1200         03    40   15146    236
ep1800         11    68   42490    480
p7b336         01    28     384     16
p7b337         01    28     768     32
p7b338         01    28     384     16
p7b339         01    28     768     32
p7c330         05    28   17082    258
p7c331         07    28   11934    216
p7c332         02    28    9902    194
p7c335         01    28   17082    258
xl78c800       01    24    6400     66
c258           01    28   32768   2048
c259           01    44   32768   2048
c330           01    28   17082    258
c331           01    28   11934    216
c332           01    28    9902    194
c335           01    28   17082    258
c336           01    28     384     16
c337           01    28     768     32
c338           01    28     384     16
c339           01    28     768     32
f100           10    28    1928     48
f103           09    28     297      9
f105           21    28    3553     48
f151           13    20     564     15
f153           11    20    1842     42
f155           14    20    2108     43
f157           15    20    2108     43
f159           19    20    2108     43
f161           14    24    1544     48
f162           07    24     165      5
f163           07    24     225      9
f167           23    24    3361     48
f168           05    24    3553     48
f173           01    24    2178     42
f179           03    24    2452     43
f253           01    20    2378     42
f273           02    24    2714     42
f405           06    28    5410     64
f415           03    28    5751     68
f473           03    24    1499     24
f501           02    52   15780    112
f502           01    68   23464    144
f506           06    24   10680     98
f507           05    24    7370     80
f529           01    20     128      8
f839           09    24    1094     32
f30k12         02    28    7424     72
f30s16         02    28    7236     71
f42va12        05    24    8994    105
f48n22         01    68    7008     73
f9800          02    20    1830     45
f7024          02    24   14088     80
f7128          02    28    8488     68
f7140          02    40   22103    120
f2552          01    68   51624    226
f2852          01    84   51624    226
f16v8          02    20    2617     72
f16v8d         02    20    2617     72
f16v8s         02    20    2617     72
f18v8z         07    20    2689     72
f18v8zd        07    20    2689     72
f18v8zs        07    20    2689     72
f20v8          03    24    3193     72
f20v8d         03    24    3193     72
f20v8s         03    24    3193     72
g16v8h         04    24    2226     64
g16v8hs        04    24    2226     64
g16v8hma       04    24    2226     64
g16v8hms       04    24    2226     64
g16v8cpms      01    20    2195     64
g16v8cp        01    20    2195     64
g16v8cpas      01    20    2195     64
g16v8cpma      01    20    2195     64
g16v8c         01    20    2194     64
g16v8cas       01    20    2194     64
g16v8cma       01    20    2194     64
g16v8cms       01    20    2194     64
g16vp8         01    20    2202     64
g16vp8s        01    20    2202     64
g16vp8ma       01    20    2202     64
g16vp8ms       01    20    2202     64
g16z8          03    24    2195     64
g16z8ma        03    24    2195     64
g16z8ms        03    24    2195     64
g16z8s         03    24    2195     64
g18v10         01    20    3540     96
g20vp8         01    24    2714     64
g20vp8s        01    24    2714     64
g20vp8ma       01    24    2714     64
g20vp8ms       01    24    2714     64
g20xv10        03    24    1671     40
g20xv10i       03    24    1671     40
g20xv10f       03    24    1671     40
g20ra10        03    24    3274     80
g22v10i        02    28    5892    132
gds22          01    28     219     11
g22v10cp       01    24    5893    132
g24v10         02    28    3492     80
g24v10ma       02    28    3942     80
g24v10ms       02    28    3942     80
g24v10s        02    28    3942     80
g26cv12        03    28    6432    120
g6001          15    24    8294     75
g6002          04    24    8330     75
mach110        04    44    6504    140
mach111        02    44    6504    140
mach120        04    68   12080    216
mach130        03    84   15552    280
mach131        01    84   15552    280
mach210        04    44   12832    280
mach211        02    44   12832    280
mach215        04    44   11936    256
mach220        05    68   23232    416
mach221        05    68   23232    416
mach231        03    84   30144    544
mach355        01   144   43740    480
mach435        03    84   54096    720
mach445        01   100   54129    720
mach446        01   100   54129    720
mach465        01   208   121185   1440
m16v8a         01    20    3136     64
m16v8as        01    20    3136     64
m16v8ac        01    20    3136     64
m16v8ar        01    20    3136     64
p1012c4        01    24    2056     32
p1016c4        01    28    2056     32
plsi1016ld4    03    24    2056     64
p1016lm4       02    24    2056     32
p1016p4        01    24    2056     32
p1016rd4       03    24    2056     64
p1016rm4       02    24    2056     32
p1016et6       01    24    1542     48
p1016ld8       03    24    2056     64
p1016p8        02    24    2056     64
p1016pe8       01    28    2056     64
p1016rd8       03    24    2056     64
p1020rp4       01    28    2568     32
p1020eg8       04    24    3616     80
p1020ev8       06    24    3616     90
p1020g8        02    24    1352     32
p1020p8        06    24    1352     32
p6l16          02    24     192     16
p8l14          02    24     224     16
p14r21         01    24    3137     86
p16p4c         01    24    2056     32
p16rsp4        01    20    2176     64
p16rsp6        01    20    2180     64
p16p8c         01    24    2056     64
p16ra8         05    20    2056     64
p16rsp8        01    20    2184     64
p16sp8         01    20    2168     64
p18cv8         02    20    2696     74
p18g8          01    20    2624     72
p18n8          01    20     304      8
p18p8          03    20    2600     72
p18u8          02    20    2688     72
p18v8          01    20    2752     74
p19r4r         06    24    2443     64
p19r4t         02    24    2443     64
p19r6r         06    24    2443     64
p19r6t         02    24    2443     64
p19l8r         07    24    2443     64
p19l8t         02    24    2443     64
p19r8r         06    24    2443     64
p19r8t         02    24    2443     64
p20rp4         01    24    2568     64
p20rp4a        02    24    3450     86
p20rsp4        01    24    2688     64
p20x4          11    24    1600     40
p20xrp4        02    24    3450     86
p20rp6         01    24    2568     64
p20rp6a        03    24    3370     84
p20rsp6        01    24    2692     64
p20xrp6        01    24    3370     84
p20rp8         01    24    2568     64
p20rp8a        04    24    3290     82
p20rsp8        01    24    2696     64
p20sp8         01    24    2680     64
p20x8          12    24    1600     40
p20xrp8        01    24    3290     82
p20cg10        02    24    4088     92
p20g10         03    24    3990     90
p20ra10        15    24    3210     80
p20rp10a       02    24    3210     80
p20x10         08    24    1600     40
p20xrp10       01    24    3210     80
p22cv10z       02    24    5873    132
p22ip6         01    24    3294     72
p22p10a        02    24    3970     90
p22rx8         05    24    3616     82
p22v10s        03    24    6657    132
p22vp10        05    24    5838    132
p22xp10        02    24    3970     90
p23s8          06    20    6234    135
p23sv8         01    20    6242    135
p24r4          01    28    3840     80
p24r8          01    28    3840     80
p24l10         02    28    3840     80
p24r10         02    28    3840     80
p26v12         04    28    7848    150
p29m16         14    24   11040    188
p29ma16        15    24   10460    188
p32r16         12    40    8466    128
p32vx10        10    24    9738    152
p64r32         16    84   33316    256
pc224          01    24    3204     72
pc508          02    28     256      8
pc960          01    28     256     16
pld9000        09   100   58104    200
plx448         13    24    5116     98
virtual        01   200   99999   5000
v750lcc        07    28   14394    171
v750blcc       02    28   14435    171
v750clcc       02    28   14504    171
v750cextlcc    02    28   14504    171
v750cextppklcc   02    28   14504    171
v750cppklcc    02    28   14504    171
v2500lcc       08    44   71648    416
v2500blcc      04    44   71745    416
ep324lcc       03    44   47493    394
ep900lcc       08    44   17402    240
f167lcc        23    28    3361     48
f168lcc        05    28    3553     48
f173lcc        01    28    2178     42
f179lcc        03    28    2452     43
f473lcc        03    28    1499     24
f506lcc        06    28   10680     98
f507lcc        05    28    7370     80
f42va12lcc     01    28    8994    105
f7024lcc       01    28   14088     80
f7128lcc       01    28    8488     68
f7140lcc       01    44   22103    120
g16v8hlcc      03    28    2226     64
g16v8hslcc     03    28    2226     64
g16v8hmalcc    03    28    2226     64
g16v8hmslcc    03    28    2226     64
g16z8lcc       03    28    2195     64
g16z8malcc     03    28    2195     64
g16z8mslcc     03    28    2195     64
g16z8slcc      03    28    2195     64
g20vp8lcc      01    28    2714     64
g20vp8slcc     01    28    2714     64
g20vp8malcc    01    28    2714     64
g20vp8mslcc    01    28    2714     64
g20xv10lcc     03    28    1671     40
g20xv10ilcc    03    28    1671     40
g20xv10flcc    03    28    1671     40
g20ra10lcc     02    28    3274     80
g22v10cplcc    01    28    5893    132
g6001lcc       15    28    8294     75
g6002lcc       04    28    8330     75
p1016ld4lcc    01    28    2056     64
p1016rd4lcc    01    28    2056     64
p1016et6lcc    01    28    1542     48
p1016rd8lcc    01    28    2056     64
p1020eg8lcc    04    28    3616     80
p1020ev8lcc    06    28    3616     90
p1020g8lcc     02    28    1352     32
p1020p8lcc     06    28    1352     32
p16p4clcc      01    28    2056     32
p16p8clcc      01    28    2056     64
p19r4rlcc      06    28    2443     64
p19r4tlcc      02    28    2443     64
p19r6rlcc      06    28    2443     64
p19r6tlcc      02    28    2443     64
p19l8rlcc      07    28    2443     64
p19l8tlcc      02    28    2443     64
p19r8rlcc      06    28    2443     64
p19r8tlcc      02    28    2443     64
p20rp4lcc      01    28    2568     64
p20rp4alcc     02    28    3450     86
p20rsp4lcc     01    28    2688     64
p20x4lcc       11    28    1600     40
p20xrp4lcc     02    28    3450     86
p20x4mlcc      12    28    1600     40
p20rp6lcc      01    28    2568     64
p20rp6alcc     03    28    3370     84
p20rsp6lcc     01    28    2692     64
p20xrp6lcc     01    28    3370     84
p20rp8alcc     04    28    3290     82
p20rs8lcc      19    28    3338     80
p20rsp8lcc     01    28    2696     64
p20sp8lcc      01    28    2680     64
p20x8lcc       12    28    1600     40
p20xrp8lcc     01    28    3290     82
p20x8mlcc      13    28    1600     40
p20cg10lcc     02    24    4088     92
p20g10lcc      04    28    3990     90
p20ra10lcc     15    28    3210     80
p20rp10alcc    02    28    3210     80
p20x10lcc      08    28    1600     40
p20xrp10lcc    01    28    3210     80
p20g10mlcc     03    28    3990     90
p20ra10mlcc    15    28    3210     80
p20ra10slcc    15    28    3210     80
p20rp8lcc      01    28    2568     64
p20x10mlcc     09    28    1600     40
p22p10alcc     02    28    3970     90
p22rx8lcc      05    28    3616     82
p22cv10lcc     02    28    5838    132
p22v10tlcc     01    28    5828    132
p22v10slcc     03    28    6657    132
p22vp10lcc     05    28    5838    132
p22xp10lcc     02    28    3970     90
p29m16lcc      14    28   11040    188
p29ma16lcc     15    28   10460    188
p32r16lcc      12    44    8466    128
p32vx10lcc     10    28    9738    152
p64r32pga      16    88   33316    256
pc224lcc       02    28    3204     72
</code>
</details>

Other people's workflows:
* https://github.com/willie68/WCPLD
* https://github.com/Manawyrm/PAL-GAL-CI

## Absurd approach: Fusemaps by hand
* See this <a href="https://blog.frankdecaire.com/2017/01/22/generic-array-logic-devices/">blog post</a> by Frank DeCaire.


While not the easiest approach, just as one can write G-Code in notepad or Assembly code in a hex editor, manually creating a fusemap is technically possible. This assumes that you have a datasheet for your device which has a description of the fusemap and the details of how the macrocells work. With this in hand, one could write a JEDEC file with the desired functionality and a text editor. This would be non-trivial and error-prone, but it demonstrates that such a thing could be done, at least with the older PLDs (16V8, 22V10), and even with the ATF750 (some datasheets actually had the fusemap for this part).


It is worth noting that the fusemap for the ATF150x parts has been recently documented in <a href="https://github.com/whitequark/prjbureau">prjbureau</a>. Given the complexity of these devices over PLDs, writing a fusemap by hand for these parts would probably be a bad idea.

## Other languages: ABEL, PALASM (ancient)
Since we're mostly covering modern approaches to these devices here, these will only be covered very briefly:
* ABEL: "Advanced Boolean Expression Language" was created in 1983 by Data I/O Corporation.
* PALASM: Introduced by Monolithic Memories, Inc. (MMI) in the 1980's
  * A modern version of this is called <a href="https://github.com/daveho/GALasm">GALASM</a> which is a continuation of something called GALer. This might be worth considering if you are happy with just PLDs.

## Atmel Prochip (Not Free, Verilog/VHDL support)
![PDF: Example Verilog Design flows with using ProChip 5.0.1](vendor-docs/CPLD_Mentor_Verilog_tutorial[1].pdf)<br />
Atmel Prochip is not free, however, you can <a href="https://ww1.microchip.com/downloads/en/DeviceDoc/ProChip5.0.1.zip">download it from here</a>, and may be able to <a href="https://www.microchip.com/prochiplicensing/#/">request a trial license from Microchip</a>. This workflow supports Verilog/VHDL, which is great if one wants to move away from CUPL entirely and can afford to purchase a license.

This packages is worth downloading regardless because there are newer fitters for the ATF150x devices that can be extracted from this installation, and these fitters are required in every other approach mentioned here. The newer versions of the fitters should mention version 1918 (3-21-07) when invoked from a command line. (The fitters that come with WinCUPL are old and should be replaced with the ones from this package.
## Quartus (Free, Verilog, VHDL, Schematic Capture). Indirect support for ATF150x.
* It turns out that the Altera (Now Intel) <a href="https://www.intel.com/content/www/us/en/software-kit/711791/intel-quartus-ii-web-edition-design-software-version-13-0sp1-for-windows.html?">Quartus 13.0sp1</a> can be used to produce a .POF file targeting various CPLD chips made by Altera in the MAX EPM3K/EPM7K series, which can be converted to target an ATF150x device.
* The resulting .POF file can be converted using a utility called <a href="http://ww1.microchip.com/downloads/archive/pof2jed.zip">POF2JED</a> from Atmel (Now Microchip). This is further detailed in <a href="http://ww1.microchip.com/downloads/en/AppNotes/DOC0916.PDF">this application note.
* Important!: Newer versions of Quartus will not work. v13.0sp1 last version that had support for the MAX EPM3K/EPM7K chips. Support for these chips has been removed from newer versions of Quartus. You MUST use the old version.

## Digital (free, use schematics instead of logic equations / programming)
"Digital is an easy-to-use digital logic designer and circuit simulator designed for educational purposes." This is an interesting option as one can create a schematic and have a .JED file generated for a GAL16V8 or GAL22V10. If one provides the fitters to Digital, it can produce .JED files for the ATF150x series as well.
https://github.com/hneemann/Digital

## Yosys (Open Source with Atmel Fitters, experimental)
In theory, one can use Yosys Open SYnthesis Suite (Yosys) with the help of the Atmel Fitters a specific CPLD and a techmap to produce .JED files. This is a bit more experimental, but some have managed to make this work. This allows an almost entirely open-source workflow using Verilog, and probably <a href="https://icestudio.io/">Icestudio</a> if one prefers schematic capture as well. A good place to start would be using the <a href="https://github.com/YosysHQ/oss-cad-suite-build">OSS CAD Suite</a> to get the big parts of the suite set up. After that, there are two approaches to making this work:
* https://github.com/whitequark/prjbureau
  * prjbureau demonstrates going from RTLIL to a .JED file
* https://github.com/hoglet67/atf15xx_yosys/
  * This example goes from plain old verilog into a .JED file by implementing a techmap.

# Programming / Burning and Device Information
There are a few choices on how the part can actually be programmed depending on whether it supports JTAG.

![A detailed overview of ways to program a given device.](PROGRAMMING.md)


# Reversing a JED file back into logic equations
Finally, if one is able to read a .JED out of a device, this can sometimes be reversed back into equations. These devices all have security fuses, however, which can disable any ability to read out the device. Given a .JED file, the following approaches can be taken to arrive at the equations:
* By hand, comparing the .JED file to the fusemap / macrocells in the datasheet. See this <a href="https://blog.frankdecaire.com/2017/01/22/generic-array-logic-devices/">blog post</a> by Frank DeCaire.
* JED2EQN.EXE - A DOS utility floating around on the internet.
* MAME can be compiled with a utility called jedutil

# Simulation
CSIM.EXE can be fed test vectors and be used to simulate the behavior of a particular chip, or even a virtual device. The following things are required to do this successfully:
* You must create an .SI file containing the desired test vectors.
* Provide an "Absolute file". The .ABS file is generated by CUPL.EXE when the -a flag is passed to it. This generates a binary file based on the logic equations from the source CUPL .PLD file.
CSIM will then generate a .SO output file, and optionally append test vectors to an existing .JED file for testing purposes.
<details>
<summary>Expand here for command-line options to CSIM.EXE</summary>
<code>csim [-flags] [library] [device] source
where
-flags is the following set of simulator options:
-l create listing file.
-j append test vectors to JEDEC file.
-n use source filename for JEDEC file.
-v display simulation results to terminal.
-u use specified library for simulation.
library is the library name and path name if the -u flag is being used to specify a
library other than the default library.
device must be the same device mnemonic as was used in the CUPL compilation.
Specifying the device is optional; if a device is not specified, CSIM uses the device
CUPL compiled (contained in the .ABS file).
source is the user-created ASCII test specification file (filename.SI). The
extension .SI is assumed for the source file and may be omitted when giving the
CSIM command.</code>
</details>


Creating a .SI file:<br />
* An .SI file should have the same header information as the original .PLD source file. If not, this will generate warnings.
* Comments begin with a /* and end with a */
* An .SI file can have the following keywords/statements: ORDER, BASE, and VECTORS
  * The ORDER keyword is used to list the variable / inputs and outputs to be used in the simulation table, and to define how they are displayed. Typically, the variable names are the same as those in the corresponding CUPL logic description file.
  * The BASE keyword specifies a number base. Hexadecimal is the default if unspecified.
  * The VECTORS keyboard specifies a list of test vectors (signals that are applied and expected outputs).
* If you simply want to see what will happen on the outputs rather than setting a pre-determined expected value, set the outputs to *

<details>
<summary>Expand for a list of valid Test Values used in a test vector</summary>
<code>0 Drive input LO (0 volts) (negate active-HI input)
1 Drive input HI (+5 volts) (assert active-HI input)
C Drive (clock) input LO, HI, LO
K Drive (clock) input HI, LO, HI
L Test output LO (0 volts) (active-HI output negated)
H Test output HI (+5 volts) (active-HI output asserted)
Z Test output for high impedance
X Input HI or LO, output HI or LO Note: Not all device programmers treat X on inputs the same; some put it to 0, some allow input to be pulled to 1, and some leave it at the previous value.
N Output not tested
P Preload internal registers (value is applied to !Q output)
* Outputs only -simulator determines test value and substitutes in vector
' ' Enclose input values to be expanded to a specified BASE (octal, decimal, or hex). Valid values are 0-F and X.
“ ” Enclose output values to be expanded to a specified BASE (octal, decimal, or hex.) Valid values are 0-F, H, L, Z, and X.
</code>
</details>
