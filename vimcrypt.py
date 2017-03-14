import sys
from random import randint

if not sys.stdin.isatty():
    input_file = sys.stdin
elif len(sys.argv) < 2:
    print("Usage: python vimcrypt.py <file to liberate>")
    exit()
else:
    try:
        input_file = open(sys.argv[1])
    except IOError:
        print("Couldn't find file: %s" % sys.argv[1])
        exit()

text_input = input_file.read()
#Validate input
for char in text_input:
    try:
        char.encode("ascii")
    # So we're compatible with python 2 and 3
    except (UnicodeDecodeError, UnicodeEncodeError):
        print("Input text must be ascii")
        exit()

out_bytes = bytearray()
for char in text_input:
    # Give each ascii byte some room to breathe by expanding it to 2-5 bytes randomly
    byte_count = randint(2,6)
    first = int("1"*byte_count + "0"*(8-byte_count), 2)
    out_bytes.append(first)

    # Append n-1 continuation bytes
    for _ in range(byte_count-1):
        out_bytes.append(0x80)
    out_bytes[-1] |= (ord(char) & 0b00111111)
    out_bytes[-2] |= (ord(char) & 0b11000000) >> 6

sys.stdout.write(out_bytes)
sys.stdout.flush()
sys.stdout.close()
