meta:
  id: cupl_abs
  file-extension: abs
  endian: le
  application:
    - CUPL.EXE
    - CSIM.EXE
  title: .ABS Absolute file decoder for files produced by the CUPL compiler.
seq:
  - id: magic
    contents: [0x25, 0x5B, 0x05, 0x00]
  - id: numofthings
    type: u2
#numofthings is likely not a single byte -- otherwise that would limit things to 255 entries.
#perhaps writing a test .PLD file to see what happens when one goes over would be interesting.

  - id: dunno0
    size: 66
  - id: name
    size: 29
    type: str
    encoding: utf-8
  - id: partnum
    size: 16
    type: str
    encoding: utf-8

#These could be anything
  - id: dunno1
    type: u4
  - id: dunno2
    size: 4
  - id: dunno3
    size: 4
  - id: dunno4
    size: 2

  - id: nameagain
    type: strz
    encoding: ascii

  - id: partno
    type: strz
    encoding: ascii

  - id: revision
    type: strz
    encoding: ascii

  - id: date
    type: strz
    encoding: ascii

  - id: designer
    type: strz
    encoding: ascii

  - id: company
    type: strz
    encoding: ascii

  - id: assembly
    type: strz
    encoding: ascii

  - id: location
    type: strz
    encoding: ascii

  - id: dunno5
    size: 12
#dunno5 is interesting because

#Whatever "things" are, they seem to be repeating 64-byte entries. This seems consistent and obvious.
#Interestingly, however, since we don't actually know anything about this file format, we have no way of knowing whether we're aligned properly.
#Meaning, dunno5 above might actually be part of the first "thing", in which case the above entry for dunno5 should be removed. If that were the case, then perhaps 12-bytes would be a remainder at the end of the file that isn't a "thing" but rather a footer of the file.
#If dunno5 does belong above, then there should be a footer that is 12-bytes.
#A third possibility is that there is actually a smaller dunno5 and then a remainder at the end that is a footer.

  - id: manythings
    type: thing
    repeat: eos
types:
  thing:
    seq:
      - id: name
        size: 32
      - id: whoknows
        size: 2
      - id: maybeseq
        type: u2
      - id: moreofthing
        size: 28
