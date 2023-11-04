#!/bin/env python3
# Built mainly using https://github.com/python-escpos/python-escpos library

from escpos.printer import Usb
from PIL import Image
from pdf2image import convert_from_path
import argparse
import sys
import dotenv
import os
# import time

# Below are some functions that just make the code look nicer and make different sections more obvious

def image_gen(file): # The function to generate and scale the given image
    img = "" # Just to save me with this try and catch

    if file.format == "PPM": # If the argument passed *is* a pillow image itself, then we don't need to try to load it from a path
        img = file

    else:
        try: # Try to set the image specified
            img = Image.open(file)
        except:
            print("Failed to print specified image")
            device.close()
            sys.exit(1) # A generic non 0 exit code

    # Obtained image, great, get some info about it
    width, height = img.size
    
    # Convert the image to a standard RGB format
    img = img.convert('RGB')

    # Next, decide if it needs to be rotated and act accordingly
    if (width > height): # Is the width of the image longer?
        print("Rotating image...") # The longer side should be the height, so it needs to be rotated
        # Transpose the image and rotate it
        img = img.transpose(Image.ROTATE_90)
        # Rescale it
        width, height = height, width # The image has been rotated, swap the axis

    # Doesn't matter if the image has been rotated, scale it 
    dimensions = (int(width*(384/width)), int(height*(384/width))) 
    edit = img.resize(dimensions)

    ''' I'm keeping this code for testing
    else: # it does not need rotating, just scale it
        dimensions = (int(width*(384/width)), int(height*(384/width))) 
        edit = img.resize(dimensions)
    '''
    # Transformations are done, return the edited file
    return(edit) #return the image object and then just print that off
    

def print_pdf(path):
    # Check that the path exists
    try: # Try to load the file 
        images = convert_from_path(path) # Create a list of all the images
    except:
        print("Failed to load file from Path, check you entered it correctly.")
        device.close()
        sys.exit(1) 

    scaled_images = [] # Instanciate a list for all of the scaled images
    
    for x in range(0, len(images)): # Run through each of the images and scale them
        scaled_images.append(image_gen(images[x])) 
 
    counter = 0 # A counter to help count 
    for i in (scaled_images): # For each individual item in the list of scaled images
        print("Printing page " + str(counter+1))# Tell the user which page it is printing based off of the counter
        device.image(i) # This is an image type, therefore it can just print it 
        device.cut()

        if (counter != (len(scaled_images) - 1)):
            input("Tear paper and press enter to print next page...")
            counter += 1

def argument_parsing(): # The function to generate any given arguments
    parser = argparse.ArgumentParser(prog="pyprint.py", description="Program to print silly little things off to silly little printer. By default will just print off Content.")
    parser.add_argument('-q', help="Print off a QR code of the Content", action='store_true')
    parser.add_argument('-i', help="Print off an image from the path of Content (can be a bit dodgy)", action='store_true')
    parser.add_argument('-b', help="Print off a barcode (CODE128) of Content (Can be a bit dodgy)", action='store_true')
    parser.add_argument('-p', help="Print off each page of a pdf file from the path of Content", action='store_true')
    parser.add_argument('-f', help="Print off a plain text file from the path of Content", action='store_true')
    # parser.add_argument('--align', help='Set the alignment for the text to print off', action='store_true')
    parser.add_argument('-nc', help="Pass to not cut the paper after printing", action='store_true')
    parser.add_argument("Content", type=str, help="The file/text you want to print/encode")
    args = parser.parse_args()

    # Argument validation
    # somehow check that only one type of item is being printed at once
    argument_values = [] # Create a new list the value will go into

    # Just manually add all of them I don't know how to iteratively do this
    argument_values.append(str(args.q))
    argument_values.append(str(args.i))
    argument_values.append(str(args.b))
    argument_values.append(str(args.p))
    argument_values.append(str(args.f))

    # Does True show up more than once, if so, stop and alert the user, it can appear 0 times so cannot check !=, has to be >
    if (argument_values.count("True") > 1):
        print("You cannot print multiple types of things at once.")
        sys.exit(1) # A generic non 0 exit code

    return(args)


# End of function definitions

# Get args
args = argument_parsing()

# Get printer values from .env file
config = dotenv.load_dotenv(dotenv.find_dotenv())
VENDOR=(os.environ['ID_VENDOR'])
PRODUCT=(os.environ['ID_PRODUCT'])
INEP=(os.environ['IN_EP'])
OUEP=(os.environ['OUT_EP'])

# Try to initialise the device over usb
device = "" # Just for this try and catch

try:
    device = Usb(idVendor=int(VENDOR, 16), idProduct=int(PRODUCT, 16), timeout=0, in_ep=int(INEP, 16), out_ep=int(OUEP, 16)) # try to find and initialize the printer

except: # This may happen due to incorrect parameters for the printer, or it is not online/plugged in
    print("Failed to initialize the printer, check it's plugged in and your parameters are set correctly.")
    sys.exit(1)

# Only one or no arguments should be true by this point
# I am sorry for people reading this, python does not have backwards compatible and nice to use switch blocs
if (args.i == True): 
    device.image(image_gen(args.Content), impl="bitImageRaster", fragment_height=128) # Print the image generated directly from the function. Creds to Sam.S for helping me with this
    device.cut()

elif (args.q == True): # Print a QR code
    device.qr(content=str(args.Content), size=10, model=2)
    device.cut()

elif (args.b == True): # Print a barcode
    if (len(args.Content) > 5):
        w = 3
    else:
        w = 4
    device.barcode(code=str(args.Content), bc="CODE128", function_type="B", height=64, width=w)
    device.cut()

elif (args.p == True): # Print a PDF
    print_pdf(args.Content) # Look at the function, it's too complex to explain simply

# elif (args.f == True): # Print a plain text file

#     device.cut()

else: # By this point, it's either text or a file, both of which the user can decide if they want to cut it

    if (args.f == True):
        with open(args.Content, "r") as f:
            text = f.read()
            f.close()
    else:
        text = args.Content
        
    device.text(str(text) + "\n")

    # End with carriage returning and cutting the paper if the user wants it
    if (args.nc == False):
        device.cut()

# Reset the alignment
# device.set(align='LEFT')

# Ensure to close the USB endpoint
device.close()

# Finish with a nice 0 exit code
sys.exit(0)