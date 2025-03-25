from math_utils import hash_bytes, scalar_mul, point_add, is_on_curve
from parameters import G


def verify(message, R, s, Q):
    if R is None or not is_on_curve(R):
        return False
    if Q is None or not is_on_curve(Q):
        return False

    e = hash_bytes(Q, R, message)

    left = scalar_mul(s, G)
    right = point_add(R, scalar_mul(e, Q))

    return left == right
