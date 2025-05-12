#!/usr/bin/python3
"""
Usage: makesi.py yourpldfile.pld yourpldfile.xlsx > yourpldfile.si
This Python program takes test vectors created in an excel spreadsheet and writes an .SI file to standard output.
The PLD file needs to be specified first as the headers from the .PLD file are used for generating the .SI
All of this is to avoid using WinSIM, but also leveraging a spreadsheet to avoid creating our own GUI.

The format of the excel sheet is very simple:
Each row belongs to one signal.
First column is the signal name (exactly as named in the PIN section of the PLD file, and is case-sensitive).
The next column is the first set of test vectors, with each cell containing a single character which defines the value to set or test a signal for in that test vector.
Subsequent columns are further test vectors, as many as necessary.
Note that CSIM.EXE has its own test values for vectors which is actually not the same as 
"""

"""
Known issues:
1. Not implemented: "BASE: " and the related processing of values in quotes (' ' and " ") that represent the number bases octal, decimal, and hex.
2. The whole .SI file should probably be checked/converted to make sure DOS-style newlines '\r\n'
"""

import sys
from pprint import pprint

#Lines that begin with any of these will be grabbed into the header section of the generated file.
header_prefixes=["NAME", "PARTNO", "REVISION", "DATE", "DESIGNER", "COMPANY", "ASSEMBLY", "LOCATION", "DEVICE", "FORMAT" ] 
#The DEVICE and FORMAT sections are only covered in CUPL_Reference.pdf and not otherwise mentioned in CUPL_USERS_GUIDE.pdf and are absent in the template file.
#FORMAT can be lowercase 'h' for ASCII format, 'i' for Signetics HL format, and 'j' for JEDEC file (probably what you want).

base="BASE: " #can be either octal, decimal, or hex. Terminated by a semicolon. Currently unimplemented.
order="ORDER: " #defines the sequence of signals.

#The excel sheet test values will be made uppercase and checked to see that it contains only these values for the vectors.
#Blanks cells will be changed to '*' (compiler determined)
valid_csim_vector_values=["0", "1", "C", "K", "L", "H", "Z", "X", "N", "P", "*" ] #A list of valid CSIM vector values

"""
CSIM provides six directives that can be placed on any row of the file after the
VECTOR statement. All directive names begin with a dollar sign and each directive
statement must end with a semicolon.

$MSG "your text"; //place documentation messages or formatting information into the simulator output file.
$REPEAT 5;        //The vector following $REPEAT 5; will be repeated 5 times. Set between 1-9999.
$TRACE 4;         //set the amount of information that CSIM prints for the vectors during simulation. 0 (default) is quiet. 4 is maximum information.
$SIMOFF;          //Turn off test vector evaluation. Useful in testing asynchronously clocked designs in which CSIM is unable to correctly evaluate registered outputs.
$SIMON;           //Cancel the effects of the $SIMOFF directive.

$EXIT;            //Abort the simulation. This directive is useful in debugging registered designs in which a false transition in one vector causes an error in every vector thereafter.
"""

"""
Test vector values.
See Atmel App Note DOC0479.PDF - Table 1, which shows the equivalent test vector values for JEDEC, ABEL, and CUPL.

The following are values recognized by the CUPL's Simulator's .SI file.
0   Drive input LO (0 volts) (negate active-HI input)
1   Drive input HI (+5 volts) (assert active-HI input)
C   Drive (clock) input LO, HI, LO
K   Drive (clock) input HI, LO, HI
L   Test output LO (0 volts) (active-HI output negated)
H   Test output HI (+5 volts) (active-HI output asserted)
Z   Test output for high impedance
X   Input HI or LO, output HI or LO.
    Note: Not all device programmers treat X on inputs the same;
    some put it to 0, some allow input to be pulled to 1, and
    some leave it at the previous value.
N   Output not tested
P   Preload internal registers (value is applied to !Q output)
*   Outputs only -simulator determines test value and
    substitutes in vector
' ' Enclose input values to be expanded to a specified BASE
    (octal, decimal, or hex). Valid values are 0-F and X.
" " Enclose output values to be expanded to a specified BASE
    (octal, decimal, or hex.) Valid values are 0-F, H, L, Z, and X.
"""

