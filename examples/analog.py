#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gpiozero import MCP3008
from time import sleep




if __name__ == '__main__':
    pot = MCP3008(0)
    try:
        while True:

            print(round(pot.value*100,4))
            sleep(1)

    except KeyboardInterrupt:
        print("program closed after keyboard interrupt")
        exit()