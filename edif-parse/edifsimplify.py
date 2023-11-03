#!/usr/bin/env python3
import argparse
import os
import spydrnet as sdn
from spydrnet.util.selection import Selection

remove_instances=["BUF", "OR1", "AND1"]

def main():
    parser = argparse.ArgumentParser(description='Accepts an EDIF netlist and removes extraneous instances that clutter things (buffers, single input AND/OR gates, etc.). Produces a file called origname_simplified.edn')
    parser.add_argument('netlist', help='input netlist', type=str)
    args = parser.parse_args()

    netlist = sdn.parse(args.netlist)

    to_remove = []

    for instance in netlist.get_instances():
        if instance.reference.name in remove_instances:
            to_remove.append(instance)
    
    for instance in to_remove:

        print("Removing " + instance.name)

        in_pins = list(x for x in instance.get_pins(selection=Selection.OUTSIDE, filter=lambda x: x.inner_pin.port.direction is sdn.IN))
        out_pins = list(x for x in instance.get_pins(selection=Selection.OUTSIDE, filter=lambda x: x.inner_pin.port.direction is sdn.OUT))

        for in_pin, out_pin in zip(in_pins, out_pins):

            in_wire = in_pin.wire
            in_wire.disconnect_pin(in_pin)

            out_wire = out_pin.wire

            for out_wire_pin in out_wire.pins:
                if out_wire_pin is out_pin:
                    continue
                out_wire.disconnect_pin(out_wire_pin)
                in_wire.connect_pin(out_wire_pin)

            out_wire.cable.remove_wire(out_wire)

        instance.parent.remove_child(instance)
    
    simplified_netlist_file=os.path.splitext(args.netlist)[0] + "_simplified.edf"
    sdn.compose(netlist, simplified_netlist_file)


if __name__ == "__main__":
    main()
