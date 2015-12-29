#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Script to compute how to cut your beams in an optimal way
# if you need a collection of beams with a given length.
#
# See
# - https://en.wikipedia.org/wiki/Cutting_stock_problem
# - http://pastebin.com/1XPiBD20

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import argparse
import math

CUT_WIDTH = 0.125

beams = []
beams_total = 0.0
lengths = []
lengths_left = 0

instructions = []
summary = []

def cut():

    global lengths_left

    i = 0
    j = 0

    if lengths_left == 0:
        beams_remaining = sum([beam for beam in beams if not math.isnan(beam)])
        efficiency = 100.0 * (1 - beams_remaining / float(beams_total))

        summary.append("Beams remaining:")

        for elem, beam in enumerate(beams):
            if not math.isnan(beam):
                summary.append("Beam " + str(elem) + ": " + str(beam))

        summary.append("Total remaining " + str(beams_remaining) + " (" + str(efficiency) + " % efficiency)")

        return True

    while i < len(lengths):
        l = lengths[i]
        if not math.isnan(l):
            while j < len(beams):
                b = beams[j]
                if not math.isnan(b):
                    beam_remaining = b - l - CUT_WIDTH
                    if beam_remaining > 0.0:

                        lengths[i] = float("nan")
                        lengths_left -= 1

                        beams[j] = float("nan")
                        beams.append(beam_remaining)

                        beams_index_new = len(beams) - 1

                        if cut():
                            instructions.append("Cut beam " + str(j+1)
                                                + " of length " + str(b) + " to size " + str(l)
                                                + " (leaving beam " + str(beams_index_new)
                                                + " of length " + str(beam_remaining) + ")")
                            return True

                        beams.pop(len(beams) - 1)
                        lengths[i] = l
                        lengths_left += 1
                        beams[j] = b
                j += 1
        i += 1

    return False


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("zipfile", help="path to zipfile")
    # args = parser.parse_args()

    beam = 48
    lengths = [36.75, 36.5, 36.5, 26.25, 26.125, 22.5, 21, 20.5, 14.5, 9.25, 9, 6.5, 4]

    lengths = sorted(lengths, reverse=True)

    for length in lengths:
        if length > beam:
            print "Solution not possible!"
            print "Needed beam length", length, "greater than available beams of length", beam, "."
            sys.exit(0)

    lengths_total = sum(lengths)

    print "Lengths needed:"
    for length in lengths:
        print length
    print "Total:", lengths_total

    beams_needed = int(math.ceil(lengths_total/float(beam)))

    beams = [beam for i in range(0, beams_needed)]
    beams_total = sum(beams)

    print "Beams available:"
    for beam in beams:
        print beam
    print "Total:", beams_total

    print "Buy", beams_needed, "beams of length", beam, "."

    lengths_left = len(lengths)

    cut()

    for i,instruction in enumerate(reversed(instructions)):
        print "Cut", i+1, ":", instruction
    print ""

    for s in summary:
        print s

    print ""




