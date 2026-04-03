#include <stdio.h>
#include <stdlib.h>

/*
Written by Clinton Reddekop 2026.04.02 and shared on the TRS-80 M100 mailing list
(m100@bitchin100.com).

Thanks for the help!
*/

// BASIC keywords corresponding to tokens 0x80..0xff
const char* tokDecode[128] = {
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
};

static int readByteVal(FILE* ifp)
{
    int val;

    if (fscanf_s(ifp, "%x", &val) != 1)
    {
        return -1;
    }

    if (val > 0xff)
    {
        fprintf(stderr, "\n\nERROR hex value > 0xff\n");
        fclose(ifp);
        exit(-50);
    }

    return val;
}

int main(int argc, char** argv)
{
    if (argc < 2)
    {
        fprintf(stderr, "ERROR no filename given\n");
        return -1;
    }

    FILE* ifp = fopen(argv[1], "rb");
    if (!ifp)
    {
        fprintf(stderr, "ERROR couldn't open file '%s'\n", argv[1]);
        return -2;
    }


    // I don't know why this is here - skip it
    if (readByteVal(ifp) != 0x8d)
    {
        fprintf(stderr, "ERROR first hex value from file '%s' not 0x8d\n", argv[1]);
        return -3;
    }


    int val = -1;
    while (!feof(ifp) && !ferror(ifp))
    {
        // Read and discard 2 byte values -- address in memory of start of next line

        if ((val = readByteVal(ifp)) <= 0)    // == 0 marks end of BASIC file, < 0 error
        {
            break;
        }
        if ((val = readByteVal(ifp)) < 0)
        {
            break;
        }

        // Read line number -- 16-bit integer

        int lnLo = readByteVal(ifp);
        int lnHi = readByteVal(ifp);
        if (lnLo < 0 || lnHi < 0)
        {
            val = -1;
            break;
        }
        int ln = (lnLo & 0x0ff) | (lnHi << 8 & 0x0ff00);

        printf("%d", ln);

        // Read and detokenize line contents.  Line ends at a zero.

        while (!feof(ifp) && !ferror(ifp))
        {
            if ((val = readByteVal(ifp)) < 0)
            {
                break;
            }

            if (val == 0)   // end of line
            {
                printf("\n");
                break;
            }
            else
                if (val < 0x80)
                {
                    printf("%c", val);
                }
                else
                {
                    printf("%s", tokDecode[val - 0x80]);
                }
        }

        if (val < 0)
        {
            break;
        }
    }

    if (ferror(ifp))
    {
        fprintf(stderr, "\n\nERROR reading from file '%s'\n", argv[1]);
        fclose(ifp);
    }

    fclose(ifp);

    if (val != 0)
    {
        fprintf(stderr, "\n\nERROR reached end of file '%s' unexpectedly\n", argv[1]);
        return -4;
    }

    printf("\n");

    return 0;
}
