# Programming / Burning and Device Information
There are a few choices on how the part can actually be programmed depending on whether it supports JTAG.

A word on programming algorithms:<br>
Programming algorithms were seldom documented on datasheets for a part. Usually, these were behind NDA and only the companies producing Device Programmers had them (Data I/O, Logical Devices, Hi-Lo Systems, BP Microsystems, Wellon). Furthermore, some parts supporting JTAG (which in theory is much more open/universal), can nonetheless be programmed to repurpose the JTAG pins, at which point a dedicated device programmer or specialized knowledge of blanking the device is required.

Open Source programmers exist (if you really want to build one):<br>
https://github.com/ole00/afterburner

## PLD Devices (ATF16V8, ATF22V10)
These parts require an EPROM programmer, and ideally one from the time period during which these parts were in vogue. <span style="color: red;">Additionally, an important gotcha' is that there are many manufacturers of these parts as well as variants within a manufacturer. While the fusemap may be compatible across variants (GAL16V8 from Lattice vs. the ATF16V8 from Atmel/Microchip), THE PROGRAMMING ALGORITHMS ARE NOT! You will need an EPROM programmer with support for the EXACT manufacturer and EXACT part number of the device you have.</span>

Choices for programmers include:<br>
* Classic Programmers from their respective time period (Modular Circuit Technologies, Data I/O, Logical Devices, etc.)
  * Advantages:
    * Implement mature, Well QA'd programming algorithms direct from the manufacturers of the chips.
  * Disadvantages:
    * In many cases you'll be stuck running the supporting software on DOS or an old version of Windows.
    * In some cases even a desktop that needs some proprietary ISA card or parallel port.
    * Transferring files to and from such a computer can become a chore when iterating on a project. But, this might motivate one to use CSIM.EXE, which is probably not a bad thing.
* Modern USB attached programmers (Autoelectric / XGecu TL866 and the like):
  * Advantages:
    * USB Attached. Works on more modern computers.
  * Disadvantages:
    * People have reported issues with the programming Algorithms used in some of these programmers in the past. These issues may be fixed in newer versions of the software. As one might imagine, these likely do not have the same level of QA as OEM support that classic programmers had.
* Open-Source Programmers:
  * There are very old versions based on the parallel port.
  * Newer projects such as <a href="https://github.com/ole00/afterburner">Afterburner</a> use an Arduino UNO and USB.

## CPLD Devices (ATF1502, ATF1504, ATF1508)
IMPORTANT: If you are relying on JTAG to program your parts, you probably want to use <code>"PROPERTY ATMEL {JTAG=ON};</code> in your .PLD file. If you are not using CUPL.EXE, you will need to pass <code>-strategy JTAG = ON</code> to the fitter. Otherwise, the resulting .JED file will disable the JTAG pins, and you will need a special device programmer to erase/reprogram the device.

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
