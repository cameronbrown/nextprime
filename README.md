# nextprime.py

A simple python program to prove Dad's algorithm.
Finds next prime number after a given integer.
Uses Eratosthenes Sieve modified to keep memory
consumption low by only investigating a range
after n. Does not rely on a starting list of primes.

## Usage

```
> python nextprime.py 100000000
100000007

> python nextprime.py -d 100000007
   Looking for prime in range of 38 following target
   Using 4999 test factors to find non-primes in range
   Added 17 non-prime offsets:
     [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 33, 35, 37]
   Found prime at offset 29
100000037

> python nextprime.py --help
usage: nextprime.py [-h] [-d] [-t] [N]

Find first prime number greater than target integer N.

positional arguments:
  N            where to start search for next prime

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  output debugging messages
  -t, --test   do some tests
````

## Algorithm

```
Let LX = | LKP = largest known prime
         | or LTEN = 10 to the n
         | or MTEN = next multiple of 10 after LKP

START INPUT: LX
      LXSR = int(sqrt(LX))
      MAXI = int(LXSR / 2)
      IODD = 1
      I = 0

100   I = I + 1                   # LABEL 100
      IODD = IODD + 2
      IQ = int(LX / IODD)
      IQR = LX % IODD
      ILEFT = IQR
      IRIGHT = IODD - ILEFT
      IF (IRIGHT is ODD) GO TO 120
      IRIGHT = IRIGHT + IODD
120   NEXT(I) = IRIGHT
      IF (I.LT.MAXI) GO TO 100
      CALL SEARCH(LX, LXSR, MAXI, NEXT, NP)
      REPORT "NP" Next PRIME
      GO TO START or
      STOP

SUB   SEARCH(LX, LXSR, MAXI, NEXT, NP)
      NP = 0
      IS = 1
130   I = 1
150   IF (IS.EQ.NEXT(I)) GO TO 200
      IF (I.GE.MAXI) GO TO 300
      I = I + 1
      GO TO 150
200   IS = IS + 2
      IF (IS.LE.LXSR) GO TO 130
      REPORT "NO NEXT PRIME FOUND"
      GO TO 500

300   NP = IS + LX
      REPORT "Next Prime =" NP "after" LX

500   EXIT SEARCH(LX, LXSR, MAXI, NEXT, NP)
```