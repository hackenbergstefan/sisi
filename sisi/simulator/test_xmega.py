#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from . import Instruction
from .xmega import XMegaSimulator
from .xmega_instruction_set import eor, add, adc, adiw


class SimpleTestCase(unittest.TestCase):

    def test_eor(self):
        a, b = 0x1b, 0x38

        sim = XMegaSimulator()
        r0, r1 = sim.regs['r0'], sim.regs['r1']
        r0.value = a
        r1.value = b
        sim.execute(Instruction(eor, r0, r1))
        self.assertEqual(r0.value, a ^ b)

    def test_add(self):
        a, b = 0x1b, 0x38

        sim = XMegaSimulator()
        r0, r1 = sim.regs['r0'], sim.regs['r1']
        r0.value = a
        r1.value = b
        sim.execute(Instruction(add, r0, r1))
        self.assertEqual(r0.value, (a + b) & 0xff)

    def test_adc(self):
        a, b = 0xff, 0x01

        sim = XMegaSimulator()
        r0, r1 = sim.regs['r0'], sim.regs['r1']
        r0.value = a
        r1.value = b
        sim.execute(Instruction(add, r0, r1))
        self.assertEqual(r0.value, (a + b) & 0xff)
        sim.execute(Instruction(adc, r0, r1))
        self.assertEqual(r0.value, (a + b + 1 + b) & 0xff)

    def test_adiw(self):
        k = 0xf3

        sim = XMegaSimulator()
        r24, r25 = sim.regs['r24'], sim.regs['r25']
        sim.execute(Instruction(adiw, r25, r24, k))
        self.assertEqual(r24.value + (r25.value << r24.number_of_bits), k)
        sim.execute(Instruction(adiw, r25, r24, k))
        self.assertEqual(r24.value + (r25.value << r24.number_of_bits), k + k)
