# Overview
Fitting, perhaps more commonly known as "place and route" is the stage that translates the logic into the physical hardware available on a given device.

Most simple devices in WinCUPL do not use an external fitter executable -- The CUPL compiler directly produces a .JED file for these using only its device library.

The following CPLD devices are unique in that they require fitters that are provided by Atmel and bundled with Atmel WinCUPL in order to ultimately produce a .JED file:
* ATF1500
* ATF1502
* ATF1504
* ATF1508

Note that these are not part of WinCUPL or the CUPL compiler per-se, but rather they are executables which are supplied by Atmel and bundled with the Atmel WinCUPL package.

When compiling a `.PLD` file, CUPL generates a `.TT2` PLA netlist and provides it to the specific fitter for that device, which then transforms it into a `.JED` fusemap. Fitters ultimately determine the optimal way to utilize the resources of the device and are responsible for the final implementation of the logic in hardware.

The fitter also has control over various low-level, device-specific options which WinCUPL/CUPL would not have direct knowledge of, but which nonetheless can be specified inside of a <code>.PLD</code> design file using the <code>PROPERTY</code> statement, allowing them to be passed down to the fitter.

```
  PROPERTY <manuf ID> { property statement };
```

As an example, the following would leave the JTAG pins enabled (allowing future reprogramming), enable the weak pullups on the TMS/TDI pins, and make pin assignments from the .PLD design file mandatory:
```
PROPERTY ATMEL { jtag=on }; /* This keeps the JTAG pins on after programming */
PROPERTY ATMEL { TMS_pullup=on };
PROPERTY ATMEL { TDI_pullup=on };
PROPERTY ATMEL { Preassign=keep }; /* This forces the Atmel Fitter to use the pin assignments you specify. */
```

A [Manual for the Atmel Fitters](https://www.microchip.com/content/dam/mchp/documents/FPGA/pld-design-resources/ATF15xx%20Fitter%20Manual.zip) is available on Microchip's website. Note that these fitters are integrated into software packages beyond just WinCUPL, and so the manual has references to Atmel Prochip, ABEL, Atmel Synario, Protel, etc.

Since these fitters ultimately process a netlist, one could in theory use these fitters in any environment that is capable of producing a netlist. Be warned that while the EDIF format is a standard, the details of the implemetation may not be consistent or compatible across software in practice.

Finally, one thing to keep in mind is that the version of these fitters included with Atmel WinCUPL is rather old and so they should be replaced with newer versions from [Atmel Prochip 5.0.1](https://ww1.microchip.com/downloads/en/DeviceDoc/ProChip5.0.1.zip)

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

In instances where one would prefer the fitter handle the pin assignments <code>Preassign=ignore</code>, it can be useful to take pin mappings that have been autoassigned by the fitter and  backannotate them into the .PLD file. The <code>backpin.exe</code> utility performs this function. One should probably change to <code>Preassign=keep</code> to make these stick across future compilations.

# In this folder
> 
> <code>README.md</code> - This file.
> 
> <code>showargs*</code> - Simple executable and source code for a Windows executable that was briefly used for determining what arguments WinCUPL was passing to the fitters.
>
> <code>Atmel-ATF1500-tshirt.webp</code> - A picture of what is perhaps the most incredible bit of programmable logic history.
