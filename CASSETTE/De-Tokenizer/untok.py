#############################################################################
# Application : untok - De-Tokenize BASIC script for the TRS-80 M100        #
#  * Input should be a hex dump of the tokenized script                     #
#                                                                           #
# Implemented based on the GREAT work of Clinton Reddekop and his untok     #
# program. + the feedback of HackerB9. Without that blueprint code I would  #
# have spent ages trying to understand this myself. Especially how          #
# to extract the line numbers...                                            #
#                                                                           #
# The main difference between this program and Clinton's untok program      #
# written in C is that this program handles the following special cases:    #
# 1) Don't try to detokenize inside quotes.                                 #
# 2) Handle the special case of the single quote character that is          #
#  expanded to three characters when tokenized (:REM').                     #
#                                                                           #
# File: untok.py                                                            #
# Author      : Retro & Gaming (2026)                                       #
# Date        : 15:32 2026.04.03                                            #
#############################################################################
#                                                                           #
# https://github.com/Warshi7819/TRS80-M100-Norwegian                        #
#                                                                           #
#############################################################################

# Refs:
# - http://justsolve.archiveteam.org/wiki/Tandy_200_BASIC_tokenized_file

# Python Modules
import argparse

# 3rd Party Modules

# Own Modules

#############################################################################

