# Overview
Fitting, perhaps more commonly known as "place and route" is the stage that translates the logic into the physical hardware available on a given device.

Most simpler devices in WinCUPL do not use an external fitter executable and so WinCUPL can directly produce a .JED file for them.

The following CPLD devices are unique in that they have fitters that are provided by Atmel and bundled with Atmel WinCUPL:
* ATF1500
* ATF1502
* ATF1504
* ATF1508

Note that these are not part of WinCUPL or the CUPL compiler per-se, but rather they are executables which are supplied by Atmel and included with the package.

The fitter accepts a netlist that WinCUPL provides and transforms it into a fusemap specific for a given device. They ultimately determine the optimal way to utilize the resources of the device and are responsible for the final implementation of the logic in hardware.

The fitter also has control over various low-level, device-specific options which WinCUPL/CUPL would not have direct knowledge of, but which nonetheless can be specified inside of a <code>.PLD</code> design file using the <code>PROPERTY</code> statement, allowing them to be passed down to the fitter.

```
  PROPERTY <manuf ID> { property statement };
```

As an example, the following would leave the JTAG pins enabled (allowing future reprogramming), and enable the weak pullups on the TCK/TDI pins, and make pin assignments from the .PLD design file mandatory:
```
PROPERTY ATMEL { jtag=on }; /* This keeps the JTAG pins on after programming */
PROPERTY ATMEL { TMS_pullup=on };
PROPERTY ATMEL { TDI_pullup=on };
PROPERTY ATMEL { Preassign=keep }; /* This forces the Atmel Fitter to use the pin assignments you specify. */
```

A [Manual for the Atmel Fitters](https://www.microchip.com/content/dam/mchp/documents/FPGA/pld-design-resources/ATF15xx%20Fitter%20Manual.zip) is available on Microchip's website. Note that these fitters are integrated into software packages beyond just WinCUPL, and so the manual has references to Atmel Prochip, ABEL, Atmel Synario, Protel, etc.

Since these fitters ultimately process a netlist, one could in theory use these fitters in any environment that is capable of producing a netlist. Be warned that while the EDIF format is a standard, the details of the implemetation may not be consistent or compatible across software in practice.

Finally, one thing to keep in mind is that the version of these fitters included with Atmel WinCUPL is rather old and so they should be replaced with newer versions from [Atmel Prochip 5.0.1](https://ww1.microchip.com/downloads/en/DeviceDoc/ProChip5.0.1.zip)
