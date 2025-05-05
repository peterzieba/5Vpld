# Programming / Burning and Device Information
There are a few choices on how the part can actually be programmed, primarily depending on whether it supports JTAG. In all cases, you'll need a <code>.JED</code> file, which is the fusemap that is burned into your device. This is an overview depending on the device you are working with.

## History of device programmers and algorithms
* First, in the good old days, the chips that were programmable consisted literally of "fuses" (often of nichrome wire) that were "burned" away, hence the term "burning rom". As one could imagine, these required exotic voltages and timing critical pulse sequences to program correctly (or at least with a decent yield). Programming algorithms were also seldom documented on datasheets for a part. Usually, these were behind NDA and only the companies producing Device Programmers had them (Data I/O, Logical Devices, Hi-Lo Systems, BP Microsystems, Wellon).
* As time went on, things like UV eraseable devices were created, and when they were packaged in a ceramic package with a quartz window, one could erase them with UV light and reprogram them. Often, the same devices were packaged in opaque plastic, and so these were effectively OTP (one-time-programmable). These relied on unusual programming voltages as well.
* Eventually, electrically eraseable parts made their way into the market, but still often required device programmers and programming voltages were sometimes required as well.
* Finally, in more recent history, devices integrated on-die charge pumps and began supporting standardized methods of programming (JTAG, I2C, SPI, etc.). This is the point at which many "EPROM/Device Programmers" fell out of relevance.

## PLD Devices (ATF16V8, ATF22V10, ATF750C)
These parts require an EPROM/Device programmer, and ideally one from the time period during which these parts were in vogue. None of these parts support JTAG.
>[!IMPORTANT]
>It should be noted that while something like a 16V8 has been produced by multiple IC manufacturers and that while these might be _functionally_ equivalent and likely have identical (or compatible) fusemaps / JEDEC files, _the programming algorithms for these devices are not the same across device manufacturers_.
>
>As an example: While the fusemap may be compatible across variants (GAL16V8 from Lattice vs. the ATF16V8 from Atmel/Microchip), THE PROGRAMMING ALGORITHMS ARE NOT! You will need an EPROM programmer with support for the EXACT manufacturer and EXACT part number of the device you have.
>
>Your device programmer must support the exact device and variant/revision you are attempting to program. Many have wasted hours due to this not being obvious.

Choices for programmers include:<br>
* Classic Programmers from their respective time period (Modular Circuit Technologies, Data I/O, Logical Devices, etc.)
  * Advantages:
    * Implement mature, well QA'd programming algorithms direct from the manufacturers of the chips.
  * Disadvantages:
    * In many cases you'll be stuck running the supporting software on DOS or an old version of Windows.
    * In some cases even a desktop that needs some proprietary ISA card or parallel port.
    * Transferring files to and from such a computer can become a chore when iterating on a project. But, this might motivate one to use simulation tools, which is probably not a bad thing.
* Modern USB attached programmers (Autoelectric / XGecu TL866 and the like):
  * Advantages:
    * USB Attached. Works on more modern computers.
  * Disadvantages:
    * People have reported issues with the programming Algorithms used in some of these programmers in the past. These issues may be fixed in newer versions of the software. As one might imagine, these likely do not have the same level of QA as OEM support that classic programmers had.
* Open-Source Programmers:
  * Newer projects such as <a href="https://github.com/ole00/afterburner">Afterburner</a> use an Arduino UNO and USB. This is probably the most practical approach and seems to work well for the supported devices.
    * The ATF750C is recently supported in <a href="https://github.com/ole00/afterburner">Afterburner</a>.
    * This project is an invaluable resource for understanding how the algorithms work for these parts and also links to programmers created by others in the past, some of which utilized the parallel port, DOS, etc.
    * While projects like these are likely created without the formal programming specifications, they nonetheless seem to be getting very good results.

