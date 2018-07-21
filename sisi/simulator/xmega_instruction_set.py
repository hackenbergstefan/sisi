#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import Register, Simulator, normalized_noisy_hamming_weight, Label
from .xmega import PointerRegister


"""The AVR instruction set."""

INSTRUCTIONS = {}


def xmega_instruction(*args):
    name = args[0]

    def _xmega_instruction(fun):
        INSTRUCTIONS[name] = fun
        return fun

    if len(args) == 1 and callable(args[0]):
        name = args[0].__name__
        return _xmega_instruction(args[0])
    else:
        return _xmega_instruction


def instruction_by_name(name):
    return INSTRUCTIONS[name]


@xmega_instruction
def nop(sim: Simulator):
    """
    NOP
    """
    sim.leakage += [normalized_noisy_hamming_weight(0x0f, 0.001)]


@xmega_instruction
def eor(sim: Simulator, rd: Register, rr: Register):
    """
    EOR Rd, Rr Exclusive OR Rd ← Rd ⊕ Rr
    """
    rd = sim.regs[rd]
    rr = sim.regs[rr]
    rd.value = rd.value ^ rr.value
    sim.leakage += [normalized_noisy_hamming_weight(rd.value, 0.1)]


@xmega_instruction('and')
def anl(sim: Simulator, rd: Register, rr: Register):
    """
    AND Rd, Rr
    Logical AND
    Rd ← Rd • Rr
    Z,N,V,S
    """
    rd = sim.regs[rd]
    rr = sim.regs[rr]
    rd.value = rd.value & rr.value
    sim.leakage += [normalized_noisy_hamming_weight(rd.value, 0.1)]


@xmega_instruction
def add(sim: Simulator, rd: Register, rr: Register):
    """
    ADD Rd, Rr
    Add without Carry
    Rd ← Rd + Rr
    Z,C,N,V,S,H
    """
    rd = sim.regs[rd]
    rr = sim.regs[rr]
    rd.value = rd.value + rr.value
    sim.leakage += [normalized_noisy_hamming_weight(rd.value, 0.1)]


@xmega_instruction
def ld(sim: Simulator, rd: Register, x: PointerRegister):
    """
    LD Rd, X
    Load Indirect
    Rd ← (X)
    None
    """
    rd = sim.regs[rd]
    x = sim.regs[x]
    rd.value = sim.memory[x.value]
    sim.leakage += [normalized_noisy_hamming_weight(rd.value, 0.01)]


@xmega_instruction
def st(sim: Simulator, x: PointerRegister, rr: Register):
    """
    ST X, Rr
    Store Indirect
    (X) ← Rr
    None
    """
    x = sim.regs[x]
    rr = sim.regs[rr]
    sim.memory[x.value] = rr.value
    sim.leakage += [normalized_noisy_hamming_weight(rr.value, 0.01)]


@xmega_instruction
def ldi(sim: Simulator, rd: Register, k: int):
    """
    LDI Rd, K
    Load Immediate
    Rd ← K
    None
    """
    if isinstance(k, str):
        k = int(k)
    rd = sim.regs[rd]
    rd.value = k
    sim.leakage += [normalized_noisy_hamming_weight(rd.value, 0.01)]


@xmega_instruction
def mov(sim: Simulator, rd: Register, rr: Register):
    """
    MOV Rd, Rr
    Copy Register
    Rd ← Rr
    """
    rd = sim.regs[rd]
    rr = sim.regs[rr]
    rd.value = rr.value
    sim.leakage += [normalized_noisy_hamming_weight(rd.value, 0.1)]


@xmega_instruction
def movw(sim: Simulator, rd: Register, rr: Register):
    """
    MOVW Rd, Rr
    Copy Register
    Pair
    Rd+1:Rd ← Rr+1:Rr
    None
    """
    rdplus = sim.regs['r%d' % (int(rd[1:]) + 1)]
    rrplus = sim.regs['r%d' % (int(rr[1:]) + 1)]
    rd = sim.regs[rd]
    rr = sim.regs[rr]
    rd.value = rr.value
    rdplus.value = rrplus.value
    sim.leakage += [
        normalized_noisy_hamming_weight(rd.value, 0.1),
        normalized_noisy_hamming_weight(rr.value, 0.1),
    ]


@xmega_instruction
def jmp(sim: Simulator, label: Label):
    """
    JMP k
    Jump
    PC ← k
    None
    """
    sim.pc.value = sim.program.labels[label]
