# Diet Number Theory

DietNT is a self-contained module for performing computations in elementary number theory. Simply download it to your default working directory, import, and you're ready to go. To download just the file dietnt.py from GitHub, you need to click on the file, then click "Raw" and save the file.

For a listing of all the functions available, while in the Python interpreter's interactive mode, type "help()", then "dietnt".

# Examples

## Getting started

    $ python3
    Python 3.5.1 (v3.5.1:37a07cee5969, Dec  5 2015, 21:12:44) 
    [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from dietnt import *

## Chinese remainder theorem

    >>> a = (1,2,3)
    >>> m = (12341234567, 750000057, 1099511627776)
    >>> is_pairwise_coprime(m)
    True
    >>> chinese_remainder(a,m)
    9910987889755468626280665055235

## greatest common divisor

    >>> gcd((987654321, 123456789))
    9
    >>> extended_gcd((987654321, 123456789))
    [9, [1, -8]]
    >>> 1*987654321 + -8*123456789
    9
    >>> a = (45666020043321, 73433510078091009)
    >>> egcd = extended_gcd(a)
    >>> egcd
    [3, [10445427205865236, -6495686882417]]
    >>> egcd[1]
    [10445427205865236, -6495686882417]
    >>> a[0]*egcd[1][0] + a[1]*egcd[1][1]
    3

## integer factorization

    >>> factor_integer(43854532213873)
    {11423: 1, 3839143151: 1}
    >>> 11423 * 3839143151 == 43854532213873
    True
    >>> is_prime(11423)
    True
    >>> is_prime(3839143151)
    True
    >>> is_prime(43854532213873)
    False

## linear congruences

    >>> linear_congruence_solve(9, 12, 15)
    [3, 8, 13]
    >>> linear_congruence_solve(6789783, 2474010, 28927951)

## linear Diophantine equations

    >>> a = (10234357, 331108819)
    >>> linear_diophantine_solve(a, 1)
    [25574692, -790497]
    >>> 25574692*a[0] + -790497*a[1]
    1
    >>> linear_diophantine_solve(a, 123456789)
    [3157369353983988, -97592221334133]
    >>> a = (1122334455, 10101010101, 9898989898)
    >>> linear_diophantine_solve(a, 1)
    [2, -194343630710083031, 198309827274819439]
    >>> linear_diophantine_solve(a, 987654321)
    [1975308642, -191944326629641803835926951, 195861557804739073423145919]
    >>> a = (15, 6, 10, 21, 35)
    >>> linear_diophantine_solve(a, 1)
    [0, 0, -2, 6, -3]

## modular exponentiation

    >>> import math
    >>> modular_exp(2, 644, 645)
    1
    >>> 2**644 % 645
    1
    >>> modular_exp(7651, math.factorial(20), 10403)
    1
    >>> modular_exp(7651, math.factorial(52)-1, 10403)
    8993

## modular inverses

    >>> inverse_mod(7, 31)
    9
    >>> 7*9 % 31
    1

## polynomial congruences

    >>> p = Polynomial((-649, -42, 0, 0, 0, 0, 0, 13))
    >>> print(p)
                    7
    -649 - 42x + 13x 
    >>> poly_congruence_solve(p, 0, 1323)
    [184, 373, 562, 751, 940, 1129, 1318]
    >>> p(751)
    1751551500602262973572
    >>> p(751) % 1323
    0

## prime numbers

    >>> sieve(50)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    >>> is_pairwise_coprime(sieve(50))
    True
