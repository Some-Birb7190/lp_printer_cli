<h1>A program to send ESC/POS commands to a usb device</h1>
<p>All this program (./pyprint) does is send out basic ESC/POS commands to a printer connected over usb, with the use of external libraries. </p><br>

<h2>Pre-Requisites</h2>
<p>For this program, you will need:</p>
<ul>
    <li>python-escpos - <a>https://github.com/python-escpos/python-escpos</a></li>
    <li>pyusb - <a>https://github.com/walac/pyusb</a></li>
    <li>Pillow - <a>https://github.com/python-pillow/Pillow</a></li>
    <li>python-qrcode - <a>https://github.com/lincolnloop/python-qrcode</a></li>
    <li>pyserial (for serial devices) - <a>https://github.com/lincolnloop/python-qrcode</a></li>
    <li>python-barcode - <a>https://github.com/WhyNotHugo/python-barcode</a></li>
</ul><br>
<p>Alternatively, you can run `pip install -f requirements.txt` and install everything listed above</p>

<h2>Usage</h2>
pyprint [-h] [-q] [-i] [-b] [-nc] Content

-h  : Displays the help message<br>
-q  : Encodes "Content" inside a QR code and prints it<br>
-i  : Takes a file path from "Content" to an image and print it (gets a bit dodgy with large images)<br>
-b  : Encodes "Content" inside a barcode (CODE128) and prints it. It will also print the encoded text below the code<br>
-nc : Pass to not carriage return and cut the paper after printing<br>
<br>
Content : The file/text you want to be printed/encoded<br>
<br>
<h2>notes</h2>
<ul>
    <li>By default, will just print out Content with standard line wrapping</li>
    <li>[-i] and [-q] cannot be passed at the same time, you cannot encode an image in a QR code</li>
    <li>[-i] and [-b] cannot be passed at the same time, you cannot encode an image in a Barcode</li>
    <li>[-b] and [-q] cannot be passed at the same time, you cannot print both off at once</li>
    <li>The max string length for barcodes is 8 characters</li>
    <li>If [-nc] is passed as well as [-q] or [-b], they will both override [-nc] as they require properly finishing the print</li>
</ul>
