# Overview
The behavior of logic equations to be programmed into a device (or even a virtual device) can be simulated with a utility called WinSim which is part of WinCUPL.

Just like WinCUPL, it is an erratic front-end. Thankfully however, the simulation itself is actually performed by the CUPL compiler and is solid.

Note that this is only a 'functional simulation' and not a 'timing simulation' and covered here are primarily details on WinSim/CSIM.EXE

<details>
<summary>Scope: Expand here for details on timing simulations instead</summary>

>There are some possibilities:

>* PLD devices are probably simple enough where the datasheet can be utilized.
>  * Perhaps this might be useful: https://github.com/ezrec/galpal
>* For ATF150x devices see the fitter options, specifically:
>  * <code>-strategy Verilog_sim [sdf | Verilog | OFF]</code>
>  * <code>-strategy Vhdl_sim [sdf | vhdl | OFF]</code>
</details>

<details>
<summary>Scope: Expand here for details on graphical/schematic logic simulators instead</summary>

>[Digital](https://github.com/hneemann/Digital) is an easy-to-use digital logic designer and circuit simulator designed for educational purposes. See also discussion here: https://github.com/peterzieba/5Vpld/issues/4

>This is an interesting option as one can create a schematic and have a .JED file generated for a GAL16V8 or GAL22V10. If one provides the fitters to Digital, it can produce .JED files for the ATF150x series as well. Note that this is more of an educational tool for learning about logic. You may have trouble if you expect fullly featured support of these devices (Tri-state pins, Bi-directional IO, etc.)
>* https://github.com/hneemann/Digital

>If this appeals to you, you might be interested in similar software (though no support for the Atmel parts):
>* <a href="http://www.cburch.com/logisim/">Logisim</a>
>* <a href="https://github.com/logisim-evolution/logisim-evolution">Logisim Evolution</a>

</details>

# Alternatives
As WinSim is somewhat erratic, alternative approaches are examined here.

Under the hood, WinSim creates a <code>.SI</code> file (simulation input) which contains test vectors that are ultimately provided to CUPL/CSIM, and result in a <code>.SO</code> file (simulation output) being generated.

One potential alternative to WinSim is to simply create test vectors in a <code>.SI</code> file and have CUPL/CSIM generate the <code>.SO</code> file for us and parse it directly.

It is worth mentioning that while legend has it that you can use <code>CSIM.EXE</code> directly, the proper invocation of it seems elusive. What seems to work well instead is passing the <code>-s</code> compiler flag to <code>CUPL.EXE</code>, which then appears to utilize <code>csima.dll</code>.
<details>
<summary>Expand here if you insist on trying to get the CSIM.EXE command-line options to work for you. Again, just use CUPL.EXE with the -s flag for something that works.</summary>
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

The <code>.SI</code> file can be populated with test vectors and be used to simulate the behavior of a particular chip, or even a virtual device.

Creating a .SI file:<br />
* An .SI file should have the same header information as the original .PLD source file. If not, this will generate warnings.
* Comments begin with a /* and end with a */
* An .SI file can have the following keywords/statements: ORDER, BASE, and VECTORS
  * The ORDER keyword is used to list the variable / inputs and outputs to be used in the simulation table, and to define how they are displayed. Typically, the variable names are the same as those in the corresponding CUPL logic description file.
  * The BASE keyword specifies a number base. Hexadecimal is the default if unspecified.
  * The VECTORS keyword specifies a list of test vectors (signals that are applied and expected outputs).
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