class DeTokenizer:
    def __init__(self):
        """
        Class constructor. Init the list of special tokens and some control logic vars.
        """

        self.tokens = [
            "END",      "FOR",      "NEXT",     "DATA",     "INPUT",    "DIM",      "READ",     "LET",
            "GOTO",     "RUN",      "IF",       "RESTORE",  "GOSUB",    "RETURN",   "REM",      "STOP",
            "WIDTH",    "ELSE",     "LINE",     "EDIT",     "ERROR",    "RESUME",   "OUT",      "ON",
            "DSKO$",    "OPEN",     "CLOSE",    "LOAD",     "MERGE",    "FILES",    "SAVE",     "LFILES",
            "LPRINT",   "DEF",      "POKE",     "PRINT",    "CONT",     "LIST",     "LLIST",    "CLEAR",
            "CLOAD",    "CSAVE",    "TIME$",    "DATE$",    "DAY$",     "COM",      "MDM",      "KEY",
            "CLS",      "BEEP",     "SOUND",    "LCOPY",    "PSET",     "PRESET",   "MOTOR",    "MAX",
            "POWER",    "CALL",     "MENU",     "IPL",      "NAME",     "KILL",     "SCREEN",   "NEW",
            "TAB(",     "TO",       "USING",    "VARPTR",   "ERL",      "ERR",      "STRING$",  "INSTR",
            "DSKI$",    "INKEY$",   "CSRLIN",   "OFF",      "HIMEM",    "THEN",     "NOT",      "STEP",
            "+",        "-",        "*",        "/",        "^",        "AND",      "OR",       "XOR",
            "EQV",      "IMP",      "MOD",      "\\",       ">",        "=",        "<",        "SGN",
            "INT",      "ABS",      "FRE",      "INP",      "LPOS",     "POS",      "SQR",      "RND",
            "LOG",      "EXP",      "COS",      "SIN",      "TAN",      "ATN",      "PEEK",     "EOF",
            "LOC",      "LOF",      "CINT",     "CSNG",     "CDBL",     "FIX",      "LEN",      "STR$",
            "VAL",      "ASC",      "CHR$",     "SPACE$",   "LEFT$",    "RIGHT$",   "MID$",     "'",
        ]

        self.firstValue = True
        self.lineChar = -1
        self.bytesList = []
        self.insideQuotes = False

        # When tokenizing, the single quote character expands to three characters: a colon (3A), the byte for REM (8E), and then FF.
        # When detokenizing a stream, we need to buffer and check for this pattern and convert it back to a single quote character.
        # REF: http://justsolve.archiveteam.org/wiki/Tandy_200_BASIC_tokenized_file
        self.tokenizeBuffer = []

    def detokenize(self, hexValue):
        """
        As we stream the file from disk, every hex value is passed to this function.
        The method will return the appropriate detokenized value(s) to be printed.
        """

        # check if files start with 0x8D. if so, discard it. This is probably a stray 
        # token from the wav2cas processing because the header is not recognized.
        # Probably not a common problem for real tokenized BASIC scripts.
        if self.firstValue:
            self.firstValue = False
            if hexValue == 0x8D:
                return ""

        # Line char count used to figure out if we
        # are going to save up data for the line number or not.  
        self.lineChar += 1

        # Check if we are on a new line, then we need to extract the line number. 
        # First two hex values can be discarded (This is the address in RAM of the next line of BASIC; unsigned 16-bit integer, little-endian.).
        # Then the next two hex values will contain the line number (unsigned 16-bit integer, little-endian.)
        if self.lineChar < 4:
            if self.lineChar == 2:
                self.bytesList.append(hexValue)
            if self.lineChar == 3:
                self.bytesList.append(hexValue)
                lineNumber = str(int.from_bytes(self.bytesList, byteorder='little'))
                self.bytesList = []
                return  lineNumber + " " # Not sure if you should add a space after line num in all cases but it does make my example files look better at least...
            else:
                return ""     

        # We need to buffer hex values so that we can handle the :REM' pattern correctly.
        self.tokenizeBuffer.append(hexValue)

        # We need to handle that special case of the single quote character that is expanded to 
        # three characters when tokenized (:REM').
        if hexValue == 0x3A:
            if len(self.tokenizeBuffer) == 1:
                return ""
        elif hexValue == 0x8E:
            if len(self.tokenizeBuffer) == 2:
                return ""
        elif hexValue == 0xFF:
            if len(self.tokenizeBuffer) == 3:
                # Special sequence recognized (3A 8E FF), flush the buffer and return the 
                # single quote character '.
                self.tokenizeBuffer = []
                return "'"
        
        # Flush the buffer to output
        return self.flushBuffer()


    def flushBuffer(self):
        """
        Method to flush the current buffer to output. 
        """

        # Handle the normal detokenization. The buffer may contain only one char, or several chars.
        returnString = ""
        for hexValue in self.tokenizeBuffer:
            # Check if we are inside quotes, if so we should not try to detokenize anything until we reach the closing quote.
            if hexValue == 0x22 and not self.insideQuotes:
                self.insideQuotes = True
            elif self.insideQuotes:
                if hexValue == 0x22:
                    self.insideQuotes = False

            # Normal Line content:
            # If the hexvalue is 0x80 or higher, we should have a special token for it! 
            # Unless we are inside quotes that is.
            if hexValue >= 0x80 and not self.insideQuotes:
                returnString += self.tokens[hexValue - 0x80]
            elif hexValue == 0x00:
                # We have a new line!
                self.lineChar = -1
                self.insideQuotes = False # A special case is that the line can end without a closing quote and still be valid syntax. Need to handle that.
                returnString += "\n"
            else:
                # If less than 0x80 or inside quotes we just try to convert it to a char.
                returnString += chr(hexValue)

        self.tokenizeBuffer = []
        return returnString


# Main program entry point.
if __name__ == "__main__":
    # Parse command line arguments to get input file.
    parser = argparse.ArgumentParser(description="De-Tokenize the given file of hex.")
    parser.add_argument(
        "-f", "--filename",
        type=str,
        required=True,
        help="Path to the input file"
    )
    args = parser.parse_args()

    # Setup the DeTokenizer and do the work.
    detok = DeTokenizer()
    with open(args.filename, 'r') as f:
        for line in f:
            hexValues =line.strip().split()
            for hexValue in hexValues:
                print(detok.detokenize(int(hexValue, 16)), end="")

    # Flush buffer at the end as it might still contain data.
    print(detok.flushBuffer(), end="")