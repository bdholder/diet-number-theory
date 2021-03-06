'''Diet Number Theory: Some of the delicious elementary number theory flavor of SymPy with fewer calories. Just drop into your home directory and you're ready to go.

This module contains a small suite of functions for performing computations in elementary number theory. The algorithms used are generally on the simple end of the spectrum. If you need better performance or a more comprehensive collection of functions, look into SymPy.
'''

import functools, itertools, math, operator



class Polynomial:
    def __init__(self, coeff):
        '''coeff should be a list of coefficients in order of increasing degree; that is, the coefficient of x**n will be the (n+1)th entry.'''
        self.coeff = tuple(coeff)
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



def hensel(f, r, p, k):
    fp = f.derivative()
    if fp(r) % p:
        t = (-inverse_mod(fp(r),p) * (f(r) // p**k)) % p
        return set((r + t*p**k,))

    if f(r) % p**(k+1):
        return set()

    solutions = set()
    for t in range(p):
        solutions.add(r + t*p**k)
    return solutions



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



def linear_congruence_solve(a, b, m):
    '''Returns the solution set of the linear congruence ax ≡ b (mod m).'''
    p = Polynomial((-b, a))
    return poly_congruence_solve(p, m)



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


def mobius(n):
    '''
    Mobius function.
    '''
    if n == 1:
        return 1
    factors = factor_integer(n)
    for v in factors.values():
        if v > 1:
            return 0
    return 1 if len(factors) % 2 == 0 else -1


def _binary_digits(n):
    '''Generator yielding the base 2 digit sequence of n.'''
    while n > 0:
        yield n % 2
        n //= 2


def _binary_powers_mod(a, m):
    '''Generator yielding the binary powers of a modulo m; i.e., the nth call to next will yield a**(2**(n-1)).'''
    cache = {}
    while True:
        yield a
        if not a in cache:
            cache[a] = a*a % m
        a = cache[a]



def modular_exp(b, n, m):
    '''Uses fast modular exponentiation to evaluate b**n % m.'''
    if n == 0:
        return 1
    if n < 0:
        b = inverse_mod(b, m)
        if not b:
            return None
        n = abs(n)
    bd = _binary_digits(n)
    pm = _binary_powers_mod(b, m)
    return functools.reduce(operator.mul, map(lambda p, d: p if d else 1, pm, bd)) % m



def _poly_congruence_prime_power(f, p, k):
    solns = _poly_congruence_brute(f, p)
    
    for i in range(1,k):
        new_solns = set()
        for j in solns:
            new_solns |= hensel(f, j, p, i)
        solns = new_solns

    return solns



def _poly_congruence_brute(p, m):
    '''Returns the solution set of a polynomial congruence of the form p(x) ≡ 0 (mod m) via brute force.
    '''
    solutions = set()
    for x in range(m):
        if p(x) % m == 0:
            solutions.add(x)
    return solutions



def poly_congruence_solve(f, m):
    '''Returns the solution set of a polynomial congruence of the form f(x) ≡ 0 (mod m).
    '''
    factor_dict = factor_integer(m)
    soln_sets_list = []
    moduli = []
    for prime in factor_dict:
        soln_sets_list.append(_poly_congruence_prime_power(f, prime, factor_dict[prime]))
        moduli.append(prime**factor_dict[prime])
    
    cartesian_product = itertools.product(*soln_sets_list)
    solutions = set()
    for a in cartesian_product:
        solutions.add(chinese_remainder(a, moduli))

    return solutions



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


def totient(n):
    '''
    Euler's totient function.
    '''
    assert n > 0
    if n < 3:
        return 1

    factors = factor_integer(n)
    return functools.reduce(operator.mul,
                            (p**(factors[p]-1) * (p-1) for p in factors))


def dirichlet_product(f, g):
    def h(n):
        return functools.reduce(operator.add, (f(d)*g(n//d) for d in range(1,n+1) if n % d == 0))
    return h
