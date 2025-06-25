# pyprint
All `pyprint` does is send out ESC/POS commands to a receipt printer connected over USB.  
It was made on and is designed for Linux as that is where the problem lay, I couldn't find a unified program to send things out to these printers...so I wrote my own. **I will not provide help for people who wish to use this on Windows.**  
All my testing was done on a generic 58mm printer, nothing special, just something cheap off of Amazon. Please do not submit issues saying it doesn't work with your printer, I won't know how to help. **Please only submit issues that are related to the code.**  
  
## Pre-Requisites  
For this program, you will need:  
- Anything greater than Python 3 (made using Python 3.8.10, tested on 3.6.15)
- pyusb - https://github.com/walac/pyusb  
- Pillow - https://github.com/python-pillow/Pillow  
- python-qrcode - https://github.com/lincolnloop/python-qrcode  
- pyserial - https://github.com/pyserial/pyserial  
- python-barcode - https://github.com/WhyNotHugo/python-barcode  
- pdf2image - https://github.com/Belval/pdf2image  
- python-dotenv - https://github.com/theskumar/python-dotenv/  
- python-escpos - https://github.com/python-escpos/python-escpos (Versions above 2.2.0 do not work)  
  
## Installation  
1. Clone repository:  
    - Run `git clone https://github.com/Some-Birb7190/lp_printer_cli.git && cd lp_printer_cli`  
2. Install pre-requisites:  
    - Run `pip install -r requirements.txt`  
3. Set up environment variables:
    - First open .env.example and a terminal. Run `lsusb` and find the device you are using. You should have a list that looks something like this (below is what my output looks like for my printer, yours will potentially be different):  
    "Bus 003 Device 085: ID 0416:5011 Winbond Electronics Corp. Virtual Com Port"  
    The number before the colon (EG 0416), place that after the "0x" on the line "ID_VENDOR" in `.env.example`. The number after the colon (EG 5011) place after the "0x" on the next line down  
    - Then in the terminal, run `lsusb -v`, this will give a long output so be prepared.  
    Find the device that matches the above credentials, and locate the line:  
    `bEndpointAddress     0x81  EP 1 IN`. Place the value after the "0" (EG 81) and place it after the "0x" in `.env.example`, on the line "IN_EP"  
    - Next find the line that ends in "OUT", EG:  
    `bEndpointAddress     0x03  EP 3 OUT`, and place the value after the "0x" (EG 03) on the last line of `.env.example`  
    - Finally, remove the ".example" off the end of the file
4. Enable certain permissions:  
    - Because you are accessing the USB socket on Linux, you need certain permissions.  
    So in a terminal, run "sudo usermod -a -G lp [your username]" (don't forget to log out and log back in for this change to take effect)  
    - In order to run this program, you must run "chmod +x /path/to/pyprint.py" to make it executable  
5. Install globally (optional):  
    - Assuming you are on a Linux system, then you can install this program globally.  
    Run "sudo ln -s /path/to/pyprint.py /usr/local/bin/pyprint && sudo ln -s /path/to/.env /usr/local/bin/.env"  
    This will create two symlinks directly to the pyprint program and the .env file. If you move the source files though, the link will break and you will have to re-run that code with the new absolute path. Try make sure they are in a place where they won't get in the way to avoid this issue  
6. Follow usage  

## Usage  
`pyprint.py [-h | -q | -i | -b | -p | -f] Content`
  
| Flags | Description                                                                                                             |  
|-------|-------------------------------------------------------------------------------------------------------------------------|  
| -h    | Displays the help message                                                                                               |  
| -q    | Encodes "Content" inside a QR code and prints it                                                                        |  
| -i    | Takes a file path from "Content" to an image, re-scales it to fit on 384px (58mm) wide paper (and rotates if necessary) |  
| -b    | Encodes "Content" inside a barcode (CODE128) and prints it. It will also print the encoded text below the code          |  
| -p    | Takes a file path from "Content" to a pdf, converts all the pages and prints them with the above image feature          |  
| -f    | Takes a plain text file path from "Content" and prints it out with standard line wrapping                               |  
|Content| The file/text you want to be printed/encoded                                                                            |  
  
## Acknowledgements  
- Creds to Sam.S from my computer science class for helping me figure out the image issue.  
