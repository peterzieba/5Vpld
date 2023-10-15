#!/usr/bin/env python3
import argparse
import os
import spydrnet as sdn
from spydrnet.util.selection import Selection
import graphviz
from graphviz import Digraph

# massage characters that confuse the graphviz library or file format
def cleanup(x):
    return graphviz.escape(x).replace(":","_")

# get a name for a pin that can be used as an endpoint for an edge
def convertPin(pin, instance):
    if isinstance(pin, sdn.OuterPin):
        if len(pin.instance.reference.children) > 0:
            if pin.inner_pin.port.direction == sdn.Port.Direction.IN:
                instance_name = pin.instance.name + "_i"
            elif pin.inner_pin.port.direction == sdn.Port.Direction.OUT:
                instance_name = pin.instance.name + "_o"
            else:
                instance_name = pin.instance.name + "_io"
        else:
            instance_name = pin.instance.name
        port_name = pin.inner_pin.port.name
    else:
        if pin.port.direction == sdn.Port.Direction.IN:
            instance_name = instance.name + "_i"
        elif pin.port.direction == sdn.Port.Direction.OUT:
            instance_name = instance.name + "_o"
        else:
            instance_name = instance.name + "_io"
        port_name = pin.port.name
    p = "%s:%s" % (cleanup(instance_name), cleanup(port_name))
    return p

# sorting predicate to sort pins from output to input
def pinSort(pin):
    if isinstance(pin, sdn.OuterPin):
        if pin.inner_pin.port.direction == sdn.Port.Direction.OUT:
            return 0
        elif pin.inner_pin.port.direction == sdn.Port.Direction.IN:
            return 2
        else:
            return 1
    else:
        if pin.port.direction == sdn.Port.Direction.OUT:
            return 2
        elif pin.port.direction == sdn.Port.Direction.IN:
            return 0
        else:
            return 1

# convert an instance into a graph - either a simple record node or a subgraph with inputs and outputs
def convertInstance(instance, p):
    definition = instance.reference
    instance_name = cleanup(instance.name)
    
    inputs = []
    outputs = []
    inouts = []
    for port in definition.ports:
        if port.direction == sdn.Port.Direction.IN:
            inputs.append(port)
        elif port.direction == sdn.Port.Direction.OUT:
            outputs.append(port)
        else:
            inouts.append(port)

    label = "%s|%s" % (instance_name, definition.name)
    
    if len(definition.children) > 0:
        with p.subgraph(name="cluster_" + instance_name) as c:
            c.attr(label=label)
        
            if len(inputs) > 0:
                label = "|".join(["<%s> %s" % (cleanup(x.name), x.name) for x in inputs])
                c.node(instance_name + "_i", "IN|%s" % label)
 
            for child in definition.children:
                convertInstance(child, c)

            if len(outputs) > 0:
                label = "|".join(["<%s> %s" % (cleanup(x.name), x.name) for x in outputs])
                c.node(instance_name + "_o", "OUT|%s" % label)

            if len(inouts) > 0:
                label = "|".join(["<%s> %s" % (cleanup(x.name), x.name) for x in inouts])
                c.node(instance_name + "_io", "INOUT|{%s}" % label)

            for cable in definition.cables:
                for wire in cable.wires:
                    n = []
                    for pin in wire.pins:
                        n.append(pin)
                    n.sort(key = pinSort)
                    for i in range(len(n)-1):
                        c.edge(convertPin(n[0], instance), convertPin(n[i+1], instance))
    else:
        ports = []
        if len(inputs) > 0:
            ports.append("{%s}" % ("|".join(["<%s> %s" % (cleanup(x.name), x.name) for x in inputs])))
        if len(inouts) > 0:
            ports.append("{%s}" % ("|".join(["<%s> %s" % (cleanup(x.name), x.name) for x in inouts])))
        if len (outputs) > 0:
            ports.append("{%s}" % ("|".join(["<%s> %s" % (cleanup(x.name), x.name) for x in outputs])))
        if len(ports) > 0:
            label += "|{%s}" % ("|".join(ports))
        p.node(instance_name, label)

# load a netlist and convert the top level instance into a dot graph
def main():
    parser = argparse.ArgumentParser(description='Convert edif netlist into graphviz dot diagram')
    parser.add_argument('netlist', help='input netlist', type=str)
    parser.add_argument('--output', help='output dot file', type=str)
    parser.add_argument('--view', help='launch viewer', action='store_const', const=True, default=False)
    parser.add_argument('--format', help='output format', default='pdf', type=str)
    args = parser.parse_args()

    netlist = sdn.parse(args.netlist)
    
    dot = Digraph(netlist.top_instance.name, node_attr={'shape': 'record'})
    dot.graph_attr['rankdir'] = 'LR'
    convertInstance(netlist.top_instance, dot)

    output = args.output
    if output == None:
        output = os.path.splitext(args.netlist)[0] + ".gv"
    dot.render(output, view=args.view, format=args.format) 

if __name__ == "__main__":
    main()
