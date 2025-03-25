from math_utils import hash_bytes, scalar_mul, point_add, random_scalar
from parameters import n, G


def sign(message, d, Q=None):
    if Q is None:
        Q = scalar_mul(d, G)

    r = random_scalar()
    R = scalar_mul(r, G)

    e = hash_bytes(Q, R, message)
    s = (r + e*d) % n

    return R, s


def multi_sign(messages, private_keys, public_keys):
    # 1) L = H(X1, X2, ...)
    L = hash_bytes(*public_keys)

    # 2) X = sum( h_i * Xi ), h_i = H(L, Xi)
    weighted_public_keys = []
    for Xi in public_keys:
        hi = hash_bytes(L, Xi)
        weighted_public_keys.append(scalar_mul(hi, Xi))
    X = None
    for WP in weighted_public_keys:
        X = point_add(X, WP)

    # 3) every participant generates ri, Ri
    r_list = []
    R_list = []
    for d_i in private_keys:
        ri = random_scalar()
        Ri = scalar_mul(ri, G)
        r_list.append(ri)
        R_list.append(Ri)

    R = None
    for Ri in R_list:
        R = point_add(R, Ri)

    # 4) every participant calculates si = ri + H(X, R, m)*H(L, Xi)*xi   (mod n)
    # we'll assume only 1 message
    if len(messages) != 1:
        raise ValueError()
    m = messages[0]

    e = hash_bytes(X, R, m)
    s_list = []
    for i, d_i in enumerate(private_keys):
        Xi = public_keys[i]
        hi = hash_bytes(L, Xi)
        si = (r_list[i] + e*hi*d_i) % n
        s_list.append(si)

    # 5) s = sum(si)
    s = 0
    for si in s_list:
        s = (s + si) % n

    return R, s, X