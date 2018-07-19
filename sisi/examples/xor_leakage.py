#/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np
# import matplotlib.pyplot as plot
from sisi.cwfileformat import CWTraceFile

from sisi.simulator import Instruction
from sisi.simulator.xmega import XMegaSimulator
from sisi.simulator.xmega_instruction_set import eor, ld, st, ldi, nop, mov, add


"""
Example demonstrating leakage of XOR.
Corresponding C-code is located at ../../examples/simpleserial-xor.c
"""


key = 0xA3


def trace(pt):
    sim = XMegaSimulator()
    sim.memory[0] = pt
    sim.regs['X'].value = 0x0000
    sim.execute([
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(ld, sim.regs['r24'], sim.regs['X']),
        Instruction(ldi, sim.regs['r25'], key),
        Instruction(eor, sim.regs['r24'], sim.regs['r25']),
        Instruction(st, sim.regs['X'], sim.regs['r24']),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
    ])
    return sim.leakage


def main():
    samples = 50
    textin = np.random.random_integers(0, 255, samples)
    traces = []
    for pt in textin:
        traces += [trace(pt)]
    traces = np.asarray(traces)

    # Uncomment to show plot
    # for t in traces:
    #     plot.plot(t, linewidth=0.5)
    # plot.show()

    CWTraceFile(
        r'xor_leakage',
        textin=textin.reshape((samples, 1)),
        textout=textin.reshape((samples, 1)),
        knownkey=np.array([key]),
        keylist=np.array([[key]]*samples),
        traces=traces,
    ).save()


if __name__ == '__main__':
    main()
