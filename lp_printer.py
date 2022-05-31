#!/bin/env python3
# a program to take a thing and print it out to a printer

import os
import argparse
import sys

# generate a parser for any command line arguments to be passed 
parser = argparse.ArgumentParser(description="A program to attempt to print to a reciept printer.")
parser.add_argument('-f', default='/dev/usb/lp0', help="Where the printer is located.")
args= parser.parse_args()

if (args.f == "/dev/usb/lp0"):
    print("No printer specified, defaulting to /dev/usb/lp0.")

# a while loop to constantly take the users input and echo it to the printer
while True:
    unput = input()
    if (unput == "0"):
        for x in range(0,2):
            os.system("sudo echo \"\" > " + str(args.f))
        sys.exit(0)
    else:
        os.system("sudo echo \"" + str(unput) + "\" > " + str(args.f))