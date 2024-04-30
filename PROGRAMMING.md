# Programming / Burning and Device Information
There are a few choices on how the part can actually be programmed depending on whether it supports JTAG. This is an overview.

## 🟥 Common Pitfall 🟥
It should be noted that while something like a 16V8 has been produced by multiple suppliers which are _functionally_ identical and likely have identical (or compatible) fusemaps / JEDEC files, _the programming algorithms for these devices are not the same across manufacturers_. Your device programmer must support the exact device and variant/revision you are attempting to program. Many have wasted hours due to this not being obvious.

## History of device programmers and algorithms
* First, in the good old days, the chips that were programmable consisted literally of "fuses" (often of nichrome wire) that were "burned" away, hence the term "burning rom". As one could imagine, these required exotic voltages and timing critical pulse sequences to program correctly (or at least with a reliable yield). Programming algorithms were also seldom documented on datasheets for a part. Usually, these were behind NDA and only the companies producing Device Programmers had them (Data I/O, Logical Devices, Hi-Lo Systems, BP Microsystems, Wellon).
* As time went on, things like UV eraseable devices were created, and when they were packaged in a ceramic package with a window, one could erase them with UV light and reprogram them. Often, the same devices were packaged in opaque plastic, and so these were effectively OTP (one-time-programmable). These relied on unusual programming voltages as well.
* Eventually, electrically eraseable parts made their way into the market, but still often required device programmers and programming voltages were sometimes required as well.
* Finally, in more recent history, devices integrated on-die charge pumps and began supporting standardized methods of programming (JTAG, I2C, SPI, etc.). This is the point at which many "EPROM/Device Programmers" fell out of relevance.

## PLD Devices (ATF16V8, ATF22V10)
These parts require an EPROM/Device programmer, and ideally one from the time period during which these parts were in vogue. <span style="color: red;">Additionally, an important gotcha' is that there are many manufacturers of these parts as well as variants within a manufacturer. While the fusemap may be compatible across variants (GAL16V8 from Lattice vs. the ATF16V8 from Atmel/Microchip), THE PROGRAMMING ALGORITHMS ARE NOT! You will need an EPROM programmer with support for the EXACT manufacturer and EXACT part number of the device you have.</span>

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
* ~~A special branch of~~ <a href="https://github.com/ole00/afterburner/">Afterburner</a> has experimental support for these chips.
  * This is great because the Arduino Uno it is based upon is cheap and ubiquitous and the project has support for generating the 12V Vpp needed to unlock JTAG-Disabled parts. You'll need to convert a .JED -> .SVF -> XSVF to successfully use this.

* To generate a .JED file for these devices, you will need the fitters. While WinCUPL has fitters within it, a much more updated version of the fitters is available inside of Atmel Prochip from <a href="https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources">Microchip's website</a>

* Finally, it is worth pointing out that the JTAG pins on these devices can be repurposed for user I/O in a design. However, if one does this, the devices will no longer be reprogrammable via JTAG. One then requires a universal device programmer (and requisite adapters) to blank the device. Some information is out there concerning a trick of applying 12V Vpp to the OE1 pin in order to unlock the device, and some unofficial documentation exists for this.

## Other Atmel CPLD Parts (ATF750, ATF1500)
* These parts do not support JTAG and are a bit more expensive, so they haven't been tried. You'll need an EPROM programmer that supports these.
* In theory the ATF1500 fitter should work fine under Wine and so if fed with a netlist it should work. This means either CUPL.EXE or in theory Yosys with the right techmap could work.
* I believe CUPL should be able to generate a .JED directly for the ATF750 without a fitter.

## Altera EPM3X and EPM7X parts
I believe these parts are no longer produced, or possibly NRND, at least as far are true 5V devices are concerned (and not merely 5V tolerant), so I would recommend moving toward the ATF150x parts. However, since a large number of people seem to really like these parts and seek them out on used markets I will say this:

The Altera EPM3X/EPM7X parts when purchased used might not be blank, and some of these parts do not support JTAG. It is possible to program them in such a way that they cannot be reprogrammed via JTAG, and the programming algorithms in almost any PLD is not actually part of the datasheet. Nonetheless, if one has a universal device programmer, or if one knows the trick of applying 12V VPP on the JTAG-supporting devices, they can be blanked. Finally, there are simply counterfeit / remarked devices out there are well, and no amount of hardware or ingenuity will solve this problem.
