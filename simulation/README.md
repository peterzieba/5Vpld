# Overview
The behavior of logic equations to be programmed into a device can be simulated with a utility called WinSim which is part of WinCUPL. Note that this is only a functional simulation and not a timing simulation.

<details>
<summary>Scope: Expand here for details on timing simulations</summary>
There are some possibilities:


* PLD devices are probably simple enough where the datasheet can be utilized.
  * Perhaps this might be useful: https://github.com/ezrec/galpal
* For ATF150x devices see the fitter options, specifically:
  * <code>-strategy Verilog_sim [sdf | Verilog | OFF]</code>
  * <code>-strategy Vhdl_sim [sdf | vhdl | OFF]</code>
</details>

# Alternatives
As this utility is somewhat erratic, alternatives are examined here.

Under the hood, WinSim creates a <code>.SI</code> file (simulation input) which contains test vectors that are ultimately provided to CUPL/CSIM, and result in a <code>.SO</code> file being generated.

One potential alternative to WinSim is to simply create test vectors in a <code>.SI</code> file and have CUPL/CSIM generate the <code>.SO</code> file for us and parse it directly.

It is worth mentioning that while legend has it that you can use <code>CSIM.EXE</code> directly, the proper invocation of it seems elusive. What seems to work well instead is passing the <code>-s</code> compiler flag to <code>CUPL.EXE</code>, which then appears to utilize <code>csima.dll</code>.
