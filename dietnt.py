'''Diet Number Theory: Some of the delicious elementary number theory flavor of SymPy with fewer calories. Just drop into your home directory and you're ready to go.

This module contains a small suite of functions for performing computations in elementary number theory. The algorithms used are generally on the simple end of the spectrum. If you need better performance or a more comprehensive collection of functions, look into SymPy.
'''

import functools, math, operator



class Polynomial:
    def __init__(self, it):
        self.coeff = tuple(it)
        #Ensures that at least one coefficient is nonzero if not the zero poly
        for i in self.coeff:
            if i != 0:
                return
        self.coeff = (0,)


    def __call__(self, x):
        it = reversed(self.coeff)
        s = next(it)
        for i in it:
            s = s*x + i
        return s

    
    def __getitem__(self, i):
        return self.coeff[i]


    def __iter__(self):
        return iter(self.coeff)


    def _modified_str(self, x):
        if x in (-1, 0, 1):
            return ''
        return str(x)


    def __str__(self):
        if self.coeff == (0,):
            return ' \n0'
        line1 = ''
        line2 = ''
        it = enumerate(self.coeff)
        # Deal with first nonzero coefficient as a special case
        i = next(it)
        while i[1] == 0:
            i = next(it)
        e = i[0]
        c = i[1]
        if e == 0:
            s = str(c)
            line1 += ' ' * len(s)
            line2 += s
        else:
            if c < 0:
                line1 += ' '
                line2 += '-'
            s = self._modified_str(abs(c))
            line1 += ' ' * len(s) + ' '
            line2 += s + 'x'
            
            s = self._modified_str(abs(e))
            line1 += s
            line2 += ' ' * len(s)
            
        for e, c in it:
            if c == 0:
                continue
            
            line1 += '   '
            line2 += ' '
            if c < 0:
                line2 += '- '
            else:
                line2 += '+ '
            
            s = self._modified_str(abs(c))
            line1 += ' ' * len(s)
            line2 += s
            if e:
                line1 += ' '
                line2 += 'x'
            s = self._modified_str(e)
            line1 += s
            line2 += ' ' * len(s)
        return line1 + '\n' + line2


    def derivative(self):
        '''Returns the derivative of the polynomial.'''
        new_coeff = []
        it = enumerate(self.coeff)
        next(it)
        for d, c in it:
            new_coeff.append(d*c)
        return Polynomial(new_coeff)
            


