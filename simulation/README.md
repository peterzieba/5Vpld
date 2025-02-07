# Overview
The behavior of logic equations to be programmed into a device (or even a virtual device) can be simulated with a utility called WinSim which is part of WinCUPL. Note that this is only a functional simulation and not a timing simulation and covered here are only details on WinSim/CSIM.EXE

<details>
<summary>Scope: Expand here for details on timing simulations instead</summary>
There are some possibilities:


* PLD devices are probably simple enough where the datasheet can be utilized.
  * Perhaps this might be useful: https://github.com/ezrec/galpal
* For ATF150x devices see the fitter options, specifically:
  * <code>-strategy Verilog_sim [sdf | Verilog | OFF]</code>
  * <code>-strategy Vhdl_sim [sdf | vhdl | OFF]</code>
</details>

<details>
<summary>Scope: Expand here for details on graphical/schematic logic simulators instead</summary>

[Digital](https://github.com/hneemann/Digital) is an easy-to-use digital logic designer and circuit simulator designed for educational purposes. See also discussion here: https://github.com/peterzieba/5Vpld/issues/4

This is an interesting option as one can create a schematic and have a .JED file generated for a GAL16V8 or GAL22V10. If one provides the fitters to Digital, it can produce .JED files for the ATF150x series as well. Note that this is more of an educational tool for learning about logic. You may have trouble if you expect fullly featured support of these devices (Tri-state pins, Bi-directional IO, etc.)
* https://github.com/hneemann/Digital


If this appeals to you, you might be interested in similar software (though no support for the Atmel parts):
* <a href="http://www.cburch.com/logisim/">Logisim</a>
* <a href="https://github.com/logisim-evolution/logisim-evolution">Logisim Evolution</a>



</details>

# Alternatives
As WinSim is somewhat erratic, alternative approaches are examined here.

Under the hood, WinSim creates a <code>.SI</code> file (simulation input) which contains test vectors that are ultimately provided to CUPL/CSIM, and result in a <code>.SO</code> file (simulation output) being generated.

One potential alternative to WinSim is to simply create test vectors in a <code>.SI</code> file and have CUPL/CSIM generate the <code>.SO</code> file for us and parse it directly.

It is worth mentioning that while legend has it that you can use <code>CSIM.EXE</code> directly, the proper invocation of it seems elusive. What seems to work well instead is passing the <code>-s</code> compiler flag to <code>CUPL.EXE</code>, which then appears to utilize <code>csima.dll</code>.
