import hashlib
import os

from parameters import n, a, b, p


def mod_inv(a, p):
    return pow(a, p-2, p)  # Fermat little theorem

def is_on_curve(P): # P = (x, y) belongs to y^2 = x^3 + a x + b (mod p)
    if P is None:
        return True
    (x, y) = P
    return (y*y - (x*x*x + a*x + b)) % p == 0

def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    (x1, y1) = P
    (x2, y2) = Q

    if x1 == x2 and y1 != y2:
        return None

    if x1 == x2 and y1 == y2:
        s = (3*x1*x1 + a) * mod_inv(2*y1, p) % p
        x3 = (s*s - 2*x1) % p
        y3 = (s*(x1 - x3) - y1) % p
        return x3, y3
    else:
        s = (y2 - y1) * mod_inv(x2 - x1, p) % p
        x3 = (s*s - x1 - x2) % p
        y3 = (s*(x1 - x3) - y1) % p
        return x3, y3

def scalar_mul(k, P):
    result = None
    addend = P
    while k > 0:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result

def int_from_bytes(b):
    return int.from_bytes(b, byteorder='big')

def hash_bytes(*args):
    hasher = hashlib.sha256()
    for x in args:
        if isinstance(x, int):
            hasher.update(x.to_bytes(32, 'big'))
        elif isinstance(x, str):
            hasher.update(x.encode('utf-8'))
        elif isinstance(x, bytes):
            hasher.update(x)
        elif isinstance(x, tuple) and len(x) == 2:
            hasher.update(x[0].to_bytes(32, 'big'))
            hasher.update(x[1].to_bytes(32, 'big'))
        else:
            hasher.update(str(x).encode('utf-8'))
    h = hasher.digest()
    return int_from_bytes(h) % n

def random_scalar():
    while True:
        candidate = int_from_bytes(os.urandom(32))
        if 1 <= candidate < n:
            return candidate