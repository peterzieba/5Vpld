# Overview
This directory only applies to the ATF150x CPLD parts.

Fitting, perhaps more commonly known as "place and route" is the stage that translates the logic into the physical hardware available on a given device.

Most simple devices in WinCUPL do not use an external fitter executable -- The CUPL compiler directly produces a .JED file for these using only its device library.

The following CPLD devices are unique in that they require fitters that are provided by Atmel and bundled with Atmel WinCUPL in order to ultimately produce a .JED file:
* ATF1500
* ATF1502
* ATF1504
* ATF1508

Note that these are not part of WinCUPL or the CUPL compiler per-se, but rather they are executables which are supplied by Atmel and bundled with the Atmel WinCUPL package.

Additionally, the fitters included with WinCUPL are fairly outdated and so the `5vcomp` script in this repository is very adamant that they be replaced with those found in the [Atmel Prochip 5.0.1](https://ww1.microchip.com/downloads/en/DeviceDoc/ProChip5.0.1.zip)

When compiling a `.PLD` file, CUPL generates a `.TT2` PLA netlist and provides it to the specific fitter for that device, which then transforms it into a `.JED` fusemap. Fitters ultimately determine the optimal way to utilize the resources of the device and are responsible for the final implementation of the logic in hardware.

The fitter also has control over various low-level, device-specific options which WinCUPL/CUPL would not have direct knowledge of, but which nonetheless can be specified inside of a <code>.PLD</code> design file using the <code>PROPERTY</code> statement, allowing them to be passed down to the fitter.

```
  PROPERTY <manuf ID> { property statement };
```

As an example of generally desirable options, the following would leave the JTAG pins enabled (allowing future reprogramming via JTAG), enable the weak pullups on the TMS/TDI pins, and make pin assignments from the .PLD design file mandatory:
```
PROPERTY ATMEL { jtag=on }; /* This keeps the JTAG pins on after programming */
PROPERTY ATMEL { TMS_pullup=on };
PROPERTY ATMEL { TDI_pullup=on };
PROPERTY ATMEL { Preassign=keep }; /* This forces the Atmel Fitter to use the pin assignments you specify. */
```

In instances where one would prefer the fitter handle the pin assignments <code>Preassign=ignore</code>, it can be useful to take pin mappings that have been autoassigned by the fitter and backannotate them into the .PLD file. The <code>backpin.exe</code> utility performs this function. One should probably change to <code>Preassign=keep</code> to make these stick across future compilations.

A [Manual for the Atmel Fitters](https://www.microchip.com/content/dam/mchp/documents/FPGA/pld-design-resources/ATF15xx%20Fitter%20Manual.zip) is available on Microchip's website. Note that these fitters are integrated into software packages beyond just WinCUPL, and so the manual has references to Atmel Prochip, ABEL, Atmel Synario, Protel, etc.

Since these fitters ultimately process a netlist, one could in theory use these fitters in any environment that is capable of sending a netlist to them, which would allow workflows that do not involve CUPL entirely for the ATF150x parts. If such a thing sounds interesting, you might want to have a look at the primitive libraries found in: `ATMEL.STD`(for PLA) and `APRIM.LIB` (for EDIF). Be warned that while the EDIF format is a standard, the details of the implemetation may not be consistent or compatible across software in practice.

<details>
<summary>Expand for command line options for the latest known version (1918 3-21-07) of the ATF1502.EXE fitter.
Options are essentially identical for the ATF1504 and ATF1508 devices.</summary>

```
Atmel ATF1502 Fitter Version 1918 (3-21-07)
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
````

Advanced help options:
```
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
```
</details>


ATF1502, ATF1504, ATF1508 fitter versions
 * WinCUPL: v 1.8.7.8 (02-05-03)
 * ProChip: 1918 (3-21-07)

<details>
<summary>Expand here for details about the ATF1500 or the ATF2500 (not recommended)</summary>
 ATF1500 Fitter Versions<br>

 While the ATF1500 is not recommended for use (No JTAG, expensive), details are covered here for completeness.<br>

 Note that the version of the ATF1500 fitter included in WinCUPL is actually newer than the version in Atmel Prochip, and so it should not be replaced. Furthermore, the Atmel Prochip version of this fitter fails to run on 64-bit machines.:<br>
  * WinCUPL: v 2.42 Jul 14 2003
  * ProChip: v 2.41 Nov 18 1997

ATF2500 fitter<br>
While Atmel Prochip seems to include a fitter for this chip, WinCUPL does not seem to require a fitter. It is probably best forgotten about. Furthermore, it does not appear to run on 64-bit machines.
</details>

# In this folder
> 
> <code>README.md</code> - This file.
> 
> <code>showargs*</code> - Simple executable and source code for a Windows executable that was briefly used for determining what arguments WinCUPL was passing to the fitters.
>
> <code>Atmel-ATF1500-tshirt.webp</code> - A picture of what is perhaps the most incredible bit of programmable logic history.
>
> [fitter15xx.pdf](fitter15xx.pdf) - A manual for the Atmel Fitters.
>
> [fitter.pdf](fitter.pdf) - A manual for the Atmel Fitters.
