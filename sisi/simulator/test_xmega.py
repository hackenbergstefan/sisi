#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from . import Instruction, hamming_weight
from .xmega import XMegaSimulator
from .xmega_instruction_set import eor, add, ld, st, ldi


class SimpleTestCase(unittest.TestCase):

    def test_eor(self):
        a, b = 0x1b, 0x38

        sim = XMegaSimulator()
        r0, r1 = sim.regs['r0'], sim.regs['r1']
        r0.value = a
        r1.value = b
        sim.execute(Instruction(eor, r0, r1))
        self.assertEqual(r0.value, a ^ b)
        self.assertEqual(sim.leakage, [hamming_weight(a ^ b)])

    def test_add(self):
        a, b = 0x1b, 0x38

        sim = XMegaSimulator()
        r0, r1 = sim.regs['r0'], sim.regs['r1']
        r0.value = a
        r1.value = b
        sim.execute(Instruction(add, r0, r1))
        self.assertEqual(r0.value, (a + b) & 0xff)

    def test_ldi(self):
        sim = XMegaSimulator()
        r0 = sim.regs['r0']
        sim.execute(Instruction(ldi, r0, 0xAB))
        self.assertEqual(r0.value, 0xAB)

    def test_pointer_registers(self):
        sim = XMegaSimulator()
        sim.regs['X'].value = 0x1234
        self.assertEqual(sim.regs['X'].value, 0x1234)
        self.assertEqual(sim.regs['r26'].value, 0x34)
        self.assertEqual(sim.regs['r27'].value, 0x12)

    def test_memory(self):
        sim = XMegaSimulator()
        addr = 0x0000
        sim.memory[addr] = 0x12
        sim.regs['X'].value = addr
        sim.execute(Instruction(ld, sim.regs['r0'], sim.regs['X']))
        self.assertEqual(sim.regs['r0'].value, 0x12)

        sim.regs['r1'].value = 0xAB
        sim.execute(Instruction(st, sim.regs['X'], sim.regs['r1']))
        self.assertEqual(sim.memory[addr], 0xAB)
