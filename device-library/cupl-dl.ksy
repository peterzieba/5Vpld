meta:
  id: cupl_dl
  file-extension: dl
  endian: le
  application:
    - CUPL.EXE
    - CSIM.EXE
    - CBLD.EXE
  title: Decoder for CUPL .DL device library files.
seq:
  - id: magic
    contents: [0x31, 0xD4, 0x28, 0x00]
  - id: libname
    type: strz
    encoding: ascii
    size: 17
  - id: lib
    type: strz
    encoding: ascii
    size: 17
  - id: copy
    type: strz
    encoding: ascii
    size: 161
