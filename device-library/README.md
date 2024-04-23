This directory is concerned with the Device Libraries used by the CUPL Compiler.

Typically, with WinCUPL, you'll be using <code>Atmel.dl</code>, which only provides support for some common Atmel PLD/CPLD chips, however, there are other libraries out there as part of other software packages which are useful to be aware of in case you are trying to work with a device not supported in WinCUPL.

A brief survey of some device libraries that exist in the wild include:
| Filename   | Library name  | Timestamp    | Number of Chips       |
| ---        | ---           | ---     | ---                   |
|pldxpert.dl | palxprt       | 8/19/99 | 233 |
|Atmel.dl    | atmel         | 3/31/04 |  84 |
|pldmstr.dl  | pldmstr       | 8/19/99 | 481 |
|pldmstr.dl  | pldmstr       | 2/21/00 | 491 |
|totaldes.dl | totaldes      | 8/19/99 | 664 |


The structure of a library file in brief looks something like this:
* Header
* Short list of all chip names along with the offsets and sizes of the details for each chip.
* Details of each chip

A more detailed Kaitai Struct [cupl-dl.ksy](cupl-dl.ksy) in this directory describes things in greater detail, however, it is incomplete the aspects that are understood might be incorrect.

It is possible that a greater understanding of this file could be used to write custom support for other devices or as a basis for programming devices through other workflows.

The current state of things is that the .ksy file works well enough to parse the same information that the vendor supplied Library Management program <code>CBLD.EXE</code> is capable of outputting from the library and seems to be correct, but has not been thoroughly compared.

The device library is typically managed with the vendor tools using <code>CBLD.EXE</code>, which has the following help output:
<code>
CBLD(PM): CUPL Device Library Management Program
Version 5.0a
Copyright (c) 1983, 1998 Logical Devices, Inc.

usage: cbld [-flags] [ build | library ] [ devices ]
flags:
          -b   generate library using build file
          -e   list valid extensions
          -l   list long contents of library
          -t   list contents of library
          -u   use specified library for listings
</code>
