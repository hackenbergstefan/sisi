#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import Simulator, Register8, Register


class PointerRegister(Register):
    number_of_bits = 16
    max_val = 0xffff

    def __init__(self, name, rd, rdplus):
        self.regs = [rd, rdplus]
        super().__init__(name)

    @property
    def value(self):
        return (self.regs[1].value << 8) | self.regs[0].value

    @value.setter
    def value(self, value):
        self.regs[0].value = value & 0xff
        self.regs[1].value = value >> 8


class XMegaSimulator(Simulator):

    def __init__(self):
        """Create 32 8bit registers and 3 PointerRegisters."""
        super().__init__()
        self.regs = {'r%d' % i: Register8('r%d' % i) for i in range(32)}
        self.regs['X'] = PointerRegister('X', self.regs['r26'], self.regs['r27'])
        self.regs['Y'] = PointerRegister('Y', self.regs['r28'], self.regs['r29'])
        self.regs['Z'] = PointerRegister('Z', self.regs['r30'], self.regs['r31'])
        self.memory = dict()
