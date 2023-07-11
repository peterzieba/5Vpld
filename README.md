# Overview
This repository centers around modern workflows for Atmel (Now Microchip) 5V GAL PLD and CPLD parts.

These parts are still active and highly worth considering wherever prototyping and 5V logic are a requirement. They can easily replace large numbers of TTL/CMOS logic chips and can be reprogrammed many times.

This repository aims to make it easier to work with the following parts:
* ATF1502, ATF1504, ATF1508 (programmable via JTAG)
* ATF16V8, ATF22V10 (Require an EPROM Programmer)

# Terminology
CPLD - Complex Programmable Logic Device
GAL - Generic Array Logic ()
WinCUPL - A Windows front-end to the CUPL compiler and related programs
CUPL - Compiler for Universal Programmable Logic (A old programming language for logic. Modern examples would be Verilog/VHDL)
FITTER - A fitter converts a netlist into the fusemap (.JED) file. Fitters are needed for the CPLD devices.
.JED/JEDEC File - A fuse map intended to be "burned/programmed" into a logic device.
.SVF File - Serial Vector Format. This file can be used by any JTAG programmer (vendor-independent) to program a device that has a JTAG interface.


# Writing logic for these parts
## CUPL / WinCUPL
While logic for these parts can be written via WinCUPL, the experience may be fraught with difficulty as it is somewhat unreliable and runs in Windows. While it does run under Linux via Wine, it is nonetheless a difficult experience.

The good news is that WinCUPL is really just a front-end / IDE for the command-line compiler CUPL.EXE, which can process a .PLD file and turn it into a .JED file ready for programming (in the case of PLD devices), or produce a netlist 

# Programming / Burning
## ATF1502, ATF1504, ATF1508
These parts can be programmed via JTAG, so there are a few options.
* Official programmer: https://www.kanda.com/CPLD-Programmers.175.html
** Software: https://www.microchip.com/en-us/development-tool/ATMISP
* OpenOCD: https://openocd.org/
** You will need an SVF file to program a device via OpenOCD. This can be created by converting the .JED file using either ATMISP, or fuseconv.py from whitequark/prjbureau

## PLD Devices (ATF16V8, ATF22V10)
These parts require an EPROM programmer. Additionally, an important gotcha' is that there are many variants and manufacturers of these parts. While the fusemap may be compatible across variants (GAL16V8 from Lattice vs. the ATF16V8 from Atmel/Microchip), THE PROGRAMMING ALGORITHMS ARE NOT! You will need an EPROM programmer with support for the EXACT manufacturer and part number of the device you have.