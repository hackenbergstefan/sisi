#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from . import Register, Simulator, hamming_weight
from .xmega import PointerRegister


"""The AVR instruction set."""


def nop(sim: Simulator):
    """
    NOP
    """
    sim.leakage += [0]


def eor(sim: Simulator, rd: Register, rr: Register):
    """
    EOR Rd, Rr Exclusive OR Rd ← Rd ⊕ Rr
    """
    rd.value = rd.value ^ rr.value
    sim.leakage += [hamming_weight(rd.value)]


def anl(sim: Simulator, rd: Register, rr: Register):
    """
    AND Rd, Rr
    Logical AND
    Rd ← Rd • Rr
    Z,N,V,S
    """
    rd.value = rd.value & rr.value
    sim.leakage += [hamming_weight(rd.value)]


def add(sim: Simulator, rd: Register, rr: Register):
    """
    ADD Rd, Rr
    Add without Carry
    Rd ← Rd + Rr
    Z,C,N,V,S,H
    """
    rd.value = rd.value + rr.value
    sim.leakage += [hamming_weight(rd.value)]


def ld(sim: Simulator, rd: Register, x: PointerRegister):
    """
    LD Rd, X
    Load Indirect
    Rd ← (X)
    None
    """
    rd.value = sim.memory[x.value]
    sim.leakage += [hamming_weight(rd.value)]


def st(sim: Simulator, x: PointerRegister, rr: Register):
    """
    ST X, Rr
    Store Indirect
    (X) ← Rr
    None
    """
    sim.memory[x.value] = rr.value
    sim.leakage += [hamming_weight(rr.value)]


def ldi(sim: Simulator, rd: Register, k: int):
    """
    LDI Rd, K
    Load Immediate
    Rd ← K
    None
    """
    rd.value = k
    sim.leakage += [hamming_weight(rd.value)]

def mov(sim: Simulator, rd: Register, rr: Register):
    """
    MOV Rd, Rr
    Copy Register
    Rd ← Rr
    """
    rd.value = rr.value
    sim.leakage += [hamming_weight(rd.value)]

def add(sim: Simulator, rd: Register, rr: Register):
    """
    ADD Rd, Rr
    Add without Carry
    Rd ← Rd + Rr
    Z,C,N,V,S,H
    """
    rd.value += rr.value
    # sim.leakage += [hamming_weight(rd.value)]
