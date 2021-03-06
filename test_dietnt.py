primes_to_1000 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
primes_to_100 = primes_to_1000[:25]


from dietnt import *
from dietnt import _binary_powers_mod, _poly_congruence_prime_power
import unittest


class TestChineseRemainder(unittest.TestCase):
    def test_chinese_remainder(self):
        test_cases = [((1, 2, 3), (3, 5, 7), 52),
                      ((1, 2, 3), (5, 6, 7), 206),
                      ((4, 3), (11, 17), 37),
                      ((1, 2, 3), (2, 3, 5), 23),
                      ((0, 0, 1, 6), (2, 3, 5, 7), 6),
                      ((2, 3, 4, 5, 6), (11, 12, 13, 17, 19), 150999)]
        for a, m, ex in test_cases:
            with self.subTest(a=a, m=m, ex=ex):
                self.assertEqual(chinese_remainder(a,m), ex)



class TestFactorInteger(unittest.TestCase):
    def test_factor_integer(self):
        test_cases = [(1, {}),
                      (2, {2: 1}),
                      (8, {2:3}),
                      (28, {2:2, 7:1}),
                      (41, {41:1}),
                      (73, {73:1}),
                      (121, {11: 2}),
                      (714, {2:1, 3:1, 7:1, 17:1}),
                      (781, {11:1, 71:1}),
                      (938, {2:1, 7:1, 67:1}),
                      (968, {2:3, 11:2}),
                      (2131, {2131: 1}),
                      (579425, {5: 2, 7: 2, 11: 1, 43: 1}),
                      (9046250, {2: 1, 5: 4, 7237: 1}),
                      (807176099, {17: 1, 23: 1, 2064389: 1}),
                      (9007199254740993, {3: 1, 28059810762433: 1, 107: 1}),
                      (271601943420736448, {2: 6, 13: 1, 17: 1, 14011: 1, 1370539297: 1})]
        for i, ex in test_cases:
            with self.subTest(i=i, ex=ex):
                self.assertEqual(factor_integer(i), ex)



class TestGCD(unittest.TestCase):
    def test_gcd(self):
        test_cases = [((20,), 20),
                      ((15, 81), 3),
                      ((24, 84), 12),
                      ((0, 0), 0),
                      ((3, 0), 3),
                      ((13, 1), 1),
                      ((15, 9), 3),
                      ((4, 10), 2),
                      ((12, 18, 30), 6),
                      ((10, 15, 25), 5),
                      ((15, 21, 35), 1)]
        for i, ex in test_cases:
            with self.subTest(i=i):
                self.assertEqual(gcd(i), ex)


    def test_extended_gcd(self):
        test_cases = [((7,), 7),
                      ((15, 81), 3),
                      ((24, 84), 12),
                      ((0, 0), 0),
                      ((3, 0), 3),
                      ((13, 1), 1),
                      ((4, 10), 2),
                      ((18, 12, 30), 6),
                      ((10, 15, 25), 5),
                      ((0, 3, 0), 3),
                      ((5, 4, 5), 1)]
        for a, d in test_cases:
            with self.subTest(a=a, d=d):
                result = extended_gcd(a)
                self.assertEqual(result[0], d)
                lc = 0
                for x, y in zip(a, result[1]):
                    lc += x * y
                self.assertEqual(lc, d)


    def test_is_pairwise_coprime(self):
        test_cases = ((tuple(), True),
                      ((2,), True),
                      ((2,3,5), True),
                      ((2,3,5,8), False),
                      ((5,10), False),
                      ((40320,11111,30003,12321), False))
        for m, ex in test_cases:
            with self.subTest(m=m, ex=ex):
                self.assertEqual(is_pairwise_coprime(m), ex)


class TestHensel(unittest.TestCase):
    def test_hensel(self):
        test_cases = ((Polynomial((29,0,1,1)), 3, 5, 1, set((23,))),
                      (Polynomial((7,1,1)), 1, 3, 1, set((1,4,7))),
                      (Polynomial((7,1,1)), 1, 3, 2, set()),
                      (Polynomial((7,1,1)), 4, 3, 2, set((4,13,22))),
                      (Polynomial((7,1,1)), 7, 3, 2, set()),
                      (Polynomial((26,2,1,1)), 2, 7, 1, set((16,))),
                      (Polynomial((26,2,1,1)), 16, 7, 2, set((114,))))
        for f, r, p, k, ex in test_cases:
            with self.subTest(f=f, r=r, p=p, k=k, ex=ex):
                self.assertEqual(hensel(f,r,p,k), ex)


    def test_poly_congruence_prime_power(self):
        test_cases = ((Polynomial((29,0,1,1)), 5, 2, set((23,))),
                      (Polynomial((7,1,1)), 3, 3, set((4,13,22))),
                      (Polynomial((26,2,1,1)), 7, 3, set((114,))),
                      (Polynomial((2,4,1)), 7, 3, set((106,233))),
                      (Polynomial((-1,-1,8,1)), 11, 3, set((1148,))),
                      (Polynomial((47,1,1)), 7, 4, set((785,1615))),
                      (Polynomial((34,1,1)), 3, 4, set()),
                      (Polynomial((36,2,0,0,1)), 5, 4, set((279,))))
        for f, p, k, ex in test_cases:
            with self.subTest(f=f, p=p, k=k, ex=ex):
                self.assertEqual(_poly_congruence_prime_power(f,p,k), ex)



