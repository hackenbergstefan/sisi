#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import Register, Simulator


"""The AVR instruction set."""


def update_status_regs(sim, res, flags='ZCNVSH'):
    if 'Z' in flags:
        sim.regs['Z'] = res == 0
    if 'C' in flags:
        sim.regs['C'] = res > 0xff


def eor(sim: Simulator, rd: Register, rr: Register):
    """
    EOR Rd, Rr Exclusive OR Rd ← Rd ⊕ Rr
    """
    rd.value = rd.value ^ rr.value
    update_status_regs(sim, rd.value)


def add(sim: Simulator, rd: Register, rr: Register):
    """
    ADD Rd, Rr
    Add without Carry
    Rd ← Rd + Rr
    Z,C,N,V,S,H
    """
    rd.value = res = rd.value + rr.value
    update_status_regs(sim, res)


def adc(sim: Simulator, rd: Register, rr: Register):
    """
    ADC Rd, Rr
    Add with Carry
    Rd ← Rd + Rr + C
    Z,C,N,V,S,H
    """
    rd.value = res = rd.value + rr.value + sim.regs['C']
    update_status_regs(sim, res)


def adiw(sim: Simulator, rd1: Register, rd: Register, k: int):
    """
    ADIW Rd, K
    Add Immediate to Word
    Rd + 1:Rd ← Rd + 1:Rd + K Z,C,N,V,S
    """
    rd.value = res = rd.value + k
    rd1.value = res = rd1.value + (res >> rd.number_of_bits)
    update_status_regs(sim, res >> rd.number_of_bits)