## CPLD Devices (ATF1502, ATF1504, ATF1508)
These parts can be programmed via JTAG, so there are a few options.
* [Official FTDI-based Kanda programmer](https://www.kanda.com/CPLD-Programmers.175.html) (basically a fancy USB-FTDI box) and [ATMISP Software](https://www.microchip.com/en-us/products/fpgas-and-plds/spld-cplds/pld-design-resources)
  * Upsides
    * Get going right away. Direct support for .JED files with included ATMISP software.
    * In-circuit programming
    * Expects VccIO from the device and sends it into IO buffers to handle different programming voltages.
  * Downsides
    * Windows only -- [If you know how to handle the sorcery required to get ftd2xx to run in Wine ATMISP might be usable in Linux](https://github.com/brentr/wineftd2xx/issues/15)
    * Cannot reprogram a device if the JTAG pins have been disabled.
    * $100.
* https://github.com/roscopeco/atfprog-tools
* https://github.com/hackup/ATF2FT232HQ
* Ancient Device Programmers (Hi-Lo ALL-07, etc.)
  * Upsides:
    * Generally support reprogramming devices even if the JTAG pins have been disabled.
  * Downsides:
    * Often require a machine running DOS. Moving files to and from can be tricky. Your PC is a deskmonster.
    * Require programming adapters for the specific socket type you have.
* Any standard JTAG Programmers (you will need to convert your .JED to an .SVF first):
  * OpenOCD: https://openocd.org/
  * Raspberry Pi Pico-based Dirty JTAG: https://github.com/phdussud/pico-dirtyJtag
  * <a href="https://github.com/ole00/afterburner/">Afterburner (An arduino-based PLD programmer)</a>~~A special branch of Afterburner~~ has experimental support for these chips.
    * This project is great because the Arduino Uno it is based upon is cheap and ubiquitous and the project has support for generating the 12V Vpp needed to unlock JTAG-Disabled parts via the secret +12V OE1 trick. You'll need to convert a .JED -> .SVF -> XSVF to successfully use this.

Unlike the case with a majority of devices in CUPL, CUPL does not directly produce a .JED file for these CPLD parts. Instead, it provides a netlist to the Atmel Fitters (essentially place-and-route in modern terminology) which in turn creates a .JED file. Since this is its own process beyond CUPL, it creates its own log file which will have a <code>.fit</code> file extension, as well as an error file with the <code>.err</code> extension. It is good to glance at these to make sure pins were assigned the way you wanted, JTAG was left on, etc. If you did not successfully produce a .JED file and it was not a CUPL error the reason might be in these logs.

>[!IMPORTANT]
>There are some bear traps when using these parts and the Atmel Fitters. Consider adding the following lines to your <code>.PLD</code> file somewhere after your header to save yourself from headaches. These lines are not processed by CUPL per-se, but rather passed onto the Atmel Fitter.
>```
>PROPERTY ATMEL { jtag=on }; /* This keeps the JTAG pins on after programming */
>PROPERTY ATMEL { TMS_pullup=on };
>PROPERTY ATMEL { TDI_pullup=on };
>PROPERTY ATMEL { Preassign=keep }; /* This forces the Atmel Fitter to use the pin assignments you specify. */
>```
>

<details>
<summary>Expand Here: What happens if I don't use <code>jtag=on</code>?</summary>

>Well, the resulting <code>.JED</code> file will disable the JTAG pins and then you can't erase or reprogram your device using JTAG. So, why on earth would you want to set this to <code>off</code>? If your design needed more pins you can set this to 'off' and repurpose the JTAG pins for your own needs. Once this is done however, the device cannot be erased or reprogrammed without using a fancy device programmer, or you need to know about the secret that involves applying +12V to the OE1 pin to re-enable the JTAG pins temporarily.
>
>If you are using the fitter in a workflow other than CUPL, you can also add this to the fitter's command line invocation:
>
><code>-strategy JTAG = ON</code>
</details>

<details>
<summary>Expand Here: What happens if I don't use <code>Preassign=keep</code>?</summary>
 
>The default is <code>Preassign=try</code>. So, in the design file, you specify what Pin numbers get mapped to what signals. If the fitter decides your design doesn't fit and the default 'try' is enabled, it can try to rerrange pins to see if that makes it fit. If that succeeds then you are presented with a <code>.JED</code> file that actually has pin mappings that differ from what you intended in your <code>.PLD</code> design file. If you don't check the <code>.fit</code> and the <code>.err</code> log files, you might be in for a long hardware debugging session.
>* try: remap pins as necessary.
>* keep: force pin mappings from the design file. Do not remap.
>* ignore: ignore all pin mappings from design file. Let the fitter decide the best arrangement of pins.
</details>

>[!IMPORTANT]
>Be Mindful of JTAG programming voltages as there are 3.3V and 5V variants of these parts. There are also 5V parts where it is acceptable to have the VccIO pins at 3.3V. If you are programming in-circuit be mindful of where power is coming (does your programmer provide power? Is there a danger of backpowering your device with your programmer?).

## Other Atmel CPLD Parts (ATF1500, ATF2500C)
* These parts do not support JTAG and are a bit more expensive, so they haven't been tried. You'll need an ancient device programmer that supports these.
* In theory the ATF1500 fitter should work fine under Wine and so if fed with a netlist it should work. This means either CUPL.EXE or in theory Yosys with the right techmap could work.
* I believe CUPL should be able to generate a .JED directly for the ATF2500C without a fitter.
  * The programming algorithm for the ATF2500C remains elusive, however, it might actually end up being similar to the ATF750C if one were to speculate.

## Altera EPM3X and EPM7X parts
I believe these parts are no longer produced, or possibly NRND, at least as far are true 5V devices are concerned (and not merely 5V tolerant), so I would recommend moving toward the ATF150x parts. However, since a large number of people seem to really like these parts and seek them out on used markets I will say this:

The Altera EPM3X/EPM7X parts when purchased used might not be blank, and some of these parts do not support JTAG. It is possible to program them in such a way that they cannot be reprogrammed via JTAG, and the programming algorithms in almost any PLD is not actually part of the datasheet. Nonetheless, if one has a universal device programmer, or if one knows the trick of applying 12V VPP on the JTAG-supporting devices, they can be blanked. Finally, there are simply counterfeit / remarked devices out there are well, and no amount of hardware or ingenuity will solve this problem.