def chinese_remainder(a, m):
    '''Solves a system of congruences specified by the list of residues, a, and list of moduli, m.

    For example, chinese_remainder([a1,a2,a3], [m1,m2,m3]) finds a solution to the system

    x ≡ a1 (mod m1)
    x ≡ a2 (mod m2)
    x ≡ a3 (mod m3)

    The function does not check that the elements of m are pairwise relatively prime and will probably raise a TypeError if they are not.
'''
    M = functools.reduce(operator.mul, m)
    f = lambda a_k, m_k, M_k: a_k * M_k * inverse_mod(M_k, m_k)
    return functools.reduce(operator.add, map(f, a, m, (M // mk for mk in m))) % M



def extended_gcd(args):
    '''Returns a list whose first argument is the GCD and whose second argument is a list of Bézout coefficients for one or more nonnegative integers.\
    '''
    if len(args) == 0:
        return None
    
    a = args[0]
    if len(args) == 1:
        return [a, [1]]

    egcd = extended_gcd(args[1:])
    b = egcd[0]

    if a < b:
        swap = True
        a, b = b, a
    else:
        swap = False

    bezco = egcd[1]
    if b == 0:
        if swap:
            return [a, [0] + bezco]
        else:
            return [a, [1] + [0]*len(bezco)]

    bezout_a = [1,0]
    bezout_b = [0,1]
    r = a % b
    while r != 0:
        q = a // b
        for i in range(2):
            bezout_a[i], bezout_b[i] = bezout_b[i], bezout_a[i] - q*bezout_b[i]
        a, b = b, r
        r = a % b

    if swap:
        bezout_b[0], bezout_b[1] = bezout_b[1], bezout_b[0]

    for i in range(len(bezco)):
        bezco[i] = bezout_b[1] * bezco[i]

    bezco.insert(0, bezout_b[0])
    return [b, bezco]



def _merge_factors(a, b):
    for i in a:
        if i in b:
            b[i] += a[i]
        else:
            b[i] = a[i]
    return b



def factor_integer(n):
    '''Returns a dictionary with the prime factorization of n.

    The keys of the dictionary are primes, and the values are the powers of their associated primes. For example, factor_integer(30) returns {2: 2, 3: 1, 5: 1}.
    '''
    if n == 1:
        return {}
    if n < 4:
        return {n: 1}

    if n % 2 == 0:
        return _merge_factors({2: 1}, factor_integer(n // 2))
    if n % 3 == 0:
        return _merge_factors({3: 1}, factor_integer(n // 3))

    root_n = int(math.sqrt(n))
    for i in range(6, root_n+2, 6):
        for j in (i-1, i+1):
            if n % j == 0:
                return _merge_factors(factor_integer(j), factor_integer(n // j))

    return {n: 1}



def gcd(args):
    '''Returns the greatest common divisor of one or more nonnegative integers.'''
    if len(args) == 0:
        return None

    a = args[0]
    if len(args) == 1:
        return a

    b = gcd(args[1:])
    if a < b:
        a, b = b, a
    assert a >= b

    if b == 0:
        return a

    while a % b != 0:
        a, b = b, a % b

    return b


#TODO: tests
def hensel(f, r, p, k):
    fp = f.derivative()
    assert fp(r) % p
    t = (-inverse_mod(fp(r),p) * (f(r) // p**k)) % p
    return r + t*p**k



def inverse_mod(a, m):
    '''Returns the inverse modulo m of a or None if no inverse exists.'''
    egcd = extended_gcd((a,m))
    if egcd[0] != 1:
        return None

    return egcd[1][0] % m


def is_pairwise_coprime(m):
    '''Returns True if the list of nonnegative integers is pairwise relatively prime and False otherwise.'''
    for i in range(len(m)):
        for j in range(i+1, len(m)):
            if gcd((m[i], m[j])) != 1:
                return False
    return True



def is_prime(n):
    '''Returns True if n is prime and False if n is composite.'''
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    root_n = int(math.sqrt(n))
    for i in range(6, root_n+2, 6):
        for j in (i-1, i+1):
            if n % j == 0:
                return False
    return True



#TODO: Slow for large inputs. Could probably speed up polynomial congruence solve and just use that.
def linear_congruence_solve(a, b, m):
    '''Returns a list of solutions of the linear congruence ax ≡ b (mod m) or None if no solution exists.'''
    d = gcd((a,m))
    if b % d:
        return None

    md = m // d
    x = 0
    while (a*x - b) % m != 0:
        x += 1

    solutions = []
    for t in range(d):
        solutions.append(x + md*t)

    return solutions



def linear_diophantine_solve(a,b):
    '''Returns a solution to the linear Diophantine equation associated with the coefficient vector a or None if no solution exists; that is, returns a vector x such that ax = b, where ax is the dot product of a and x.'''
    assert len(a) >= 1

    egcd = extended_gcd(a)
    d = egcd[0]

    if b % d:
        return None

    scalar = b // d
    for i in range(len(egcd[1])):
        egcd[1][i] = scalar * egcd[1][i]

    return egcd[1]


#Currently uses brute force
def poly_congruence_solve(p, a, m):
    '''Solves a polynomial congruence of the form p(x) ≡ a (mod m), or returns None if no solution exists.

    p should be a Polynomial object or a list of coefficients in ascending order of degree; that is, the coefficient of x**n will be the (n+1)th list entry.
    '''

    solutions = []
    for x in range(m):
        if p(x) % m == a:
            solutions.append(x)
    if solutions:
        return solutions
    return None



def sieve(n):
    '''Returns a list of all primes less than n using the sieve of Eratosthenes.'''
    if n < 2:
        return []
    upper = int(math.sqrt(n))
    sieve_list = [1] * n
    prime_list = []
    sieve_list[0] = 0
    sieve_list[1] = 0

    for i in range(2, upper+1):
        if sieve_list[i]:
            prime_list.append(i)
            for j in range(2*i, n, i):
                sieve_list[j] = 0
    
    for i in range(upper+1, n):
        if sieve_list[i]:
            prime_list.append(i)

    return prime_list
