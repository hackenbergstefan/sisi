#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
from . import Label, Instruction
from .xmega_instruction_set import instruction_by_name


"""
Parser for AVR listings.
"""


class XmegaParser(object):
    re_label = re.compile(r'\s*(?P<labelname>\w+):')
    """Regex matching a label."""
    re_instruction = re.compile(r'\s*(?P<ins>\w+)\s*(?P<args>.*)')
    """Regex matching an instruction."""

    def __init__(self, listing):
        self.listing = [line for line in listing.splitlines() if line.strip()]

    def parse(self):
        program = []
        for progline in self.listing:
            match = self.re_label.match(progline)
            if match:
                program += [Label(match.group('labelname'))]
                continue

            match = self.re_instruction.match(progline)
            if match:
                args = match.group('args')
                args = [arg.strip() for arg in args.split(',')] if args else []
                args = [int(arg) if arg.isdigit() else arg for arg in args]
                program += [Instruction(
                    instruction_by_name(match.group('ins')),
                    *args or []
                )]
        return program