class TestInverseMod(unittest.TestCase):
    def test_inverse_mod(self):
        test_cases = [(13, 17, 4),
                      (14, 99, 92),
                      (22, 41, 28),
                      (12, 98, None),
                      (9, 31, 7)]
        for a, m, e in test_cases:
            with self.subTest(a=a, m=m, e=e):
                self.assertEqual(inverse_mod(a,m), e)


class TestIsPrime(unittest.TestCase):
    def test_is_prime_list(self):
        for i in primes_to_1000:
            with self.subTest(i=i):
                self.assertTrue(is_prime(i))



class TestLinearCongruenceSolve(unittest.TestCase):
    def test_linear_congruence_solve(self):
        test_cases = ((9, 12, 15, set([3,8,13])),
                      (7, 4, 12, set([4])),
                      (2, 5, 7, set([6])),
                      (3, 6, 9, set([2,5,8])),
                      (6789783, 2474010, 28927951, set()))
        for a, b, m, ex in test_cases:
            with self.subTest(a=a, b=b, m=m, ex=ex):
                self.assertEqual(linear_congruence_solve(a,b,m), ex)



class TestLinearDiophantineSolve(unittest.TestCase):
    def test_linear_diophantine_solve(self):
        test_cases = [((21, 14), 70),
                      ((20, 50), 510),
                      ((1402, 1969), 1),
                      ((2, 3, 4), 5)]
        for a, rhs in test_cases:
            with self.subTest(a=a, rhs=rhs):
                result = linear_diophantine_solve(a, rhs)
                lc = 0
                for x, y in zip(a, result):
                    lc += x * y
                self.assertEqual(lc, rhs)


    def test_linear_diophantine_solve_no_solution(self):
        test_cases = [((15, 6), 7),
                      ((6, 15), 83),
                      ((60, 18), 97),
                      ((7, 21, 35), 8)]
        for a, rhs in test_cases:
            with self.subTest(a=a, rhs=rhs):
                self.assertEqual(linear_diophantine_solve(a, rhs), None)


class TestMobius(unittest.TestCase):
    def test_mobius(self):
        test_cases = [(1, 1),
                      (29, -1),
                      (18, 0),
                      (6, 1),
                      (7, -1),
                      (20, 0)]
        for n, ex in test_cases:
            with self.subTest(n=n, ex=ex):
                self.assertEqual(mobius(n), ex)



class TestModularExponentiation(unittest.TestCase):
    def test_modular_exp(self):
        test_cases = ((2, 0, 101, 1),
                      (2, 644, 645, 1),
                      (2, 32, 47, 42),
                      (2, 47, 47, 2),
                      (2, 200, 47, 18),
                      (2, 12, 13, 1),
                      (3, 10, 11, 1),
                      (7651, 891, 10403, 1362),
                      (7651, 3628800, 10403, 4546),
                      (3, -1, 6, None),
                      (7, -1, 19, 11),
                      (7, -2, 19, 7),
                      (9, -1, 101, 45),
                      (9, -2, 101, 5),
                      (9, -3, 101, 23))
        for b, n, m, ex in test_cases:
            with self.subTest(b=b, n=n, m=m, ex=ex):
                self.assertEqual(modular_exp(b, n, m), ex)


    def test_binary_powers_mod(self):
        test_cases = ((2, 645, [2,4,16,256,391,16,256,391,16,256]),
                      (7651, 10403, [7651,120,3997,7404,5809,7552,3458,4717,8475,3313]),
                      (3, 47, [3,9,34,28,32,37,6,36,27,24,12,3,9]))
        for a, m, ex in test_cases:
            with self.subTest(a=a, m=m, ex=ex):
                g = _binary_powers_mod(a, m)
                s = []
                for i in ex:
                    s.append(next(g))
                self.assertEqual(s, ex)



