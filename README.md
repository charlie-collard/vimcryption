# vimcryption
Liberating ASCII characters from their cramped 1-byte prisons by abusing vim's incorrect UTF-8 decoding.

Simply pipe the script some ascii text to balloon it up to, on average, 3.5x the size! If this isn't enough for you, as an added bonus only other vim users will be able to read it. Bask in the smugness that can only come from using standard-defying software.

## Usage
`(python2 | python3) vimcrypt.py inputfile > outputfile && vim outputfile`

`some-command | (python2 | python3) vimcrypt.py > outputfile && vim outputfile`

## How?
UTF-8 encodes codepoints in the following way (using 🍓 U+1F353 as an example)

* If the codepoint is < 128 (ASCII), simply encode it as such.
* Otherwise, taking your codepoint as bits, fill in the gaps in the following pattern from the right:

> 10------ 10------ 10------ 10------ 10------
>
> 0x1F353 == **11111001101010011**
>
> 10------ 10------ 10-**11111** 10**001101** 10**010011**

* Delete any unused bytes:

> 100**11111** 10**001101** 10**010011**

* Prepend a byte consisting of as many 1's as bytes you have used (+1 to include itself) followed by 0's. We've used 3 bytes so we should have four 1's followed by four 0's:

> **11110000** 10011111 10001101 10010011

* If you are wasting space, i.e. you could fit the topmost 1 of your codepoint in the length byte's 0's, then shuffle it down and remove one of the 1's to reflect the new length.

* We're done! Therefore U+1F353 is encoded by UTF-8 as **F0 9F 8D 93**

* If you're still confused, Tom Scott explains it much more elegantly than I ever could in [this video](https://www.youtube.com/watch?v=MijmeoH9LT4).

You will notice that once we've decided to use multiple bytes, we only have 6 bits of space in our least significant byte, but most ascii characters require 7. This is an invalid use of UTF-8 according to http://unicode.org/versions/corrigendum1.html

>_the Unicode Technical Committee has modified the definition of UTF-8 to forbid conformant implementations from interpreting non-shortest forms for BMP characters, and clarified some of the conformance clauses_

...but vim ignores this and parses non-shortest forms of characters regardless. As a result, if you write the bytes **C1 A1** to a file and open it in vim, the letter "a" is displayed despite the fact that this is technically an invalid encoding. This script just takes this to another level by re-encoding each character given to it to use between 2-5 bytes randomly.

## Why?
Boredom, mostly.

## This isn't real encryption. You suck.
:(
