import numpy as np
#import matplotlib
import os

from sisi.simulator import Instruction
from sisi.simulator.xmega import XMegaSimulator
from sisi.simulator.xmega_instruction_set import eor, ld, st, ldi, nop


key = 0x11

def trace(pt):
    sim = XMegaSimulator()
    sim.memory[0] = pt
    sim.regs['Z'].value = 0
    sim.execute([
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(ld, sim.regs['r25'], sim.regs['Z']),
        Instruction(ldi, sim.regs['r24'], key),
        Instruction(eor, sim.regs['r25'], sim.regs['r24']),
        Instruction(st, sim.regs['Z'], sim.regs['r25']),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
        Instruction(nop),
    ])
    return sim.leakage


def main():
    samples = 500
    textins = np.random.random_integers(0, 255, samples)
    traces = []
    for pt in textins:
        traces += [trace(pt)]
    traces = np.asarray(traces)

    path = r'C:/Users/hackenbs/chipwhisperer/projects/base-01_data/traces'
    np.save(os.path.join(path, r'simple_leakage_textin'), textins.reshape((samples, 1)))
    np.save(os.path.join(path, r'simple_leakage_traces'), traces)
    np.save(os.path.join(path, r'simple_leakage_textout'), textins.reshape((samples, 1)))
    np.save(os.path.join(path, r'simple_leakage_knownkey'), np.array([key]*16))
    np.save(os.path.join(path, r'simple_leakage_keylist'), np.array([[key]*16]*samples))



if __name__ == '__main__':
    main()