def transpose_multiline_text(input_text, prepend="", append=""):
    # Split the input into lines
    lines = input_text.splitlines()
    
    # Find the maximum length of the lines
    max_len = max(len(line) for line in lines)
    
    # Create a list to hold the transformed lines
    result = []
    
    # Loop through each position in the line and form the new lines
    for i in range(max_len):
        # Create a new line by collecting the i-th character from each original line
        new_line = ''.join(line[i] if i < len(line) else ' ' for line in lines)
        #result.append("//" + new_line)
        result.append(prepend + new_line + append)

    # Join the result into a single string with line breaks
    #print(result)
    return "\r\n".join(result)


def get_headers_from_pld_file(fn):
    """
    This accepts the filename of a .PLD file and returns a multi-line variable with the headers.
    A generated .SI file needs to have header information that matches this.
    """
    header=""
    with open(fn, "r") as f:
        for line in f:
            matchline=line.lstrip().upper()
            if any(matchline.startswith(prefix) for prefix in header_prefixes):
                header+=line.rstrip("\n") + "\r\n" #FIXME -- this should probably not assume unix-style newlines. Otherwise we might add "\r\r\n" inadvertently. This is needed because the .SI file in particular seems to need DOS style '\r\n'
    return(header)


def get_vectors_from_xlsx(fn, make_header=True):
    """
    This uses pandas to read an excel sheet with signal names and test vectors.
    Potentially to be considered are the 'transpose' functions in numpy and pandas, which will swap rows and columns.
    This can also be done using zip()
    """
    import pandas as pd
    signals=[] #A list of signals
    vectors={} #Dict containing a series of signals and their vectors.
    prepend="   " #Extra spaces to add before printing vectors
    dfs = pd.read_excel(fn, sheet_name=None, header=None, na_values='NULL', dtype='str') #index_col=0,
    #print(dfs)
    df = dfs['Sheet1'].T #transpose the sheet
    df.columns = df.iloc[0] #set first row as column names
    df=df.drop(0, axis=0)
    df.reset_index(drop=True, inplace=True)
    
    #shape = df.shape
    #print("shape:",shape) #rows X cols
    #is it worth also having dimensions which exclude blank rows or columns?

    #print(df)
    #print(df.T)

    #Create a list of signals. Convert blank cells into the string "/* */"
    #for sig in df.loc[0]: #.tolist():
    for sig in df.columns.tolist():
        if not pd.isna(sig):
            signals.append(sig)
        else:
            signals.append("/* */")

    vector_text=""
    #Go through each signal, picking out each test condition, one by one
    for sig in df.columns:
        #print(f"\nColumn: {sig}")
        #print("shape", df[sig].shape[0], "count", df[sig].count())
        if pd.isna(sig):
            df[sig]=" "

    #Go through row by row.
    tv=[] #Store a list of strings
    vector_text=""
    for name,row in df.iterrows():
        for cell in row:
            if not pd.isna(cell):
                tv.append(cell)
            else:
                tv.append("*")
        if all(char == '*' or char ==' ' for char in tv):
            tv=[]
        tv=[str(x) for x in tv]
        tv="".join(tv) #Make list into a single string.
        tv=tv.upper()
        #print(tv)
        vector_text+=prepend + tv + "\r\n"
        tv=[]

    if make_header:
        signal_header=""
        max_sig_len=len(max(signals, key=len))
        for i in signals:
            if i != "/* */":
                signal_header+=i.rjust(max_sig_len) + "\r\n"
            else:
                signal_header+="\r\n"
        signal_header=transpose_multiline_text(signal_header, "/* ", "*/") + "\r\n"
        vector_text=signal_header + vector_text

    return(signals, vectors, "VECTORS:\r\n" + vector_text)

def make_order(signal_list):
    order="ORDER: "
    blank=0
    for index,signal in enumerate(signal_list):
        if signal != '/* */':
            if blank != 0:
                order+="%" + str(blank) + ", "
                blank=0
            order+=signal + ", "
        else:
            blank+=1
    return(order[:-2] + ";\r\n")

header=get_headers_from_pld_file(sys.argv[1])
signals,vectors,vector_text=get_vectors_from_xlsx(sys.argv[2])
order=make_order(signals)

print(header + "\r\n" + order + "\r\n" + vector_text)
