# Overview

>[!IMPORTANT]
>This is a rabbit hole which probably serves no practical purpose. You have been warned.

This is an early attempt at decoding the `.ABS` files that CUPL.EXE generates when the `-a` flag is passed to it.

The purpose of an `.ABS` file is to be ingested by the CSIM.EXE simulator.

In theory, decoding this file could maybe lend itself running simulations in more modern tools.

# Methods
[Kaitai Struct](https://kaitai.io/) is used to help [define the file format](cupl-abs.ksy) of `.ABS` files.<br>

Kaitai Struct is a great way of handling data structures of binary file formats, and has the added benefit that once a `.ksy` file has been created for a given file type, you can automatically create a parser for quite a few different languages automatically (C++, PHP, Python, and many more). This is especially beneficial when you have a poorly understood format which is undergoing multiple attempts at refinement and you don't want to maintain several parsers across languages.<br>

Kaitai's `.ksy` files themselves are just a yaml file that defines the various regions within the `.ABS` and what they contain. It is a human readable description of how to parse a binary file.

You can use the [.ksy file in this repository](cupl-abs.ksy) here to look at an `.ABS` file for a project that you have:
* In a terminal using the [ksv tool](https://github.com/kaitai-io/kaitai_struct_visualizer) command:
  * <code>ksv your-file.abs cupl-abs.ksy</code>
* In a web browser using the [Kaitai Web IDE](https://ide.kaitai.io/)
* You can compile the `.ksy` file here into a decoder for just about any language you work in (Python, C++, PHP, Javascript, Java, etc. etc.)
  * Though it might be premature to do so -- the current understanding of the file is limited and therefore it serves merely as a template for further work.
