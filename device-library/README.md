This directory is concerned with the Device Libraries used by the CUPL Compiler.

Typically, with WinCUPL, you'll be using <code>Atmel.dl</code>, however, there are other libraries out there as part of other software packages which are useful to be aware of in case you are trying to work with a device not supported in WinCUPL.

Further, some rudimentary efforts to understanding the device library format might show up in here in the form of a Kaitai Struct called <code>cupl-dl.ksy</code>

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
