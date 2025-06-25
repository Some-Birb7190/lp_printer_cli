#!/usr/bin/env python3
# Built mainly using https://github.com/python-escpos/python-escpos library

from escpos.printer import Usb
from escpos import exceptions
from PIL import Image
from pdf2image import convert_from_path
import argparse
import sys
import dotenv
import os

def image_gen(file): # The function to generate and scale the given image
    img = "" # Just to save me with this try and catch

    if file.format == "PPM": # For direct pillow images
        img = file

    else:
        try: # Try to set the image specified
            img = Image.open(file)
        except:
            device.close()
            raise Exception("Failed to find/load image")

    # Obtained image, great, get some info about it
    width, height = img.size

    # Convert the image to a standard RGB format
    img = img.convert('RGB')

    # Next, decide if it needs to be rotated and act accordingly
    if (width > height): # Longer side on printing edge?
        print("Rotating image...") 
        # Transpose the image and rotate it
        img = img.transpose(Image.ROTATE_90)
        # Rescale it
        width, height = height, width # Swap the axis

    # Doesn't matter if the image has been rotated, scale it
    dimensions = (int(width*(384/width)), int(height*(384/width)))
    edit = img.resize(dimensions)

    # Transformations are done, return the edited file
    return(edit)

def print_pdf(path, device): # Device has to be passed
    # Check that the path exists
    try: # Try to load the file
        images = convert_from_path(path) # Create a list of all the images
    except:
        device.close()
        raise Exception("Failed to load pdf from path")

    scaled_images = [] # Instanciate a list for all of the scaled images

    for x in range(0, len(images)): # Scale each of the images
        scaled_images.append(image_gen(images[x]))

    counter = 0
    for i in (scaled_images):
        print("Printing page " + str(counter+1))
        device.image(i)

        if (counter != (len(scaled_images) - 1)):
            device.cut()
            input("Tear paper and press enter to print next page...")
            counter += 1

def pre_print_init(action, content):
    VENDOR = (os.environ['ID_VENDOR'])
    PRODUCT = (os.environ['ID_PRODUCT'])
    INEP = (os.environ['IN_EP'])
    OUEP = (os.environ['OUT_EP'])

    # Try to initialise the device over usb
    device = Usb(idVendor=int(VENDOR, 16), idProduct=int(PRODUCT, 16), timeout=0, in_ep=int(INEP, 16), out_ep=int(OUEP, 16)) # try to find and initialize the printer, will fail with USBNotFoundError

    try:
        if (action == 1):
            device.image(image_gen(content), impl="bitImageRaster", fragment_height=128) # Creds to Sam.S for helping me with this

        elif (action == 2):
            device.qr(content=str(content), size=10, model=2)

        elif (action == 3):
            if (len(content) > 8):
                w = 2
            elif (len(content) > 5):
                w = 3
            else:
                w = 4
            device.barcode(code=str(content), bc="CODE128", function_type="B", height=64, width=w)

        elif (action == 4):
            print_pdf(content, device) # It's too complex to explain in a comment

        elif (action == 5):
            device.text(str(content) + "\n")

    finally: # Used so that the USB connection is always terminated, regardless of failure
        device.cut()
        device.close()        

def argument_parsing(): # The function to generate any given arguments
    parser = argparse.ArgumentParser(prog="pyprint.py", description="Program to print silly little things off on a silly little printer. By default will just print off \"Content\" as text.")
    parser.add_argument('-q', help="Print off a QR code encoded from Content", action='store_true')
    parser.add_argument('-i', help="Print off an image from the path of Content (beware of spaces in your file path)", action='store_true')
    parser.add_argument('-b', help="Print off a barcode (CODE128) encoded from Content", action='store_true')
    parser.add_argument('-p', help="Print off each page of a pdf file from the path of Content", action='store_true')
    parser.add_argument('-f', help="Print off a plain text file from the path of Content", action='store_true')
    # parser.add_argument('--align', help='Set the alignment for the text to print off', action='store_true') # WIP
    # parser.add_argument('-nc', help="Pass to not cut the paper after printing", action='store_true')
    parser.add_argument("Content", type=str, help="The file/text you want to print/encode")
    args = parser.parse_args()

    # Argument validation
    # Check that only one type of item is being printed at once
    argument_values = [] # Create a new list the value will go into

    # Just manually add all of them I don't know how to iteratively do this
    argument_values.append(str(args.q))
    argument_values.append(str(args.i))
    argument_values.append(str(args.b))
    argument_values.append(str(args.p))
    argument_values.append(str(args.f))

    # Does True show up more than once, if so, stop and alert the user, it can appear 0 times so cannot check !=, has to be >
    if (argument_values.count("True") > 1):
        raise Exception("Only one output type permitted")

    return(args)

# End of function definitions
# Get args
args = argument_parsing()

# Get printer values from .env file
config = dotenv.load_dotenv()

# Only one or no arguments should be true by this point
if (args.i is True): # Print an image
    pre_print_init(1, args.Content)

elif (args.q is True): # Print a QR code
    pre_print_init(2, args.Content)

elif (args.b is True): # Print a barcode
    pre_print_init(3, args.Content)

elif (args.p is True): # Print a PDF
    pre_print_init(4, args.Content)

else: # It's text/file, the user decides to cut it
    if (args.f is True):
        with open(args.Content, "r") as f:
            text = f.read()
            f.close()
    else:
        text = args.Content

    pre_print_init(5, text)

# Finish with a nice 0 exit code
sys.exit(0)
