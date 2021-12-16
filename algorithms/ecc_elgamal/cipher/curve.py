from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import urandom
from typing import Optional

from math_utils.mod_inverse import modinv
from math_utils.mod_sqrt import modsqrt
from utils import int_length_in_byte


@dataclass
class Point:
    x: Optional[int]
    y: Optional[int]
    curve: "Curve"

    def is_at_infinity(self) -> bool:
        return self.x is None and self.y is None

    def __post_init__(self):
        if not self.is_at_infinity() and not self.curve.is_on_curve(self):
            raise ValueError("The point is not on the curve.")

    def __str__(self):
        if self.is_at_infinity():
            return f"Point(At infinity, Curve={str(self.curve)})"
        else:
            return f"Point(X={self.x}, Y={self.y}, Curve={str(self.curve)})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.curve == other.curve and self.x == other.x and self.y == other.y

    def __neg__(self):
        return self.curve.neg_point(self)

    def __add__(self, other):
        return self.curve.add_point(self, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        negative = -other
        return self.__add__(negative)

    def __mul__(self, scalar: int):
        return self.curve.mul_point(scalar, self)

    def __rmul__(self, scalar: int):
        return self.__mul__(scalar)


@dataclass
class Curve(ABC):
    name: str
    a: int
    b: int
    p: int
    n: int
    G_x: int
    G_y: int

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.a == other.a
            and self.b == other.b
            and self.p == other.p
            and self.n == other.n
            and self.G_x == other.G_x
            and self.G_y == other.G_y
        )

    @property
    def G(self) -> Point:
        return Point(self.G_x, self.G_y, self)

    @property
    def INF(self) -> Point:
        return Point(None, None, self)

    def is_on_curve(self, P: Point) -> bool:
        if P.curve != self:
            return False
        return P.is_at_infinity() or self._is_on_curve(P)

    @abstractmethod
    def _is_on_curve(self, P: Point) -> bool:
        pass

    def add_point(self, P: Point, Q: Point) -> Point:
        if (not self.is_on_curve(P)) or (not self.is_on_curve(Q)):
            raise ValueError("The points are not on the curve.")
        if P.is_at_infinity():
            return Q
        elif Q.is_at_infinity():
            return P

        if P == Q:
            return self._double_point(P)
        if P == -Q:
            return self.INF

        return self._add_point(P, Q)

    @abstractmethod
    def _add_point(self, P: Point, Q: Point) -> Point:
        pass

    def double_point(self, P: Point) -> Point:
        if not self.is_on_curve(P):
            raise ValueError("The point is not on the curve.")
        if P.is_at_infinity():
            return self.INF

        return self._double_point(P)

    @abstractmethod
    def _double_point(self, P: Point) -> Point:
        pass

    def mul_point(self, d: int, P: Point) -> Point:
        """
        https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        """
        if not self.is_on_curve(P):
            raise ValueError("The point is not on the curve.")
        if P.is_at_infinity():
            return self.INF
        if d == 0:
            return self.INF

        res = None
        is_negative_scalar = d < 0
        d = -d if is_negative_scalar else d
        tmp = P
        while d:
            if d & 0x1 == 1:
                if res:
                    res = self.add_point(res, tmp)
                else:
                    res = tmp
            tmp = self.double_point(tmp)
            d >>= 1
        if is_negative_scalar:
            return -res
        else:
            return res

    def neg_point(self, P: Point) -> Point:
        if not self.is_on_curve(P):
            raise ValueError("The point is not on the curve.")
        if P.is_at_infinity():
            return self.INF

        return self._neg_point(P)

    @abstractmethod
    def _neg_point(self, P: Point) -> Point:
        pass

    @abstractmethod
    def compute_y(self, x: int) -> int:
        pass

    def encode_point(self, plaintext: bytes) -> Point:
        plaintext = len(plaintext).to_bytes(1, byteorder="big") + plaintext
        while True:
            x = int.from_bytes(plaintext, "big")
            y = self.compute_y(x)
            if y:
                return Point(x, y, self)
            plaintext += urandom(1)

    def decode_point(self, M: Point) -> bytes:
        byte_len = int_length_in_byte(M.x)
        plaintext_len = (M.x >> ((byte_len - 1) * 8)) & 0xFF
        plaintext = (M.x >> ((byte_len - plaintext_len - 1) * 8)) & (
            int.from_bytes(b"\xff" * plaintext_len, "big")
        )
        return plaintext.to_bytes(plaintext_len, byteorder="big")


