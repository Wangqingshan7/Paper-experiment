
from Crypto.Util.py3compat import is_native_int
from Crypto.Util import number
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Random import get_random_bytes as rng

def _mult_gf2(f1, f2):
    """Multiply two polynomials in GF(2)"""
    # Ensure f2 is the smallest
    if f2 > f1:
        f1, f2 = f2, f1
    z = 0
    while f2:
        if f2 & 1:
            z ^= f1
        f1 <<= 1
        f2 >>= 1
    return z


def _div_gf2(a, b):
    """
    Compute division of polynomials over GF(2).
    Given a and b, it finds two polynomials q and r such that:

    a = b*q + r with deg(r)<deg(b)
    """

    if (a < b):
        return 0, a

    deg = number.size
    q = 0
    r = a
    d = deg(b)
    while deg(r) >= d:
        s = 1 << (deg(r) - d)
        q ^= s
        r ^= _mult_gf2(b, s)
    return (q, r)


class _Element(object):
    """Element of GF(2^128) field"""
    """私有的类"""
    # The irreducible polynomial defining this field is 1+x+x^2+x^7+x^128
    irr_poly = 1 + 2 + 4 + 128 + 2 ** 128

    def __init__(self, encoded_value):
        """Initialize the element to a certain value.

        The value passed as parameter is internally encoded as
        a 128-bit integer, where each bit represents a polynomial
        coefficient. The LSB is the constant coefficient.
        """

        if is_native_int(encoded_value):
            self._value = encoded_value
        elif len(encoded_value) == 16:
            self._value = bytes_to_long(encoded_value)
        else:
            print("The encoded value must be an integer or a 16 byte string")

    def __int__(self):
        """Return the field element, encoded as a 128-bit integer."""

        return self._value

    def encode(self):
        """Return the field element, encoded as a 16 byte string."""
        return long_to_bytes(self._value, 16)

    def __mul__(self, factor):

        f1 = self._value
        f2 = factor._value

        # Make sure that f2 is the smallest, to speed up the loop
        if f2 > f1:
            f1, f2 = f2, f1

        if self.irr_poly in (f1, f2):
            return _Element(0)
        mask1 = 2 ** 128
        v, z = f1, 0
        while f2:
            if f2 & 1:
                z ^= v
            v <<= 1
            if v & mask1:
                v ^= self.irr_poly
            f2 >>= 1
        return _Element(z)

    def __add__(self, term):
        return _Element(self._value ^ term._value)

    def inverse(self):
        """Return the inverse of this element in GF(2^128)."""

        # We use the Extended GCD algorithm
        # http://en.wikipedia.org/wiki/Polynomial_greatest_common_divisor

        r0, r1 = self._value, self.irr_poly
        s0, s1 = 1, 0
        while r1 > 0:
            q = _div_gf2(r0, r1)[0]
            r0, r1 = r1, r0 ^ _mult_gf2(q, r1)
            s0, s1 = s1, s0 ^ _mult_gf2(q, s1)
        return _Element(s0)


class Shamir(object):

    #return polynomial
    def pol(k,secret):
        """
        Args:
          k (integer):
            The number of shares that must be present in order to reconstruct
            the secret.
          secret (byte string):
            The 16 byte string (e.g. the AES128 key) to split.
        """
        coeffs = [_Element(rng(16)) for i in range(k - 1)]
        coeffs.insert(0, _Element(secret))
        return coeffs

    #return shares
    def make_share(user, coeffs):
        share, x, idx = [_Element(p) for p in (0, 1, user)]
        for coeff in coeffs:
            share += coeff * x
            x *= idx
        return share.encode()



    @staticmethod
    def combine(shares):
        """Recombine a secret, if enough shares are presented.
        Args:
          shares (tuples):
            At least *k* tuples, each containin the index (an integer) and
            the share (a byte string, 16 bytes long) that were assigned to
            a participant.
        Return:
            The original secret, as a byte string (16 bytes long).
        """
        #
        # Given k points (x,y), the interpolation polynomial of degree k-1 is:
        #
        # L(x) = \sum_{j=0}^{k-1} y_i * l_j(x)
        #
        # where:
        #
        # l_j(x) = \prod_{ \overset{0 \le m \le k-1}{m \ne j} }
        #          \frac{x - x_m}{x_j - x_m}
        #
        # However, in this case we are purely intersted in the constant
        # coefficient of L(x).
        #

        shares = [[_Element(y) for y in x] for x in shares]

        result = _Element(0)
        k = len(shares)
        for j in range(k):
            x_j, y_j = shares[j]

            coeff_0_l = _Element(0)
            while not int(coeff_0_l):
                coeff_0_l = _Element(rng(16))
            inv = coeff_0_l.inverse()

            for m in range(k):
                x_m = shares[m][0]
                if m != j:
                    t = x_m * (x_j + x_m).inverse()
                    coeff_0_l *= t
            result += y_j * coeff_0_l * inv
        return result.encode()