class TestPolynomial(unittest.TestCase):
    def test_poly_call(self):
        test_cases = [(Polynomial([2,3,1,9]), 3, 263),
                      (Polynomial([4,6,-3,-4]), 7, -1473),
                      (Polynomial([0]), 2, 0),
                      (Polynomial([2]), 0, 2),
                      (Polynomial([1, 1]), 3, 4),
                      (Polynomial([4,-2,4]), -6, 160),
                      (Polynomial([5, -1]), -3, 8)]
        for p, x, ex in test_cases:
            with self.subTest(p=p, x=x, ex=ex):
                self.assertEqual(p(x), ex)


    def test_poly_derivative(self):
        test_cases = ((Polynomial((0,)), (0,)),
                      (Polynomial((1,)), (0,)),
                      (Polynomial((-1,)), (0,)),
                      (Polynomial((0,1)), (1,)),
                      (Polynomial((0,-1)), (-1,)),
                      (Polynomial((0,2)), (2,)),
                      (Polynomial((0,0,1)), (0,2)),
                      (Polynomial((0,0,-1)), (0,-2)),
                      (Polynomial((100336,-1,0,13,0,0,0,0,0,1)), 
                       (-1,0,39,0,0,0,0,0,9)),
                      (Polynomial((0,1,0,0,0,343,0,0,0,0,0,-7,49)),
                       (1,0,0,0,1715,0,0,0,0,0,-77,588)),
                      (Polynomial((1,1,0,0,0,1)), (1,0,0,0,5)),
                      (Polynomial((0,0,-1,-3)), (0,-2,-9)))
        for p, ex in test_cases:
            with self.subTest(p=p, ex=ex):
                self.assertEqual(p.derivative().coeff, ex)


    def test_poly_str(self):
        test_cases = ((Polynomial((0,)),
                       ' \n0'),
                      (Polynomial((1,)),
                       ' \n1'),
                      (Polynomial((-1,)),
                       '  \n-1'),
                      (Polynomial((0,1)),
                       ' \nx'),
                      (Polynomial((0,-1)),
                       '  \n-x'),
                      (Polynomial((0,2)),
                       '  \n2x'),
                      (Polynomial((0,0,1)),
                       ' 2\nx '),
                      (Polynomial((0,0,-1)),
                       '  2\n-x '),
                      (Polynomial((100336, -1, 0, 13, 0, 0, 0, 0, 0, 1)),
                       '                3    9\n100336 - x + 13x  + x '),
                      (Polynomial((0,1,0,0,0,343,0,0,0,0,0,-7,49)),
                       '        5     11      12\nx + 343x  - 7x   + 49x  '),
                      (Polynomial((1,1,0,0,0,1)),
                       '         5\n1 + x + x '),
                      (Polynomial((0,0,-1,-3)),
                       '  2     3\n-x  - 3x '))
        for p, ex in test_cases:
            with self.subTest(p=p, ex=ex):
                self.assertEqual(str(p), ex)


class TestPolynomialCongruenceSolve(unittest.TestCase):
    def test_poly_congruence_solve(self):
        test_cases = [(Polynomial((-4,7,0,2)), 25, set((16,))),
                      (Polynomial((29,0,1,1)), 25, set((23,))),
                      (Polynomial((7,1,1)), 27, set((4,13,22))),
                      (Polynomial((26,2,1,1)), 343, set((114,))),
                      (Polynomial((-649,-42,0,0,0,0,0,13)), 1323, set((184, 373, 562, 751, 940, 1129, 1318))),
                      (Polynomial((1001,0,0,0,-1,0,0,0,1)), 539, set((155, 188, 253, 286, 351, 384))),
                      (Polynomial((36,2,0,0,1)), 4375, set((279, 3404))),
                      (Polynomial((-35,0,0,0,0,-2,1)), 6125, set((3257,)))]
        for f, m, ex in test_cases:
            with self.subTest(f=f, m=m, ex=ex):
                self.assertEqual(poly_congruence_solve(f, m), ex)



class TestSieve(unittest.TestCase):
    def test_sieve(self):
        test_cases = [(2, []),
                      (100, primes_to_100),
                      (1000, primes_to_1000)]
        for n, l in test_cases:
            with self.subTest(n=n, l=l):
                self.assertEqual(sieve(n), l)


class TestTotient(unittest.TestCase):
    def test_totient(self):
        test_cases = [(1, 1),
                      (85, 64),
                      (71, 70),
                      (67, 66),
                      (51, 32),
                      (93, 60)]
        for n, ex in test_cases:
            with self.subTest(n=n, ex=ex):
                self.assertEqual(totient(n), ex)


if __name__ == '__main__':
    unittest.main()
