# Overview
This is an early attempt at decoding the .ABS files that CUPL.EXE generates when the -a flag is passed to it.

The historical purpose of an .ABS file was to be ingested by the CSIM.EXE simulator.

In theory, decoding this file could lend itself to:
* Running simulations in more modern tools, such as:
  * [Surfer Project](https://app.surfer-project.org/?load_url=https://app.surfer-project.org/picorv32.vcd&startup_commands=show_quick_start;module_add%20testbench.top)
* Maybe exporting a netlist???

# Implementation Here
Kaitai struct is used to help [define the file format](cupl-abs.ksy) of .ABS files.<br>
Kaitai's .ksy files themselves are just a yaml file that defines the various regions within the .ABS and what they contain. It is a human readable description of how to parse this binary file.

You can use the [.ksy file in this repository](cupl-abs.ksy) here to look at an .ABS file for a project that you have:
* In a terminal using the [ksv tool](https://github.com/kaitai-io/kaitai_struct_visualizer) command:
  * <code>ksv your-file.abs cupl-abs.ksy</code>
* In a web browser using the [Kaitai Web IDE](https://ide.kaitai.io/)
* You can compile the .ksy file here into a decoder for just about any language you work in (Python, C++, PHP, Javascript, Java, etc. etc.)
  * Though it might be premature to do so -- the current understanding of the file is limited and therefore it serves merely as a template for further work.
