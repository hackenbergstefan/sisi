#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from . import Instruction, Program, Label
from .xmega import XMegaSimulator
from .xmega_instruction_set import eor, add, ld, st, ldi, movw, nop, jmp
from .xmega_parser import XmegaParser


class InstructionTestCase(unittest.TestCase):

    def test_eor(self):
        a, b = 0x1b, 0x38

        sim = XMegaSimulator()
        r0, r1 = sim.regs['r0'], sim.regs['r1']
        r0.value = a
        r1.value = b
        sim.execute(Instruction(eor, 'r0', 'r1'))
        self.assertEqual(r0.value, a ^ b)

    def test_add(self):
        a, b = 0x1b, 0x38

        sim = XMegaSimulator()
        r0, r1 = sim.regs['r0'], sim.regs['r1']
        r0.value = a
        r1.value = b
        sim.execute(Instruction(add, 'r0', 'r1'))
        self.assertEqual(r0.value, (a + b) & 0xff)

    def test_ldi(self):
        sim = XMegaSimulator()
        r0 = sim.regs['r0']
        sim.execute(Instruction(ldi, 'r0', 0xAB))
        self.assertEqual(r0.value, 0xAB)

    def test_movw(self):
        sim = XMegaSimulator()
        sim.regs['r0'].value = 0x12
        sim.regs['r1'].value = 0x34
        sim.execute(Instruction(movw, 'r2', 'r0'))
        self.assertEqual(sim.regs['r2'].value, 0x12)
        self.assertEqual(sim.regs['r3'].value, 0x34)

    def test_pointer_registers(self):
        sim = XMegaSimulator()
        sim.regs['X'].value = 0x1234
        self.assertEqual(sim.regs['X'].value, 0x1234)
        self.assertEqual(sim.regs['r26'].value, 0x34)
        self.assertEqual(sim.regs['r27'].value, 0x12)


class MemoryTestCase(unittest.TestCase):

    def test_memory(self):
        sim = XMegaSimulator()
        addr = 0x0000
        sim.memory[addr] = 0x12
        sim.regs['X'].value = addr
        sim.execute(Instruction(ld, 'r0', 'X'))
        self.assertEqual(sim.regs['r0'].value, 0x12)

        sim.regs['r1'].value = 0xAB
        sim.execute(Instruction(st, 'X', 'r1'))
        self.assertEqual(sim.memory[addr], 0xAB)


class ProgramTestCase(unittest.TestCase):
    """Test Program functionalities."""

    def test_program(self):
        sim = XMegaSimulator()
        sim.execute(Program([
            Instruction(nop),
            Instruction(nop),
            Instruction(nop),
        ]))
        self.assertEqual(sim.pc.value, 3)

    def test_jmp(self):
        sim = XMegaSimulator()
        sim.execute(Program([
            Instruction(nop),
            Instruction(jmp, 'foobar'),
            Instruction(ldi, 'r0', 5),
            Label('foobar'),
            Instruction(nop),
        ]))
        self.assertEqual(sim.regs['r0'].value, 0)


class ProgramParserTestCase(unittest.TestCase):
    """Test ProgramParser."""

    def test_eor(self):
        prog = XmegaParser("""
            eor r0, r1
        """).parse()

        self.assertEqual(
            prog,
            [Instruction(eor, 'r0', 'r1')]
        )

    def test_nop(self):
        prog = XmegaParser("""
            nop
            nop
        """).parse()

        self.assertEqual(
            prog,
            [
                Instruction(nop),
                Instruction(nop),
            ]
        )

    def test_jmp(self):
        prog = XmegaParser("""
            nop
            jmp foobar
            ldi r0, 5
            foobar:
            nop
        """).parse()

        self.assertEqual(
            prog,
            [
                Instruction(nop),
                Instruction(jmp, 'foobar'),
                Instruction(ldi, 'r0', 5),
                Label('foobar'),
                Instruction(nop),
            ]
        )