class ShortWeierstrassCurve(Curve):
    """
    y^2 = x^3 + a*x + b
    https://en.wikipedia.org/wiki/Elliptic_curve
    """

    def _is_on_curve(self, P: Point) -> bool:
        left = P.y * P.y
        right = (P.x * P.x * P.x) + (self.a * P.x) + self.b
        return (left - right) % self.p == 0

    def _add_point(self, P: Point, Q: Point) -> Point:
        # s = (yP - yQ) / (xP - xQ)
        # xR = s^2 - xP - xQ
        # yR = yP + s * (xR - xP)
        delta_x = P.x - Q.x
        delta_y = P.y - Q.y
        s = delta_y * modinv(delta_x, self.p)
        res_x = (s * s - P.x - Q.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return -Point(res_x, res_y, self)

    def _double_point(self, P: Point) -> Point:
        # s = (3 * xP^2 + a) / (2 * yP)
        # xR = s^2 - 2 * xP
        # yR = yP + s * (xR - xP)
        s = (3 * P.x * P.x + self.a) * modinv(2 * P.y, self.p)
        res_x = (s * s - 2 * P.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return -Point(res_x, res_y, self)

    def _neg_point(self, P: Point) -> Point:
        return Point(P.x, -P.y % self.p, self)

    def compute_y(self, x) -> int:
        right = (x * x * x + self.a * x + self.b) % self.p
        y = modsqrt(right, self.p)
        return y


class MontgomeryCurve(Curve):
    """
    by^2 = x^3 + ax^2 + x
    https://en.wikipedia.org/wiki/Montgomery_curve
    """

    def _is_on_curve(self, P: Point) -> bool:
        left = self.b * P.y * P.y
        right = (P.x * P.x * P.x) + (self.a * P.x * P.x) + P.x
        return (left - right) % self.p == 0

    def _add_point(self, P: Point, Q: Point) -> Point:
        # s = (yP - yQ) / (xP - xQ)
        # xR = b * s^2 - a - xP - xQ
        # yR = yP + s * (xR - xP)
        delta_x = P.x - Q.x
        delta_y = P.y - Q.y
        s = delta_y * modinv(delta_x, self.p)
        res_x = (self.b * s * s - self.a - P.x - Q.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return -Point(res_x, res_y, self)

    def _double_point(self, P: Point) -> Point:
        # s = (3 * xP^2 + 2 * a * xP + 1) / (2 * b * yP)
        # xR = b * s^2 - a - 2 * xP
        # yR = yP + s * (xR - xP)
        up = 3 * P.x * P.x + 2 * self.a * P.x + 1
        down = 2 * self.b * P.y
        s = up * modinv(down, self.p)
        res_x = (self.b * s * s - self.a - 2 * P.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return -Point(res_x, res_y, self)

    def _neg_point(self, P: Point) -> Point:
        return Point(P.x, -P.y % self.p, self)

    def compute_y(self, x: int) -> int:
        right = (x * x * x + self.a * x * x + x) % self.p
        inv_b = modinv(self.b, self.p)
        right = (right * inv_b) % self.p
        y = modsqrt(right, self.p)
        return y


class TwistedEdwardsCurve(Curve):
    """
    ax^2 + y^2 = 1 + bx^2y^2
    https://en.wikipedia.org/wiki/Twisted_Edwards_curve
    """

    def _is_on_curve(self, P: Point) -> bool:
        left = self.a * P.x * P.x + P.y * P.y
        right = 1 + self.b * P.x * P.x * P.y * P.y
        return (left - right) % self.p == 0

    def _add_point(self, P: Point, Q: Point) -> Point:
        # xR = (xP * yQ + yP * xQ) / (1 + b * xP * xQ * yP * yQ)
        up_x = P.x * Q.y + P.y * Q.x
        down_x = 1 + self.b * P.x * Q.x * P.y * Q.y
        res_x = (up_x * modinv(down_x, self.p)) % self.p
        # yR = (yP * yQ - a * xP * xQ) / (1 - b * xP * xQ * yP * yQ)
        up_y = P.y * Q.y - self.a * P.x * Q.x
        down_y = 1 - self.b * P.x * Q.x * P.y * Q.y
        res_y = (up_y * modinv(down_y, self.p)) % self.p
        return Point(res_x, res_y, self)

    def _double_point(self, P: Point) -> Point:
        # xR = (2 * xP * yP) / (a * xP^2 + yP^2)
        up_x = 2 * P.x * P.y
        down_x = self.a * P.x * P.x + P.y * P.y
        res_x = (up_x * modinv(down_x, self.p)) % self.p
        # yR = (yP^2 - a * xP * xP) / (2 - a * xP^2 - yP^2)
        up_y = P.y * P.y - self.a * P.x * P.x
        down_y = 2 - self.a * P.x * P.x - P.y * P.y
        res_y = (up_y * modinv(down_y, self.p)) % self.p
        return Point(res_x, res_y, self)

    def _neg_point(self, P: Point) -> Point:
        return Point(-P.x % self.p, P.y, self)

    def compute_y(self, x: int) -> int:
        # (bx^2 - 1) * y^2 = ax^2 - 1
        right = self.a * x * x - 1
        left_scale = (self.b * x * x - 1) % self.p
        inv_scale = modinv(left_scale, self.p)
        right = (right * inv_scale) % self.p
        y = modsqrt(right, self.p)
        return y


P256 = ShortWeierstrassCurve(
    name="P256",
    a=-3,
    b=41058363725152142129326129780047268409114441015993725554835256314039467401291,
    p=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
    n=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
    G_x=0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
    G_y=0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5,
)

secp256k1 = ShortWeierstrassCurve(
    name="secp256k1",
    a=0,
    b=7,
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    G_x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    G_y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)

Curve25519 = MontgomeryCurve(
    name="Curve25519",
    a=486662,
    b=1,
    p=0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFED,
    n=0x1000000000000000000000000000000014DEF9DEA2F79CD65812631A5CF5D3ED,
    G_x=0x9,
    G_y=0x20AE19A1B8A086B4E01EDD2C7748D14C923D4D7E6D7C61B229E9C5A27ECED3D9,
)

M383 = MontgomeryCurve(
    name="M383",
    a=2065150,
    b=1,
    p=0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF45,
    n=0x10000000000000000000000000000000000000000000000006C79673AC36BA6E7A32576F7B1B249E46BBC225BE9071D7,
    G_x=0xC,
    G_y=0x1EC7ED04AAF834AF310E304B2DA0F328E7C165F0E8988ABD3992861290F617AA1F1B2E7D0B6E332E969991B62555E77E,
)

E222 = TwistedEdwardsCurve(
    name="E222",
    a=1,
    b=160102,
    p=0x3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF8B,
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFF70CBC95E932F802F31423598CBF,
    G_x=0x19B12BB156A389E55C9768C303316D07C23ADAB3736EB2BC3EB54E51,
    G_y=0x1C,
)

E382 = TwistedEdwardsCurve(
    name="E382",
    a=1,
    b=-67254,
    p=0x3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF97,
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD5FB21F21E95EEE17C5E69281B102D2773E27E13FD3C9719,
    G_x=0x196F8DD0EAB20391E5F05BE96E8D20AE68F840032B0B64352923BAB85364841193517DBCE8105398EBC0CC9470F79603,
    G_y=0x11,
)
