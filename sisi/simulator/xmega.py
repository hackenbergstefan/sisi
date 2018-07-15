#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import Simulator, Register8


class XMegaSimulator(Simulator):

    def __init__(self):
        self.regs = {'r%d' % i: Register8() for i in range(32)}
        """Create 32 8bit registers."""
