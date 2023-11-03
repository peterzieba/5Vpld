#!/usr/bin/env python3
import argparse
import os
import spydrnet as sdn
from spydrnet.util.selection import Selection

def main():
    parser = argparse.ArgumentParser(description='Convert an EDIF netlist into verilog')
    parser.add_argument('netlist', help='input netlist', type=str)
    args = parser.parse_args()

    netlist = sdn.parse(args.netlist)

    verilog_out_filename=os.path.splitext(args.netlist)[0] + ".v"
    sdn.compose(netlist, verilog_out_filename)

if __name__ == "__main__":
    main()