# The Norwegian TRS80 Model 100
PICTURE TBD
As you can see we could buy real Norwegian versions of the TRS-80 Model 100 back in the day! All with the beautiful ÆØÅ characters and also being able to input the date in our native toung as DD/MM/YY. The logo **Tele** was the logo of our national phone company at the time. 

As I was working on and documenting my simple program [M100Link](https://github.com/Warshi7819/M100Link) for transfering files to and from it I also learned that there is still quite the interest for these small machines and also the different nationalized versions. In this repository I will therefore try to store what I have learned/documented about my Norwegian: **Tele - Modell 100 - Bærbar Tekstterminal**. Which translates to: Tele - Model 100 - Portable Text Terminal. 

**MODEL**: TRS-80 Modell 100
**SERIAL NO**: 409000149
CUSTOM MFD. IN JAPAN FOR TANDY CORPORATION 

**Tele**
**CAT NO**: 269-9101
**TV NR** 25-132-4248
**Tillatelse nr.**: 84/015


## Norwegian Pamphlet/Packaging
AS part of the package when you bought this you got:
* A nicely nationalized packaging
* A Norwegian pamphlet - Get Started Guid
* The massive brick of a manual from Tandy (in English)
* Needed cables to hook it up to the phone lines of the time

Scan of the Pamphlet and pictures of the box is included in the images folder of this repository. 

## ROM Dump
With the help of the people on the [M100 maling](http://lists.bitchin100.com/listinfo.cgi/m100-bitchin100.com) list I finally got my hands on a working script that outputs the entire ROM as a comma seperated list of bytes (0-255) over serial. The script (RDUMP.DO), the raw output (raw_output.txt) of the script, the hexified version (hex_version.txt) and the ASCIIfied version (ascii_version.txt) is available in the ROM folder if you're curious like me. 

```
10 REM RAM Dump Utility by Clinton Reddekop (January 2026)
20 REM       Dumps the contents of RAM over serial
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
