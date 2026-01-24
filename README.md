# The Norwegian TRS80 Model 100
PICTURE TBD

As you can see we could buy a real Norwegian versions of the TRS-80 Model 100 back in the day! All with the beautiful ÆØÅ characters and also being able to input the date in our native toung as DD/MM/YY. The logo **Tele** was the logo of our national phone company at the time. Custom mfd. in Japan for Tandy Corporation. 

As I was working on and documenting my simple program [M100Link](https://github.com/Warshi7819/M100Link) for transfering files to and from it I also learned that there is still quite the interest for these small machines and also the different nationalized versions. In this repository I will therefore try to store what I have learned/documented about my Norwegian: **Tele - Modell 100 - Bærbar Tekstterminal**. Which translates to: Tele - Model 100 - Portable Text Terminal. 

## Norwegian Packaging/Pamphlet
Larger scans of the Pamphlet (Get Started Guide) and pictures of the box is included in the images folder of this repository. 



## What Was Included?
The unit itself came in a nice box as detailed above. In the box I got the following was present:
* The Norwegian Get Started Guid (Pamphlet)
* The full TRS-80 Model 100 Manual from Tandy (English language)
* The needed cables to hook it up to the phone line of the time
* A Cassette - See section below.

## The Cassette
INFO GOES HERE


## ROM Dump
With the help of the people on the [M100 maling](http://lists.bitchin100.com/listinfo.cgi/m100-bitchin100.com) list I finally got my hands on a working script that outputs the entire ROM as a comma seperated list of bytes (0-255) over serial. The script (RDUMP.DO), the raw output (raw_output.txt) of the script and the hexified version (hex_version.txt) is available in the ROM folder. The hexified version was created by myself by reading each byte value into a python script and then outputing each byte value as hex pairs using the following conversion: **format(int(value), '02X')**.

The user B9 then helped me to convert the hex file to a rom file using the unix command **xxd -r -p  < output_hex.txt  > m100.norway.rom**. The resulting rom file (m100.norway.rom) can also be found in the ROM folder of this repository. 

```
10 REM ROM Dump Utility by Clinton Reddekop (January 2026)
20 REM    Dumps the contents of main ROM over serial
100 open "com:58N1E" for output as 1
120 sum=0
140 for a=0to32767
160 b=peek(a)
180 print #1,b;","
200 sum=sum+b
220 if sum>8192 then sum=sum-8192
240 next a
260 print #1,"sum=";sum
280 end
```
The script probably took close to 30 minutes to complete at 1200 bauds over serial. But I had to run it slow to ensure I didn't loose data during transfer. 

## VERSION INFO
**MODEL**: TRS-80 Modell 100

**SERIAL NO**: 409000149

CUSTOM MFD. IN JAPAN FOR TANDY CORPORATION 

**Tele**

**CAT NO**: 269-9101

**TV NR** 25-132-4248

**Tillatelse nr.**: 84/015

> [!NOTE]
> "Tillatelse nr." translates to Permit number. 

## IMAGES
I used the [PerspectiveFix](https://oathanrex.github.io/perspective-fix/) free online tool to create the traighten out images for the pamphlet. The original images are there as well if I at some point find a better free tool.
