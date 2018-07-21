#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random


HAMMING_WEIGHT = [bin(i).count('1') for i in range(256)]


def hamming_weight(x):
    return HAMMING_WEIGHT[x]


def normalized_hamming_weight(x):
    return (HAMMING_WEIGHT[x] - 4.0) / 4.0


def normalized_noisy_hamming_weight(x, noise_strength):
    return normalized_hamming_weight(x) + (random.random() - 0.5) * noise_strength


class Simulator(object):

    def __init__(self):
        self.leakage = []

    def execute(self, ins):
        if isinstance(ins, list):
            [i.execute(self) for i in ins]
        else:
            ins.execute(self)


class ListingParser(object):

    def __init__(self, lstinput):
        self.parse(lstinput)


class Register(object):

    def __init__(self, name):
        self.value = 0
        self.name = name

    def __setattr__(self, name, value):
        if name == 'value':
            value &= self.max_val
        super().__setattr__(name, value)

    def __repr__(self):
        fmt = '0%dx' % (self.number_of_bits // 4)
        return ('<{} value=0x{:%s}>' % fmt).format(self.__class__.__name__, self.value)


class Register1(Register):
    """1bit register"""
    number_of_bits = 1
    max_val = 1


class Register8(Register):
    """8bit register"""
    number_of_bits = 8
    max_val = 0xff


class Instruction(object):

    def __init__(self, operation, *operands):
        # self.text = text
        self.operation = operation
        self.operands = operands

    def execute(self, sim):
        self.operation(sim, *self.operands)
