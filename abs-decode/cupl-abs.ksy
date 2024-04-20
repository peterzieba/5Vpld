meta:
  id: cupl_abs
  file-extension: abs
  application:
    - CUPL.EXE
    - CSIM.EXE
  title: .ABS Absolute file decoder for files produced by the CUPL compiler.
  endian: le
seq:
  - id: magic
    contents: [0x25, 0x5B, 0x05, 0x00]
  - id: dunno
    size: 1
  - id: thing0
    size: 67
  - id: name
    size: 29
    type: str
    encoding: utf-8
  - id: partnum
    size: 16
    type: str
    encoding: utf-8
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

  - id: manypins
    type: pin
    repeat: eos
types:
  pin:
    seq:
      - id: pinname
        size: 32
      - id: pindunno
        size: 32
