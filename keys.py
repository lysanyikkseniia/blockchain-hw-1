from math_utils import scalar_mul, random_scalar, is_on_curve
from parameters import G, n

# generates private key d and public Q=dG
def generate_keys():
    d = random_scalar()
    Q = scalar_mul(d, G)
    if Q is None or not is_on_curve(Q) or scalar_mul(n, Q) is not None:
        raise ValueError("Q is not correct.")
    return d, Q