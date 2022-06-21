<h1>A program to send ESC/POS commands to a usb device</h1>
<p>All this program (./pyprint) does is send out basic ESC/POS commands to a printer connected over usb, with the use of external libraries.<br>
It was made on and is designed for Linux as that is where the problem lay, I couldn't find a unified program to send things out to these printers...so I wrote my own.<br>
All my testing was done on a generic 58mm printer, nothing special, just something cheap off of Amazon. <b>Please do not submit issues saying it doesn't work with your printer, I won't know how to help.</b></p><br>

<h2>Pre-Requisites</h2>
<p>For this program, you will need:</p>
<ul>
    <li>Anything greater than Python 3 (made using Python 3.8.10)
    <li>pyusb - <a>https://github.com/walac/pyusb</a></li>
    <li>Pillow - <a>https://github.com/python-pillow/Pillow</a></li>
    <li>python-qrcode - <a>https://github.com/lincolnloop/python-qrcode</a></li>
    <li>pyserial (for serial devices) - <a>https://github.com/lincolnloop/python-qrcode</a></li>
    <li>python-barcode - <a>https://github.com/WhyNotHugo/python-barcode</a></li>
    <li>pdf2image - <a>https://github.com/Belval/pdf2image</a></li>
    <li>python-dotenv - <a>https://github.com/theskumar/python-dotenv/</a></li>
    <li>python-escpos - <a>https://github.com/python-escpos/python-escpos</a></li>
</ul><br>

<h2>Installation</h2>
<ol>
    <li>Clone repository</li>
    <ul>
        <li><p>Run "git clone https://git.birb.not.hpkns.uk/hbirb/lp_printer.git && cd lp_printer" OR "git clone https://github.com/Some-Birb7190/lp_printer.git && cd lp_printer"</p></li>
    </ul>
    <li>Install pre-requisites:</li>
    <ul>
        <li><p>You can do this manually by running "pip install pyusb", "pip install Pillow" etc, or run "pip install -r requirements.txt"</p></li>
    </ul>
    <li>Set up environmental variables</li>
    <ul>
        <li><p>First open .env.example and a terminal. Run "lsusb" and find the device you are using. You should have a like that looks like this:<br>
        "Bus 003 Device 085: ID 0416:5011 Winbond Electronics Corp. Virtual Com Port"<br>
        The number before the colon (EG 0416), place that after the "0x" on the line "ID_VENDOR" in ".env.example". The number after the colon (EG 5011) place after the "0x" on the next line down.</p></li>
        <li><p>Then in the terminal, run "lusb -v", this will give a long output so be prepared.<br>
        Find the device that matches the above credentials, and locate the line:<br>
        "bEndpointAddress     0x81  EP 1 IN" and make sure it's the line that says "IN". Place the value after the "0x" (EG 81) and place it after the "0x" in ".env.example", on the line "IN_EP"</p></li>
        <li></p>Next find the line that ends in "OUT", EG:<br>
        "bEndpointAddress     0x03  EP 3 OUT", and place the value after the "0x" (EG 03) on the last line of ".env.example"</p></li>
        <li><p>Finally, remove the ".example" off the end of the file, and you should be good to go</p></li>
    </ul>
    <li>Enable certain permissions</li>
    <ul>
        <li><p>Because you are accessing the USB kernel on Linux, you need certain permissions.<br>
        So in a terminal, run "sudo usermod -a -G lp [username]" which should do the trick.</p></li>
    </ul>
    <li>(Optionally) install globally</li>
    <ul>
        <li><p>If you are indeed on a Linux system, then you can install this mini program globally.<br>
        Run "sudo ln -s /path/to/pyprint /usr/local/bin/pyprint && sudo ln -s /path/to/.env /usr/local/bin/.env"<br>
        This will create two symlinks directly to the pyprint program and the .env file. If you move the source files though, the link will break and you will have to redo it.</p></li>
    </ul>
    <li>Follow Usage steps</li>
</ol><br>


<h2>Usage</h2>
pyprint [-h] [-q] [-i] [-b] [-p] [-f] [-nc] Content<br>
<br>
-h  : Displays the help message<br>
-q  : Encodes "Content" inside a QR code and prints it<br>
-i  : Takes a file path from "Content" to an image, re-scales it to fit on 384px wide paper (and rotates if necessary) and prints it accordingly (goes haywire if the height of the original image is very small comparatively to the width.)<br>
-b  : Encodes "Content" inside a barcode (CODE128) and prints it. It will also print the encoded text below the code<br>
-p  : Takes a file path from "Content" to a pdf, converts all the pages and recursively prints them with the above image feature<br>
-f  : Take a plain text file path from "Content" and prints it out with standard line wrapping<br>
-nc : Pass to not carriage return and cut the paper after printing<br>
<br>
Content : The file/text you want to be printed/encoded<br>
<br>

<h2>Notes</h2>
<ul>
    <li>By default, will just print out Content with standard line wrapping</li>
    <li>You can only print off one thing at once, passing multiple flags will throw an error</li>
    <li>The max string length for barcodes is 8 characters (for 58mm paper)</li>
    <li>If [-nc] is passed as well as the optional flags ([-q], [-i], [-b], [-p]), they will all override [-nc] as they require properly finishing the print</li>
    <li>./(PYUSB)_usb_receipt_printer_demo.py and ./lp_printer.py are both programs written to test stuff, use at your own risk, I provide no documentation for them</li>
    <li>Printing an image or pdf requires permissions to read/write in the folder you are executing "pyprint" from due to temporary file writing when re-scaling the image you are printing.</li>
</ul><br>

<h2>Some final words</h2>
<p>I am a student, my programming skills are obviously not going to be perfect and the code I have written...isn't great and is mostly copy pasted from other sources but hey, it works for me and I thought that I'd share it with the world and see if it helps anyone else.<br>
That being said, I do permit anyone to use this code for inspiration or to help them with whatever they need, if it works then who am I to complain; I couldn't find anything like this when I needed it, so I solved the problem myself and in the process hopefully saving some time for others.</p>  
