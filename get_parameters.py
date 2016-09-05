# -*- coding: utf-8 -*-

import sys
import math


def main(arguments):
    r = float(arguments[0])
    x = float(arguments[1])
    yp = math.sqrt(r*r - x*x)
    ym = -math.sqrt(r*r - x*x)
    print("y+: {}".format(yp))
    print("y-: {}".format(ym))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
